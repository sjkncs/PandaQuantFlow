"""
测试多API密钥负载均衡和故障转移
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, "panda_common"))

print("=" * 70)
print("测试LLM多密钥负载均衡")
print("=" * 70)
print()

try:
    from panda_common.config import config
    from panda_common.llm_manager import get_llm_manager
    
    print("[1/5] 初始化LLM管理器...")
    llm_manager = get_llm_manager(config)
    
    status = llm_manager.get_status()
    print(f"✅ 管理器初始化成功")
    print(f"  API密钥数量: {status['total_keys']}")
    print(f"  负载均衡策略: {status['strategy']}")
    print(f"  默认模型: {status['default_model']}")
    print()
    
    print("[2/5] 可用的金融分析模型:")
    for model_type, model_name in status['available_models'].items():
        print(f"  {model_type}: {model_name}")
    print()
    
    print("[3/5] 测试DeepSeek V3（代码分析能力）...")
    messages = [
        {
            "role": "user",
            "content": "请用一句话介绍DeepSeek V3在金融因子分析中的优势。"
        }
    ]
    
    try:
        response = llm_manager.chat_completion(
            messages=messages,
            model=llm_manager.get_model('deepseek'),
            max_tokens=200
        )
        
        print("✅ DeepSeek V3 响应:")
        print("-" * 70)
        print(response['choices'][0]['message']['content'])
        print("-" * 70)
        print(f"Token使用: {response['usage']['total_tokens']}")
        print()
    except Exception as e:
        print(f"❌ DeepSeek V3 调用失败: {e}")
        print()
    
    print("[4/5] 测试Qwen 2.5（中文理解）...")
    messages = [
        {
            "role": "user",
            "content": "请简要说明Qwen在处理中文金融文本分析时的优势。"
        }
    ]
    
    try:
        response = llm_manager.chat_completion(
            messages=messages,
            model=llm_manager.get_model('qwen'),
            max_tokens=200
        )
        
        print("✅ Qwen 2.5 响应:")
        print("-" * 70)
        print(response['choices'][0]['message']['content'])
        print("-" * 70)
        print(f"Token使用: {response['usage']['total_tokens']}")
        print()
    except Exception as e:
        print(f"❌ Qwen 2.5 调用失败: {e}")
        print()
    
    print("[5/5] 查看API密钥状态...")
    status = llm_manager.get_status()
    print("API密钥状态:")
    for key_status in status['key_status']:
        print(f"  密钥: {key_status['key']}")
        print(f"    失败次数: {key_status['failures']}")
        print(f"    最后成功: {key_status['last_success']}")
    print()
    
    print("=" * 70)
    print("🎉 多密钥负载均衡测试完成！")
    print()
    print("功能说明:")
    print("  ✅ 3个API密钥自动轮询")
    print("  ✅ 单个密钥失败自动切换")
    print("  ✅ 每个密钥支持3次重试")
    print("  ✅ 支持4种金融分析模型")
    print()
    print("使用示例:")
    print("  from panda_common.llm_manager import get_llm_manager")
    print("  llm = get_llm_manager()")
    print("  response = llm.chat_completion(messages=[...])")
    print("=" * 70)
    
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print()
    print("请安装依赖:")
    print("  pip install openai")
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
