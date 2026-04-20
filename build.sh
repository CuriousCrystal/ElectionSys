#!/bin/bash

# Build script for combined deployment
# This script builds the frontend and prepares the backend for deployment

echo "=================================="
echo "Building Event Management System"
echo "=================================="
echo ""

# Build frontend
echo "Step 1: Building React frontend..."
cd dashboard

if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

echo "Running npm build..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Frontend build failed!"
    exit 1
fi

echo "✅ Frontend built successfully"
cd ..

echo ""
echo "Step 2: Verifying backend..."
if [ ! -f "data_engine.py" ]; then
    echo "❌ Backend file not found!"
    exit 1
fi

echo "✅ Backend verified"

echo ""
echo "Step 3: Checking build output..."
if [ -d "dashboard/dist" ]; then
    echo "✅ Frontend build exists at dashboard/dist/"
    ls -la dashboard/dist/
else
    echo "❌ Frontend build not found!"
    exit 1
fi

echo ""
echo "=================================="
echo "✅ Build Complete!"
echo "=================================="
echo ""
echo "The application is ready for deployment."
echo "Both frontend and backend are now combined."
echo ""
echo "To run locally:"
echo "  uvicorn data_engine:app --reload"
echo ""
echo "Access the app at: http://localhost:8000"
