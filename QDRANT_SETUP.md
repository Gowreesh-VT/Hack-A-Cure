# Qdrant Setup Guide

## Overview
You need to set up Qdrant (vector database) before using the dataset ingestion endpoints. Here are your options:

---

## Option 1: Qdrant Cloud (Recommended - Free Tier Available)

**Easiest and fastest way to get started!**

### Steps:

1. **Sign up for Qdrant Cloud**
   - Go to: https://cloud.qdrant.io/
   - Create a free account
   - Create a new cluster (free tier: 1GB storage)
   API: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.1YbxjeThyBUT9b4YkfZ82RCmROfeh3rq1JTRq3PqYB0


   curl \
    -X GET 'https://3b2c4f4c-4034-40e7-b04a-cfcf7ce68a8f.europe-west3-0.gcp.cloud.qdrant.io:6333' \
    --header 'api-key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.1YbxjeThyBUT9b4YkfZ82RCmROfeh3rq1JTRq3PqYB0'

    from qdrant_client import QdrantClient

qdrant_client = QdrantClient(
    url="https://3b2c4f4c-4034-40e7-b04a-cfcf7ce68a8f.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.1YbxjeThyBUT9b4YkfZ82RCmROfeh3rq1JTRq3PqYB0",
)

print(qdrant_client.get_collections())

2. **Get your credentials**
   - Once your cluster is created, you'll get:
     - **Cluster URL**: `https://your-cluster-id.us-east-1-0.aws.cloud.qdrant.io:6333`
     - **API Key**: Click "API Keys" and create one

3. **Create a collection**
   
   You can create the collection using their web UI or via Python:
   
   ```python
   from qdrant_client import QdrantClient
   from qdrant_client.models import Distance, VectorParams

   client = QdrantClient(
       url="YOUR_QDRANT_URL",
       api_key="YOUR_API_KEY"
   )

   # Create collection for text-embedding-3-small (1536 dimensions)
   client.create_collection(
       collection_name="medical_qa",
       vectors_config=VectorParams(
           size=1536,  # for text-embedding-3-small
           distance=Distance.COSINE
       )
   )
   ```

4. **Update your `.env` file** (see below)

---

## Option 2: Local Qdrant with Docker (For Development)

**Run Qdrant locally on your machine**

### Steps:

1. **Run Qdrant in Docker**
   ```bash
   docker run -p 6333:6333 -p 6334:6334 \
       -v $(pwd)/qdrant_storage:/qdrant/storage:z \
       qdrant/qdrant
   ```

2. **Create collection** using the Python script below

3. **Update your `.env` file** with:
   ```env
   QDRANT_URL=http://localhost:6333
   QDRANT_API_KEY=  # Leave empty for local
   ```

---

## Option 3: Add Qdrant to Docker Compose

**Run Qdrant alongside your backend**

### Steps:

1. **Update `docker-compose.yml`** to include Qdrant:
   ```yaml
   services:
     backend:
       # ... existing backend config ...
       depends_on:
         - qdrant

     qdrant:
       image: qdrant/qdrant:latest
       container_name: qdrant
       ports:
         - "6333:6333"
         - "6334:6334"
       volumes:
         - qdrant_storage:/qdrant/storage
       networks:
         - app_network

   volumes:
     qdrant_storage:

   networks:
     app_network:
       name: app_network
       driver: bridge
   ```

2. **Update `.env`**:
   ```env
   QDRANT_URL=http://qdrant:6333
   QDRANT_API_KEY=  # Leave empty
   ```

3. **Start everything**:
   ```bash
   docker-compose up -d
   ```

---

## Creating the Collection

After setting up Qdrant, you need to create a collection. Here's a script to help:

### Save this as `setup_qdrant.py` in your project root:

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")

# Get credentials from environment
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "medical_qa")
EMBEDDING_SIZE = 1536  # for text-embedding-3-small

# Connect to Qdrant
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY if QDRANT_API_KEY else None
)

print(f"Connecting to Qdrant at: {QDRANT_URL}")

# Check if collection exists
try:
    existing = client.get_collection(COLLECTION_NAME)
    print(f"✅ Collection '{COLLECTION_NAME}' already exists!")
    print(f"   Vectors count: {existing.vectors_count}")
    print(f"   Points count: {existing.points_count}")
except Exception:
    print(f"Creating collection: {COLLECTION_NAME}")
    
    # Create collection
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=EMBEDDING_SIZE,
            distance=Distance.COSINE
        )
    )
    
    print(f"✅ Collection '{COLLECTION_NAME}' created successfully!")
```

### Run it:
```bash
python setup_qdrant.py
```

---

## Environment Variables

Create a `.env` file in the `backend/` directory with these values:

```env
# === Qdrant Configuration ===
QDRANT_URL=https://your-cluster.cloud.qdrant.io:6333
QDRANT_API_KEY=your_api_key_here
QDRANT_COLLECTION_NAME=medical_qa

# === OpenAI Configuration ===
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL_NAME=gpt-4o-mini
OPENAI_EMBEDDINGS_NAME=text-embedding-3-small

# === Database Configuration ===
SQLALCHEMY_DATABASE_URI=sqlite:///./db.sqlite

# === Security ===
SECRET_KEY=your_secret_key_here
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=changeme123
FIRST_SUPERUSER_FIRST_NAME=Admin
FIRST_SUPERUSER_LAST_NAME=User
JWT_USER=user@example.com
JWT_USER_PASSWORD=user123
JWT_USER_FIRST_NAME=Test
JWT_USER_LAST_NAME=User

# === Other ===
DOMAIN=localhost
ENVIRONMENT=local
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8000
TIME_ZONE=UTC
```

---

## Important Notes

### Embedding Dimensions
Make sure your collection's vector size matches your embedding model:

| Model | Dimensions |
|-------|------------|
| text-embedding-3-small | 1536 |
| text-embedding-3-large | 3072 |
| text-embedding-ada-002 | 1536 |

### Quick Test
After setup, test your Qdrant connection:

```python
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# List all collections
collections = client.get_collections()
print("Available collections:", [c.name for c in collections.collections])

# Get info about your collection
info = client.get_collection(os.getenv("QDRANT_COLLECTION_NAME"))
print(f"Collection info: {info}")
```

---

## Next Steps

1. ✅ Set up Qdrant (choose an option above)
2. ✅ Create `.env` file with your credentials
3. ✅ Create the collection using `setup_qdrant.py`
4. ✅ Start your backend: `python backend/main.py`
5. ✅ Test ingestion: `python test_ingestion.py`

---

## Troubleshooting

**Error: "Collection not found"**
- Run `setup_qdrant.py` to create the collection

**Error: "Connection refused"**
- For Qdrant Cloud: Check your URL and API key
- For local: Make sure Qdrant is running (`docker ps`)

**Error: "Wrong vector size"**
- Make sure collection size matches embedding model dimensions

---

## Need Help?

- Qdrant Cloud Dashboard: https://cloud.qdrant.io/
- Qdrant Documentation: https://qdrant.tech/documentation/
- OpenAI Embeddings: https://platform.openai.com/docs/guides/embeddings
