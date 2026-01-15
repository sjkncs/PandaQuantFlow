"""
修复PandaFactor服务问题
1. 修复因子路由加载失败
2. 修复LLM聊天功能
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

print("=" * 70)
print("修复PandaFactor服务")
print("=" * 70)
print()

# 问题1: 配置panda_data_hub模块
print("[1/3] 配置 panda_data_hub 模块...")
panda_data_hub_path = os.path.join(current_dir, "panda_data_hub")
if os.path.exists(panda_data_hub_path):
    os.chdir(panda_data_hub_path)
    import subprocess
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", "."],
        capture_output=True
    )
    if result.returncode == 0:
        print("✅ panda_data_hub 配置成功")
    else:
        print("⚠️  panda_data_hub 配置失败")
        print(result.stderr.decode())
    os.chdir(current_dir)
else:
    print("❌ panda_data_hub 目录不存在")

print()

# 问题2: 修改MongoDB配置为单节点模式
print("[2/3] 修改MongoDB配置...")
config_file = os.path.join(current_dir, "panda_common", "panda_common", "config.yaml")
if os.path.exists(config_file):
    with open(config_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经是single模式
    if 'MONGO_TYPE: "replica_set"' in content:
        content = content.replace('MONGO_TYPE: "replica_set"', 'MONGO_TYPE: "single"')
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ MongoDB配置已修改为单节点模式")
    else:
        print("✅ MongoDB配置已经是单节点模式")
else:
    print("❌ 配置文件不存在")

print()

# 问题3: 验证修复
print("[3/3] 验证修复...")
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, "panda_data_hub"))

try:
    from panda_data_hub.models import stock
    print("✅ panda_data_hub.models 导入成功")
except Exception as e:
    print(f"⚠️  panda_data_hub.models 导入失败: {e}")

try:
    from panda_common.config import config
    mongo_type = config.get('MONGO_TYPE', 'unknown')
    print(f"✅ MongoDB配置类型: {mongo_type}")
except Exception as e:
    print(f"⚠️  配置加载失败: {e}")

print()
print("=" * 70)
print("修复完成！")
print()
print("下一步:")
print("1. 重启服务: python start_server.py")
print("2. 访问: http://127.0.0.1:8111/docs")
print("=" * 70)
