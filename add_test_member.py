import requests
import json

# Test member data
member_data = {
    "name": "John Doe",
    "mId": "M001",
    "mobile": "1234567890",
    "trainingType": "Gym",
    "address": "123 Main St",
    "idProof": "DL12345",
    "batch": "Morning",
    "planType": "Monthly",
    "purchaseDate": "2023-01-01",
    "expiryDate": "2023-02-01",
    "totalAmount": 1000,
    "amountPaid": 1000,
    "dueAmount": 0,
    "paymentDetails": "Cash"
}

# Send POST request to add member
response = requests.post(
    "http://localhost:5000/api/members",
    json=member_data,
    headers={"Content-Type": "application/json"}
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")