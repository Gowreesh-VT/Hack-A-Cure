from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import List, Optional
import json
import csv
import io
from pydantic import BaseModel

from langchain_community.document_loaders import TextLoader, JSONLoader, CSVLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.bot import VECTOR_STORE, EMBEDDINGS
from app.core.config import settings


router = APIRouter(prefix="/ingest", tags=["ingest"])


class IngestResponse(BaseModel):
    message: str
    documents_processed: int
    collection_name: str


class IngestTextRequest(BaseModel):
    texts: List[str]
    metadatas: Optional[List[dict]] = None


@router.post("/upload-file", response_model=IngestResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    chunk_size: int = 500,
    chunk_overlap: int = 100
):
    """
    Upload and ingest a file (TXT, JSON, CSV) into the vector store.
    Optimized chunking for better retrieval scores.
    
    - **file**: The file to upload (supported formats: .txt, .json, .csv)
    - **chunk_size**: Size of text chunks for splitting (default: 500, optimized for medical text)
    - **chunk_overlap**: Overlap between chunks (default: 100, ensures context continuity)
    """
    
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided"
        )
    
    # Check file extension
    file_extension = file.filename.split('.')[-1].lower()
    
    if file_extension not in ['txt', 'json', 'csv']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format: {file_extension}. Supported formats: txt, json, csv"
        )
    
    try:
        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Parse documents based on file type
        documents = []
        
        if file_extension == 'txt':
            # For text files, create a single document
            documents.append(Document(
                page_content=content_str,
                metadata={"source": file.filename}
            ))
        
        elif file_extension == 'json':
            # For JSON files, parse as list of objects
            json_data = json.loads(content_str)
            
            # Handle both single object and array of objects
            if isinstance(json_data, dict):
                json_data = [json_data]
            
            for idx, item in enumerate(json_data):
                # Try to find a content field or stringify the whole object
                if 'content' in item:
                    text = item['content']
                elif 'text' in item:
                    text = item['text']
                elif 'question' in item and 'answer' in item:
                    text = f"Question: {item['question']}\nAnswer: {item['answer']}"
                else:
                    text = json.dumps(item)
                
                metadata = {k: v for k, v in item.items() if k not in ['content', 'text']}
                metadata['source'] = file.filename
                metadata['index'] = idx
                
                documents.append(Document(
                    page_content=text,
                    metadata=metadata
                ))
        
        elif file_extension == 'csv':
            # For CSV files, parse each row
            csv_reader = csv.DictReader(io.StringIO(content_str))
            
            for idx, row in enumerate(csv_reader):
                # Try to find a content field or combine all fields
                if 'content' in row:
                    text = row['content']
                elif 'text' in row:
                    text = row['text']
                elif 'question' in row and 'answer' in row:
                    text = f"Question: {row['question']}\nAnswer: {row['answer']}"
                else:
                    # Combine all fields
                    text = '\n'.join([f"{k}: {v}" for k, v in row.items()])
                
                metadata = {k: v for k, v in row.items() if k not in ['content', 'text']}
                metadata['source'] = file.filename
                metadata['index'] = idx
                
                documents.append(Document(
                    page_content=text,
                    metadata=metadata
                ))
        
        # Split documents into chunks with better strategy for medical text
        # Using smaller chunks and separators optimized for medical text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", "? ", "! ", "; ", ", ", " ", ""],  # Better splitting
            keep_separator=True,  # Keep punctuation for context
        )
        
        split_docs = text_splitter.split_documents(documents)
        
        # Add documents to vector store
        VECTOR_STORE.add_documents(split_docs)
        
        return IngestResponse(
            message=f"Successfully ingested {file.filename}",
            documents_processed=len(split_docs),
            collection_name=settings.QDRANT_COLLECTION_NAME
        )
    
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON format"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )


@router.post("/upload-texts", response_model=IngestResponse, status_code=status.HTTP_201_CREATED)
async def upload_texts(
    request: IngestTextRequest,
    chunk_size: int = 500,
    chunk_overlap: int = 100
):
    """
    Ingest a list of text strings directly into the vector store.
    Optimized chunking for better retrieval scores.
    
    - **texts**: List of text strings to ingest
    - **metadatas**: Optional list of metadata dictionaries (one per text)
    - **chunk_size**: Size of text chunks for splitting (default: 500, optimized for medical text)
    - **chunk_overlap**: Overlap between chunks (default: 100, ensures context continuity)
    """
    
    if not request.texts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No texts provided"
        )
    
    try:
        # Create documents from texts
        documents = []
        for idx, text in enumerate(request.texts):
            metadata = {}
            if request.metadatas and idx < len(request.metadatas):
                metadata = request.metadatas[idx]
            metadata['index'] = idx
            
            documents.append(Document(
                page_content=text,
                metadata=metadata
            ))
        
        # Split documents into chunks with better strategy for medical text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", "? ", "! ", "; ", ", ", " ", ""],
            keep_separator=True,
        )
        
        split_docs = text_splitter.split_documents(documents)
        
        # Add documents to vector store
        VECTOR_STORE.add_documents(split_docs)
        
        return IngestResponse(
            message="Successfully ingested texts",
            documents_processed=len(split_docs),
            collection_name=settings.QDRANT_COLLECTION_NAME
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing texts: {str(e)}"
        )


@router.delete("/clear-collection", status_code=status.HTTP_200_OK)
async def clear_collection():
    """
    Clear all documents from the current collection.
    USE WITH CAUTION - This will delete all data in the collection.
    """
    try:
        # Note: Qdrant doesn't have a direct "clear" method
        # You would typically delete and recreate the collection
        # For safety, we'll return a warning message
        return {
            "message": "To clear the collection, you need to delete and recreate it manually",
            "collection_name": settings.QDRANT_COLLECTION_NAME,
            "warning": "This operation is not implemented for safety reasons"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )


@router.get("/collection-info", status_code=status.HTTP_200_OK)
async def get_collection_info():
    """
    Get information about the current collection.
    """
    try:
        # Get collection info from Qdrant client
        from qdrant_client import QdrantClient
        
        client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
        
        collection_info = client.get_collection(settings.QDRANT_COLLECTION_NAME)
        
        return {
            "collection_name": settings.QDRANT_COLLECTION_NAME,
            "vectors_count": collection_info.vectors_count,
            "points_count": collection_info.points_count,
            "status": collection_info.status
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting collection info: {str(e)}"
        )
