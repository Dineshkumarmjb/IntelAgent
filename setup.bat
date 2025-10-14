@echo off
REM Setup script for Windows

echo ========================================
echo   IntelAgent - Setup
echo ========================================
echo.

echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Copy .env.example to .env
echo 2. Add your OPENAI_API_KEY to .env
echo 3. Run: run.bat
echo.

pause

