import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

print(f"MONGODB_URI: {MONGODB_URI}")
print(f"DB_NAME: {DB_NAME}")
print(f"COLLECTION_NAME: {COLLECTION_NAME}")

try:
    # Initialize MongoDB client
    client = MongoClient(MONGODB_URI)
    
    # Access database
    db = client[DB_NAME]
    
    # Check if collection exists
    if COLLECTION_NAME in db.list_collection_names():
        collection = db[COLLECTION_NAME]
        count = collection.count_documents({})
        print(f"Collection '{COLLECTION_NAME}' exists with {count} documents")
        
        # Show first 5 documents
        documents = list(collection.find().limit(5))
        for i, doc in enumerate(documents):
            print(f"Document {i+1}: {doc}")
    else:
        print(f"Collection '{COLLECTION_NAME}' does not exist")
        
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
finally:
    if 'client' in locals():
        client.close()