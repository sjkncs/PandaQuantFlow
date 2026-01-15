#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 LLM API 调用
"""

import requests
import json

print("="*60)
print("测试 LLM API 调用")
print("="*60)

# 1. 测试 LLM 状态
print("\n1. 测试 LLM 状态...")
try:
    response = requests.get("http://127.0.0.1:8111/llm/status")
    print(f"   状态码: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('content-type')}")
    
    if response.status_code == 200:
        data = response.json()
        print("   ✅ LLM 状态获取成功")
        print(f"   数据: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}")
    else:
        print(f"   ❌ 失败: {response.text}")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 2. 测试获取模型列表
print("\n2. 测试获取模型列表...")
try:
    response = requests.get("http://127.0.0.1:8111/llm/models")
    print(f"   状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("   ✅ 模型列表获取成功")
        print(f"   可用模型: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}")
    else:
        print(f"   ❌ 失败: {response.text}")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 3. 测试简化聊天接口
print("\n3. 测试简化聊天接口...")
try:
    response = requests.post(
        "http://127.0.0.1:8111/llm/chat/simple",
        headers={"Content-Type": "application/json"},
        json={
            "message": "你好，请用一句话介绍你自己",
            "model": "deepseek",
            "history": []
        },
        timeout=30
    )
    
    print(f"   状态码: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('content-type')}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   完整响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        if data.get("success"):
            print("   ✅ LLM 调用成功！")
            print(f"   回复: {data.get('response', '无回复')[:200]}")
        else:
            print("   ❌ LLM 调用失败！")
            print(f"   错误: {data.get('error', '未知错误')}")
            print(f"   消息: {data.get('message', '无消息')}")
    else:
        print(f"   ❌ HTTP 错误: {response.text}")
except Exception as e:
    print(f"   ❌ 异常: {e}")

print("\n" + "="*60)
print("测试完成")
print("="*60)
