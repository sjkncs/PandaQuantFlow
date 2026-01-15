"""
配置PandaFactor环境
运行: python setup_env.py
"""

import sys
import os
import subprocess

print("=" * 70)
print("PandaFactor 环境配置")
print("=" * 70)
print()

current_dir = os.path.dirname(os.path.abspath(__file__))

# 需要配置的模块
modules = [
    "panda_common",
    "panda_data", 
    "panda_factor",
    "panda_llm",
    "panda_factor_server"
]

# 基础依赖
base_deps = [
    "fastapi",
    "uvicorn",
    "pydantic",
    "pymongo",
    "loguru",
    "PyYAML",
    "pandas",
    "numpy"
]

print("[1/3] 安装基础依赖...")
print()

for dep in base_deps:
    print(f"  安装 {dep}...", end=" ")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", dep, 
             "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "--quiet"],
            capture_output=True,
            timeout=60
        )
        if result.returncode == 0:
            print("✅")
        else:
            print("⚠️  (可能已安装)")
    except Exception as e:
        print(f"❌ {e}")

print()
print("[2/3] 配置模块...")
print()

success_count = 0
for module in modules:
    module_path = os.path.join(current_dir, module)
    if os.path.exists(module_path):
        print(f"  配置 {module}...", end=" ")
        try:
            os.chdir(module_path)
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-e", "."],
                capture_output=True,
                timeout=60
            )
            if result.returncode == 0:
                print("✅")
                success_count += 1
            else:
                print("⚠️")
        except Exception as e:
            print(f"❌ {e}")
        finally:
            os.chdir(current_dir)
    else:
        print(f"  ⚠️  {module} 目录不存在")

print()
print("[3/3] 验证安装...")
print()

# 验证模块
sys.path.insert(0, current_dir)
for module in modules:
    sys.path.insert(0, os.path.join(current_dir, module))

test_results = []
for module in ["panda_common", "panda_factor_server"]:
    try:
        __import__(module)
        print(f"  ✅ {module}")
        test_results.append(True)
    except Exception as e:
        print(f"  ❌ {module}: {e}")
        test_results.append(False)

print()
print("=" * 70)

if all(test_results):
    print("🎉 环境配置成功！")
    print()
    print("下一步:")
    print("  python start_server.py")
elif any(test_results):
    print("⚠️  部分配置成功")
    print()
    print("可以尝试启动:")
    print("  python start_server.py")
else:
    print("❌ 配置失败")
    print()
    print("建议:")
    print("1. 检查Python版本: python --version")
    print("2. 手动安装依赖: pip install fastapi uvicorn")
    print("3. 查看详细错误信息")

print("=" * 70)
