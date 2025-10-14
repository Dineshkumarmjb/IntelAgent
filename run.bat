@echo off
REM Quick start script for Windows

echo ========================================
echo   IntelAgent - Starting Application
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate

REM Check if .env exists
if not exist ".env" (
    echo .env file not found!
    echo Please create .env file with your API keys
    echo See .env.example for reference
    pause
    exit /b 1
)

echo Starting IntelAgent UI...
echo.
echo Access the UI at: http://127.0.0.1:7860
echo Press Ctrl+C to stop
echo.

python ui\gradio_app.py

pause

