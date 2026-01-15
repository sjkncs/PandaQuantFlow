@echo off
chcp 65001 >nul
echo ============================================================
echo 直接运行PandaFactor示例 (无需配置)
echo ============================================================
echo.

cd /d c:\Users\Lenovo\Desktop\PandaQuantFlow

echo [1/2] 检查基础依赖...
python -c "import numpy, pandas, torch" 2>nul
if errorlevel 1 (
    echo 正在安装基础依赖...
    pip install numpy pandas torch -i https://pypi.tuna.tsinghua.edu.cn/simple --quiet
    echo 依赖安装完成
) else (
    echo 依赖已安装
)
echo.

echo [2/2] 运行示例...
echo.
python run_pandafactor_example.py

echo.
pause
