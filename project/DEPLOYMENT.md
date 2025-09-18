# Deployment Guide

This guide explains how to deploy the Gym Membership Management System to various hosting platforms.

## Deployment Architecture

The application consists of two separate components:
1. **Frontend**: React/Vite application (static files)
2. **Backend**: Flask API server (Python application)

These components need to be deployed separately since they have different runtime requirements.

## Option 1: Deploy to Netlify (Frontend) + Render (Backend) - Recommended

### Deploying the Frontend to Netlify

1. **Prepare your code**:
   - Make sure your frontend code is in a Git repository
   - Ensure the `.env.production` file is configured with your backend URL

2. **Deploy to Netlify**:
   - Go to [Netlify](https://netlify.com) and sign up/sign in
   - Click "New site from Git"
   - Connect your Git provider (GitHub, GitLab, or Bitbucket)
   - Select your repository
   - Configure the deployment settings:
     - Build command: `npm run build`
     - Publish directory: `dist`
   - Click "Deploy site"

3. **Configure Environment Variables**:
   - Go to your site settings in Netlify
   - Navigate to "Environment variables"
   - Add the following variable:
     - Key: `VITE_BACKEND_URL`
     - Value: Your deployed backend URL (e.g., `https://your-app.onrender.com`)

4. **Redeploy**:
   - Trigger a new deployment for the changes to take effect

### Deploying the Backend to Render

1. **Prepare your code**:
   - Make sure your backend code is in a Git repository
   - Ensure the `.env` file is configured with your MongoDB connection details

2. **Deploy to Render**:
   - Go to [Render](https://render.com) and sign up/sign in
   - Click "New Web Service"
   - Connect your Git provider
   - Select your repository
   - Configure the service:
     - Name: Choose a name for your service
     - Runtime: Python 3
     - Build command: `pip install -r requirements.txt`
     - Start command: `python app.py`
     - Plan: Choose a free or paid plan
   - Click "Create Web Service"

3. **Configure Environment Variables**:
   - In the Render dashboard, go to your service settings
   - Navigate to "Environment variables"
   - Add the following variables:
     - `MONGODB_URI`: Your MongoDB connection string
     - `DB_NAME`: Your database name (e.g., `Members`)
     - `COLLECTION_NAME`: Your collection name (e.g., `Members_List`)

4. **Update Frontend Configuration**:
   - Update the `VITE_BACKEND_URL` in Netlify to point to your Render service URL
   - Redeploy your frontend

## Option 2: Deploy Both to Render

You can deploy both the frontend and backend to Render:

### Deploying the Frontend

1. Create a new Web Service on Render
2. Set the root directory to your frontend folder (`project`)
3. Set the build command to: `npm install && npm run build`
4. Set the start command to: `npm run start`
5. Add environment variables as needed

### Deploying the Backend

1. Create a new Web Service on Render
2. Set the root directory to your backend folder (`backend`)
3. Set the build command to: `pip install -r requirements.txt`
4. Set the start command to: `python app.py`
5. Add environment variables for MongoDB connection

## Option 3: Deploy to Vercel (Frontend) + Railway (Backend)

### Deploying the Frontend to Vercel

1. Go to [Vercel](https://vercel.com) and sign up/sign in
2. Import your Git repository
3. Configure the project:
   - Framework Preset: Vite
   - Root Directory: `project`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Add environment variables in the project settings

### Deploying the Backend to Railway

1. Go to [Railway](https://railway.app) and sign up/sign in
2. Create a new project
3. Deploy from your Git repository
4. Configure the service:
   - Build command: `pip install -r requirements.txt`
   - Start command: `python app.py`
5. Add environment variables for MongoDB connection

## Environment Variables Summary

### Frontend (.env files)
```
VITE_BACKEND_URL=http://localhost:5000  # For development
VITE_BACKEND_URL=https://your-backend-url.com  # For production
```

### Backend (.env file)
```
MONGODB_URI=your_mongodb_connection_string
DB_NAME=Members
COLLECTION_NAME=Members_List
```

## Troubleshooting

### CORS Issues
If you encounter CORS issues after deployment, make sure your Flask backend has the proper CORS configuration:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://your-frontend-url.netlify.app"])
```

### Environment Variables Not Loading
- Make sure environment variable names start with `VITE_` for frontend variables
- Check that environment variables are correctly set in your hosting platform's dashboard
- Redeploy your application after changing environment variables

### Database Connection Issues
- Verify your MongoDB connection string is correct
- Ensure your MongoDB database is accessible from your hosting platform
- Check that IP whitelisting is configured correctly in MongoDB Atlas (if using)

## Best Practices

1. **Use Environment Variables**: Never hardcode sensitive information like API keys or database URLs
2. **Separate Environments**: Use different databases for development and production
3. **Error Handling**: Implement proper error handling in both frontend and backend
4. **Security**: Use HTTPS in production and validate all user inputs
5. **Monitoring**: Set up monitoring and logging for your deployed applications