@echo off
chcp 65001 >nul
echo ========================================
echo   上传 PandaQuantFlow 到 GitHub
echo ========================================
echo.

echo 📋 请按照以下步骤操作：
echo.
echo 1️⃣  在 GitHub 上创建新仓库
echo    访问: https://github.com/new
echo    仓库名: PandaQuantFlow
echo    描述: AI-driven quantitative factor platform
echo    可见性: Public 或 Private
echo    ⚠️  不要勾选 "Initialize this repository with a README"
echo.

echo 2️⃣  复制仓库地址
echo    创建完成后，复制 HTTPS 地址，格式如:
echo    https://github.com/your-username/PandaQuantFlow.git
echo.

echo 3️⃣  设置远程仓库并推送
echo.
set /p repo_url="请输入你的 GitHub 仓库地址: "

if "%repo_url%"=="" (
    echo ❌ 错误: 未提供仓库地址
    pause
    exit /b 1
)

echo.
echo 🔗 设置远程仓库...
git remote add origin %repo_url%

echo.
echo 📤 推送到 GitHub...
git push -u origin master

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ 上传成功！
    echo ========================================
    echo.
    echo 🎉 你的项目已成功上传到 GitHub！
    echo.
    echo 📱 访问你的仓库:
    echo    %repo_url%
    echo.
    echo 💡 后续更新代码使用:
    echo    git add .
    echo    git commit -m "更新说明"
    echo    git push
    echo.
) else (
    echo.
    echo ========================================
    echo ❌ 上传失败
    echo ========================================
    echo.
    echo 可能的原因:
    echo 1. 未配置 Git 用户信息
    echo 2. 未登录 GitHub
    echo 3. 网络问题
    echo.
    echo 💡 配置 Git 用户信息:
    echo    git config --global user.name "Your Name"
    echo    git config --global user.email "your@email.com"
    echo.
    echo 💡 GitHub 登录:
    echo    Windows: 使用 Git Credential Manager
    echo    Linux: git config --global credential.helper store
    echo.
)

pause
