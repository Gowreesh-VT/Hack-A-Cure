"""
Test script for dataset ingestion endpoints
"""

import requests
import json

# Base URL - update this if your backend is running on a different port
BASE_URL = "http://localhost:8000/api/v1/ingest"


def test_upload_texts():
    """Test uploading texts directly"""
    print("\n" + "="*50)
    print("TEST 1: Upload Texts")
    print("="*50)
    
    url = f"{BASE_URL}/upload-texts"
    data = {
        "texts": [
            "Question: What is hypertension? Answer: Hypertension, also known as high blood pressure, is a condition where blood pressure is consistently too high. It can lead to serious health complications.",
            "Question: What are symptoms of flu? Answer: Common flu symptoms include fever, cough, sore throat, body aches, headache, and fatigue. Some people may also experience vomiting and diarrhea.",
            "Question: What is diabetes mellitus? Answer: Diabetes mellitus is a group of diseases that affect how your body uses blood sugar (glucose). It can lead to high blood sugar levels."
        ],
        "metadatas": [
            {"category": "cardiology", "source": "test_data"},
            {"category": "infectious_disease", "source": "test_data"},
            {"category": "endocrinology", "source": "test_data"}
        ]
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def test_upload_csv_file(filepath):
    """Test uploading a CSV file"""
    print("\n" + "="*50)
    print("TEST 2: Upload CSV File")
    print("="*50)
    
    url = f"{BASE_URL}/upload-file"
    
    try:
        with open(filepath, 'rb') as f:
            files = {'file': f}
            params = {'chunk_size': 1000, 'chunk_overlap': 200}
            response = requests.post(url, files=files, params=params)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 201
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        print("Skipping CSV file test...")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def test_collection_info():
    """Test getting collection info"""
    print("\n" + "="*50)
    print("TEST 3: Get Collection Info")
    print("="*50)
    
    url = f"{BASE_URL}/collection-info"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def create_sample_csv():
    """Create a sample CSV file for testing"""
    print("\n" + "="*50)
    print("Creating sample CSV file...")
    print("="*50)
    
    import csv
    
    sample_data = [
        {
            "question": "What is cholesterol?",
            "answer": "Cholesterol is a waxy, fat-like substance found in all cells of the body. Your body needs some cholesterol to make hormones, vitamin D, and substances that help you digest foods.",
            "category": "cardiology"
        },
        {
            "question": "What is a migraine?",
            "answer": "A migraine is a type of headache characterized by intense pain, often on one side of the head, accompanied by nausea, vomiting, and sensitivity to light and sound.",
            "category": "neurology"
        },
        {
            "question": "What is asthma?",
            "answer": "Asthma is a condition in which your airways narrow and swell and may produce extra mucus. This can make breathing difficult and trigger coughing, wheezing, and shortness of breath.",
            "category": "pulmonology"
        }
    ]
    
    filename = "sample_medical_qa.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['question', 'answer', 'category']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in sample_data:
                writer.writerow(row)
        
        print(f"Sample CSV file created: {filename}")
        return filename
    except Exception as e:
        print(f"Error creating sample CSV: {str(e)}")
        return None


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("DATASET INGESTION API - TEST SUITE")
    print("="*60)
    print(f"Testing endpoints at: {BASE_URL}")
    
    results = []
    
    # Test 1: Upload texts
    results.append(("Upload Texts", test_upload_texts()))
    
    # Test 2: Create and upload CSV file
    csv_file = create_sample_csv()
    if csv_file:
        results.append(("Upload CSV File", test_upload_csv_file(csv_file)))
    
    # Test 3: Get collection info
    results.append(("Get Collection Info", test_collection_info()))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print("\n" + "="*60)
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"Total: {passed}/{total} tests passed")
    print("="*60)


if __name__ == "__main__":
    main()
