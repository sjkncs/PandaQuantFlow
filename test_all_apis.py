#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试所有 API 端点
"""

import requests
import json

API_BASE = "http://127.0.0.1:8111"

print("="*60)
print("测试所有 API 端点")
print("="*60)

# 测试列表
tests = [
    {
        "name": "API 状态",
        "method": "GET",
        "url": f"{API_BASE}/api/status"
    },
    {
        "name": "LLM 状态",
        "method": "GET",
        "url": f"{API_BASE}/llm/status"
    },
    {
        "name": "LLM 模型列表",
        "method": "GET",
        "url": f"{API_BASE}/llm/models"
    },
    {
        "name": "市场概览",
        "method": "GET",
        "url": f"{API_BASE}/analysis/market_overview"
    },
    {
        "name": "简化聊天",
        "method": "POST",
        "url": f"{API_BASE}/llm/chat/simple",
        "json": {
            "message": "测试消息",
            "model": "deepseek",
            "history": []
        }
    },
    {
        "name": "股票分析",
        "method": "POST",
        "url": f"{API_BASE}/analysis/stock",
        "json": {
            "code": "000001",
            "period": 30,
            "analysis_type": "technical"
        }
    }
]

# 执行测试
results = {"passed": 0, "failed": 0}

for i, test in enumerate(tests, 1):
    print(f"\n{i}. 测试 {test['name']}...")
    print(f"   URL: {test['url']}")
    
    try:
        if test['method'] == 'GET':
            response = requests.get(test['url'], timeout=10)
        else:
            response = requests.post(
                test['url'],
                headers={"Content-Type": "application/json"},
                json=test.get('json'),
                timeout=30
            )
        
        print(f"   状态码: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type')}")
        
        if response.status_code == 200:
            data = response.json()
            
            # 检查是否有 success 字段
            if 'success' in data:
                if data['success']:
                    print(f"   ✅ 成功")
                    results['passed'] += 1
                else:
                    print(f"   ❌ API 返回失败: {data.get('error', '未知错误')}")
                    results['failed'] += 1
            else:
                print(f"   ✅ 成功（无 success 字段）")
                results['passed'] += 1
            
            # 显示部分响应数据
            response_preview = json.dumps(data, ensure_ascii=False, indent=2)[:300]
            print(f"   响应预览: {response_preview}...")
        else:
            print(f"   ❌ HTTP 错误: {response.status_code}")
            print(f"   错误信息: {response.text[:200]}")
            results['failed'] += 1
            
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        results['failed'] += 1

# 总结
print("\n" + "="*60)
print("测试总结")
print("="*60)
print(f"通过: {results['passed']}/{len(tests)}")
print(f"失败: {results['failed']}/{len(tests)}")
print(f"成功率: {results['passed']/len(tests)*100:.1f}%")

if results['failed'] == 0:
    print("\n🎉 所有测试通过！")
else:
    print(f"\n⚠️  有 {results['failed']} 个测试失败")

print("="*60)
