"""
测试LLM聊天功能
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, "panda_common"))

print("=" * 70)
print("测试LLM聊天功能")
print("=" * 70)
print()

try:
    from panda_common.config import config
    
    print("[1/3] 读取配置...")
    llm_api_key = config.get('LLM_API_KEY', '')
    llm_model = config.get('LLM_MODEL', '')
    llm_base_url = config.get('LLM_BASE_URL', '')
    
    print(f"  API Key: {llm_api_key[:20]}...")
    print(f"  模型: {llm_model}")
    print(f"  Base URL: {llm_base_url}")
    print()
    
    print("[2/3] 测试API连接...")
    
    import requests
    
    # 测试聊天补全
    headers = {
        "Authorization": f"Bearer {llm_api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": llm_model,
        "messages": [
            {
                "role": "user",
                "content": "你好，请用一句话介绍你自己。"
            }
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    print(f"  发送请求到: {llm_base_url}/chat/completions")
    print(f"  使用模型: {llm_model}")
    print()
    
    response = requests.post(
        f"{llm_base_url}/chat/completions",
        headers=headers,
        json=data,
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ API连接成功！")
        print()
        print("[3/3] 响应内容:")
        print("-" * 70)
        
        if 'choices' in result and len(result['choices']) > 0:
            message = result['choices'][0]['message']['content']
            print(message)
            print("-" * 70)
            print()
            
            # 显示使用情况
            if 'usage' in result:
                usage = result['usage']
                print("Token使用情况:")
                print(f"  输入: {usage.get('prompt_tokens', 0)} tokens")
                print(f"  输出: {usage.get('completion_tokens', 0)} tokens")
                print(f"  总计: {usage.get('total_tokens', 0)} tokens")
        else:
            print("响应格式异常:")
            print(result)
    else:
        print(f"❌ API请求失败")
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.text}")
    
    print()
    print("=" * 70)
    print("🎉 LLM功能测试完成！")
    print()
    print("可用的模型:")
    print("  1. Pro/moonshotai/Kimi-K2-Thinking (当前)")
    print("  2. claude-4.5-thinking")
    print("  3. Qwen/Qwen2.5-72B-Instruct")
    print("  4. deepseek-ai/DeepSeek-V3")
    print()
    print("切换模型: 修改 config.yaml 中的 LLM_MODEL")
    print("=" * 70)
    
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print()
    print("请安装依赖:")
    print("  pip install requests")
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
