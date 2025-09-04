from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

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

# Initialize MongoDB client
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
members_collection = db[COLLECTION_NAME]

# Helper function to convert ObjectId to string
def member_to_dict(member):
    member['_id'] = str(member['_id'])
    return member

# Health check endpoint
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({'message': 'Backend server is running'})

# Get all members
@app.route('/api/members', methods=['GET'])
def get_members():
    try:
        members = list(members_collection.find())
        return jsonify([member_to_dict(member) for member in members])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get a specific member by ID
@app.route('/api/members/<member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = members_collection.find_one({'_id': ObjectId(member_id)})
        if member:
            return jsonify(member_to_dict(member))
        else:
            return jsonify({'error': 'Member not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create a new member
@app.route('/api/members', methods=['POST'])
def create_member():
    try:
        member_data = request.json
        
        # Remove _id if present (it will be auto-generated)
        if '_id' in member_data:
            del member_data['_id']
            
        # Insert the member into the database
        result = members_collection.insert_one(member_data)
        
        # Add the generated _id to the response
        member_data['_id'] = str(result.inserted_id)
        
        return jsonify(member_data), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update an existing member
@app.route('/api/members/<member_id>', methods=['PUT'])
def update_member(member_id):
    try:
        member_data = request.json
        
        # Remove _id from the update data if present
        if '_id' in member_data:
            del member_data['_id']
            
        # Update the member in the database
        result = members_collection.update_one(
            {'_id': ObjectId(member_id)},
            {'$set': member_data}
        )
        
        if result.matched_count > 0:
            # Fetch and return the updated member
            updated_member = members_collection.find_one({'_id': ObjectId(member_id)})
            return jsonify(member_to_dict(updated_member))
        else:
            return jsonify({'error': 'Member not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete a member
@app.route('/api/members/<member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        result = members_collection.delete_one({'_id': ObjectId(member_id)})
        
        if result.deleted_count > 0:
            return jsonify({'message': 'Member deleted successfully'})
        else:
            return jsonify({'error': 'Member not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Use the PORT environment variable provided by Render, default to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    # Check if we're in a production environment
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    print(f"Starting server on port {port} with debug={debug_mode}")
    app.run(debug=debug_mode, host='0.0.0.0', port=port)