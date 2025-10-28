# Quick Start Guide - Dataset Ingestion

## API Endpoints for Dataset Ingestion

Your backend now has the following endpoints available for uploading new datasets:

### 1. **Upload File Endpoint**
```
POST http://localhost:8000/api/v1/ingest/upload-file
```

**What it does:** Upload CSV, JSON, or TXT files containing medical Q&A data

**How to use:**
```bash
curl -X POST "http://localhost:8000/api/v1/ingest/upload-file" \
  -F "file=@your_dataset.csv"
```

---

### 2. **Upload Texts Endpoint**
```
POST http://localhost:8000/api/v1/ingest/upload-texts
```

**What it does:** Upload text strings directly (useful for API-based data ingestion)

**How to use:**
```bash
curl -X POST "http://localhost:8000/api/v1/ingest/upload-texts" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Question: ... Answer: ..."],
    "metadatas": [{"category": "cardiology"}]
  }'
```

---

### 3. **Collection Info Endpoint**
```
GET http://localhost:8000/api/v1/ingest/collection-info
```

**What it does:** Get statistics about your vector database

**How to use:**
```bash
curl -X GET "http://localhost:8000/api/v1/ingest/collection-info"
```

---

## For Your Friend (Dataset Creator)

When your friend is ready to push the dataset, they should format it as:

### Option 1: CSV Format (Recommended)
```csv
question,answer,category
"What is diabetes?","Diabetes is a disease...","endocrinology"
"What causes heart disease?","Heart disease can be caused by...","cardiology"
```

### Option 2: JSON Format
```json
[
  {
    "question": "What is diabetes?",
    "answer": "Diabetes is a disease...",
    "category": "endocrinology"
  }
]
```

Then upload using:
```bash
curl -X POST "YOUR_API_URL/api/v1/ingest/upload-file" \
  -F "file=@medical_dataset.csv"
```

---

## Testing

Run the test script to verify everything works:

```bash
python test_ingestion.py
```

This will:
1. Test uploading text data
2. Create and upload a sample CSV
3. Check the collection information

---

## URL to Submit

**Local Development:**
```
http://localhost:8000/api/v1/ingest/upload-file
```

**Production:** (Update with your actual domain)
```
https://your-domain.com/api/v1/ingest/upload-file
```

---

## Documentation

Full API documentation with examples is available in: `DATASET_INGESTION.md`

---

## Need Help?

- Check the FastAPI auto-generated docs at: `http://localhost:8000/docs`
- All endpoints are under the `/api/v1/ingest` prefix
- Test the endpoints using the provided test script
