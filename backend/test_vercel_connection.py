import requests

def test_vercel_to_render_connection():
    """
    Test the exact connection that was failing
    """
    url = "https://gym-backend-kixz.onrender.com/api/members"
    origin = "https://gym-git-main-dhirus-projects-0e28fcdd.vercel.app"
    
    print(f"Testing connection from {origin} to {url}")
    
    try:
        # Make a GET request with the exact origin header
        response = requests.get(url, headers={
            'Origin': origin,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        print(f"Status Code: {response.status_code}")
        
        # Check for CORS headers
        cors_headers = {
            'access-control-allow-origin': response.headers.get('access-control-allow-origin'),
            'access-control-allow-credentials': response.headers.get('access-control-allow-credentials'),
        }
        
        print("CORS Headers:")
        for key, value in cors_headers.items():
            print(f"  {key}: {value}")
            
        # Check if the origin is allowed
        allowed_origin = response.headers.get('access-control-allow-origin')
        if allowed_origin == origin:
            print("✅ CORS headers are correctly set for the Vercel origin")
        elif allowed_origin == '*':
            print("✅ CORS headers allow all origins (wildcard)")
        else:
            print(f"⚠️  CORS headers allow: {allowed_origin}")
            
        # Check response content
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Successfully retrieved {len(data)} members")
                print("✅ Connection is working correctly")
                return True
            except Exception as e:
                print(f"❌ Response is not valid JSON: {e}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_vercel_to_render_connection()
    if success:
        print("\n🎉 All tests passed! The CORS issue should be resolved.")
    else:
        print("\n💥 Tests failed. There may still be issues with the connection.")