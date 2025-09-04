@echo off
title Building Gym Membership Management System

echo Building Gym Membership Management System...
echo ==========================================

echo Removing existing dist folder...
rmdir /s /q dist 2>nul

echo Installing dependencies...
npm install

echo Building project...
npx vite build

if %ERRORLEVEL% EQU 0 (
    echo Build completed successfully!
    echo.
    echo To preview the build:
    echo   npm run serve
    echo.
    echo To deploy to Netlify:
    echo   1. Go to Netlify dashboard
    echo   2. Select your site
    echo   3. Trigger a new deployment
    echo   4. Set publish directory to: dist
    echo.
    echo To deploy to other platforms:
    echo   npm run serve
) else (
    echo Build failed with error code %ERRORLEVEL%
    echo Please check the error messages above
)

pause