@echo off
echo Starting Django API...

REM Activate virtual environment (if you have one)
call .venv\Scripts\activate

REM Start server
python manage.py runserver

pause
