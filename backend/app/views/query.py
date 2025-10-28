from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

from app.core.bot import VECTOR_STORE, retrieve, generate_sync
from app.core.config import settings


router = APIRouter(prefix="/query", tags=["query"])


class QueryRequest(BaseModel):
    query: str = Field(..., description="The user's question")
    top_k: int = Field(default=5, description="Number of context snippets to retrieve")


class QueryResponse(BaseModel):
    answer: str = Field(..., description="The generated answer")
    contexts: List[str] = Field(..., description="List of context snippets used")


@router.post("", response_model=QueryResponse, status_code=status.HTTP_200_OK)
async def query_endpoint(req: QueryRequest):
    """
    Query endpoint for RAG evaluation.
    
    - **query**: The user's medical question (required)
    - **top_k**: Number of context snippets to retrieve (default: 5)
    
    Returns:
    - **answer**: The generated answer
    - **contexts**: List of relevant context snippets
    """
    
    if not req.query or req.query.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="query is required and cannot be empty"
        )
    
    # Ensure top_k is positive
    top_k = max(0, req.top_k) if req.top_k else 5
    
    try:
        # Retrieve relevant documents from vector store
        retrieved_docs = VECTOR_STORE.similarity_search(req.query, k=top_k)
        
        # Extract context snippets as plain strings, clean and deduplicate
        raw_contexts = [doc.page_content for doc in retrieved_docs]
        
        # Clean unicode escape sequences and normalize whitespace
        cleaned_contexts = []
        seen = set()
        for ctx in raw_contexts:
            # Remove unicode soft hyphens and other special chars
            cleaned = ctx.replace('\u00ad', '').replace('\xa0', ' ')
            # Normalize whitespace
            cleaned = ' '.join(cleaned.split())
            # Deduplicate
            if cleaned not in seen and cleaned.strip():
                seen.add(cleaned)
                cleaned_contexts.append(cleaned)
        
        contexts = cleaned_contexts
        
        # Generate answer using RAG
        state = {
            'question': req.query,
            'context': retrieved_docs,
            'answer': ''
        }
        
        # Generate answer synchronously
        message = generate_sync(state)
        answer = message.content if hasattr(message, 'content') else str(message)
        
        # Ensure answer is a string and not empty
        if not answer or answer.strip() == "":
            answer = "I don't have enough information to answer this question."
        
        return QueryResponse(
            answer=answer.strip(),
            contexts=contexts
        )
    
    except Exception as e:
        # Log the error but return a proper response
        print(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )
