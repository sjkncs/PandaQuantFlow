@echo off
chcp 65001 >nul
echo ============================================================
echo PandaFactor 配置并启动服务
echo ============================================================
echo.

cd /d c:\Users\Lenovo\Desktop\PandaQuantFlow\panda_factor-main\panda_factor-main

echo [步骤 1/4] 安装基础依赖...
pip install fastapi uvicorn pydantic -i https://pypi.tuna.tsinghua.edu.cn/simple --quiet
if errorlevel 1 (
    echo 依赖安装失败，尝试不使用镜像...
    pip install fastapi uvicorn pydantic
)
echo 依赖安装完成
echo.

echo [步骤 2/4] 配置 panda_common...
cd panda_common
pip install -e . --quiet 2>nul
cd ..
echo.

echo [步骤 3/4] 配置 panda_factor_server...
cd panda_factor_server
pip install -e . --quiet 2>nul
cd ..
echo.

echo [步骤 4/4] 启动服务...
echo.
echo 服务地址:
echo   - 主页:     http://127.0.0.1:8111/
echo   - API文档:  http://127.0.0.1:8111/docs
echo.
echo 按 Ctrl+C 停止服务
echo ============================================================
echo.

python -m panda_factor_server

if errorlevel 1 (
    echo.
    echo 启动失败，尝试备用方式...
    cd panda_factor_server\panda_factor_server
    python __main__.py
)

pause
