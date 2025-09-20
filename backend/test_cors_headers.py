import requests

def test_cors_headers():
    """
    Test if the backend is correctly setting CORS headers
    """
    url = "https://gym-backend-kixz.onrender.com/api/members"
    
    # Test with a preflight OPTIONS request
    print("Testing OPTIONS request...")
    try:
        response = requests.options(url, headers={
            'Origin': 'https://gym-git-main-dhirus-projects-0e28fcdd.vercel.app',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type'
        })
        
        print(f"OPTIONS Status Code: {response.status_code}")
        print("OPTIONS Response Headers:")
        for key, value in response.headers.items():
            if 'access-control' in key.lower():
                print(f"  {key}: {value}")
                
    except Exception as e:
        print(f"Error with OPTIONS request: {e}")
    
    # Test with a GET request
    print("\nTesting GET request...")
    try:
        response = requests.get(url, headers={
            'Origin': 'https://gym-git-main-dhirus-projects-0e28fcdd.vercel.app'
        })
        
        print(f"GET Status Code: {response.status_code}")
        print("GET Response Headers:")
        for key, value in response.headers.items():
            if 'access-control' in key.lower():
                print(f"  {key}: {value}")
                
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Successfully retrieved {len(data)} members")
            except:
                print("Response is not JSON")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error with GET request: {e}")

if __name__ == "__main__":
    test_cors_headers()