"""
PandaFactor 服务启动脚本
直接运行: python start_server.py
"""

import sys
import os

# 添加所有模块到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, "panda_common"))
sys.path.insert(0, os.path.join(current_dir, "panda_data"))
sys.path.insert(0, os.path.join(current_dir, "panda_factor"))
sys.path.insert(0, os.path.join(current_dir, "panda_llm"))
sys.path.insert(0, os.path.join(current_dir, "panda_factor_server"))

print("=" * 70)
print("PandaFactor 服务启动")
print("=" * 70)
print()

# 检查并安装依赖
print("[1/2] 检查依赖...")
missing_deps = []

try:
    import fastapi
except ImportError:
    missing_deps.append("fastapi")

try:
    import uvicorn
except ImportError:
    missing_deps.append("uvicorn")

try:
    import pydantic
except ImportError:
    missing_deps.append("pydantic")

if missing_deps:
    print(f"⚠️  缺少依赖: {', '.join(missing_deps)}")
    print("正在安装...")
    import subprocess
    subprocess.run([
        sys.executable, "-m", "pip", "install"] + missing_deps + 
        ["-i", "https://pypi.tuna.tsinghua.edu.cn/simple"
    ])
    print("✅ 依赖安装完成")
else:
    print("✅ 所有依赖已安装")

print()
print("[2/2] 启动服务...")
print()
print("服务地址:")
print("  - 主页:     http://127.0.0.1:8111/")
print("  - API文档:  http://127.0.0.1:8111/docs")
print()
print("按 Ctrl+C 停止服务")
print("=" * 70)
print()

try:
    # 导入FastAPI组件
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
    from pathlib import Path
    import mimetypes
    
    # 创建应用
    app = FastAPI(
        title="PandaFactor Server",
        description="PandaAI Factor System",
        version="1.0.0"
    )
    
    # CORS配置
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 尝试加载路由
    routes_loaded = []
    
    try:
        from panda_factor_server.routes import user_factor_pro
        app.include_router(user_factor_pro.router, prefix="/api/v1", tags=["user_factors"])
        routes_loaded.append("因子API")
    except Exception as e:
        print(f"⚠️  因子路由加载失败: {e}")
    
    try:
        from panda_llm.routes import chat_router
        app.include_router(chat_router.router, prefix="/llm", tags=["panda_llm"])
        routes_loaded.append("LLM API")
    except Exception as e:
        print(f"⚠️  LLM路由加载失败: {e}")
    
    # 静态文件
    frontend_folder = Path(current_dir) / "panda_web" / "panda_web" / "static"
    if frontend_folder.exists():
        try:
            from starlette.staticfiles import StaticFiles
            mimetypes.add_type("text/css", ".css")
            mimetypes.add_type("application/javascript", ".js")
            app.mount("/factor", StaticFiles(directory=str(frontend_folder), html=True), name="static")
            routes_loaded.append("Web界面")
        except Exception as e:
            print(f"⚠️  前端资源加载失败: {e}")
    
    # 主页路由
    @app.get("/")
    async def home():
        return {
            "message": "Welcome to PandaFactor Server!",
            "version": "1.0.0",
            "loaded_routes": routes_loaded,
            "endpoints": {
                "api_docs": "/docs",
                "api_v1": "/api/v1",
                "llm": "/llm",
                "factor_ui": "/factor"
            }
        }
    
    if routes_loaded:
        print(f"✅ 已加载: {', '.join(routes_loaded)}")
    print()
    
    # 启动服务
    uvicorn.run(app, host="0.0.0.0", port=8111, log_level="info")
    
except KeyboardInterrupt:
    print("\n\n✅ 服务已停止")
except Exception as e:
    print(f"\n❌ 启动失败: {e}")
    import traceback
    traceback.print_exc()
    print("\n可能的解决方案:")
    print("1. 安装依赖: pip install fastapi uvicorn pydantic")
    print("2. 配置模块: cd panda_common && pip install -e .")
    print("3. 检查Python版本: python --version (需要3.8+)")
