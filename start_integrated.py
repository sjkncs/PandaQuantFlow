#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PandaAI 集成启动脚本
同时启动 PandaFactor 和 QuantFlow 服务
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def print_header():
    """打印启动标题"""
    print("=" * 80)
    print("🐼 PandaAI 量化平台 - 集成启动")
    print("=" * 80)
    print("包含: PandaFactor + QuantFlow")
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
                    return True, parts[-1]  # 返回True和PID
        return False, None
    except:
        return False, None

def kill_process(pid):
    """结束进程"""
    try:
        subprocess.run(['taskkill', '/F', '/PID', str(pid)], capture_output=True)
        return True
    except:
        return False

def install_dependencies():
    """检查并安装必要的依赖"""
    print("📦 检查依赖...")
    
    required = [
        "fastapi",
        "uvicorn", 
        "pydantic",
        "numpy",
        "pandas",
        "matplotlib",
        "pymongo",
        "websockets",
        "aiofiles"
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"  ❌ {package}")
    
    if missing:
        print(f"\n正在安装缺失的包: {', '.join(missing)}...")
        for package in missing:
            subprocess.run([
                sys.executable, "-m", "pip", "install", package,
                "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"
            ], capture_output=True)
        print("✅ 依赖安装完成")
    
    print()

def start_panda_factor():
    """启动 PandaFactor 服务"""
    print("🔧 启动 PandaFactor 服务...")
    
    # 检查端口8111
    occupied, pid = check_port(8111)
    if occupied:
        print(f"  ⚠️  端口 8111 被占用 (PID: {pid})")
        choice = input("  是否结束该进程？(y/n): ").strip().lower()
        if choice == 'y':
            if kill_process(pid):
                print("  ✅ 已结束进程")
                time.sleep(2)
            else:
                print("  ❌ 无法结束进程，请手动处理")
                return None
        else:
            print("  ✅ PandaFactor 已在运行")
            return None
    
    # 启动 start_complete.py
    factor_script = project_root / "panda_factor-main" / "panda_factor-main" / "start_complete.py"
    if not factor_script.exists():
        print(f"  ❌ 找不到 {factor_script}")
        return None
    
    try:
        process = subprocess.Popen(
            [sys.executable, str(factor_script)],
            cwd=str(factor_script.parent),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        
        # 等待服务启动
        for i in range(10):
            time.sleep(1)
            if check_port(8111)[0]:
                print("  ✅ PandaFactor 启动成功")
                print("     访问: http://127.0.0.1:8111/")
                return process
        
        print("  ⚠️  PandaFactor 启动超时")
        return process
        
    except Exception as e:
        print(f"  ❌ 启动失败: {e}")
        return None

def start_quantflow():
    """启动 QuantFlow 服务"""
    print("🚀 启动 QuantFlow 工作流服务...")
    
    # 检查端口8000
    occupied, pid = check_port(8000)
    if occupied:
        print(f"  ⚠️  端口 8000 被占用 (PID: {pid})")
        choice = input("  是否结束该进程？(y/n): ").strip().lower()
        if choice == 'y':
            if kill_process(pid):
                print("  ✅ 已结束进程")
                time.sleep(2)
            else:
                print("  ❌ 无法结束进程，请手动处理")
                return None
        else:
            print("  ✅ QuantFlow 已在运行")
            return None
    
    # 启动 main.py
    main_script = project_root / "src" / "panda_server" / "main.py"
    if not main_script.exists():
        print(f"  ❌ 找不到 {main_script}")
        return None
    
    try:
        process = subprocess.Popen(
            [sys.executable, str(main_script)],
            cwd=str(project_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        
        # 等待服务启动
        for i in range(10):
            time.sleep(1)
            if check_port(8000)[0]:
                print("  ✅ QuantFlow 启动成功")
                print("     工作流: http://127.0.0.1:8000/quantflow/")
                print("     图表: http://127.0.0.1:8000/charts/")
                print("     API文档: http://127.0.0.1:8000/docs")
                return process
        
        print("  ⚠️  QuantFlow 启动超时")
        return process
        
    except Exception as e:
        print(f"  ❌ 启动失败: {e}")
        return None

def main():
    """主函数"""
    print_header()
    
    # 1. 检查依赖
    install_dependencies()
    
    # 2. 启动服务
    processes = []
    
    # 启动 PandaFactor
    print()
    factor_process = start_panda_factor()
    if factor_process:
        processes.append(factor_process)
    
    print()
    
    # 启动 QuantFlow
    quantflow_process = start_quantflow()
    if quantflow_process:
        processes.append(quantflow_process)
    
    # 3. 显示访问信息
    print()
    print("=" * 80)
    print("✨ 所有服务已启动！")
    print("=" * 80)
    print()
    print("📍 访问地址:")
    print()
    print("  🎯 主入口 (推荐):")
    print("     http://127.0.0.1:8111/")
    print()
    print("  📊 PandaFactor 因子库:")
    print("     http://127.0.0.1:8111/factor/professional.html")
    print()
    print("  🚀 QuantFlow 工作流:")
    print("     http://127.0.0.1:8000/quantflow/")
    print()
    print("  📈 超级图表:")
    print("     http://127.0.0.1:8000/charts/")
    print()
    print("  📚 API文档:")
    print("     Factor API: http://127.0.0.1:8111/docs")
    print("     QuantFlow API: http://127.0.0.1:8000/docs")
    print()
    print("=" * 80)
    print("💡 提示: 按 Ctrl+C 停止所有服务")
    print("=" * 80)
    
    # 4. 自动打开浏览器
    time.sleep(3)
    try:
        webbrowser.open("http://127.0.0.1:8111/")
    except:
        pass
    
    # 5. 保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n正在停止所有服务...")
        for p in processes:
            if p:
                try:
                    p.terminate()
                    p.wait(timeout=5)
                except:
                    p.kill()
        print("✅ 所有服务已停止")
        sys.exit(0)

if __name__ == "__main__":
    main()
