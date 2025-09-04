import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

try:
    # Initialize MongoDB client
    client = MongoClient(MONGODB_URI)
    
    # Test connection
    client.admin.command('ping')
    print("MongoDB connection successful!")
    
    # Access database and collection
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    # Test query
    count = collection.count_documents({})
    print(f"Connected to database '{DB_NAME}' and collection '{COLLECTION_NAME}'")
    print(f"Collection contains {count} documents")
    
    # List first 5 members (if any)
    members = list(collection.find().limit(5))
    print(f"\nFirst {len(members)} members:")
    for member in members:
        print(f"- {member.get('name', 'Unknown')} (ID: {member.get('mId', 'Unknown')})")
        
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
finally:
    if 'client' in locals():
        client.close()