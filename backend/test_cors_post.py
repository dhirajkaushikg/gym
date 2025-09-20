import requests
import json

def test_cors_post():
    """
    Test POST request with CORS headers
    """
    backend_url = "https://gym-backend-kixz.onrender.com"
    
    # Sample member data
    member_data = {
        "name": "Test Member",
        "mId": "999",
        "mobile": "9876543210",
        "trainingType": "Gym",
        "address": "Test Address",
        "idProof": "Test ID",
        "batch": "Morning",
        "planType": "Monthly",
        "purchaseDate": "2025-09-21",
        "expiryDate": "2025-10-21",
        "totalAmount": 1000,
        "amountPaid": 1000,
        "dueAmount": 0,
        "paymentDetails": "Test Payment"
    }
    
    print(f"Testing POST request to {backend_url}")
    print("=" * 50)
    
    # Test the POST endpoint with CORS headers
    try:
        print("Testing POST endpoint with CORS headers...")
        response = requests.post(
            f"{backend_url}/api/members",
            json=member_data,
            headers={
                'Origin': 'https://efcgym.vercel.app',
                'Content-Type': 'application/json'
            },
            timeout=15
        )
        print(f"POST endpoint status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 201:
            try:
                data = response.json()
                print(f"POST response: {data}")
                print("✅ POST request successful")
            except:
                print("POST response: (not JSON)")
                print(f"Response text: {response.text[:200]}...")
        elif response.status_code == 409:
            print("⚠️  Member already exists (this is expected if testing multiple times)")
            try:
                data = response.json()
                print(f"Error response: {data}")
            except:
                print(f"Error response: {response.text}")
        else:
            print(f"POST response: {response.text}")
    except Exception as e:
        print(f"❌ Error accessing POST endpoint: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cors_post()