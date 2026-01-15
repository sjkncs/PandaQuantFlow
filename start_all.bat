@echo off
chcp 65001 >nul
echo ================================================================================
echo 🐼 PandaAI 量化平台 - 一键启动
echo ================================================================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python
    pause
    exit /b 1
)

echo 正在启动服务...
echo.

REM 结束已有进程
echo 清理旧进程...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *8111*" >nul 2>&1
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *8000*" >nul 2>&1
timeout /t 2 /nobreak >nul

REM 启动 PandaFactor
echo [1/2] 启动 PandaFactor 服务...
cd /d "%~dp0panda_factor-main\panda_factor-main"
start "PandaFactor-8111" python start_complete.py

timeout /t 5 /nobreak >nul

REM 启动 QuantFlow
echo [2/2] 启动 QuantFlow 服务...
cd /d "%~dp0"
start "QuantFlow-8000" python src\panda_server\main.py

timeout /t 5 /nobreak >nul

echo.
echo ================================================================================
echo ✅ 所有服务已启动！
echo ================================================================================
echo.
echo 📍 访问地址:
echo.
echo   🎯 主入口: http://127.0.0.1:8111/
echo   🚀 工作流: http://127.0.0.1:8000/quantflow/
echo   📊 图表: http://127.0.0.1:8000/charts/
echo.
echo ================================================================================
echo.

REM 打开浏览器
start http://127.0.0.1:8111/

echo 按任意键停止所有服务...
pause >nul

REM 停止服务
taskkill /F /FI "WINDOWTITLE eq PandaFactor-8111" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq QuantFlow-8000" >nul 2>&1

echo ✅ 所有服务已停止
pause
