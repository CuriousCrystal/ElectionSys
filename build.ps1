# Build script for combined deployment (PowerShell)
# This script builds the frontend and prepares the backend for deployment

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Building Event Management System" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Build frontend
Write-Host "Step 1: Building React frontend..." -ForegroundColor Green
Set-Location dashboard

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing npm dependencies..." -ForegroundColor Yellow
    npm install
}

Write-Host "Running npm build..." -ForegroundColor Yellow
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Frontend build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Frontend built successfully" -ForegroundColor Green
Set-Location ..

Write-Host ""
Write-Host "Step 2: Verifying backend..." -ForegroundColor Green
if (-not (Test-Path "data_engine.py")) {
    Write-Host "❌ Backend file not found!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Backend verified" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Checking build output..." -ForegroundColor Green
if (Test-Path "dashboard/dist") {
    Write-Host "✅ Frontend build exists at dashboard/dist/" -ForegroundColor Green
    Get-ChildItem dashboard/dist -Recurse | Select-Object FullName, Length
} else {
    Write-Host "❌ Frontend build not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "✅ Build Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The application is ready for deployment." -ForegroundColor White
Write-Host "Both frontend and backend are now combined." -ForegroundColor White
Write-Host ""
Write-Host "To run locally:" -ForegroundColor Yellow
Write-Host "  uvicorn data_engine:app --reload" -ForegroundColor White
Write-Host ""
Write-Host "Access the app at: http://localhost:8000" -ForegroundColor White
