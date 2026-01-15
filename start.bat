@echo off
echo.
echo ========================================
echo  TechBuddy Dating Site
echo ========================================
echo.
echo Starting Flask development server...
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat
python run.py

pause
