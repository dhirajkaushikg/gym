import requests
import time

def test_frontend_backend_communication():
    """
    Test if frontend can communicate with backend
    """
    print("Testing frontend-backend communication...")
    
    # Test 1: Check if backend is running
    try:
        backend_response = requests.get("http://localhost:5000/")
        print(f"Backend status: {backend_response.status_code}")
        print(f"Backend response: {backend_response.json()}")
    except Exception as e:
        print(f"Error connecting to backend: {e}")
        return
    
    # Test 2: Check if we can get members from backend
    try:
        members_response = requests.get("http://localhost:5000/api/members")
        print(f"Members API status: {members_response.status_code}")
        if members_response.status_code == 200:
            members = members_response.json()
            print(f"Number of members: {len(members)}")
            for member in members:
                print(f"Member: {member['name']} (ID: {member['mId']})")
        else:
            print(f"Error getting members: {members_response.text}")
    except Exception as e:
        print(f"Error getting members: {e}")
        return
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_frontend_backend_communication()