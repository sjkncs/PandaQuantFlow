@echo off
echo Starting PandaAI Platform...
echo.

echo [1/2] Starting PandaFactor...
cd panda_factor-main\panda_factor-main
start cmd /k "py start_complete.py"

cd ..\..

timeout /t 5 >nul

echo [2/2] Starting QuantFlow...
start cmd /k "py src\panda_server\main.py"

timeout /t 3 >nul

echo.
echo ========================================
echo Services Started!
echo ========================================
echo.
echo PandaFactor: http://127.0.0.1:8111/
echo QuantFlow: http://127.0.0.1:8000/quantflow/
echo.
echo Opening browser...

start http://127.0.0.1:8111/

echo.
echo Press any key to exit...
pause >nul
