import requests
import time

def check_backend_status():
    """
    Check the status of the backend server
    """
    backend_url = "https://gym-backend-kixz.onrender.com"
    
    print(f"Checking backend status at {backend_url}")
    print("=" * 50)
    
    # Test the root endpoint
    try:
        print("Testing root endpoint...")
        response = requests.get(backend_url, timeout=10)
        print(f"Root endpoint status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Root response: {data}")
            except:
                print("Root response: (not JSON)")
                print(f"Response text: {response.text[:200]}...")
        else:
            print(f"Root response: {response.text}")
    except Exception as e:
        print(f"❌ Error accessing root endpoint: {e}")
    
    print("\n" + "-" * 50)
    
    # Test the members endpoint
    try:
        print("Testing members endpoint...")
        response = requests.get(f"{backend_url}/api/members", timeout=10)
        print(f"Members endpoint status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Members count: {len(data)}")
            except:
                print("Members response: (not JSON)")
                print(f"Response text: {response.text[:200]}...")
        else:
            print(f"Members response: {response.text}")
    except Exception as e:
        print(f"❌ Error accessing members endpoint: {e}")
    
    print("\n" + "-" * 50)
    
    # Test CORS headers
    try:
        print("Testing CORS headers...")
        response = requests.get(
            f"{backend_url}/api/members",
            headers={'Origin': 'https://efcgym.vercel.app'},
            timeout=10
        )
        cors_origin = response.headers.get('Access-Control-Allow-Origin', 'Not set')
        cors_credentials = response.headers.get('Access-Control-Allow-Credentials', 'Not set')
        print(f"Access-Control-Allow-Origin: {cors_origin}")
        print(f"Access-Control-Allow-Credentials: {cors_credentials}")
        
        if cors_origin == 'https://efcgym.vercel.app' or cors_origin == '*':
            print("✅ CORS headers are correctly configured")
        else:
            print("⚠️  CORS headers may not be properly configured")
            
    except Exception as e:
        print(f"❌ Error testing CORS headers: {e}")

if __name__ == "__main__":
    check_backend_status()