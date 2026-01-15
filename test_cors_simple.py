#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单的 CORS 测试脚本
"""

import requests
import time

print("等待服务启动...")
time.sleep(5)

print("\n" + "="*60)
print("测试 CORS 配置")
print("="*60 + "\n")

# 测试 OPTIONS 请求（预检请求）
print("1. 测试 OPTIONS 预检请求...")
try:
    response = requests.options(
        "http://127.0.0.1:8111/llm/status",
        headers={
            "Origin": "http://127.0.0.1:56849",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "content-type"
        }
    )
    print(f"   状态码: {response.status_code}")
    print(f"   Access-Control-Allow-Origin: {response.headers.get('access-control-allow-origin', 'MISSING')}")
    print(f"   Access-Control-Allow-Methods: {response.headers.get('access-control-allow-methods', 'MISSING')}")
    print(f"   Access-Control-Allow-Headers: {response.headers.get('access-control-allow-headers', 'MISSING')}")
    
    if response.headers.get('access-control-allow-origin') == '*':
        print("   ✅ CORS 配置正确！")
    else:
        print("   ❌ CORS 配置错误！")
except Exception as e:
    print(f"   ❌ 错误: {e}")

print("\n2. 测试实际 GET 请求...")
try:
    response = requests.get(
        "http://127.0.0.1:8111/llm/status",
        headers={
            "Origin": "http://127.0.0.1:56849"
        }
    )
    print(f"   状态码: {response.status_code}")
    print(f"   Access-Control-Allow-Origin: {response.headers.get('access-control-allow-origin', 'MISSING')}")
    
    if response.status_code == 200:
        print("   ✅ 请求成功！")
        data = response.json()
        print(f"   响应数据: {data}")
    else:
        print(f"   ❌ 请求失败: {response.text}")
except Exception as e:
    print(f"   ❌ 错误: {e}")

print("\n3. 测试 POST 请求...")
try:
    response = requests.post(
        "http://127.0.0.1:8111/llm/chat/simple",
        headers={
            "Origin": "http://127.0.0.1:56849",
            "Content-Type": "application/json"
        },
        json={
            "message": "CORS测试",
            "model": "deepseek"
        }
    )
    print(f"   状态码: {response.status_code}")
    print(f"   Access-Control-Allow-Origin: {response.headers.get('access-control-allow-origin', 'MISSING')}")
    
    if response.status_code == 200:
        print("   ✅ POST 请求成功！")
    else:
        print(f"   ❌ POST 请求失败: {response.text[:100]}")
except Exception as e:
    print(f"   ❌ 错误: {e}")

print("\n" + "="*60)
print("测试完成！")
print("="*60)
