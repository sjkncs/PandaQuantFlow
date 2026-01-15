@echo off
chcp 65001 >nul
echo ========================================
echo 🐼 Panda AI 因子库启动器
echo ========================================
echo.

cd /d "%~dp0"

echo 正在启动服务...
echo.

py start_complete.py

pause
