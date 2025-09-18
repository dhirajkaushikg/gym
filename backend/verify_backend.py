#!/usr/bin/env python3
"""
Simple script to verify backend is running and responding correctly
"""

import requests
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_backend():
    """Test if backend is running and responding correctly"""
    port = os.environ.get('PORT', '5000')
    base_url = f'http://localhost:{port}'
    
    print(f"Testing backend at {base_url}")
    
    try:
        # Test health check endpoint
        print("1. Testing health check endpoint...")
        response = requests.get(f'{base_url}/', timeout=5)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            print("   ✓ Health check passed")
        else:
            print("   ✗ Health check failed")
            
        # Test members endpoint
        print("\n2. Testing members endpoint...")
        response = requests.get(f'{base_url}/api/members', timeout=5)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   Response: {len(data)} members found")
                print("   ✓ Members endpoint working")
            except:
                print(f"   Response: {response.text[:100]}...")
                print("   ✗ Members endpoint returned non-JSON response")
        else:
            print(f"   Response: {response.text[:100]}...")
            print("   ✗ Members endpoint failed")
            
    except requests.exceptions.ConnectionError:
        print("   ✗ Could not connect to backend. Is it running?")
        return False
    except requests.exceptions.Timeout:
        print("   ✗ Request timed out")
        return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
        
    return True

if __name__ == "__main__":
    print("=== Backend Verification ===")
    success = test_backend()
    
    if success:
        print("\n=== Backend verification completed successfully ===")
        sys.exit(0)
    else:
        print("\n=== Backend verification failed ===")
        sys.exit(1)