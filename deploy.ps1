# Event Management System - Deployment Script (PowerShell)
# This script helps you deploy to Netlify and Render

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Event Management System Deployer" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
try {
    $null = Get-Command git -ErrorAction Stop
} catch {
    Write-Host "Error: Git is not installed" -ForegroundColor Red
    exit 1
}

# Check if Netlify CLI is installed
$netlifyInstalled = $null -ne (Get-Command netlify -ErrorAction SilentlyContinue)
if (-not $netlifyInstalled) {
    Write-Host "Netlify CLI not found. Install with: npm install -g netlify-cli" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Select deployment option:" -ForegroundColor White
Write-Host "1. Deploy Frontend to Netlify" -ForegroundColor Green
Write-Host "2. Deploy Backend to Render (manual steps)" -ForegroundColor Green
Write-Host "3. Full deployment guide" -ForegroundColor Green
Write-Host "4. Test build locally" -ForegroundColor Green
Write-Host ""

$choice = Read-Host "Enter choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "Deploying Frontend to Netlify..." -ForegroundColor Green
        Write-Host ""
        
        # Check if .env.production has correct URL
        $envFile = "dashboard\.env.production"
        $content = Get-Content $envFile -Raw
        if ($content -match "http://localhost:8000") {
            Write-Host "Warning: Backend URL is still set to localhost" -ForegroundColor Yellow
            $backendUrl = Read-Host "Enter your Render backend URL (or press Enter to skip)"
            if ($backendUrl) {
                "VITE_API_URL=$backendUrl" | Set-Content $envFile
            }
        }
        
        Set-Location dashboard
        
        # Install dependencies
        Write-Host "Installing dependencies..." -ForegroundColor Cyan
        npm install
        
        # Build
        Write-Host "Building project..." -ForegroundColor Cyan
        npm run build
        
        # Deploy
        Write-Host ""
        Write-Host "Starting Netlify deployment..." -ForegroundColor Green
        if ($netlifyInstalled) {
            netlify deploy --prod
        } else {
            Write-Host "Netlify CLI not installed. Please install it first:" -ForegroundColor Red
            Write-Host "npm install -g netlify-cli"
            Write-Host ""
            Write-Host "Or deploy manually:"
            Write-Host "1. Go to https://netlify.com"
            Write-Host "2. Drag and drop the 'dist' folder"
        }
        
        Set-Location ..
    }
    
    "2" {
        Write-Host ""
        Write-Host "Backend Deployment to Render" -ForegroundColor Green
        Write-Host ""
        Write-Host "Follow these steps:" -ForegroundColor White
        Write-Host ""
        Write-Host "1. Push your code to GitHub:" -ForegroundColor Yellow
        Write-Host "   git add ."
        Write-Host "   git commit -m 'Deploy to Render'"
        Write-Host "   git push origin main"
        Write-Host ""
        Write-Host "2. Go to https://render.com and login" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "3. Click 'New +' → 'Web Service'" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "4. Connect your repository and configure:" -ForegroundColor Yellow
        Write-Host "   - Name: event-management-api"
        Write-Host "   - Build Command: pip install -r requirements.txt"
        Write-Host "   - Start Command: uvicorn data_engine:app --host 0.0.0.0 --port `$PORT"
        Write-Host ""
        Write-Host "5. Add environment variables:" -ForegroundColor Yellow
        Write-Host "   - XAI_API_KEY: Your API key"
        Write-Host "   - JWT_SECRET_KEY: Random secure string"
        Write-Host "   - JWT_ALGORITHM: HS256"
        Write-Host "   - DATABASE_URL: sqlite:///./event_management.db"
        Write-Host ""
        Write-Host "6. Click 'Create Web Service'" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "7. Copy your backend URL and update dashboard/.env.production" -ForegroundColor Yellow
    }
    
    "3" {
        Write-Host ""
        Write-Host "Opening deployment guide..." -ForegroundColor Green
        Start-Process "DEPLOYMENT.md"
    }
    
    "4" {
        Write-Host ""
        Write-Host "Testing Local Build..." -ForegroundColor Green
        Write-Host ""
        
        Set-Location dashboard
        
        Write-Host "Installing dependencies..." -ForegroundColor Cyan
        npm install
        
        Write-Host "Building project..." -ForegroundColor Cyan
        npm run build
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✓ Build successful!" -ForegroundColor Green
            Write-Host "Build output is in: dashboard/dist/"
            Write-Host ""
            Write-Host "To preview locally:"
            Write-Host "npm run preview"
        } else {
            Write-Host ""
            Write-Host "✗ Build failed. Please check the errors above" -ForegroundColor Red
        }
        
        Set-Location ..
    }
    
    default {
        Write-Host "Invalid choice" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
