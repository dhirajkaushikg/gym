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
    
    # Access database
    db = client[DB_NAME]
    
    # Create collection if it doesn't exist
    if COLLECTION_NAME not in db.list_collection_names():
        db.create_collection(COLLECTION_NAME)
        print(f"Collection '{COLLECTION_NAME}' created successfully!")
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists.")
        
    # Create indexes for better performance
    collection = db[COLLECTION_NAME]
    collection.create_index("mId", unique=True)  # Member ID should be unique
    collection.create_index("mobile")  # Index on mobile for faster searches
    collection.create_index("name")  # Index on name for faster searches
    print("Indexes created successfully!")
    
    print("Database initialization completed!")
    
except Exception as e:
    print(f"Error initializing database: {e}")
finally:
    if 'client' in locals():
        client.close()