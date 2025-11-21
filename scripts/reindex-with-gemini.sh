#!/bin/bash
# Script to re-index documents with Gemini embeddings

BACKEND_URL="https://hackacure-api-ex8q.onrender.com"

echo "⚠️  WARNING: This will delete all existing data in your Qdrant collection!"
echo "Press Ctrl+C to cancel, or Enter to continue..."
read

echo "🗑️  Clearing existing collection..."
curl -X DELETE "$BACKEND_URL/api/v1/ingest/clear-collection"
echo -e "\n"

echo "✅ Collection cleared!"
echo ""
echo "📤 Now you need to re-upload your medical documents."
echo "You can do this through the API at: $BACKEND_URL/api/v1/ingest/upload-file"
echo "Or use the docs interface: $BACKEND_URL/docs"
