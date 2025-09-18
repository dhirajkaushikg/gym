from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient, ASCENDING
from bson import ObjectId
from bson.errors import InvalidId
import os
from dotenv import load_dotenv
import time
import traceback

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS for different environments
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')
CORS(app, origins=[FRONTEND_URL, 'http://localhost:5173', 'http://localhost:5174', 'https://*.netlify.app', 'https://*.vercel.app'])

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

# Initialize MongoDB client with connection pooling
try:
    client = MongoClient(
        MONGODB_URI,
        maxPoolSize=50,
        minPoolSize=10,
        serverSelectionTimeoutMS=5000,
        socketTimeoutMS=5000,
        connectTimeoutMS=5000
    )
    # Test the connection
    client.admin.command('ping')
    print("MongoDB connection successful")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    client = None

if client:
    db = client[DB_NAME]
    members_collection = db[COLLECTION_NAME]
    
    # Create indexes for better query performance
    try:
        members_collection.create_index([("mId", ASCENDING)], unique=True)
        members_collection.create_index([("mobile", ASCENDING)])
        members_collection.create_index([("name", ASCENDING)])
        members_collection.create_index([("expiryDate", ASCENDING)])
        print("Database indexes created successfully")
    except Exception as e:
        print(f"Error creating indexes: {e}")
else:
    print("Failed to connect to MongoDB. Backend will not function properly.")
    members_collection = None

# Helper function to convert ObjectId to string
def member_to_dict(member):
    if '_id' in member:
        member['_id'] = str(member['_id'])
    return member

# Add a middleware to log request processing time
@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request(response):
    if hasattr(request, 'start_time'):
        duration = time.time() - request.start_time
        app.logger.info(f"{request.method} {request.path} - {response.status_code} - {duration:.3f}s")
    return response

# Health check endpoint
@app.route('/', methods=['GET'])
def health_check():
    if not client:
        return jsonify({'message': 'Backend server running but MongoDB connection failed'}), 500
    return jsonify({'message': 'Backend server is running'})

