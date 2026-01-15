@echo off
chcp 65001 >nul
echo ============================================================
echo PandaFactor 一键修复并启动
echo ============================================================
echo.

cd /d c:\Users\Lenovo\Desktop\PandaQuantFlow\panda_factor-main\panda_factor-main

echo [步骤 1/2] 修复服务问题...
python fix_services.py
echo.

echo [步骤 2/2] 启动服务...
echo.
python start_server_fixed.py

pause
