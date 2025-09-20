# Backend Setup Instructions

## Prerequisites

1. Install Python 3.7 or higher
2. Install MongoDB on your system or sign up for MongoDB Atlas (cloud service)
3. Ensure MongoDB is running

## Local MongoDB Installation

### Windows

1. Download MongoDB Community Server from https://www.mongodb.com/try/download/community
2. Run the installer and follow the installation wizard
3. Start MongoDB service:
   ```
   net start MongoDB
   ```

### macOS

1. Install MongoDB using Homebrew:
   ```
   brew tap mongodb/brew
   brew install mongodb-community
   ```

2. Start MongoDB:
   ```
   brew services start mongodb-community
   ```

### Linux (Ubuntu)

1. Import the MongoDB public GPG key:
   ```
   wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
   ```

2. Create a list file for MongoDB:
   ```
   echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
   ```

3. Update package database:
   ```
   sudo apt-get update
   ```

4. Install MongoDB:
   ```
   sudo apt-get install -y mongodb-org
   ```

5. Start MongoDB:
   ```
   sudo systemctl start mongod
   ```

## MongoDB Atlas (Cloud)

1. Sign up at https://www.mongodb.com/cloud/atlas
2. Create a new cluster
3. Configure database access and network access
4. Get your connection string

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure environment variables in the `backend/.env` file:
   ```
   MONGODB_URI=your_mongodb_connection_string
   DB_NAME=Members
   COLLECTION_NAME=Members List
   ```

   ### Example for local MongoDB:
   ```
   MONGODB_URI=mongodb://localhost:27017
   DB_NAME=Members
   COLLECTION_NAME=Members List
   ```

   ### Example for MongoDB Atlas:
   ```
   MONGODB_URI=mongodb+srv://dhirajkaushikg_db_user:i7NgJDG18XZA0swX@gymmembership.cjz3e8i.mongodb.net/
   DB_NAME=Members
   COLLECTION_NAME=Members List
   ```      

6. (Optional) Initialize the database:
   ```bash
   python init_db.py
   ```

7. Run the application:
   ```bash
   python app.py
   ```

The backend will be available at `http://localhost:5000`.

## Testing Backend Connection

To test the backend connection:

1. Start the backend server
2. Run the test script:
   ```bash
   python test_connection.py
   ```

This will verify that the backend can connect to MongoDB and display information about the database.

## Fallback to localStorage

If the backend is unavailable, the frontend will automatically fall back to localStorage for data storage.