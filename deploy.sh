#!/bin/bash

# Event Management System - Deployment Script
# This script helps you deploy to Netlify and Render

echo "=================================="
echo "Event Management System Deployer"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: Git is not installed${NC}"
    exit 1
fi

# Check if Netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo -e "${YELLOW}Netlify CLI not found. Install with: npm install -g netlify-cli${NC}"
    echo ""
fi

echo "Select deployment option:"
echo "1. Deploy Frontend to Netlify"
echo "2. Deploy Backend to Render (manual steps)"
echo "3. Full deployment guide"
echo "4. Test build locally"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}Deploying Frontend to Netlify...${NC}"
        echo ""
        
        # Check if .env.production has correct URL
        if grep -q "http://localhost:8000" dashboard/.env.production; then
            echo -e "${YELLOW}Warning: Backend URL is still set to localhost${NC}"
            read -p "Enter your Render backend URL (or press Enter to skip): " backend_url
            if [ ! -z "$backend_url" ]; then
                echo "VITE_API_URL=$backend_url" > dashboard/.env.production
            fi
        fi
        
        cd dashboard
        
        # Install dependencies
        echo "Installing dependencies..."
        npm install
        
        # Build
        echo "Building project..."
        npm run build
        
        # Deploy
        echo ""
        echo -e "${GREEN}Starting Netlify deployment...${NC}"
        if command -v netlify &> /dev/null; then
            netlify deploy --prod
        else
            echo -e "${RED}Netlify CLI not installed. Please install it first:${NC}"
            echo "npm install -g netlify-cli"
            echo ""
            echo "Or deploy manually:"
            echo "1. Go to https://netlify.com"
            echo "2. Drag and drop the 'dist' folder"
        fi
        
        cd ..
        ;;
        
    2)
        echo ""
        echo -e "${GREEN}Backend Deployment to Render${NC}"
        echo ""
        echo "Follow these steps:"
        echo ""
        echo "1. Push your code to GitHub:"
        echo "   git add ."
        echo "   git commit -m 'Deploy to Render'"
        echo "   git push origin main"
        echo ""
        echo "2. Go to https://render.com and login"
        echo ""
        echo "3. Click 'New +' → 'Web Service'"
        echo ""
        echo "4. Connect your repository and configure:"
        echo "   - Name: event-management-api"
        echo "   - Build Command: pip install -r requirements.txt"
        echo "   - Start Command: uvicorn data_engine:app --host 0.0.0.0 --port \$PORT"
        echo ""
        echo "5. Add environment variables:"
        echo "   - XAI_API_KEY: Your API key"
        echo "   - JWT_SECRET_KEY: Random secure string"
        echo "   - JWT_ALGORITHM: HS256"
        echo "   - DATABASE_URL: sqlite:///./event_management.db"
        echo ""
        echo "6. Click 'Create Web Service'"
        echo ""
        echo "7. Copy your backend URL and update dashboard/.env.production"
        ;;
        
    3)
        echo ""
        echo -e "${GREEN}Full Deployment Guide${NC}"
        echo ""
        echo "Opening deployment guide..."
        if command -v xdg-open &> /dev/null; then
            xdg-open DEPLOYMENT.md
        elif command -v open &> /dev/null; then
            open DEPLOYMENT.md
        else
            echo "Please open DEPLOYMENT.md manually"
        fi
        ;;
        
    4)
        echo ""
        echo -e "${GREEN}Testing Local Build...${NC}"
        echo ""
        
        cd dashboard
        
        echo "Installing dependencies..."
        npm install
        
        echo "Building project..."
        npm run build
        
        if [ $? -eq 0 ]; then
            echo ""
            echo -e "${GREEN}✓ Build successful!${NC}"
            echo "Build output is in: dashboard/dist/"
            echo ""
            echo "To preview locally:"
            echo "npm run preview"
        else
            echo ""
            echo -e "${RED}✗ Build failed. Please check the errors above${NC}"
        fi
        
        cd ..
        ;;
        
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Done!${NC}"
