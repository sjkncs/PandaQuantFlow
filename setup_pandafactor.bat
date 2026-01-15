@echo off
REM PandaFactor 一键配置脚本 (Windows)
REM 自动安装所有依赖和配置子模块

echo ============================================================
echo PandaFactor 一键配置脚本
echo ============================================================
echo.

REM 设置项目根目录
set PROJECT_ROOT=c:\Users\Lenovo\Desktop\PandaQuantFlow\panda_factor-main\panda_factor-main
cd /d %PROJECT_ROOT%

echo [步骤 1/8] 检查Python环境...
python --version
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    pause
    exit /b 1
)
echo ✅ Python环境正常
echo.

echo [步骤 2/8] 安装基础依赖...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)
echo ✅ 基础依赖安装完成
echo.

echo [步骤 3/8] 配置 panda_common...
cd panda_common
pip install -e .
if errorlevel 1 (
    echo ❌ panda_common 配置失败
    cd ..
    pause
    exit /b 1
)
cd ..
echo ✅ panda_common 配置完成
echo.

echo [步骤 4/8] 配置 panda_data...
cd panda_data
pip install -e .
if errorlevel 1 (
    echo ❌ panda_data 配置失败
    cd ..
    pause
    exit /b 1
)
cd ..
echo ✅ panda_data 配置完成
echo.

echo [步骤 5/8] 配置 panda_data_hub...
cd panda_data_hub
pip install -e .
if errorlevel 1 (
    echo ❌ panda_data_hub 配置失败
    cd ..
    pause
    exit /b 1
)
cd ..
echo ✅ panda_data_hub 配置完成
echo.

echo [步骤 6/8] 配置 panda_factor...
cd panda_factor
pip install -e .
if errorlevel 1 (
    echo ❌ panda_factor 配置失败
    cd ..
    pause
    exit /b 1
)
cd ..
echo ✅ panda_factor 配置完成
echo.

echo [步骤 7/8] 配置 panda_llm...
cd panda_llm
pip install -e .
if errorlevel 1 (
    echo ❌ panda_llm 配置失败
    cd ..
    pause
    exit /b 1
)
cd ..
echo ✅ panda_llm 配置完成
echo.

echo [步骤 8/8] 配置 panda_factor_server...
cd panda_factor_server
pip install -e .
if errorlevel 1 (
    echo ❌ panda_factor_server 配置失败
    cd ..
    pause
    exit /b 1
)
cd ..
echo ✅ panda_factor_server 配置完成
echo.

echo ============================================================
echo 🎉 所有模块配置完成！
echo ============================================================
echo.
echo 下一步:
echo 1. 配置 MongoDB 连接 (编辑 panda_common/config.yaml)
echo 2. 启动 MongoDB 服务
echo 3. 运行测试: python test_installation.py
echo.

pause
