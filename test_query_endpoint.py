"""
Test script for the /query endpoint
Tests the endpoint according to the event specifications
"""

import requests
import json
import time

# Base URL - update this with your actual endpoint
BASE_URL = "http://localhost:8000"
QUERY_ENDPOINT = f"{BASE_URL}/query"


def test_query_endpoint():
    """Test the /query endpoint with various scenarios"""
    
    print("=" * 60)
    print("TESTING /query ENDPOINT")
    print("=" * 60)
    
    # Test 1: Basic query with default top_k
    print("\n" + "=" * 60)
    print("TEST 1: Basic Query (default top_k)")
    print("=" * 60)
    
    payload = {
        "query": "What is diabetes?",
        "top_k": 5
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            QUERY_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        elapsed = time.time() - start_time
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {elapsed:.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nAnswer: {data.get('answer', 'N/A')}")
            print(f"\nContexts ({len(data.get('contexts', []))}):")
            for i, ctx in enumerate(data.get('contexts', []), 1):
                print(f"  {i}. {ctx[:100]}..." if len(ctx) > 100 else f"  {i}. {ctx}")
            print("\n✅ Test 1 PASSED")
        else:
            print(f"❌ Test 1 FAILED: {response.text}")
            
    except Exception as e:
        print(f"❌ Test 1 FAILED: {str(e)}")
    
    # Test 2: Query with custom top_k
    print("\n" + "=" * 60)
    print("TEST 2: Query with top_k=3")
    print("=" * 60)
    
    payload = {
        "query": "When to give Tdap booster?",
        "top_k": 3
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            QUERY_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        elapsed = time.time() - start_time
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {elapsed:.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nAnswer: {data.get('answer', 'N/A')}")
            print(f"\nContexts ({len(data.get('contexts', []))}):")
            for i, ctx in enumerate(data.get('contexts', []), 1):
                print(f"  {i}. {ctx[:100]}..." if len(ctx) > 100 else f"  {i}. {ctx}")
            
            # Verify contexts count
            if len(data.get('contexts', [])) <= 3:
                print("\n✅ Test 2 PASSED")
            else:
                print(f"\n⚠️  Warning: Expected max 3 contexts, got {len(data.get('contexts', []))}")
        else:
            print(f"❌ Test 2 FAILED: {response.text}")
            
    except Exception as e:
        print(f"❌ Test 2 FAILED: {str(e)}")
    
    # Test 3: Verify response structure
    print("\n" + "=" * 60)
    print("TEST 3: Verify Response Structure")
    print("=" * 60)
    
    payload = {
        "query": "What causes heart disease?",
        "top_k": 4
    }
    
    try:
        response = requests.post(
            QUERY_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields
            has_answer = 'answer' in data and isinstance(data['answer'], str)
            has_contexts = 'contexts' in data and isinstance(data['contexts'], list)
            contexts_are_strings = all(isinstance(ctx, str) for ctx in data.get('contexts', []))
            
            print(f"Has 'answer' field (string): {'✅' if has_answer else '❌'}")
            print(f"Has 'contexts' field (list): {'✅' if has_contexts else '❌'}")
            print(f"All contexts are strings: {'✅' if contexts_are_strings else '❌'}")
            
            if has_answer and has_contexts and contexts_are_strings:
                print("\n✅ Test 3 PASSED - Response structure is correct")
            else:
                print("\n❌ Test 3 FAILED - Response structure is invalid")
        else:
            print(f"❌ Test 3 FAILED: Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test 3 FAILED: {str(e)}")
    
    # Test 4: Empty query handling
    print("\n" + "=" * 60)
    print("TEST 4: Empty Query Handling")
    print("=" * 60)
    
    payload = {
        "query": "",
        "top_k": 5
    }
    
    try:
        response = requests.post(
            QUERY_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 400:
            print("✅ Test 4 PASSED - Correctly rejects empty query")
        else:
            print(f"⚠️  Test 4: Expected 400, got {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test 4 FAILED: {str(e)}")
    
    # Test 5: cURL example from specs
    print("\n" + "=" * 60)
    print("TEST 5: Example from Specifications")
    print("=" * 60)
    
    payload = {
        "query": "When to give Tdap booster?",
        "top_k": 3
    }
    
    print(f"\nRequest:")
    print(f"curl -X POST {QUERY_ENDPOINT} \\")
    print(f"  -H 'Content-Type: application/json' \\")
    print(f"  -d '{json.dumps(payload)}'")
    
    try:
        response = requests.post(
            QUERY_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        print(f"\nResponse:")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
            print("\n✅ Test 5 PASSED")
        else:
            print(response.text)
            print("\n❌ Test 5 FAILED")
            
    except Exception as e:
        print(f"❌ Test 5 FAILED: {str(e)}")
    
    # Final Summary
    print("\n" + "=" * 60)
    print("ENDPOINT DETAILS FOR SUBMISSION")
    print("=" * 60)
    print(f"\n📍 Endpoint URL: {QUERY_ENDPOINT}")
    print(f"📍 Method: POST")
    print(f"📍 Content-Type: application/json")
    print(f"\n📋 Request Format:")
    print(json.dumps({"query": "string", "top_k": "integer"}, indent=2))
    print(f"\n📋 Response Format:")
    print(json.dumps({"answer": "string", "contexts": ["string", "..."]}, indent=2))
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_query_endpoint()
