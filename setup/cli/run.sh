#!/bin/bash

echo "==================================================="
echo "🚀 Setting up Hellobuddy environment (Bash Shell)"
echo "==================================================="

# Exit immediately if a command exits with a non-zero status
set -e

# 1. Generate virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[1/4] Creating virtual environment..."
    python3 -m venv venv || python -m venv venv
else
    echo "[1/4] Virtual environment already exists. Skipping creation."
fi

# 2. Activate the virtual environment
echo "[2/4] Activating virtual environment..."
source venv/bin/activate

# 3. Change directory to hellobuddy folder and install requirements
echo "[3/4] Navigating to hellobuddy and installing packages..."
cd hellobuddy
pip install -r requirements.txt

# 4. Navigate to src folder and run the app
echo "[4/4] Starting main application..."
cd src
exec python3 app/main.py || python app/main.py