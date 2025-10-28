# Quick Start Guide

## 🚀 Get Your Medical RAG Chatbot Running

Follow these steps to set up and run your medical chatbot backend with dataset ingestion capabilities.

---

## Step 1: Clone and Setup

```bash
git clone https://github.com/Gowreesh-VT/Hack-A-Cure.git
cd Hack-A-Cure
```

---

## Step 2: Set Up Qdrant (Vector Database)

Choose ONE of these options:

### Option A: Qdrant Cloud (Recommended - Easiest) ⭐

1. Go to https://cloud.qdrant.io/ and create a free account
2. Create a new cluster (free tier available)
3. Get your cluster URL and API key
4. Continue to Step 3

### Option B: Local Qdrant with Docker Compose

```bash
# Qdrant is already configured in docker-compose.yml
# Just make sure to set QDRANT_URL=http://qdrant:6333 in .env
```

### Option C: Standalone Local Qdrant

```bash
docker run -d -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

📖 **Detailed instructions**: See `QDRANT_SETUP.md`

---

## Step 3: Configure Environment Variables

```bash
cd backend
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# OpenAI (Required)
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL_NAME=gpt-4o-mini
OPENAI_EMBEDDINGS_NAME=text-embedding-3-small

# Qdrant Cloud
QDRANT_URL=https://your-cluster.cloud.qdrant.io:6333
QDRANT_API_KEY=your-api-key-here
QDRANT_COLLECTION_NAME=medical_qa

# OR for Local Qdrant
# QDRANT_URL=http://localhost:6333
# QDRANT_API_KEY=
# QDRANT_COLLECTION_NAME=medical_qa
```

---

## Step 4: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or using Poetry:
```bash
poetry install
poetry shell
```

---

## Step 5: Create Qdrant Collection

```bash
cd ..  # Back to project root
python setup_qdrant.py
```

Expected output:
```
✅ Connected successfully!
✅ Collection 'medical_qa' created successfully!
```

---

## Step 6: Start the Backend

### Option A: Direct Python

```bash
cd backend
python main.py
```

### Option B: Docker Compose

```bash
docker-compose up --build
```

The API will be running at: **http://localhost:8000**

---

## Step 7: Verify Everything Works

### Check API Health
```bash
curl http://localhost:8000/health-check
```

### View API Documentation
Open in browser: http://localhost:8000/docs

---

## Step 8: Upload Your Dataset

### Option 1: Use the Test Script

```bash
python test_ingestion.py
```

### Option 2: Upload via cURL

```bash
curl -X POST "http://localhost:8000/api/v1/ingest/upload-file" \
  -F "file=@your_dataset.csv"
```

### Option 3: Upload via Python

```python
import requests

url = "http://localhost:8000/api/v1/ingest/upload-file"
files = {'file': open('your_dataset.csv', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

---

## 📊 Dataset Format

Your CSV should look like this:

```csv
question,answer,category
"What is diabetes?","Diabetes is a disease that occurs when...","endocrinology"
"What causes heart disease?","Heart disease can be caused by...","cardiology"
```

Or JSON:
```json
[
  {
    "question": "What is diabetes?",
    "answer": "Diabetes is a disease...",
    "category": "endocrinology"
  }
]
```

---

## 🔗 Important URLs

- **API Base**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health-check

### API Endpoints

**Chat:**
- `POST /api/v1/chat` - Ask a medical question
- `WebSocket /api/v1/ws/chat` - Real-time chat

**Ingestion:**
- `POST /api/v1/ingest/upload-file` - Upload dataset file
- `POST /api/v1/ingest/upload-texts` - Upload text strings
- `GET /api/v1/ingest/collection-info` - Get database stats

---

## 📚 Documentation Files

- `README.md` - Project overview
- `QDRANT_SETUP.md` - Detailed Qdrant setup guide
- `DATASET_INGESTION.md` - Complete API documentation
- `QUICK_START_INGESTION.md` - Quick ingestion reference

---

## 🧪 Testing the Chat

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is diabetes?"}'
```

Or use the Swagger UI at http://localhost:8000/docs

---

## 🐛 Troubleshooting

### Backend won't start
- Check `.env` file exists and has correct values
- Verify all dependencies installed: `pip list`

### Can't connect to Qdrant
- Run `python setup_qdrant.py` to test connection
- For local: Check if Qdrant is running: `docker ps`
- For cloud: Verify URL and API key

### Upload fails
- Check Qdrant collection exists: `python setup_qdrant.py`
- Verify OpenAI API key is valid
- Check file format (CSV/JSON/TXT)

### No results from chat
- Make sure you've uploaded data first
- Check collection has data: `GET /api/v1/ingest/collection-info`

---

## 🎯 For Your Friend (Dataset Creator)

Share this endpoint URL:
```
http://localhost:8000/api/v1/ingest/upload-file
```

Or for production:
```
https://your-domain.com/api/v1/ingest/upload-file
```

They can upload with:
```bash
curl -X POST "YOUR_URL_HERE" \
  -F "file=@medical_dataset.csv"
```

---

## ✅ Next Steps

1. ✅ Start backend
2. ✅ Upload initial dataset
3. ✅ Test chat functionality
4. ✅ Deploy to production (optional)
5. ✅ Share ingestion endpoint with team

---

Need help? Check the detailed documentation or create an issue on GitHub!
