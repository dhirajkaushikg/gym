#!/bin/bash

# Deployment script for Gym Membership Management System

echo "Gym Membership Management System Deployment Script"
echo "================================================="

echo "This script provides guidance for deploying the application."
echo "Please follow the steps below:"

echo "
1. FRONTEND DEPLOYMENT (Netlify):
   - Build the frontend:
     cd project
     npm run build
   
   - Deploy to Netlify:
     * Go to https://netlify.com
     * Create a new site from Git
     * Set build command to: npm run build
     * Set publish directory to: dist
     * Add environment variable:
       Key: VITE_BACKEND_URL
       Value: https://your-backend-url.com

2. BACKEND DEPLOYMENT (Render):
   - Deploy to Render:
     * Go to https://render.com
     * Create a new Web Service
     * Set build command to: pip install -r requirements.txt
     * Set start command to: python app.py
     * Add environment variables:
       MONGODB_URI=your_mongodb_connection_string
       DB_NAME=Members
       COLLECTION_NAME=Members_List
       FRONTEND_URL=https://your-frontend-url.netlify.app

3. POST-DEPLOYMENT:
   - Update VITE_BACKEND_URL in Netlify to point to your Render backend URL
   - Redeploy the frontend
   - Test the application thoroughly
"

echo "For detailed instructions, please refer to DEPLOYMENT.md and DEPLOYMENT_SUMMARY.md"