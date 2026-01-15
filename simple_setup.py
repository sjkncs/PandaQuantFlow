"""
PandaFactor 超级简单配置脚本 (Python版本)
最可靠的配置方式
"""

import os
import sys
import subprocess

print("=" * 70)
print("PandaFactor 简单配置")
print("=" * 70)
print()

PROJECT_ROOT = r"c:\Users\Lenovo\Desktop\PandaQuantFlow\panda_factor-main\panda_factor-main"

# 步骤1: 检查Python
print("[1/4] 检查Python环境...")
try:
    version = sys.version.split()[0]
    print(f"✅ Python {version}")
except:
    print("❌ Python检查失败")
    input("按回车退出...")
    sys.exit(1)

print()

# 步骤2: 安装核心依赖
print("[2/4] 安装核心依赖...")
core_deps = [
    "numpy",
    "pandas", 
    "pymongo",
    "loguru",
    "PyYAML",
    "setuptools"
]

for dep in core_deps:
    print(f"  安装 {dep}...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", dep, 
             "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", 
             "--quiet"],
            check=True,
            capture_output=True
        )
    except:
        print(f"  ⚠️  {dep} 安装失败，跳过...")

print("✅ 核心依赖安装完成")
print()

# 步骤3: 配置核心模块
print("[3/4] 配置核心模块...")
modules = ["panda_common", "panda_data", "panda_factor"]

for module in modules:
    module_path = os.path.join(PROJECT_ROOT, module)
    if os.path.exists(module_path):
        print(f"  配置 {module}...")
        os.chdir(module_path)
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-e", "."],
                check=True,
                capture_output=True
            )
            print(f"  ✅ {module} 配置成功")
        except:
            print(f"  ⚠️  {module} 配置失败，跳过...")
    else:
        print(f"  ⚠️  {module} 目录不存在")

print()

# 步骤4: 验证安装
print("[4/4] 验证安装...")
os.chdir(r"c:\Users\Lenovo\Desktop\PandaQuantFlow")

success_count = 0
for module in modules:
    try:
        __import__(module)
        print(f"  ✅ {module}")
        success_count += 1
    except Exception as e:
        print(f"  ❌ {module}: {e}")

print()
print("=" * 70)

if success_count == len(modules):
    print("🎉 配置成功！")
elif success_count > 0:
    print(f"⚠️  部分成功 ({success_count}/{len(modules)})")
else:
    print("❌ 配置失败")

print("=" * 70)
print()
print("下一步:")
print("  python run_pandafactor_example.py")
print()

input("按回车退出...")
