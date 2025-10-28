# Medical RAG Chatbot - Backend API

Medical FAQ chatbot backend using Retrieval Augmented Generation to provide accurate answers.

## Key Features:
- Retrieval-Augmented Generation (RAG): Combines vector-based retrieval with LLMs to generate accurate, context-aware medical responses.
- Optimized Vector Search with Qdrant: Enables fast and accurate semantic search across medical datasets.
- FastAPI-Powered Backend: High-performance API ensuring low-latency response times.
- LangChain-Integrated Query Processing: Enhances contextual understanding and document retrieval.
- OpenAI API Integration: Leverages advanced language models to improve the quality and relevance of generated answers.
- Dataset Ingestion API: Easy-to-use endpoints for uploading and managing medical Q&A datasets.

## Tech Stack

### Backend
- Python
- FastAPI
- LangChain
- Qdrant (Vector Database)
- OpenAI API
- PostgreSQL (for user management)

## API Endpoints

### Chat Endpoints
- `POST /api/v1/chat` - Chat with the medical bot
- `WebSocket /api/v1/ws/chat` - Real-time chat via WebSocket

### Dataset Ingestion Endpoints
- `POST /api/v1/ingest/upload-file` - Upload CSV/JSON/TXT files
- `POST /api/v1/ingest/upload-texts` - Upload text strings directly
- `GET /api/v1/ingest/collection-info` - Get vector database statistics

See `DATASET_INGESTION.md` and `QUICK_START_INGESTION.md` for detailed documentation.

## Prompt Engineering
> You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
>
> If you don't know the answer, just say that you don't know. Keep the answer short and concise. Try to use less than 5 sentences.

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database
- Qdrant Cloud account (or local Qdrant instance)
- OpenAI API key

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Gowreesh-VT/Hack-A-Cure.git
   cd Hack-A-Cure
   ```

2. **Set up environment variables**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
   
   Or using Poetry:
   ```bash
   poetry install
   poetry shell
   ```

4. **Run the backend**
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

5. **Access API Documentation**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Using Docker

```bash
docker-compose up --build
```

## Dataset Ingestion

To upload your medical datasets:

1. **Prepare your data** in CSV, JSON, or TXT format
   
2. **Upload using the API:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/ingest/upload-file" \
     -F "file=@your_dataset.csv"
   ```

3. **Or test using the provided script:**
   ```bash
   python test_ingestion.py
   ```

See full documentation in `DATASET_INGESTION.md`

## Configuration

Required environment variables:

```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL_NAME=gpt-4o-mini
OPENAI_EMBEDDINGS_NAME=text-embedding-3-small

# Qdrant
QDRANT_COLLECTION_NAME=medical_qa
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_URL=https://your-qdrant-instance.com

# Database
SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost/dbname

# Security
SECRET_KEY=your_secret_key
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=your_secure_password
```
