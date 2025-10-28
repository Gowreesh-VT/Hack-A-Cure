#!/usr/bin/env python3
"""
Batch upload script - uploads JSON data in smaller batches to avoid timeouts
"""

import json
import requests
import time
import sys

BACKEND_URL = "http://localhost:8000"
BATCH_SIZE = 50  # Upload 50 documents at a time (reduced to avoid quota)
DELAY_BETWEEN_BATCHES = 10  # Wait 10 seconds between batches

def upload_batch(texts_batch, batch_num, total_batches):
    """Upload a batch of texts"""
    print(f"\n📦 Batch {batch_num}/{total_batches} ({len(texts_batch)} documents)...")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/ingest/upload-texts",
            json={"texts": texts_batch},
            timeout=300  # 5 minute timeout per batch
        )
        
        if response.status_code == 200:
            print(f"✅ Batch {batch_num} uploaded successfully!")
            return True
        else:
            print(f"❌ Batch {batch_num} failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"⏱️  Batch {batch_num} timed out, retrying...")
        return False
    except Exception as e:
        print(f"❌ Error uploading batch {batch_num}: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 batch_upload.py <json_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    print("=" * 60)
    print("BATCH UPLOAD SCRIPT")
    print("=" * 60)
    print(f"\n📄 File: {file_path}")
    print(f"📦 Batch size: {BATCH_SIZE} documents")
    
    # Load JSON data
    print(f"\n📖 Loading JSON file...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        sys.exit(1)
    
    # Extract text from JSON items
    print(f"✅ Loaded {len(data)} items")
    print(f"\n🔄 Extracting text fields...")
    
    texts = []
    for item in data:
        if isinstance(item, dict) and 'text' in item:
            texts.append(item['text'])
        elif isinstance(item, str):
            texts.append(item)
    
    print(f"✅ Extracted {len(texts)} text documents")
    
    # Calculate batches
    total_batches = (len(texts) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"\n📊 Will upload in {total_batches} batches")
    
    # Upload in batches
    successful = 0
    failed = 0
    start_time = time.time()
    
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i+BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        
        max_retries = 3
        for attempt in range(max_retries):
            if upload_batch(batch, batch_num, total_batches):
                successful += 1
                break
            else:
                if attempt < max_retries - 1:
                    print(f"   Retry {attempt + 1}/{max_retries}...")
                    time.sleep(30)  # Wait 30 seconds before retry if quota exceeded
                else:
                    failed += 1
                    print(f"   ⚠️ Batch {batch_num} failed after {max_retries} attempts")
        
        # Add delay between successful batches to avoid quota limits
        if successful > 0 and batch_num < total_batches:
            print(f"   ⏳ Waiting {DELAY_BETWEEN_BATCHES}s before next batch...")
            time.sleep(DELAY_BETWEEN_BATCHES)
        
        # Check current status
        try:
            response = requests.get(f"{BACKEND_URL}/api/v1/ingest/collection-info")
            if response.status_code == 200:
                info = response.json()
                print(f"   📊 Total in collection: {info.get('points_count', 0)} documents")
        except:
            pass
        
        # Small delay between batches
        if batch_num < total_batches:
            time.sleep(2)
    
    # Final summary
    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print("UPLOAD COMPLETE!")
    print("=" * 60)
    print(f"\n✅ Successful batches: {successful}/{total_batches}")
    print(f"❌ Failed batches: {failed}/{total_batches}")
    print(f"⏱️  Total time: {elapsed/60:.1f} minutes")
    
    # Final collection status
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/ingest/collection-info")
        if response.status_code == 200:
            info = response.json()
            print(f"\n📊 Final collection status:")
            print(f"   Collection: {info.get('collection_name')}")
            print(f"   Documents: {info.get('points_count', 0)}")
            print(f"   Status: {info.get('status')}")
    except Exception as e:
        print(f"\n⚠️ Could not fetch final status: {e}")
    
    print("\n🎉 All done! Your medical chatbot is ready to use!")
    print(f"💡 Test it with: python3 test_query_endpoint.py")
    print()

if __name__ == "__main__":
    main()
