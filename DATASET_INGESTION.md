# Dataset Ingestion API Documentation

## Overview
This document describes the API endpoints available for ingesting new datasets into the medical chatbot's vector store.

## Base URL
```
http://localhost:8000/api/v1/ingest
```

## Endpoints

### 1. Upload File
Upload and ingest a file (TXT, JSON, CSV) into the vector store.

**Endpoint:** `POST /upload-file`

**Parameters:**
- `file` (required): The file to upload (supported formats: .txt, .json, .csv)
- `chunk_size` (optional, default: 1000): Size of text chunks for splitting
- `chunk_overlap` (optional, default: 200): Overlap between chunks

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/ingest/upload-file?chunk_size=1000&chunk_overlap=200" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_dataset.csv"
```

**Example using Python:**
```python
import requests

url = "http://localhost:8000/api/v1/ingest/upload-file"
files = {'file': open('your_dataset.csv', 'rb')}
params = {'chunk_size': 1000, 'chunk_overlap': 200}

response = requests.post(url, files=files, params=params)
print(response.json())
```

**Response:**
```json
{
  "message": "Successfully ingested your_dataset.csv",
  "documents_processed": 150,
  "collection_name": "medical_qa"
}
```

---

### 2. Upload Texts
Ingest a list of text strings directly into the vector store.

**Endpoint:** `POST /upload-texts`

**Parameters:**
- `chunk_size` (optional, default: 1000): Size of text chunks for splitting
- `chunk_overlap` (optional, default: 200): Overlap between chunks

**Request Body:**
```json
{
  "texts": [
    "Question: What is diabetes? Answer: Diabetes is a disease that occurs when your blood glucose is too high.",
    "Question: What causes heart disease? Answer: Heart disease can be caused by multiple factors including high blood pressure..."
  ],
  "metadatas": [
    {"category": "diabetes", "source": "medical_db"},
    {"category": "cardiology", "source": "medical_db"}
  ]
}
```

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/ingest/upload-texts" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Question: What is diabetes? Answer: Diabetes is a disease...",
      "Question: What causes heart disease? Answer: Heart disease..."
    ],
    "metadatas": [
      {"category": "diabetes"},
      {"category": "cardiology"}
    ]
  }'
```

**Example using Python:**
```python
import requests

url = "http://localhost:8000/api/v1/ingest/upload-texts"
data = {
    "texts": [
        "Question: What is diabetes? Answer: Diabetes is a disease...",
        "Question: What causes heart disease? Answer: Heart disease..."
    ],
    "metadatas": [
        {"category": "diabetes", "source": "medical_db"},
        {"category": "cardiology", "source": "medical_db"}
    ]
}

response = requests.post(url, json=data)
print(response.json())
```

**Response:**
```json
{
  "message": "Successfully ingested texts",
  "documents_processed": 2,
  "collection_name": "medical_qa"
}
```

---

### 3. Get Collection Info
Get information about the current collection.

**Endpoint:** `GET /collection-info`

**Example using curl:**
```bash
curl -X GET "http://localhost:8000/api/v1/ingest/collection-info" \
  -H "accept: application/json"
```

**Example using Python:**
```python
import requests

url = "http://localhost:8000/api/v1/ingest/collection-info"
response = requests.get(url)
print(response.json())
```

**Response:**
```json
{
  "collection_name": "medical_qa",
  "vectors_count": 5420,
  "points_count": 5420,
  "status": "green"
}
```

---

## Supported File Formats

### 1. CSV Format
Your CSV file should have columns for questions and answers, or a content column.

**Example CSV:**
```csv
question,answer,category
What is diabetes?,Diabetes is a disease that occurs when your blood glucose is too high.,endocrinology
What causes heart disease?,"Heart disease can be caused by multiple factors including high blood pressure, high cholesterol, and smoking.",cardiology
```

### 2. JSON Format
Your JSON file should be an array of objects or a single object.

**Example JSON (Array):**
```json
[
  {
    "question": "What is diabetes?",
    "answer": "Diabetes is a disease that occurs when your blood glucose is too high.",
    "category": "endocrinology"
  },
  {
    "question": "What causes heart disease?",
    "answer": "Heart disease can be caused by multiple factors...",
    "category": "cardiology"
  }
]
```

**Example JSON (Question-Answer pairs):**
```json
[
  {
    "content": "Question: What is diabetes?\nAnswer: Diabetes is a disease that occurs when your blood glucose is too high.",
    "category": "endocrinology"
  }
]
```

### 3. TXT Format
Plain text files will be ingested as-is and split into chunks.

**Example TXT:**
```
Medical FAQ Database

Question: What is diabetes?
Answer: Diabetes is a disease that occurs when your blood glucose, also called blood sugar, is too high.

Question: What causes heart disease?
Answer: Heart disease can be caused by multiple factors including high blood pressure, high cholesterol, and smoking.
```

---

## Testing the Endpoints

### Quick Test Script
```python
import requests

BASE_URL = "http://localhost:8000/api/v1/ingest"

# Test 1: Upload texts
def test_upload_texts():
    url = f"{BASE_URL}/upload-texts"
    data = {
        "texts": [
            "Question: What is hypertension? Answer: Hypertension, also known as high blood pressure, is a condition where blood pressure is consistently too high.",
            "Question: What are symptoms of flu? Answer: Common flu symptoms include fever, cough, sore throat, body aches, and fatigue."
        ],
        "metadatas": [
            {"category": "cardiology", "source": "test"},
            {"category": "infectious_disease", "source": "test"}
        ]
    }
    response = requests.post(url, json=data)
    print("Upload Texts Response:", response.json())

# Test 2: Get collection info
def test_collection_info():
    url = f"{BASE_URL}/collection-info"
    response = requests.get(url)
    print("Collection Info:", response.json())

if __name__ == "__main__":
    test_upload_texts()
    test_collection_info()
```

---

## Important Notes

1. **Authentication**: Currently, these endpoints are not protected. Consider adding authentication before deploying to production.

2. **Chunk Size**: Adjust `chunk_size` based on your content:
   - Short Q&A pairs: 500-800
   - Medium documents: 1000-1500
   - Long articles: 2000-3000

3. **Chunk Overlap**: Keep 20-30% overlap to maintain context between chunks.

4. **Rate Limiting**: For large datasets, consider implementing rate limiting or batch processing.

5. **File Size**: There may be file size limits depending on your FastAPI configuration.

---

## Production Deployment

When deploying to production, update the base URL accordingly:

```python
# Example for production
BASE_URL = "https://your-api-domain.com/api/v1/ingest"
```

---

## Contact
For issues or questions, please contact the development team.
