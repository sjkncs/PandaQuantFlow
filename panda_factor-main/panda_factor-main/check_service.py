#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查PandaFactor服务状态
"""

import requests
import webbrowser
import time

def check_service():
    """检查服务是否正常运行"""
    
    urls = {
        "因子界面": "http://127.0.0.1:8111/factor/",
        "API文档": "http://127.0.0.1:8111/docs",
        "LLM状态": "http://127.0.0.1:8111/llm/status",
        "主页": "http://127.0.0.1:8111/"
    }
    
    print("=" * 60)
    print("🔍 检查PandaFactor服务状态")
    print("=" * 60)
    print()
    
    all_ok = True
    
    for name, url in urls.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: 正常")
                print(f"   URL: {url}")
            else:
                print(f"⚠️  {name}: 返回状态码 {response.status_code}")
                print(f"   URL: {url}")
                all_ok = False
        except requests.exceptions.ConnectionError:
            print(f"❌ {name}: 无法连接")
            print(f"   URL: {url}")
            all_ok = False
        except Exception as e:
            print(f"❌ {name}: 错误 - {e}")
            print(f"   URL: {url}")
            all_ok = False
        print()
    
    print("=" * 60)
    
    if all_ok:
        print("🎉 所有服务正常运行！")
        print()
        print("📋 可访问的界面：")
        for name, url in urls.items():
            print(f"   • {name}: {url}")
        print()
        
        # 询问是否打开浏览器
        choice = input("是否在浏览器中打开因子界面？(y/n): ").strip().lower()
        if choice == 'y':
            print("🌐 正在打开浏览器...")
            webbrowser.open(urls["因子界面"])
            print("✅ 已在浏览器中打开！")
    else:
        print("⚠️  部分服务未正常运行")
        print()
        print("💡 请确保：")
        print("   1. 已运行 py start_server_fixed.py")
        print("   2. 服务已完全启动（可能需要等待10-20秒）")
        print("   3. 端口8111未被占用")
        print()
        print("🔄 如果服务未启动，请运行：")
        print("   py start_server_fixed.py")
    
    print("=" * 60)

if __name__ == "__main__":
    check_service()
