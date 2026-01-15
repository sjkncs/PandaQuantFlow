# PandaFactor 快速配置脚本 (简化版)
# 仅配置必要的模块，跳过可选依赖

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "PandaFactor 快速配置 (简化版)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$PROJECT_ROOT = "c:\Users\Lenovo\Desktop\PandaQuantFlow\panda_factor-main\panda_factor-main"

Write-Host "[1/4] 检查Python环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python未安装" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}
Write-Host ""

Write-Host "[2/4] 安装核心依赖..." -ForegroundColor Yellow
Write-Host "提示: 跳过可选依赖以加快安装速度" -ForegroundColor Gray

# 只安装核心依赖
$coreDeps = @(
    "numpy>=1.24.2",
    "pandas>=2.0.0",
    "pymongo>=4.3.3",
    "loguru>=0.6.0",
    "PyYAML>=6.0",
    "setuptools>=67.6.1"
)

foreach ($dep in $coreDeps) {
    Write-Host "  安装 $dep..." -ForegroundColor Gray
    pip install $dep -i https://pypi.tuna.tsinghua.edu.cn/simple --quiet
}
Write-Host "✅ 核心依赖安装完成" -ForegroundColor Green
Write-Host ""

Write-Host "[3/4] 配置核心模块..." -ForegroundColor Yellow
Set-Location $PROJECT_ROOT

$modules = @("panda_common", "panda_data", "panda_factor")

foreach ($module in $modules) {
    Write-Host "  配置 $module..." -ForegroundColor Gray
    Set-Location $module
    pip install -e . --quiet 2>$null
    Set-Location ..
}
Write-Host "✅ 核心模块配置完成" -ForegroundColor Green
Write-Host ""

Write-Host "[4/4] 验证安装..." -ForegroundColor Yellow
Set-Location "c:\Users\Lenovo\Desktop\PandaQuantFlow"

$testScript = @"
import sys
sys.path.insert(0, r'$PROJECT_ROOT')

success = True
modules = ['panda_common', 'panda_data', 'panda_factor']

for mod in modules:
    try:
        __import__(mod)
        print(f'✅ {mod}')
    except Exception as e:
        print(f'❌ {mod}: {e}')
        success = False

if success:
    print('\n🎉 安装成功！')
else:
    print('\n⚠️ 部分模块安装失败')
"@

$testScript | python -
Write-Host ""

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "配置完成！" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "快速开始:" -ForegroundColor Yellow
Write-Host "  python run_pandafactor_example.py" -ForegroundColor White
Write-Host ""

Read-Host "按任意键退出"
