import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

print("Checking real data in MongoDB...")
print(f"Connecting to: {MONGODB_URI}")
print(f"Database: {DB_NAME}")
print(f"Collection: {COLLECTION_NAME}")

try:
    # Initialize MongoDB client
    client = MongoClient(MONGODB_URI)
    
    # List all databases
    print("\nAvailable databases:")
    print("=" * 30)
    for db_name in client.list_database_names():
        print(f"- {db_name}")
        
        # List collections in each database
        db = client[db_name]
        collections = db.list_collection_names()
        if collections:
            print(f"  Collections: {', '.join(collections)}")
            for collection_name in collections:
                count = db[collection_name].count_documents({})
                print(f"    - {collection_name} ({count} documents)")
    
    # Access the specified database
    db = client[DB_NAME]
    
    # Check if collection exists
    if COLLECTION_NAME in db.list_collection_names():
        collection = db[COLLECTION_NAME]
        count = collection.count_documents({})
        print(f"\nFound {count} documents in the '{COLLECTION_NAME}' collection")
        
        if count > 0:
            print("\nReal data from MongoDB:")
            print("=" * 50)
            documents = list(collection.find().limit(10))  # Limit to 10 documents
            for i, doc in enumerate(documents):
                print(f"Document {i+1}:")
                for key, value in doc.items():
                    print(f"  {key}: {value}")
                print()
        else:
            print("\nNo documents found in the collection")
    else:
        print(f"\nCollection '{COLLECTION_NAME}' does not exist in database '{DB_NAME}'")
        
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    print("This might be because:")
    print("1. MongoDB is not running locally")
    print("2. The connection string is incorrect")
    print("3. Network issues")
finally:
    if 'client' in locals():
        client.close()