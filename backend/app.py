from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from pymongo import MongoClient, ASCENDING
from bson import ObjectId
from bson.errors import InvalidId
import os
from dotenv import load_dotenv
import time
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get FRONTEND_URL from environment variables first
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')

# Configure CORS with comprehensive settings
cors_config = {
    "origins": [
        FRONTEND_URL,
        'http://localhost:5173',
        'http://localhost:5174',
        'https://*.netlify.app',
        'https://*.vercel.app',
        'https://gym-git-main-dhirus-projects-0e28fcdd.vercel.app',
        'https://gym-backend-kixz.onrender.com',
        'https://efcgym.vercel.app'  # Add your new Vercel domain
    ],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": [
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Credentials"
    ],
    "supports_credentials": True,
    "max_age": 3600
}

# Configure CORS using flask-cors as a fallback
CORS(app, **cors_config)

# Add a middleware to log request processing time
@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request(response):
    # This will run after the first after_request, adding timing info
    if hasattr(request, 'start_time'):
        duration = time.time() - request.start_time
        logger.info(f"{request.method} {request.path} - {response.status_code} - {duration:.3f}s")
    return response

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

db = None
members_collection = None

# In-memory storage as fallback when MongoDB is not available
in_memory_storage = []

# Initialize MongoDB client with connection pooling
try:
    if MONGODB_URI:
        client = MongoClient(
            MONGODB_URI,
            maxPoolSize=50,
            minPoolSize=10,
            serverSelectionTimeoutMS=10000,  # Increased to 10 seconds
            socketTimeoutMS=10000,           # Increased to 10 seconds
            connectTimeoutMS=10000,          # Increased to 10 seconds
            retryWrites=True,
            retryReads=True
        )
        # Test the connection
        client.admin.command('ping')
        logger.info("MongoDB connection successful")
        
        db = client[DB_NAME]
        members_collection = db[COLLECTION_NAME]
        
        # Create indexes for better query performance
        try:
            members_collection.create_index([("mId", ASCENDING)], unique=True)
            members_collection.create_index([("mobile", ASCENDING)])
            members_collection.create_index([("name", ASCENDING)])
            members_collection.create_index([("expiryDate", ASCENDING)])
            logger.info("Database indexes created successfully")
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")
    else:
        logger.warning("MONGODB_URI not found in environment variables - using in-memory storage")
except Exception as e:
    logger.error(f"MongoDB connection failed: {e}")
    logger.warning("Using in-memory storage as fallback")

# Helper function to convert ObjectId to string
def member_to_dict(member):
    if '_id' in member:
        member['_id'] = str(member['_id'])
    return member

# Enhanced health check endpoint
@app.route('/', methods=['GET'])
def health_check():
    status = {
        'message': 'Backend server is running',
        'mongodb': {
            'connected': members_collection is not None,
            'database': DB_NAME,
            'collection': COLLECTION_NAME
        },
        'environment': {
            'frontend_url': FRONTEND_URL,
            'port': os.environ.get('PORT', 5000)
        },
        'cors': {
            'allowed_origins': [
                FRONTEND_URL,
                'http://localhost:5173',
                'http://localhost:5174',
                'https://*.netlify.app',
                'https://*.vercel.app',
                'https://gym-git-main-dhirus-projects-0e28fcdd.vercel.app',
                'https://gym-backend-kixz.onrender.com',
                'https://efcgym.vercel.app'  # Add your new Vercel domain
            ]
        }
    }
    
    if members_collection is None:
        status['message'] = 'Backend server running but MongoDB connection failed - using in-memory storage'
        status['storage_type'] = 'in-memory'
    
    return jsonify(status)

# Add a specific CORS test endpoint
@app.route('/cors-test', methods=['GET', 'OPTIONS'])
def cors_test():
    return jsonify({
        'message': 'CORS headers are working correctly!',
        'origin_received': request.headers.get('Origin', 'No Origin header'),
        'method': request.method
    })

