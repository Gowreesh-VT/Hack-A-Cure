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
    summarize_context: bool = Field(default=True, description="Use AI to summarize contexts before answering")


class QueryResponse(BaseModel):
    answer: str = Field(..., description="The generated answer")
    contexts: List[str] = Field(..., description="List of context snippets (summarized if enabled)")
    scores: List[float] = Field(..., description="Similarity scores for each context")
    metadata: List[Dict] = Field(default=[], description="Metadata for each context (e.g., source, book name)")


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


def summarize_contexts(query: str, contexts: List[str], llm) -> List[str]:
    """
    Use AI to intelligently summarize and condense contexts while keeping relevant information.
    Optimized to process all contexts in a single LLM call for better performance.
    """
    # Skip if all contexts are already short
    if all(len(c) < 200 for c in contexts):
        return contexts
    
    # Build a single prompt with all contexts numbered
    contexts_text = "\n\n".join([f"Context {i+1}:\n{ctx}" for i, ctx in enumerate(contexts)])
    
    summarization_prompt = f"""Extract ONLY the key medical information from each context that directly answers this question. 
Remove unnecessary details, references, or background information. Keep each summary concise and focused.

Question: {query}

{contexts_text}

Provide a concise summary for each context (under 100 words each). Format as:
Context 1: [summary]
Context 2: [summary]
..."""
    
    try:
        response = llm.invoke(summarization_prompt)
        summary_text = response.content if hasattr(response, 'content') else str(response)
        
        # Parse the numbered summaries
        summarized = []
        lines = summary_text.strip().split('\n')
        current_summary = []
        
        for line in lines:
            # Check if this is a new context marker
            if line.strip().startswith('Context ') and ':' in line:
                # Save previous summary if exists
                if current_summary:
                    summary = ' '.join(current_summary).strip()
                    # Clean markdown and formatting
                    summary = summary.replace('*', '').replace('•', '').replace('-', '')
                    summary = ' '.join(summary.split())
                    summarized.append(summary)
                    current_summary = []
                
                # Start new summary (skip the "Context N:" part)
                content_after_colon = line.split(':', 1)[1] if ':' in line else ''
                if content_after_colon.strip():
                    current_summary.append(content_after_colon.strip())
            else:
                # Continue current summary
                if line.strip():
                    current_summary.append(line.strip())
        
        # Add the last summary
        if current_summary:
            summary = ' '.join(current_summary).strip()
            summary = summary.replace('*', '').replace('•', '').replace('-', '')
            summary = ' '.join(summary.split())
            summarized.append(summary)
        
        # If parsing failed or we got wrong number of summaries, fallback to original
        if len(summarized) != len(contexts):
            return contexts
            
        return summarized
        
    except Exception as e:
        print(f"Summarization failed: {e}")
        return contexts  # Fallback to original


@router.post("", response_model=QueryResponse, status_code=status.HTTP_200_OK)
async def query_endpoint(req: QueryRequest):
    """
    Query endpoint for RAG evaluation with enhanced retrieval.
    
    - **query**: The user's medical question (required)
    - **top_k**: Number of context snippets to retrieve (default: 5)
    - **use_query_expansion**: Expand query with medical terminology (default: False)
    - **score_threshold**: Minimum similarity score to include results (default: 0.0)
    - **summarize_context**: Use AI to intelligently condense contexts (default: False)
    
    Returns:
    - **answer**: The generated answer
    - **contexts**: List of relevant context snippets (original)
    - **scores**: Similarity scores for each context
    - **expanded_query**: Expanded query if query expansion was used
    - **summarized_contexts**: AI-condensed contexts if summarization was used
    - **original_context_length**: Total characters in original contexts
    - **summarized_context_length**: Total characters after summarization
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
        
        # Extract metadata from documents
        metadata_list = [doc.metadata for doc in retrieved_docs]
        
        # Extract context snippets as plain strings, clean and deduplicate
        raw_contexts = [doc.page_content for doc in retrieved_docs]
        
        # Clean unicode escape sequences and normalize whitespace
        cleaned_contexts = []
        seen = set()
        cleaned_scores = []
        cleaned_metadata = []
        
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
                cleaned_metadata.append(metadata_list[idx])
        
        contexts = cleaned_contexts
        final_scores = cleaned_scores
        final_metadata = cleaned_metadata
        
        # AI Context Summarization (optional)
        contexts_for_answer = contexts  # Default to original contexts
        
        if req.summarize_context:
            summarized_contexts = summarize_contexts(req.query, contexts, LLM)
            
            # Use summarized contexts for answer generation AND response
            contexts_for_answer = summarized_contexts
            contexts = summarized_contexts  # Replace contexts with summarized version
            
            # Create documents with summarized content
            from langchain_core.documents import Document
            retrieved_docs = [Document(page_content=ctx, metadata={}) for ctx in summarized_contexts]
        
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
            metadata=final_metadata
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
