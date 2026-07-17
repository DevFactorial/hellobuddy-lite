# If Windows blocks you from running this file due to security policies, open PowerShell as an administrator once and run Set-ExecutionPolicy RemoteSigned -Scope CurrentUser.

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "🚀 Setting up Hellobuddy environment (PowerShell)" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

# 1. Generate virtual environment if it doesn't exist
if (-not (Test-Path -Path "venv")) {
    Write-Host "[1/4] Creating virtual environment..." -ForegroundColor Yellow
    try { python -m venv venv } catch { python3 -m venv venv }
} else {
    Write-Host "[1/4] Virtual environment already exists. Skipping creation." -ForegroundColor Green
}

# 2. Activate the virtual environment
Write-Host "[2/4] Activating virtual environment..." -ForegroundColor Yellow
. .\venv\Scripts\Activate.ps1

# 3. Change directory to hellobuddy folder and install requirements
Write-Host "[3/4] Navigating to hellobuddy and installing packages..." -ForegroundColor Yellow
Set-Location -Path "hellobuddy"
pip install -r requirements.txt

# 4. Navigate to src folder and run the app
Write-Host "[4/4] Starting main application..." -ForegroundColor Green
Set-Location -Path "src"
try { python app/main.py } catch { python3 app/main.py }