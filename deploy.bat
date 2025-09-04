@echo off
title Gym Membership Management System Deployment

echo Gym Membership Management System Deployment Script
echo =================================================

echo This script provides guidance for deploying the application.
echo Please follow the steps below:

echo.
echo 1. FRONTEND DEPLOYMENT (Netlify):
echo    - Build the frontend:
echo      cd project
echo      npm run build
echo.
echo    - Deploy to Netlify:
echo      * Go to https://netlify.com
echo      * Create a new site from Git
echo      * Set build command to: npm run build
echo      * Set publish directory to: dist
echo      * Add environment variable:
echo        Key: VITE_BACKEND_URL
echo        Value: https://your-backend-url.com

echo.
echo 2. BACKEND DEPLOYMENT (Render):
echo    - Deploy to Render:
echo      * Go to https://render.com
echo      * Create a new Web Service
echo      * Set build command to: pip install -r requirements.txt
echo      * Set start command to: python app.py
echo      * Add environment variables:
echo        MONGODB_URI=your_mongodb_connection_string
echo        DB_NAME=Members
echo        COLLECTION_NAME=Members_List
echo        FRONTEND_URL=https://your-frontend-url.netlify.app

echo.
echo 3. POST-DEPLOYMENT:
echo    - Update VITE_BACKEND_URL in Netlify to point to your Render backend URL
echo    - Redeploy the frontend
echo    - Test the application thoroughly

echo.
echo For detailed instructions, please refer to DEPLOYMENT.md and DEPLOYMENT_SUMMARY.md

pause