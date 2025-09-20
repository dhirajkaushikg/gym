import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

print("Checking data in MongoDB Atlas...")
print(f"Connecting to: {MONGODB_URI}")
print(f"Database: {DB_NAME}")
print(f"Collection: {COLLECTION_NAME}")

try:
    # Initialize MongoDB client
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    
    # Test the connection
    client.admin.command('ping')
    print("\n✓ Successfully connected to MongoDB Atlas!")
    
    # List all databases
    print("\nAvailable databases:")
    print("=" * 30)
    try:
        for db_name in client.list_database_names():
            print(f"- {db_name}")
            
            # List collections in each database
            db = client[db_name]
            collections = db.list_collection_names()
            if collections:
                print(f"  Collections: {', '.join(collections)}")
                for collection_name in collections:
                    try:
                        count = db[collection_name].count_documents({})
                        print(f"    - {collection_name} ({count} documents)")
                    except Exception as e:
                        print(f"    - {collection_name} (count unavailable: {e})")
    except Exception as e:
        print(f"Could not list databases: {e}")
    
    # Access the specified database and collection
    try:
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        count = collection.count_documents({})
        print(f"\nFound {count} documents in the '{COLLECTION_NAME}' collection")
        
        if count > 0:
            print("\nReal data from MongoDB Atlas:")
            print("=" * 50)
            # Show first 5 documents
            documents = list(collection.find().limit(5))
            for i, doc in enumerate(documents):
                print(f"Document {i+1}:")
                for key, value in doc.items():
                    # Limit the length of values for readability
                    if isinstance(value, str) and len(value) > 100:
                        print(f"  {key}: {value[:100]}...")
                    else:
                        print(f"  {key}: {value}")
                print()
        else:
            print(f"\nNo documents found in the '{COLLECTION_NAME}' collection")
    except Exception as e:
        print(f"\nError accessing collection '{COLLECTION_NAME}': {e}")
        print("Available collections in database:")
        try:
            collections = db.list_collection_names()
            for collection_name in collections:
                print(f"  - {collection_name}")
        except Exception as e2:
            print(f"Could not list collections: {e2}")
        
except Exception as e:
    print(f"Error connecting to MongoDB Atlas: {e}")
    print("This might be because:")
    print("1. The connection string is incorrect")
    print("2. Network issues")
    print("3. Authentication failed")
    print("4. The database/collection doesn't exist")
finally:
    if 'client' in locals():
        client.close()