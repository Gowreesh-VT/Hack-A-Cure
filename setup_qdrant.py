"""
Setup script for Qdrant vector database
Creates the collection needed for the medical chatbot
"""

import os
import sys
from dotenv import load_dotenv

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
if not os.path.exists(env_path):
    print("❌ Error: .env file not found!")
    print(f"   Expected location: {env_path}")
    print("\n📝 Please create a .env file based on backend/.env.example")
    print("   Then update it with your Qdrant and OpenAI credentials.")
    sys.exit(1)

load_dotenv(env_path)

# Import after loading env vars
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# Get credentials from environment
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "medical_qa")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDINGS_NAME", "text-embedding-3-small")

# Embedding dimensions for different models
EMBEDDING_DIMENSIONS = {
    "text-embedding-3-small": 1536,
    "text-embedding-3-large": 3072,
    "text-embedding-ada-002": 1536,
}

EMBEDDING_SIZE = EMBEDDING_DIMENSIONS.get(EMBEDDING_MODEL, 1536)

def main():
    print("=" * 60)
    print("QDRANT SETUP SCRIPT")
    print("=" * 60)
    
    # Validate environment variables
    if not QDRANT_URL:
        print("❌ Error: QDRANT_URL not set in .env file")
        sys.exit(1)
    
    print(f"\n📊 Configuration:")
    print(f"   Qdrant URL: {QDRANT_URL}")
    print(f"   Collection Name: {COLLECTION_NAME}")
    print(f"   Embedding Model: {EMBEDDING_MODEL}")
    print(f"   Vector Dimensions: {EMBEDDING_SIZE}")
    print(f"   API Key: {'✅ Set' if QDRANT_API_KEY else '❌ Not set (OK for local)'}")
    
    # Connect to Qdrant
    try:
        print(f"\n🔌 Connecting to Qdrant...")
        client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY if QDRANT_API_KEY else None
        )
        print("✅ Connected successfully!")
    except Exception as e:
        print(f"❌ Failed to connect to Qdrant: {str(e)}")
        print("\n💡 Troubleshooting:")
        print("   - Check if Qdrant is running (for local setup)")
        print("   - Verify QDRANT_URL and QDRANT_API_KEY are correct")
        print("   - For Qdrant Cloud, check your cluster status")
        sys.exit(1)
    
    # Check if collection exists
    print(f"\n🔍 Checking for collection '{COLLECTION_NAME}'...")
    try:
        existing = client.get_collection(COLLECTION_NAME)
        print(f"✅ Collection '{COLLECTION_NAME}' already exists!")
        print(f"   📊 Statistics:")
        print(f"      - Vectors count: {existing.vectors_count}")
        print(f"      - Points count: {existing.points_count}")
        print(f"      - Status: {existing.status}")
        
        # Verify vector dimensions
        if existing.config.params.vectors.size != EMBEDDING_SIZE:
            print(f"\n⚠️  WARNING: Vector size mismatch!")
            print(f"   Collection size: {existing.config.params.vectors.size}")
            print(f"   Expected size: {EMBEDDING_SIZE}")
            print(f"   You may need to recreate the collection or change your embedding model.")
        
    except Exception as e:
        print(f"ℹ️  Collection does not exist. Creating...")
        
        try:
            # Create collection
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=EMBEDDING_SIZE,
                    distance=Distance.COSINE
                )
            )
            
            print(f"✅ Collection '{COLLECTION_NAME}' created successfully!")
            print(f"   Vector size: {EMBEDDING_SIZE}")
            print(f"   Distance metric: COSINE")
            
        except Exception as create_error:
            print(f"❌ Failed to create collection: {str(create_error)}")
            sys.exit(1)
    
    # List all collections
    print(f"\n📋 All collections in this Qdrant instance:")
    try:
        collections = client.get_collections()
        for collection in collections.collections:
            print(f"   - {collection.name}")
    except Exception as e:
        print(f"   ⚠️  Could not list collections: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ SETUP COMPLETE!")
    print("=" * 60)
    print("\n📝 Next steps:")
    print("   1. Start your backend: cd backend && python main.py")
    print("   2. Test ingestion: python test_ingestion.py")
    print("   3. Check API docs: http://localhost:8000/docs")
    print("\n")


if __name__ == "__main__":
    main()
