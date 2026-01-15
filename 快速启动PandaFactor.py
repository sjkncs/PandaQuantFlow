"""
PandaFactor 快速启动脚本
无需配置，直接启动服务
"""

import sys
import os

# 添加项目路径
project_root = r"c:\Users\Lenovo\Desktop\PandaQuantFlow\panda_factor-main\panda_factor-main"
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "panda_factor_server"))
sys.path.insert(0, os.path.join(project_root, "panda_common"))
sys.path.insert(0, os.path.join(project_root, "panda_data"))
sys.path.insert(0, os.path.join(project_root, "panda_factor"))
sys.path.insert(0, os.path.join(project_root, "panda_llm"))

print("=" * 70)
print("PandaFactor 服务启动")
print("=" * 70)
print()

# 检查依赖
print("[1/3] 检查依赖...")
try:
    import fastapi
    import uvicorn
    print("✅ FastAPI 和 Uvicorn 已安装")
except ImportError:
    print("⚠️  正在安装 FastAPI 和 Uvicorn...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", 
                   "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"], check=True)
    print("✅ 依赖安装完成")

print()

# 启动服务
print("[2/3] 启动服务...")
print()
print("服务地址:")
print("  - 主页:     http://127.0.0.1:8111/")
print("  - 因子界面: http://127.0.0.1:8111/factor")
print("  - API文档:  http://127.0.0.1:8111/docs")
print()
print("按 Ctrl+C 停止服务")
print("=" * 70)
print()

try:
    # 直接导入并运行
    os.chdir(os.path.join(project_root, "panda_factor_server", "panda_factor_server"))
    
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
    from pathlib import Path
    import mimetypes
    from starlette.staticfiles import StaticFiles
    
    app = FastAPI(
        title="Panda Server",
        description="Server for Panda AI Factor System",
        version="1.0.0"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 尝试加载路由（可选）
    try:
        from panda_factor_server.routes import user_factor_pro
        app.include_router(user_factor_pro.router, prefix="/api/v1", tags=["user_factors"])
        print("✅ 因子路由已加载")
    except Exception as e:
        print(f"⚠️  因子路由加载失败: {e}")
    
    try:
        from panda_llm.routes import chat_router
        app.include_router(chat_router.router, prefix="/llm", tags=["panda_llm"])
        print("✅ LLM路由已加载")
    except Exception as e:
        print(f"⚠️  LLM路由加载失败: {e}")
    
    # 静态文件
    frontend_folder = Path(project_root) / "panda_web" / "panda_web" / "static"
    if frontend_folder.exists():
        mimetypes.add_type("text/css", ".css")
        mimetypes.add_type("application/javascript", ".js")
        app.mount("/factor", StaticFiles(directory=str(frontend_folder), html=True), name="static")
        print(f"✅ 前端资源已加载: {frontend_folder}")
    else:
        print(f"⚠️  前端资源不存在: {frontend_folder}")
    
    @app.get("/")
    async def home():
        return {
            "message": "Welcome to PandaFactor Server!",
            "version": "1.0.0",
            "endpoints": {
                "factor_ui": "/factor",
                "api_docs": "/docs",
                "api_v1": "/api/v1",
                "llm": "/llm"
            }
        }
    
    print()
    print("[3/3] 服务启动中...")
    print()
    
    # 启动服务
    uvicorn.run(app, host="0.0.0.0", port=8111)
    
except KeyboardInterrupt:
    print("\n\n服务已停止")
except Exception as e:
    print(f"\n❌ 启动失败: {e}")
    print("\n详细错误:")
    import traceback
    traceback.print_exc()
    print("\n建议:")
    print("1. 检查是否安装了所有依赖")
    print("2. 运行: python simple_setup.py")
    print("3. 或使用轻量级因子库: python run_pandafactor_example.py")
    input("\n按回车退出...")