# Get all members with caching headers
@app.route('/api/members', methods=['GET'])
def get_members():
    # Use in-memory storage if MongoDB is not available
    if members_collection is None:
        response = jsonify([member_to_dict(member) for member in in_memory_storage])
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
        
    try:
        # Add pagination support
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))  # Default to 50 members per page
        skip = (page - 1) * per_page
        
        members = list(members_collection.find().skip(skip).limit(per_page))
        response = jsonify([member_to_dict(member) for member in members])
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except Exception as e:
        logger.error(f"Error fetching members: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to fetch members: {str(e)}'}), 500

# Get a specific member by ID
@app.route('/api/members/<member_id>', methods=['GET'])
def get_member(member_id):
    # Use in-memory storage if MongoDB is not available
    if members_collection is None:
        # Find member in in-memory storage
        member = next((m for m in in_memory_storage if str(m.get('_id', m.get('id', ''))) == member_id), None)
        if member:
            response = jsonify(member_to_dict(member))
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
        else:
            return jsonify({'error': 'Member not found'}), 404
    
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
        logger.error(f"Error fetching member {member_id}: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to fetch member: {str(e)}'}), 500

# Create a new member
@app.route('/api/members', methods=['POST'])
def create_member():
    # Use in-memory storage if MongoDB is not available
    if members_collection is None:
        try:
            # Check if request has JSON data
            if not request.is_json:
                return jsonify({'error': 'Request must be JSON'}), 400
                
            member_data = request.json
            logger.info(f"Creating member with data: {member_data}")
            
            # Validate required fields
            required_fields = ['name', 'mId', 'mobile', 'trainingType', 'address', 
                              'idProof', 'batch', 'planType', 'purchaseDate', 
                              'expiryDate', 'totalAmount', 'amountPaid', 'dueAmount', 
                              'paymentDetails']
            
            missing_fields = [field for field in required_fields if field not in member_data]
            if missing_fields:
                return jsonify({'error': f'Missing required fields: {missing_fields}'}), 400
                
            # Generate a simple ID for in-memory storage
            import uuid
            member_id = str(uuid.uuid4())
            member_data['_id'] = member_id
            member_data['id'] = member_id  # For consistency with frontend
            
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
                
            # Add to in-memory storage
            in_memory_storage.append(member_data)
            
            # Log the operation
            logger.info(f"Created member: {member_data.get('name', 'Unknown')}")
            
            response = jsonify(member_to_dict(member_data))
            response.status_code = 201
            return response
        except Exception as e:
            logger.error(f"Error creating member: {e}")
            logger.error(traceback.format_exc())
            return jsonify({'error': f'Failed to create member: {str(e)}'}), 500
    
    try:
        # Check if request has JSON data
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
            
        member_data = request.json
        logger.info(f"Creating member with data: {member_data}")
        
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
        logger.info(f"Created member: {member_data.get('name', 'Unknown')}")
        
        response = jsonify(member_to_dict(member_data))
        response.status_code = 201
        return response
    except Exception as e:
        logger.error(f"Error creating member: {e}")
        logger.error(traceback.format_exc())
        
        # Handle specific MongoDB errors
        error_message = str(e)
        if "E11000 duplicate key error" in error_message:
            # Extract the duplicate field from the error message
            import re
            match = re.search(r'dup key: { ([^:]+): "([^"]+)" }', error_message)
            if match:
                field_name = match.group(1)
                field_value = match.group(2)
                if field_name == "mId":
                    return jsonify({'error': f'A member with ID "{field_value}" already exists. Please use a different Member ID.'}), 409
                else:
                    return jsonify({'error': f'A member with {field_name} "{field_value}" already exists.'}), 409
            else:
                return jsonify({'error': 'A member with this ID already exists. Please use a different Member ID.'}), 409
        elif "duplicate key error" in error_message.lower():
            return jsonify({'error': 'A member with this ID already exists. Please use a different Member ID.'}), 409
        
        return jsonify({'error': f'Failed to create member: {str(e)}'}), 500

# Update an existing member
@app.route('/api/members/<member_id>', methods=['PUT'])
def update_member(member_id):
    # Use in-memory storage if MongoDB is not available
    if members_collection is None:
        try:
            # Check if request has JSON data
            if not request.is_json:
                return jsonify({'error': 'Request must be JSON'}), 400
                
            member_data = request.json
            logger.info(f"Updating member {member_id} with data: {member_data}")
            
            # Validate required fields
            required_fields = ['name', 'mId', 'mobile', 'trainingType', 'address', 
                              'idProof', 'batch', 'planType', 'purchaseDate', 
                              'expiryDate', 'totalAmount', 'amountPaid', 'dueAmount', 
                              'paymentDetails']
            
            missing_fields = [field for field in required_fields if field not in member_data]
            if missing_fields:
                return jsonify({'error': f'Missing required fields: {missing_fields}'}), 400
                
            # Find and update member in in-memory storage
            member_index = None
            for i, m in enumerate(in_memory_storage):
                if str(m.get('_id', m.get('id', ''))) == member_id:
                    member_index = i
                    break
            
            if member_index is None:
                return jsonify({'error': 'Member not found'}), 404
                
            # Update the member data
            member_data['_id'] = member_id
            member_data['id'] = member_id  # For consistency with frontend
            
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
                
            # Update in in-memory storage
            in_memory_storage[member_index] = member_data
            
            # Log the operation
            logger.info(f"Updated member: {member_data.get('name', 'Unknown')}")
            response = jsonify(member_to_dict(member_data))
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
        except Exception as e:
            logger.error(f"Error updating member {member_id}: {e}")
            logger.error(traceback.format_exc())
            return jsonify({'error': f'Failed to update member: {str(e)}'}), 500
    
    try:
        # Validate ObjectId format
        ObjectId(member_id)
        
        # Check if request has JSON data
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
            
        member_data = request.json
        logger.info(f"Updating member {member_id} with data: {member_data}")
        
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
            logger.info(f"Updated member: {updated_member.get('name', 'Unknown')}")
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
        logger.error(f"Error updating member {member_id}: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to update member: {str(e)}'}), 500

# Delete a member
@app.route('/api/members/<member_id>', methods=['DELETE'])
def delete_member(member_id):
    # Use in-memory storage if MongoDB is not available
    if members_collection is None:
        try:
            # Find and remove member from in-memory storage
            member_index = None
            for i, m in enumerate(in_memory_storage):
                if str(m.get('_id', m.get('id', ''))) == member_id:
                    member_index = i
                    break
            
            if member_index is None:
                return jsonify({'error': 'Member not found'}), 404
                
            # Remove from in-memory storage
            deleted_member = in_memory_storage.pop(member_index)
            
            logger.info(f"Deleted member with ID: {member_id}")
            return jsonify({'message': 'Member deleted successfully'})
        except Exception as e:
            logger.error(f"Error deleting member {member_id}: {e}")
            logger.error(traceback.format_exc())
            return jsonify({'error': f'Failed to delete member: {str(e)}'}), 500
    
    try:
        # Validate ObjectId format
        ObjectId(member_id)
        
        result = members_collection.delete_one({'_id': ObjectId(member_id)})
        
        if result.deleted_count > 0:
            logger.info(f"Deleted member with ID: {member_id}")
            return jsonify({'message': 'Member deleted successfully'})
        else:
            return jsonify({'error': 'Member not found'}), 404
    except InvalidId:
        return jsonify({'error': 'Invalid member ID format'}), 400
    except Exception as e:
        logger.error(f"Error deleting member {member_id}: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to delete member: {str(e)}'}), 500

# Enhanced CORS middleware that manually adds headers to all responses
@app.after_request
def after_request(response):
    # Get the origin from the request
    origin = request.headers.get('Origin')
    
    # List of allowed origins
    allowed_origins = [
        FRONTEND_URL,  # Use the environment variable
        'http://localhost:5173',
        'http://localhost:5734',
        'https://gym-git-main-dhirus-projects-0e28fcdd.vercel.app',
        'https://gym-backend-kixz.onrender.com',
        'https://*.netlify.app',
        'https://*.vercel.app',
        'https://efcgym.vercel.app'  # Add your new Vercel domain
    ]
    
    # Check if origin is in allowed origins or if it's a Vercel deployment
    if origin:
        # Check if it matches any of the allowed patterns
        is_allowed = False
        for allowed_origin in allowed_origins:
            if allowed_origin == origin or (allowed_origin.startswith('https://*.') and origin.startswith('https://' + allowed_origin[10:])):
                is_allowed = True
                break
            # Special case for Vercel deployments
            if 'vercel.app' in origin and 'vercel.app' in allowed_origin:
                is_allowed = True
                break
            # Special case for your specific domain
            if origin == 'https://efcgym.vercel.app':
                is_allowed = True
                break
                
        if is_allowed:
            response.headers['Access-Control-Allow-Origin'] = origin
        else:
            # Allow all for testing (you might want to remove this in production)
            response.headers['Access-Control-Allow-Origin'] = origin
    else:
        # If no origin, allow all
        response.headers['Access-Control-Allow-Origin'] = '*'
    
    # Add all necessary CORS headers
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Access-Control-Allow-Origin, Access-Control-Allow-Credentials'
    response.headers['Access-Control-Max-Age'] = '3600'
    
    # Add security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    
    return response

# Handle preflight OPTIONS requests
@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = make_response()
        origin = request.headers.get('Origin')
        
        # List of allowed origins
        allowed_origins = [
            FRONTEND_URL,  # Use the environment variable
            'http://localhost:5173',
            'http://localhost:5174',
            'https://gym-git-main-dhirus-projects-0e28fcdd.vercel.app',
            'https://gym-backend-kixz.onrender.com',
            'https://*.netlify.app',
            'https://*.vercel.app',
            'https://efcgym.vercel.app'  # Add your new Vercel domain
        ]
        
        # Check if origin is in allowed origins
        if origin:
            is_allowed = False
            for allowed_origin in allowed_origins:
                if allowed_origin == origin or (allowed_origin.startswith('https://*.') and origin.startswith('https://' + allowed_origin[10:])):
                    is_allowed = True
                    break
                # Special case for Vercel deployments
                if 'vercel.app' in origin and 'vercel.app' in allowed_origin:
                    is_allowed = True
                    break
                # Special case for your specific domain
                if origin == 'https://efcgym.vercel.app':
                    is_allowed = True
                    break
                    
            if is_allowed:
                response.headers['Access-Control-Allow-Origin'] = origin
            else:
                # Allow all for testing
                response.headers['Access-Control-Allow-Origin'] = origin
        else:
            response.headers['Access-Control-Allow-Origin'] = '*'
        
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Access-Control-Allow-Origin, Access-Control-Allow-Credentials'
        response.headers['Access-Control-Max-Age'] = '3600'
        response.status_code = 200
        return response

if __name__ == '__main__':
    # Use the PORT environment variable provided by Render, default to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    # Check if we're in a production environment
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    logger.info(f"Starting server on port {port} with debug={debug_mode}")
    app.run(debug=debug_mode, host='0.0.0.0', port=port)