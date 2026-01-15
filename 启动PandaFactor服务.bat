@echo off
chcp 65001 >nul
echo ============================================================
echo 启动 PandaFactor 服务
echo ============================================================
echo.

cd /d c:\Users\Lenovo\Desktop\PandaQuantFlow\panda_factor-main\panda_factor-main

echo [1/3] 检查依赖...
python -c "import fastapi, uvicorn" 2>nul
if errorlevel 1 (
    echo 正在安装Web服务依赖...
    pip install fastapi uvicorn -i https://pypi.tuna.tsinghua.edu.cn/simple --quiet
    echo 依赖安装完成
) else (
    echo 依赖已安装
)
echo.

echo [2/3] 启动服务...
echo.
echo 服务将在以下地址启动:
echo   - 主页: http://127.0.0.1:8111/
echo   - 因子界面: http://127.0.0.1:8111/factor
echo   - API文档: http://127.0.0.1:8111/docs
echo.
echo 按 Ctrl+C 停止服务
echo.

python -m panda_factor_server

pause
