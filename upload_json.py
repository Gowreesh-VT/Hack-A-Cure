"""
Upload JSON dataset to the medical chatbot
"""

import requests
import json
import sys

# Update this with your JSON file path
JSON_FILE_PATH = "path/to/your/dataset.json"  # CHANGE THIS!

# API endpoint
BASE_URL = "http://localhost:8000"
UPLOAD_ENDPOINT = f"{BASE_URL}/api/v1/ingest/upload-file"


def upload_json_file(file_path, chunk_size=1000, chunk_overlap=200):
    """
    Upload a JSON file to the ingestion endpoint
    
    Args:
        file_path: Path to your JSON file
        chunk_size: Size of text chunks (default: 1000)
        chunk_overlap: Overlap between chunks (default: 200)
    """
    print("=" * 60)
    print("UPLOADING JSON DATASET")
    print("=" * 60)
    print(f"\nFile: {file_path}")
    print(f"Endpoint: {UPLOAD_ENDPOINT}")
    
    try:
        # Open and upload the file
        with open(file_path, 'rb') as f:
            files = {'file': f}
            params = {
                'chunk_size': chunk_size,
                'chunk_overlap': chunk_overlap
            }
            
            print("\n⏳ Uploading... This may take a while for large files.")
            
            response = requests.post(
                UPLOAD_ENDPOINT,
                files=files,
                params=params,
                timeout=300  # 5 minute timeout for large files
            )
        
        print(f"\n📊 Status Code: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("\n✅ SUCCESS!")
            print(f"   Message: {data.get('message')}")
            print(f"   Documents Processed: {data.get('documents_processed')}")
            print(f"   Collection: {data.get('collection_name')}")
            return True
        else:
            print(f"\n❌ FAILED!")
            print(f"   Error: {response.text}")
            return False
            
    except FileNotFoundError:
        print(f"\n❌ ERROR: File not found: {file_path}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False


def preview_json_structure(file_path, num_items=3):
    """Preview the structure of your JSON file"""
    print("\n" + "=" * 60)
    print("JSON STRUCTURE PREVIEW")
    print("=" * 60)
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            print(f"\n📄 Type: Array of {len(data)} items")
            print(f"\n🔍 First {min(num_items, len(data))} items:")
            for i, item in enumerate(data[:num_items], 1):
                print(f"\n  Item {i}:")
                if isinstance(item, dict):
                    for key, value in list(item.items())[:5]:  # Show first 5 keys
                        value_str = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                        print(f"    {key}: {value_str}")
                else:
                    print(f"    {str(item)[:100]}")
        elif isinstance(data, dict):
            print(f"\n📄 Type: Single object")
            print(f"\n🔍 Keys: {list(data.keys())}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR reading file: {str(e)}")


def main():
    """Main function"""
    
    # Check if file path provided as argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = JSON_FILE_PATH
    
    # Validate file path
    if file_path == "path/to/your/dataset.json":
        print("❌ ERROR: Please update JSON_FILE_PATH in the script or provide as argument")
        print("\nUsage:")
        print("  python3 upload_json.py /path/to/your/dataset.json")
        print("\nOr edit the script and update JSON_FILE_PATH variable")
        sys.exit(1)
    
    # Preview the JSON structure
    preview_json_structure(file_path)
    
    # Ask for confirmation
    response = input("\n📤 Upload this file? (y/n): ")
    if response.lower() != 'y':
        print("❌ Upload cancelled")
        sys.exit(0)
    
    # Upload the file
    success = upload_json_file(file_path)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ UPLOAD COMPLETE!")
        print("=" * 60)
        print("\n📝 Next steps:")
        print("   1. Test your endpoint: python3 test_query_endpoint.py")
        print("   2. Check collection info:")
        print("      curl http://localhost:8000/api/v1/ingest/collection-info")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
