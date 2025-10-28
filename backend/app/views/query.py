from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

from app.core.bot import VECTOR_STORE, retrieve, generate_sync, LLM
from app.core.config import settings


router = APIRouter(prefix="/query", tags=["query"])


class QueryRequest(BaseModel):
    query: str = Field(..., description="The user's question")
    top_k: int = Field(default=5, description="Number of context snippets to retrieve")
    use_query_expansion: bool = Field(default=False, description="Expand query with medical terms")
    score_threshold: float = Field(default=0.0, description="Minimum similarity score (0-1)")


class QueryResponse(BaseModel):
    answer: str = Field(..., description="The generated answer")
    contexts: List[str] = Field(..., description="List of context snippets used")
    scores: List[float] = Field(..., description="Similarity scores for each context")
    expanded_query: Optional[str] = Field(None, description="Query after expansion (if used)")


def expand_medical_query(query: str, llm) -> str:
    """
    Expand the query with medical terminology and synonyms to improve retrieval.
    """
    expansion_prompt = f"""Given this medical question, expand it with relevant medical terms, synonyms, and related concepts that would help find relevant information. Keep it concise (1-2 sentences max).

Original question: {query}

Expanded query with medical terms:"""
    
    try:
        response = llm.invoke(expansion_prompt)
        expanded = response.content if hasattr(response, 'content') else str(response)
        # Combine original and expanded
        return f"{query} {expanded.strip()}"
    except Exception as e:
        print(f"Query expansion failed: {e}")
        return query


@router.post("", response_model=QueryResponse, status_code=status.HTTP_200_OK)
async def query_endpoint(req: QueryRequest):
    """
    Query endpoint for RAG evaluation with enhanced retrieval.
    
    - **query**: The user's medical question (required)
    - **top_k**: Number of context snippets to retrieve (default: 5)
    - **use_query_expansion**: Expand query with medical terminology (default: False)
    - **score_threshold**: Minimum similarity score to include results (default: 0.0)
    
    Returns:
    - **answer**: The generated answer
    - **contexts**: List of relevant context snippets
    - **scores**: Similarity scores for each context
    - **expanded_query**: Expanded query if query expansion was used
    """
    
    if not req.query or req.query.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="query is required and cannot be empty"
        )
    
    # Ensure top_k is positive
    top_k = max(1, req.top_k) if req.top_k else 5
    
    # Increase top_k for better recall, we'll filter later
    retrieval_k = top_k * 2
    
    try:
        # Query expansion (optional)
        search_query = req.query
        expanded_query = None
        
        if req.use_query_expansion:
            expanded_query = expand_medical_query(req.query, LLM)
            search_query = expanded_query
            print(f"🔍 Expanded query: {expanded_query}")
        
        # Retrieve relevant documents with scores
        retrieved_docs_with_scores = VECTOR_STORE.similarity_search_with_score(
            search_query, 
            k=retrieval_k
        )
        
        # Filter by score threshold and sort by score (higher is better for most embeddings)
        # Note: Qdrant returns scores where higher is better
        filtered_results = [
            (doc, score) for doc, score in retrieved_docs_with_scores
            if score >= req.score_threshold
        ]
        
        # Sort by score descending and take top_k
        filtered_results.sort(key=lambda x: x[1], reverse=True)
        filtered_results = filtered_results[:top_k]
        
        if not filtered_results:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No documents found with similarity score >= {req.score_threshold}"
            )
        
        # Extract documents and scores
        retrieved_docs = [doc for doc, score in filtered_results]
        scores = [float(score) for doc, score in filtered_results]
        
        # Extract context snippets as plain strings, clean and deduplicate
        raw_contexts = [doc.page_content for doc in retrieved_docs]
        
        # Clean unicode escape sequences and normalize whitespace
        cleaned_contexts = []
        seen = set()
        cleaned_scores = []
        
        for idx, ctx in enumerate(raw_contexts):
            # Remove unicode soft hyphens and other special chars
            cleaned = ctx.replace('\u00ad', '').replace('\xa0', ' ')
            # Normalize whitespace
            cleaned = ' '.join(cleaned.split())
            # Deduplicate
            if cleaned not in seen and cleaned.strip():
                seen.add(cleaned)
                cleaned_contexts.append(cleaned)
                cleaned_scores.append(scores[idx])
        
        contexts = cleaned_contexts
        final_scores = cleaned_scores
        
        # Generate answer using RAG
        state = {
            'question': req.query,  # Use original query for answer generation
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
            contexts=contexts,
            scores=final_scores,
            expanded_query=expanded_query
        )
    
    except HTTPException:
        raise
    except Exception as e:
        # Log the error but return a proper response
        print(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )
