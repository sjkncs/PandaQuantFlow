"""
PandaFactor 安装测试脚本
验证所有模块是否正确安装和配置
"""

import sys
import os

print("="*70)
print("PandaFactor 安装测试")
print("="*70)
print()

# 添加项目路径
project_root = r"c:\Users\Lenovo\Desktop\PandaQuantFlow\panda_factor-main\panda_factor-main"
sys.path.insert(0, project_root)

test_results = []

# ==================== 测试1: 模块导入 ====================
print("[测试 1/5] 模块导入测试...")

modules_to_test = [
    'panda_common',
    'panda_data',
    'panda_data_hub',
    'panda_factor',
    'panda_llm',
    'panda_factor_server'
]

for module_name in modules_to_test:
    try:
        __import__(module_name)
        print(f"  ✅ {module_name} 导入成功")
        test_results.append((module_name, True, "导入成功"))
    except ImportError as e:
        print(f"  ❌ {module_name} 导入失败: {e}")
        test_results.append((module_name, False, str(e)))
    except Exception as e:
        print(f"  ⚠️  {module_name} 导入异常: {e}")
        test_results.append((module_name, False, str(e)))

print()

# ==================== 测试2: 配置文件 ====================
print("[测试 2/5] 配置文件测试...")

config_path = os.path.join(project_root, "panda_common", "config.yaml")
if os.path.exists(config_path):
    print(f"  ✅ 配置文件存在: {config_path}")
    test_results.append(("config.yaml", True, "文件存在"))
    
    try:
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print(f"  ✅ 配置文件格式正确")
        print(f"     MongoDB配置: {config.get('mongodb', {})}")
        test_results.append(("config_format", True, "格式正确"))
    except Exception as e:
        print(f"  ❌ 配置文件读取失败: {e}")
        test_results.append(("config_format", False, str(e)))
else:
    print(f"  ❌ 配置文件不存在: {config_path}")
    test_results.append(("config.yaml", False, "文件不存在"))

print()

# ==================== 测试3: 依赖包 ====================
print("[测试 3/5] 依赖包测试...")

required_packages = [
    'pandas',
    'numpy',
    'pymongo',
    'fastapi',
    'loguru',
    'yaml'
]

for package in required_packages:
    try:
        __import__(package)
        print(f"  ✅ {package} 已安装")
        test_results.append((f"pkg_{package}", True, "已安装"))
    except ImportError:
        print(f"  ❌ {package} 未安装")
        test_results.append((f"pkg_{package}", False, "未安装"))

print()

# ==================== 测试4: MongoDB连接 ====================
print("[测试 4/5] MongoDB连接测试...")

try:
    from pymongo import MongoClient
    
    # 尝试连接本地MongoDB
    client = MongoClient('localhost', 27017, serverSelectionTimeoutMS=2000)
    client.server_info()  # 触发连接
    
    print(f"  ✅ MongoDB连接成功")
    print(f"     服务器版本: {client.server_info()['version']}")
    test_results.append(("mongodb_connection", True, "连接成功"))
    
    client.close()
except Exception as e:
    print(f"  ⚠️  MongoDB连接失败: {e}")
    print(f"     提示: 请确保MongoDB服务已启动")
    test_results.append(("mongodb_connection", False, str(e)))

print()

# ==================== 测试5: 因子库功能 ====================
print("[测试 5/5] 因子库功能测试...")

try:
    # 测试我们自己实现的因子库
    sys.path.insert(0, r"c:\Users\Lenovo\Desktop\PandaQuantFlow\lightweight")
    from factor_library import FactorLibrary
    import pandas as pd
    import numpy as np
    
    # 创建测试数据
    test_data = pd.DataFrame({
        'close': np.random.randn(100).cumsum() + 100,
        'open': np.random.randn(100).cumsum() + 100,
        'high': np.random.randn(100).cumsum() + 102,
        'low': np.random.randn(100).cumsum() + 98,
        'volume': np.random.randint(1000, 10000, 100)
    })
    
    # 测试基础函数
    close = FactorLibrary.CLOSE(test_data)
    ma20 = FactorLibrary.MA(close, 20)
    
    print(f"  ✅ 因子库功能正常")
    print(f"     测试数据: {len(test_data)} 条")
    print(f"     MA(20)最新值: {ma20.iloc[-1]:.2f}")
    test_results.append(("factor_library", True, "功能正常"))
    
except Exception as e:
    print(f"  ⚠️  因子库测试失败: {e}")
    test_results.append(("factor_library", False, str(e)))

print()

# ==================== 测试结果汇总 ====================
print("="*70)
print("测试结果汇总")
print("="*70)

success_count = sum(1 for _, success, _ in test_results if success)
total_count = len(test_results)

print(f"\n总计: {success_count}/{total_count} 项测试通过\n")

# 分类显示结果
print("✅ 通过的测试:")
for name, success, msg in test_results:
    if success:
        print(f"   - {name}: {msg}")

print("\n❌ 失败的测试:")
failed_tests = [(name, msg) for name, success, msg in test_results if not success]
if failed_tests:
    for name, msg in failed_tests:
        print(f"   - {name}: {msg}")
else:
    print("   (无)")

print()
print("="*70)

if success_count == total_count:
    print("🎉 所有测试通过！PandaFactor已正确配置")
elif success_count >= total_count * 0.7:
    print("⚠️  大部分测试通过，但仍有问题需要解决")
else:
    print("❌ 多项测试失败，请检查配置")

print("="*70)
print()

# ==================== 下一步提示 ====================
print("📝 下一步操作:")
print()

if not any(name == "mongodb_connection" and success for name, success, _ in test_results):
    print("1. ⚠️  启动MongoDB服务:")
    print("   Windows: net start MongoDB")
    print("   Linux: sudo systemctl start mongod")
    print()

if failed_tests:
    print("2. 📦 安装缺失的依赖:")
    print("   pip install -r requirements.txt")
    print()

print("3. 🚀 开始使用PandaFactor:")
print("   - 编写自定义因子")
print("   - 启动Web服务器")
print("   - 配置数据源")
print()

print("4. 📚 查看文档:")
print("   - PANDAFACTOR_SETUP_GUIDE.md")
print("   - FACTOR_LIBRARY_README.md")
print()
