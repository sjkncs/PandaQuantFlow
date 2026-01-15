#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Panda AI 因子库 - 完整启动脚本
集成端口检查、MongoDB配置、服务启动
"""

import sys
import os
import subprocess
import time

# 添加所有模块到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, "panda_common"))
sys.path.insert(0, os.path.join(current_dir, "panda_data"))
sys.path.insert(0, os.path.join(current_dir, "panda_data_hub"))
sys.path.insert(0, os.path.join(current_dir, "panda_factor"))
sys.path.insert(0, os.path.join(current_dir, "panda_llm"))
sys.path.insert(0, os.path.join(current_dir, "panda_factor_server"))

def print_header():
    """打印标题"""
    print("=" * 80)
    print("🐼 Panda AI 因子库 - 智能量化因子平台")
    print("=" * 80)
    print()

def check_port(port):
    """检查端口是否被占用"""
    try:
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True,
            text=True,
            encoding='gbk',
            timeout=5
        )
        
        for line in result.stdout.split('\n'):
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    return True, parts[-1]  # 返回PID
        
        return False, None
        
    except Exception as e:
        print(f"⚠️  端口检查失败: {e}")
        return False, None

def kill_process(pid):
    """结束进程"""
    try:
        subprocess.run(['taskkill', '/PID', pid, '/F'], 
                      capture_output=True, timeout=5)
        return True
    except:
        return False

def check_dependencies():
    """检查依赖"""
    print("[1/4] 检查依赖...")
    
    required_deps = {
        "fastapi": "fastapi",
        "uvicorn": "uvicorn",
        "pydantic": "pydantic",
        "numpy": "numpy",
        "pandas": "pandas",
        "matplotlib": "matplotlib"
    }
    
    optional_deps = {
        "pymongo": "pymongo"
    }
    
    missing_required = []
    missing_optional = []
    
    for module, package in required_deps.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            missing_required.append(package)
            print(f"  ❌ {package} (必需)")
    
    for module, package in optional_deps.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            missing_optional.append(package)
            print(f"  ⚠️  {package} (可选)")
    
    if missing_required:
        print()
        print(f"⚠️  缺少必需依赖: {', '.join(missing_required)}")
        choice = input("是否自动安装？(y/n): ").strip().lower()
        
        if choice == 'y':
            print("正在安装...")
            subprocess.run([
                sys.executable, "-m", "pip", "install"] + missing_required + 
                ["-i", "https://pypi.tuna.tsinghua.edu.cn/simple"
            ])
            print("✅ 安装完成")
        else:
            print("❌ 无法继续，请先安装依赖")
            return False
    
    if missing_optional:
        print()
        print(f"💡 提示: 可选依赖 {', '.join(missing_optional)} 未安装")
        print("   - 没有MongoDB，数据将存储在内存中")
        print("   - 如需完整功能，请运行: py mongodb_setup.py")
    
    print()
    return True

def check_port_availability():
    """检查端口可用性"""
    print("[2/4] 检查端口...")
    
    port = 8111
    occupied, pid = check_port(port)
    
    if occupied:
        print(f"⚠️  端口 {port} 被占用 (PID: {pid})")
        choice = input("是否自动清理？(y/n): ").strip().lower()
        
        if choice == 'y':
            print(f"正在结束进程 {pid}...")
            if kill_process(pid):
                print("✅ 端口已清理")
                time.sleep(1)
            else:
                print("❌ 清理失败，请手动结束进程或运行: py port_manager.py")
                return False
        else:
            print("💡 请运行端口管理工具: py port_manager.py")
            return False
    else:
        print(f"✅ 端口 {port} 可用")
    
    print()
    return True

def check_mongodb():
    """检查MongoDB（可选）"""
    print("[3/4] 检查MongoDB...")
    
    try:
        import pymongo
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017/', 
                                     serverSelectionTimeoutMS=2000)
        client.server_info()
        client.close()
        print("✅ MongoDB已连接")
        return True
    except ImportError:
        print("⚠️  pymongo未安装（可选）")
        return False
    except Exception:
        print("⚠️  MongoDB未运行（可选）")
        print("   - 服务将在无MongoDB模式下运行")
        print("   - 如需配置MongoDB，请运行: py mongodb_setup.py")
        return False
    
    print()

def load_config():
    """加载配置"""
    print("[4/4] 加载配置...")
    
    try:
        import yaml
        config_path = os.path.join(current_dir, "panda_common", "panda_common", "config.yaml")
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # 显示LLM配置
            if 'LLM_API_KEYS' in config:
                api_keys = config['LLM_API_KEYS']
                print(f"✅ LLM API密钥: {len(api_keys)}个")
                
                if 'LLM_MODEL' in config:
                    print(f"✅ 默认模型: {config['LLM_MODEL']}")
                
                if 'LLM_MODELS' in config:
                    models = config['LLM_MODELS']
                    print(f"✅ 可用模型: {len(models)}个")
                    for name, model in models.items():
                        print(f"   - {name}: {model}")
            else:
                print("⚠️  未找到LLM配置")
        else:
            print("⚠️  配置文件不存在")
            
    except Exception as e:
        print(f"⚠️  加载配置失败: {e}")
    
    print()

def start_server():
    """启动服务"""
    print("=" * 80)
    print("🚀 启动服务...")
    print("=" * 80)
    print()
    
    try:
        # 导入FastAPI组件
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.responses import HTMLResponse, FileResponse
        import uvicorn
        from pathlib import Path
        import mimetypes
        
        # 创建应用
        app = FastAPI(
            title="Panda AI Factor Library",
            description="智能量化因子开发平台",
            version="2.0.0"
        )
        
        # CORS配置 - 完全开放本地访问（仅开发环境）
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # 允许所有源
            allow_credentials=False,  # 关闭凭证要求，避免与 * 冲突
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"],
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
            routes_failed.append(f"⚠️  因子API: {str(e)[:50]}")
        
        # 2. LLM路由
        try:
            from panda_llm.routes import chat_router
            app.include_router(chat_router.router, tags=["panda_llm"])  # 不添加prefix，路由已经包含完整路径
            routes_loaded.append("✅ LLM API")
        except Exception as e:
            routes_failed.append(f"⚠️  LLM API: {str(e)[:50]}")
        
        # 3. 数据分析路由（路由已包含 /analysis 前缀，不需要再添加）
        try:
            from panda_llm.routes import analysis_router
            app.include_router(analysis_router.router, tags=["analysis"])
            routes_loaded.append("✅ 数据分析API")
        except Exception as e:
            routes_failed.append(f"⚠️  数据分析API: {str(e)[:50]}")
        
        # 4. 静态文件
        frontend_folder = Path(current_dir) / "panda_web" / "panda_web" / "static"
        if frontend_folder.exists():
            try:
                from starlette.staticfiles import StaticFiles
                mimetypes.add_type("text/css", ".css")
                mimetypes.add_type("application/javascript", ".js")
                mimetypes.add_type("text/html", ".html")
                app.mount("/factor", StaticFiles(directory=str(frontend_folder), html=True), name="static")
                
                # 添加icon文件夹映射
                icon_folder = Path("C:/Users/Lenovo/Desktop/PandaQuantFlow/icon")
                if icon_folder.exists():
                    app.mount("/icon", StaticFiles(directory=str(icon_folder)), name="icon")
                    routes_loaded.append("✅ 图标资源")
                
                routes_loaded.append("✅ Web界面")
            except Exception as e:
                routes_failed.append(f"⚠️  Web界面: {str(e)[:50]}")
        
        # 主页路由 - 重定向到新界面
        from fastapi.responses import RedirectResponse
        
        @app.get("/")
        async def home():
            # 自动重定向到专业版界面
            return RedirectResponse(url="/factor/professional.html")
        
        @app.get("/api/status")
        async def api_status():
            # API状态端点
            return {
                "message": "Welcome to Panda AI Factor Library!",
                "version": "2.0.0",
                "status": "running",
                "loaded_routes": routes_loaded,
                "failed_routes": routes_failed,
                "endpoints": {
                    "factor_library": "/factor/factor_library.html",
                    "api_docs": "/docs",
                    "api_v1": "/api/v1",
                    "llm": "/llm"
                }
            }
        
        # 显示加载状态
        print("路由加载状态:")
        for route in routes_loaded:
            print(f"  {route}")
        for route in routes_failed:
            print(f"  {route}")
        print()
        
        print("=" * 80)
        print("✅ 服务已启动！")
        print("=" * 80)
        print()
        print("📋 访问地址:")
        print(f"  🌐 因子库界面: http://127.0.0.1:8111/factor/factor_library.html")
        print(f"  📚 API文档:     http://127.0.0.1:8111/docs")
        print(f"  🏠 主页:        http://127.0.0.1:8111/")
        print()
        print("💡 功能:")
        print(f"  - AI因子生成 (支持4个模型)")
        print(f"  - 智能代码生成")
        print(f"  - 因子库管理")
        print(f"  - API接口调用")
        print()
        print("按 Ctrl+C 停止服务")
        print("=" * 80)
        print()
        
        # 启动服务
        uvicorn.run(app, host="0.0.0.0", port=8111, log_level="info")
        
    except KeyboardInterrupt:
        print("\n\n✅ 服务已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    print_header()
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 检查端口
    if not check_port_availability():
        return
    
    # 检查MongoDB（可选）
    check_mongodb()
    
    # 加载配置
    load_config()
    
    # 启动服务
    start_server()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 已取消")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