# Get all members with caching headers
@app.route('/api/members', methods=['GET'])
def get_members():
    if not members_collection:
        return jsonify({'error': 'Database connection not available'}), 500
        
    try:
        members = list(members_collection.find())
        response = jsonify([member_to_dict(member) for member in members])
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except Exception as e:
        app.logger.error(f"Error fetching members: {e}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to fetch members: {str(e)}'}), 500

# Get a specific member by ID
@app.route('/api/members/<member_id>', methods=['GET'])
def get_member(member_id):
    if not members_collection:
        return jsonify({'error': 'Database connection not available'}), 500
        
    try:
        # Validate ObjectId format
        ObjectId(member_id)
        member = members_collection.find_one({'_id': ObjectId(member_id)})
        if member:
            response = jsonify(member_to_dict(member))
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
        else:
            return jsonify({'error': 'Member not found'}), 404
    except InvalidId:
        return jsonify({'error': 'Invalid member ID format'}), 400
    except Exception as e:
        app.logger.error(f"Error fetching member {member_id}: {e}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to fetch member: {str(e)}'}), 500

# Create a new member
@app.route('/api/members', methods=['POST'])
def create_member():
    if not members_collection:
        return jsonify({'error': 'Database connection not available'}), 500
        
    try:
        member_data = request.json
        app.logger.info(f"Creating member with data: {member_data}")
        
        # Validate required fields
        required_fields = ['name', 'mId', 'mobile', 'trainingType', 'address', 
                          'idProof', 'batch', 'planType', 'purchaseDate', 
                          'expiryDate', 'totalAmount', 'amountPaid', 'dueAmount', 
                          'paymentDetails']
        
        missing_fields = [field for field in required_fields if field not in member_data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {missing_fields}'}), 400
            
        # Remove _id if present (it will be auto-generated)
        if '_id' in member_data:
            del member_data['_id']
            
        # Validate numeric fields
        try:
            member_data['totalAmount'] = float(member_data['totalAmount'])
            member_data['amountPaid'] = float(member_data['amountPaid'])
            member_data['dueAmount'] = float(member_data['dueAmount'])
        except (ValueError, TypeError) as e:
            return jsonify({'error': f'Invalid numeric values: {str(e)}'}), 400
            
        # Validate date fields
        try:
            # This will raise ValueError if dates are invalid
            from datetime import datetime
            datetime.strptime(member_data['purchaseDate'], '%Y-%m-%d')
            datetime.strptime(member_data['expiryDate'], '%Y-%m-%d')
        except ValueError as e:
            return jsonify({'error': f'Invalid date format. Use YYYY-MM-DD: {str(e)}'}), 400
            
        # Insert the member into the database
        result = members_collection.insert_one(member_data)
        
        # Add the generated _id to the response
        member_data['_id'] = str(result.inserted_id)
        
        # Log the operation
        app.logger.info(f"Created member: {member_data.get('name', 'Unknown')}")
        
        response = jsonify(member_to_dict(member_data))
        response.status_code = 201
        return response
    except Exception as e:
        app.logger.error(f"Error creating member: {e}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to create member: {str(e)}'}), 500

# Update an existing member
@app.route('/api/members/<member_id>', methods=['PUT'])
def update_member(member_id):
    if not members_collection:
        return jsonify({'error': 'Database connection not available'}), 500
        
    try:
        # Validate ObjectId format
        ObjectId(member_id)
        
        member_data = request.json
        app.logger.info(f"Updating member {member_id} with data: {member_data}")
        
        # Validate required fields
        required_fields = ['name', 'mId', 'mobile', 'trainingType', 'address', 
                          'idProof', 'batch', 'planType', 'purchaseDate', 
                          'expiryDate', 'totalAmount', 'amountPaid', 'dueAmount', 
                          'paymentDetails']
        
        missing_fields = [field for field in required_fields if field not in member_data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {missing_fields}'}), 400
            
        # Remove _id from the update data if present
        if '_id' in member_data:
            del member_data['_id']
            
        # Validate numeric fields
        try:
            member_data['totalAmount'] = float(member_data['totalAmount'])
            member_data['amountPaid'] = float(member_data['amountPaid'])
            member_data['dueAmount'] = float(member_data['dueAmount'])
        except (ValueError, TypeError) as e:
            return jsonify({'error': f'Invalid numeric values: {str(e)}'}), 400
            
        # Validate date fields
        try:
            # This will raise ValueError if dates are invalid
            from datetime import datetime
            datetime.strptime(member_data['purchaseDate'], '%Y-%m-%d')
            datetime.strptime(member_data['expiryDate'], '%Y-%m-%d')
        except ValueError as e:
            return jsonify({'error': f'Invalid date format. Use YYYY-MM-DD: {str(e)}'}), 400
            
        # Update the member in the database
        result = members_collection.update_one(
            {'_id': ObjectId(member_id)},
            {'$set': member_data}
        )
        
        if result.matched_count > 0:
            # Fetch and return the updated member
            updated_member = members_collection.find_one({'_id': ObjectId(member_id)})
            app.logger.info(f"Updated member: {updated_member.get('name', 'Unknown')}")
            response = jsonify(member_to_dict(updated_member))
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
        else:
            return jsonify({'error': 'Member not found'}), 404
    except InvalidId:
        return jsonify({'error': 'Invalid member ID format'}), 400
    except Exception as e:
        app.logger.error(f"Error updating member {member_id}: {e}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to update member: {str(e)}'}), 500

# Delete a member
@app.route('/api/members/<member_id>', methods=['DELETE'])
def delete_member(member_id):
    if not members_collection:
        return jsonify({'error': 'Database connection not available'}), 500
        
    try:
        # Validate ObjectId format
        ObjectId(member_id)
        
        result = members_collection.delete_one({'_id': ObjectId(member_id)})
        
        if result.deleted_count > 0:
            app.logger.info(f"Deleted member with ID: {member_id}")
            return jsonify({'message': 'Member deleted successfully'})
        else:
            return jsonify({'error': 'Member not found'}), 404
    except InvalidId:
        return jsonify({'error': 'Invalid member ID format'}), 400
    except Exception as e:
        app.logger.error(f"Error deleting member {member_id}: {e}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to delete member: {str(e)}'}), 500

if __name__ == '__main__':
    # Use the PORT environment variable provided by Render, default to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    # Check if we're in a production environment
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    print(f"Starting server on port {port} with debug={debug_mode}")
    app.run(debug=debug_mode, host='0.0.0.0', port=port)