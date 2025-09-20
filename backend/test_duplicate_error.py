import requests
import json

def test_duplicate_member_error():
    """
    Test that the backend properly handles duplicate member ID errors
    """
    url = "https://gym-backend-kixz.onrender.com/api/members"
    
    # Try to create a member with an ID that already exists
    duplicate_member = {
        "name": "Test Member",
        "mId": "005",  # This ID already exists
        "mobile": "1234567890",
        "trainingType": "General Training",
        "address": "Test Address",
        "idProof": "TEST123",
        "batch": "Morning(5AM-10AM)",
        "planType": "Monthly",
        "purchaseDate": "2023-01-01",
        "expiryDate": "2023-02-01",
        "totalAmount": 1000,
        "amountPaid": 1000,
        "dueAmount": 0,
        "paymentDetails": "Cash"
    }
    
    print("Testing duplicate member ID error handling...")
    print(f"Attempting to create member with existing ID: {duplicate_member['mId']}")
    
    try:
        response = requests.post(url, 
                               json=duplicate_member,
                               headers={'Content-Type': 'application/json'})
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        # Check if we get the improved error message
        if response.status_code in [409, 500]:
            try:
                error_data = response.json()
                print(f"Error Response: {json.dumps(error_data, indent=2)}")
                
                # Check if the error message is helpful
                if 'error' in error_data:
                    error_msg = error_data['error']
                    if 'already exists' in error_msg:
                        print("✅ Improved error handling is working correctly!")
                        print(f"✅ Clear error message: {error_msg}")
                    else:
                        print(f"⚠️  Error message could be clearer: {error_msg}")
                else:
                    print("❌ No error message in response")
            except Exception as e:
                print(f"❌ Could not parse error response: {e}")
                print(f"Response text: {response.text}")
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            try:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
            except:
                print(f"Response text: {response.text}")
                
    except Exception as e:
        print(f"❌ Error making request: {e}")

if __name__ == "__main__":
    test_duplicate_member_error()