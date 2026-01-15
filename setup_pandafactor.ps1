# PandaFactor 一键配置脚本 (PowerShell版本)
# 自动安装所有依赖和配置子模块

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "PandaFactor 一键配置脚本" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# 设置项目根目录
$PROJECT_ROOT = "c:\Users\Lenovo\Desktop\PandaQuantFlow\panda_factor-main\panda_factor-main"
Set-Location $PROJECT_ROOT

Write-Host "[步骤 1/8] 检查Python环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✅ Python环境正常: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python未安装或未添加到PATH" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}
Write-Host ""

Write-Host "[步骤 2/8] 安装基础依赖..." -ForegroundColor Yellow
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 依赖安装失败" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}
Write-Host "✅ 基础依赖安装完成" -ForegroundColor Green
Write-Host ""

Write-Host "[步骤 3/8] 配置 panda_common..." -ForegroundColor Yellow
Set-Location panda_common
pip install -e .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ panda_common 配置失败" -ForegroundColor Red
    Set-Location ..
    Read-Host "按任意键退出"
    exit 1
}
Set-Location ..
Write-Host "✅ panda_common 配置完成" -ForegroundColor Green
Write-Host ""

Write-Host "[步骤 4/8] 配置 panda_data..." -ForegroundColor Yellow
Set-Location panda_data
pip install -e .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ panda_data 配置失败" -ForegroundColor Red
    Set-Location ..
    Read-Host "按任意键退出"
    exit 1
}
Set-Location ..
Write-Host "✅ panda_data 配置完成" -ForegroundColor Green
Write-Host ""

Write-Host "[步骤 5/8] 配置 panda_data_hub..." -ForegroundColor Yellow
Set-Location panda_data_hub
pip install -e .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ panda_data_hub 配置失败" -ForegroundColor Red
    Set-Location ..
    Read-Host "按任意键退出"
    exit 1
}
Set-Location ..
Write-Host "✅ panda_data_hub 配置完成" -ForegroundColor Green
Write-Host ""

Write-Host "[步骤 6/8] 配置 panda_factor..." -ForegroundColor Yellow
Set-Location panda_factor
pip install -e .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ panda_factor 配置失败" -ForegroundColor Red
    Set-Location ..
    Read-Host "按任意键退出"
    exit 1
}
Set-Location ..
Write-Host "✅ panda_factor 配置完成" -ForegroundColor Green
Write-Host ""

Write-Host "[步骤 7/8] 配置 panda_llm..." -ForegroundColor Yellow
Set-Location panda_llm
pip install -e .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ panda_llm 配置失败" -ForegroundColor Red
    Set-Location ..
    Read-Host "按任意键退出"
    exit 1
}
Set-Location ..
Write-Host "✅ panda_llm 配置完成" -ForegroundColor Green
Write-Host ""

Write-Host "[步骤 8/8] 配置 panda_factor_server..." -ForegroundColor Yellow
Set-Location panda_factor_server
pip install -e .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ panda_factor_server 配置失败" -ForegroundColor Red
    Set-Location ..
    Read-Host "按任意键退出"
    exit 1
}
Set-Location ..
Write-Host "✅ panda_factor_server 配置完成" -ForegroundColor Green
Write-Host ""

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🎉 所有模块配置完成！" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步:" -ForegroundColor Yellow
Write-Host "1. 配置 MongoDB 连接 (编辑 panda_common/config.yaml)" -ForegroundColor White
Write-Host "2. 启动 MongoDB 服务" -ForegroundColor White
Write-Host "3. 运行测试: python test_pandafactor.py" -ForegroundColor White
Write-Host ""

Read-Host "按任意键退出"
