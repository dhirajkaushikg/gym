#!/usr/bin/env python3
"""
Test script to diagnose backend connection issues
"""

import os
import sys
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_mongodb_connection():
    """Test MongoDB connection and basic operations"""
    print("Testing MongoDB connection...")
    
    # Get environment variables
    MONGODB_URI = os.getenv('MONGODB_URI')
    DB_NAME = os.getenv('DB_NAME', 'Members')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'Members_List')
    
    if not MONGODB_URI:
        print("ERROR: MONGODB_URI not found in environment variables")
        print("Please check your .env file")
        return False
    
    print(f"Connecting to: {MONGODB_URI}")
    print(f"Database: {DB_NAME}")
    print(f"Collection: {COLLECTION_NAME}")
    
    try:
        # Test connection
        client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000
        )
        
        # Test ping
        client.admin.command('ping')
        print("✓ MongoDB connection successful")
        
        # Test database and collection access
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        # Test basic operations
        test_member = {
            "name": "Test User",
            "mId": "TEST001",
            "mobile": "1234567890",
            "trainingType": "Gym",
            "address": "Test Address",
            "idProof": "Test ID",
            "batch": "Morning",
            "planType": "Monthly",
            "purchaseDate": "2023-01-01",
            "expiryDate": "2023-12-31",
            "totalAmount": 1000,
            "amountPaid": 1000,
            "dueAmount": 0,
            "paymentDetails": "Test payment"
        }
        
        # Insert test member
        result = collection.insert_one(test_member)
        print(f"✓ Insert test successful, ID: {result.inserted_id}")
        
        # Find test member
        found_member = collection.find_one({"_id": result.inserted_id})
        if found_member:
            print("✓ Find test successful")
        else:
            print("✗ Find test failed")
            return False
            
        # Delete test member
        delete_result = collection.delete_one({"_id": result.inserted_id})
        if delete_result.deleted_count > 0:
            print("✓ Delete test successful")
        else:
            print("✗ Delete test failed")
            return False
            
        # Count total members
        count = collection.count_documents({})
        print(f"✓ Total members in collection: {count}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = '.env'
    if not os.path.exists(env_path):
        print(f"WARNING: {env_path} file not found")
        return False
    
    print(f"Checking {env_path} file...")
    required_vars = ['MONGODB_URI', 'DB_NAME', 'COLLECTION_NAME']
    missing_vars = []
    
    with open(env_path, 'r') as f:
        content = f.read()
        for var in required_vars:
            if var not in content:
                missing_vars.append(var)
    
    if missing_vars:
        print(f"WARNING: Missing environment variables: {missing_vars}")
        return False
    else:
        print("✓ All required environment variables present")
        return True

def main():
    print("=== Backend Connection Diagnostics ===\n")
    
    # Check environment file
    env_ok = check_env_file()
    print()
    
    # Test MongoDB connection
    mongo_ok = test_mongodb_connection()
    print()
    
    if env_ok and mongo_ok:
        print("=== All tests passed! ===")
        return 0
    else:
        print("=== Some tests failed ===")
        return 1

if __name__ == "__main__":
    sys.exit(main())