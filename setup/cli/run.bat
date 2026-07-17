@echo off
echo ===================================================
echo 🚀 Setting up Hellobuddy environment (CMD Batch)
echo ===================================================

:: 1. Generate virtual environment if it doesn't exist
if not exist venv (
    echo [1/4] Creating virtual environment...
    python -m venv venv || python3 -m venv venv
) else (
    echo [1/4] Virtual environment already exists. Skipping creation.
)

:: 2. Activate the virtual environment
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

:: 3. Change directory to hellobuddy folder and install requirements
echo [3/4] Navigating to hellobuddy and installing packages...
cd hellobuddy
pip install -r requirements.txt

:: 4. Navigate to src folder and run the app
echo [4/4] Starting main application...
cd src
python app/main.py || python3 app/main.py
