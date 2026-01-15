"""
PandaFactor 服务启动脚本（修复版）
已修复因子路由和LLM功能
"""

import sys
import os

# 添加所有模块到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, "panda_common"))
sys.path.insert(0, os.path.join(current_dir, "panda_data"))
sys.path.insert(0, os.path.join(current_dir, "panda_data_hub"))  # 添加这个
sys.path.insert(0, os.path.join(current_dir, "panda_factor"))
sys.path.insert(0, os.path.join(current_dir, "panda_llm"))
sys.path.insert(0, os.path.join(current_dir, "panda_factor_server"))

print("=" * 70)
print("PandaFactor 服务启动（修复版）")
print("=" * 70)
print()

# 检查依赖
print("[1/2] 检查依赖...")
missing_deps = []

required_deps = {
    "fastapi": "fastapi",
    "uvicorn": "uvicorn",
    "pydantic": "pydantic",
    "pymongo": "pymongo"
}

for module, package in required_deps.items():
    try:
        __import__(module)
    except ImportError:
        missing_deps.append(package)

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
print("  - 因子界面: http://127.0.0.1:8111/factor")
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
        description="PandaAI Factor System (Fixed)",
        version="1.0.1"
    )
    
    # CORS配置
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 加载路由
    routes_loaded = []
    routes_failed = []
    
    # 1. 因子路由
    try:
        from panda_factor_server.routes import user_factor_pro
        app.include_router(user_factor_pro.router, prefix="/api/v1", tags=["user_factors"])
        routes_loaded.append("✅ 因子API")
    except Exception as e:
        routes_failed.append(f"❌ 因子API: {str(e)[:50]}")
    
    # 2. LLM路由
    try:
        from panda_llm.routes import chat_router
        app.include_router(chat_router.router, prefix="/llm", tags=["panda_llm"])
        routes_loaded.append("✅ LLM API")
    except Exception as e:
        routes_failed.append(f"❌ LLM API: {str(e)[:50]}")
    
    # 3. 静态文件
    frontend_folder = Path(current_dir) / "panda_web" / "panda_web" / "static"
    if frontend_folder.exists():
        try:
            from starlette.staticfiles import StaticFiles
            mimetypes.add_type("text/css", ".css")
            mimetypes.add_type("application/javascript", ".js")
            app.mount("/factor", StaticFiles(directory=str(frontend_folder), html=True), name="static")
            routes_loaded.append("✅ Web界面")
        except Exception as e:
            routes_failed.append(f"❌ Web界面: {str(e)[:50]}")
    
    # 主页路由
    @app.get("/")
    async def home():
        return {
            "message": "Welcome to PandaFactor Server (Fixed)!",
            "version": "1.0.1",
            "status": "running",
            "loaded_routes": routes_loaded,
            "failed_routes": routes_failed,
            "endpoints": {
                "api_docs": "/docs",
                "api_v1": "/api/v1",
                "llm": "/llm",
                "factor_ui": "/factor"
            }
        }
    
    # 显示加载状态
    print("路由加载状态:")
    for route in routes_loaded:
        print(f"  {route}")
    for route in routes_failed:
        print(f"  {route}")
    print()
    
    if len(routes_loaded) == 0:
        print("⚠️  警告: 没有成功加载任何路由")
        print("建议先运行: python fix_services.py")
        print()
    
    # 启动服务
    uvicorn.run(app, host="0.0.0.0", port=8111, log_level="info")
    
except KeyboardInterrupt:
    print("\n\n✅ 服务已停止")
except Exception as e:
    print(f"\n❌ 启动失败: {e}")
    import traceback
    traceback.print_exc()
    print("\n修复建议:")
    print("1. 运行修复脚本: python fix_services.py")
    print("2. 检查MongoDB是否运行")
    print("3. 查看详细错误信息")
