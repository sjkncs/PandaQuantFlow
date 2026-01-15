#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试后端服务是否正常运行
"""

import requests
import json

def test_pandafactor():
    """测试 PandaFactor 服务"""
    print("=" * 60)
    print("测试 PandaFactor 服务 (端口 8111)")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8111"
    
    tests = [
        ("主页", "/"),
        ("LLM状态", "/llm/status"),
        ("可用模型", "/llm/models"),
        ("API文档", "/docs"),
    ]
    
    for name, endpoint in tests:
        try:
            url = base_url + endpoint
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: OK ({url})")
            else:
                print(f"⚠️  {name}: {response.status_code} ({url})")
        except Exception as e:
            print(f"❌ {name}: {str(e)}")
    
    print()

def test_quantflow():
    """测试 QuantFlow 服务"""
    print("=" * 60)
    print("测试 QuantFlow 服务 (端口 8000)")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000"
    
    tests = [
        ("主页", "/"),
        ("健康检查", "/api/health"),
        ("工作流列表", "/api/workflows"),
        ("节点库", "/api/nodes"),
        ("市场数据", "/api/market/overview"),
        ("API文档", "/docs"),
    ]
    
    for name, endpoint in tests:
        try:
            url = base_url + endpoint
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: OK ({url})")
                # 显示部分响应内容
                if endpoint.startswith("/api/"):
                    try:
                        data = response.json()
                        print(f"   数据: {json.dumps(data, ensure_ascii=False)[:100]}...")
                    except:
                        pass
            else:
                print(f"⚠️  {name}: {response.status_code} ({url})")
        except Exception as e:
            print(f"❌ {name}: {str(e)}")
    
    print()

def test_llm_chat():
    """测试 LLM 对话功能"""
    print("=" * 60)
    print("测试 LLM 对话功能")
    print("=" * 60)
    
    try:
        url = "http://127.0.0.1:8111/llm/chat/simple"
        data = {
            "message": "你好，请介绍一下你自己"
        }
        
        print(f"发送请求: {url}")
        print(f"消息: {data['message']}")
        
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ LLM对话成功")
            print(f"回复: {result.get('response', '无回复')[:200]}...")
        else:
            print(f"⚠️  状态码: {response.status_code}")
            print(f"响应: {response.text[:200]}")
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
    
    print()

def main():
    """主函数"""
    print()
    print("🔍 PandaAI 后端服务测试")
    print()
    
    # 测试 PandaFactor
    test_pandafactor()
    
    # 测试 QuantFlow
    test_quantflow()
    
    # 测试 LLM 对话
    test_llm_chat()
    
    print("=" * 60)
    print("测试完成！")
    print("=" * 60)
    print()
    print("📍 访问地址:")
    print("   PandaFactor: http://127.0.0.1:8111/")
    print("   QuantFlow: http://127.0.0.1:8000/quantflow/")
    print()

if __name__ == "__main__":
    main()
