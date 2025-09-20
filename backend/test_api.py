import requests
import json

# Test getting members from the API
try:
    response = requests.get("http://localhost:5000/api/members")
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    print(f"Response Content: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Number of members: {len(data)}")
        for i, member in enumerate(data):
            print(f"Member {i+1}: {member}")
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Error connecting to API: {e}")