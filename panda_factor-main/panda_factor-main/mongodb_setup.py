#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MongoDB 配置和测试工具
"""

import subprocess
import sys
import time

def check_mongodb_installed():
    """检查MongoDB是否已安装"""
    try:
        result = subprocess.run(
            ['mongod', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            return True, version_line
        else:
            return False, "MongoDB未安装"
            
    except FileNotFoundError:
        return False, "MongoDB未安装或未添加到PATH"
    except Exception as e:
        return False, f"检查失败: {e}"

def check_mongodb_service():
    """检查MongoDB服务是否运行"""
    try:
        result = subprocess.run(
            ['sc', 'query', 'MongoDB'],
            capture_output=True,
            text=True,
            encoding='gbk'
        )
        
        if 'RUNNING' in result.stdout:
            return True, "运行中"
        elif 'STOPPED' in result.stdout:
            return False, "已停止"
        else:
            return False, "未安装服务"
            
    except Exception as e:
        return False, f"检查失败: {e}"

def start_mongodb_service():
    """启动MongoDB服务"""
    try:
        print("正在启动MongoDB服务...")
        result = subprocess.run(
            ['net', 'start', 'MongoDB'],
            capture_output=True,
            text=True,
            encoding='gbk'
        )
        
        if result.returncode == 0 or '已经启动' in result.stdout:
            return True, "启动成功"
        else:
            return False, result.stderr or result.stdout
            
    except Exception as e:
        return False, f"启动失败: {e}"

def test_mongodb_connection():
    """测试MongoDB连接"""
    try:
        import pymongo
        
        print("正在测试MongoDB连接...")
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017/', serverSelectionTimeoutMS=5000)
        
        # 尝试连接
        client.server_info()
        
        # 获取数据库列表
        dbs = client.list_database_names()
        
        client.close()
        
        return True, f"连接成功！数据库: {', '.join(dbs)}"
        
    except ImportError:
        return False, "pymongo未安装，运行: pip install pymongo"
    except Exception as e:
        return False, f"连接失败: {e}"

def install_pymongo():
    """安装pymongo"""
    try:
        print("正在安装pymongo...")
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', 'pymongo', 
             '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return True, "安装成功"
        else:
            return False, result.stderr
            
    except Exception as e:
        return False, f"安装失败: {e}"

def create_panda_database():
    """创建Panda数据库和集合"""
    try:
        import pymongo
        
        print("正在创建Panda数据库...")
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
        
        # 创建数据库
        db = client['panda']
        
        # 创建集合
        collections = ['factors', 'stocks', 'users', 'strategies']
        
        for coll_name in collections:
            if coll_name not in db.list_collection_names():
                db.create_collection(coll_name)
                print(f"  ✅ 创建集合: {coll_name}")
            else:
                print(f"  ℹ️  集合已存在: {coll_name}")
        
        # 插入测试数据
        if db.factors.count_documents({}) == 0:
            test_factor = {
                'name': '测试因子',
                'description': '这是一个测试因子',
                'type': 'momentum',
                'created_at': time.time()
            }
            db.factors.insert_one(test_factor)
            print("  ✅ 插入测试数据")
        
        client.close()
        
        return True, "数据库创建成功"
        
    except Exception as e:
        return False, f"创建失败: {e}"

def main():
    """主函数"""
    print("=" * 70)
    print("🗄️  MongoDB 配置工具")
    print("=" * 70)
    print()
    
    # 1. 检查MongoDB是否安装
    print("[1/5] 检查MongoDB安装...")
    installed, message = check_mongodb_installed()
    
    if installed:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        print()
        print("💡 MongoDB未安装。您有两个选择:")
        print()
        print("选项1: 安装MongoDB (推荐用于生产环境)")
        print("  - 下载地址: https://www.mongodb.com/try/download/community")
        print("  - 安装后重新运行此脚本")
        print()
        print("选项2: 不使用MongoDB (开发测试)")
        print("  - Panda因子库可以在没有MongoDB的情况下运行")
        print("  - 数据将存储在内存中")
        print("  - 运行: py start_server_fixed.py")
        print()
        
        choice = input("是否继续配置（即使MongoDB未安装）？(y/n): ").strip().lower()
        if choice != 'y':
            print("\n👋 已退出")
            return
    
    print()
    
    # 2. 检查MongoDB服务
    print("[2/5] 检查MongoDB服务...")
    running, status = check_mongodb_service()
    
    if running:
        print(f"✅ MongoDB服务{status}")
    else:
        print(f"⚠️  MongoDB服务{status}")
        
        if '未安装服务' not in status:
            choice = input("是否启动MongoDB服务？(y/n): ").strip().lower()
            if choice == 'y':
                success, message = start_mongodb_service()
                if success:
                    print(f"✅ {message}")
                else:
                    print(f"❌ {message}")
                    print("💡 请尝试以管理员身份运行此脚本")
    
    print()
    
    # 3. 检查pymongo
    print("[3/5] 检查pymongo...")
    try:
        import pymongo
        print(f"✅ pymongo已安装 (版本: {pymongo.__version__})")
    except ImportError:
        print("❌ pymongo未安装")
        choice = input("是否安装pymongo？(y/n): ").strip().lower()
        if choice == 'y':
            success, message = install_pymongo()
            if success:
                print(f"✅ {message}")
            else:
                print(f"❌ {message}")
                return
    
    print()
    
    # 4. 测试连接
    print("[4/5] 测试MongoDB连接...")
    success, message = test_mongodb_connection()
    
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        print()
        print("💡 提示:")
        print("  - 确保MongoDB服务正在运行")
        print("  - 检查防火墙设置")
        print("  - 或者选择不使用MongoDB运行")
        print()
        
        choice = input("是否继续（跳过MongoDB）？(y/n): ").strip().lower()
        if choice != 'y':
            print("\n👋 已退出")
            return
    
    print()
    
    # 5. 创建数据库
    if success:
        print("[5/5] 创建Panda数据库...")
        db_success, db_message = create_panda_database()
        
        if db_success:
            print(f"✅ {db_message}")
        else:
            print(f"❌ {db_message}")
    else:
        print("[5/5] 跳过数据库创建（MongoDB未连接）")
    
    print()
    print("=" * 70)
    print("📋 配置总结")
    print("=" * 70)
    print()
    
    if success:
        print("✅ MongoDB配置完成！")
        print()
        print("数据库信息:")
        print("  - 地址: mongodb://127.0.0.1:27017/")
        print("  - 数据库: panda")
        print("  - 集合: factors, stocks, users, strategies")
        print()
        print("配置文件位置:")
        print("  panda_common/panda_common/config.yaml")
        print()
        print("当前配置:")
        print("  MONGO_URI: 127.0.0.1:27017")
        print("  MONGO_DB: panda")
        print("  MONGO_USER: (空 - 无认证)")
        print()
    else:
        print("⚠️  MongoDB未配置")
        print()
        print("您仍然可以使用Panda因子库:")
        print("  - 数据将存储在内存中")
        print("  - 重启服务后数据会丢失")
        print("  - 适合开发和测试")
        print()
    
    print("下一步:")
    print("  1. 运行: py start_server_fixed.py")
    print("  2. 访问: http://127.0.0.1:8111/factor_library.html")
    print()
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 已取消")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
