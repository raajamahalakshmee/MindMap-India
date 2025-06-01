@echo off
echo ===================================
echo    Mindmap India: Career Explorer   
echo ===================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8 or later from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check if required packages are installed
echo Checking Python dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to install required Python packages.
    pause
    exit /b 1
)

:: Create necessary directories
echo Setting up directories...
if not exist "output" mkdir output
if not exist "output\wordclouds" mkdir output\wordclouds
if not exist "cache" mkdir cache

:: Run the Streamlit app
echo.
echo Starting Mindmap India...
echo This will open in your default web browser shortly.
echo.
echo If the browser doesn't open automatically, please visit:
echo http://localhost:8501
echo.
echo Press Ctrl+C in this window to stop the application.
echo ===================================
echo.

start http://localhost:8501
streamlit run run.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: Failed to start the application.
    echo Please make sure all dependencies are installed and try again.
    echo.
    pause
    exit /b 1
)

pause
