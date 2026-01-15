@echo off
echo Restarting PandaAI Services...

echo Killing processes on port 8111...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8111 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1

echo Killing processes on port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1

timeout /t 3 /nobreak >nul

echo Starting PandaFactor...
cd /d "%~dp0panda_factor-main\panda_factor-main"
start "PandaFactor" cmd /k "py start_complete.py"

cd /d "%~dp0"

timeout /t 5 /nobreak >nul

echo Starting QuantFlow...
start "QuantFlow" cmd /k "py src\panda_server\main.py"

timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo Services Restarted!
echo ========================================
echo.
echo PandaFactor: http://127.0.0.1:8111/
echo QuantFlow: http://127.0.0.1:8000/
echo.

start http://127.0.0.1:8111/

echo Press any key to exit...
pause >nul
