@echo off
chcp 65001
echo Setting up Network Inspection System...

echo Installing dependencies...
pip install -r requirements.txt

echo Creating database tables...
python backend/manage.py migrate

echo Initializing demo data...
python backend/manage.py initialize_demo --username admin --password adminpassword --email admin@example.com

echo Starting backend server...
start cmd /k "python backend/manage.py runserver"

echo Setup successfully!
echo You can use the following credentials to login:
echo Username: admin
echo Password: adminpassword
echo.
echo Backend API address: http://127.0.0.1:8000/
echo API documentation address: http://127.0.0.1:8000/swagger/