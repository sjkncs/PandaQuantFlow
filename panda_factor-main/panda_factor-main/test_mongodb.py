"""
测试MongoDB连接
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, "panda_common"))

print("=" * 70)
print("MongoDB 连接测试")
print("=" * 70)
print()

try:
    from pymongo import MongoClient
    from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
    
    print("[1/4] 导入pymongo...")
    print("✅ pymongo已安装")
    print()
    
    print("[2/4] 读取配置...")
    from panda_common.config import config
    
    mongo_uri = config.get('MONGO_URI', '127.0.0.1:27017')
    mongo_user = config.get('MONGO_USER', 'panda')
    mongo_password = config.get('MONGO_PASSWORD', 'panda')
    mongo_type = config.get('MONGO_TYPE', 'single')
    mongo_db = config.get('MONGO_DB', 'panda')
    
    print(f"  MongoDB URI: {mongo_uri}")
    print(f"  MongoDB 类型: {mongo_type}")
    print(f"  数据库名: {mongo_db}")
    print()
    
    print("[3/4] 测试连接...")
    
    # 尝试简单连接（无认证）
    try:
        client = MongoClient(f'mongodb://{mongo_uri}/', serverSelectionTimeoutMS=5000)
        # 测试连接
        client.admin.command('ping')
        print("✅ MongoDB连接成功（无认证）")
        
        # 列出数据库
        dbs = client.list_database_names()
        print(f"  可用数据库: {', '.join(dbs)}")
        
        client.close()
        connection_ok = True
    except Exception as e:
        print(f"⚠️  无认证连接失败: {e}")
        connection_ok = False
    
    # 尝试带认证的连接
    if not connection_ok:
        try:
            auth_uri = f'mongodb://{mongo_user}:{mongo_password}@{mongo_uri}/'
            client = MongoClient(auth_uri, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
            print("✅ MongoDB连接成功（带认证）")
            
            dbs = client.list_database_names()
            print(f"  可用数据库: {', '.join(dbs)}")
            
            client.close()
            connection_ok = True
        except Exception as e:
            print(f"❌ 带认证连接失败: {e}")
    
    print()
    print("[4/4] 测试数据库操作...")
    
    if connection_ok:
        try:
            # 重新连接
            client = MongoClient(f'mongodb://{mongo_uri}/', serverSelectionTimeoutMS=5000)
            db = client[mongo_db]
            
            # 测试写入
            test_collection = db['test_connection']
            result = test_collection.insert_one({'test': 'connection', 'timestamp': 'now'})
            print(f"✅ 写入测试成功，ID: {result.inserted_id}")
            
            # 测试读取
            doc = test_collection.find_one({'test': 'connection'})
            print(f"✅ 读取测试成功: {doc}")
            
            # 清理测试数据
            test_collection.delete_one({'_id': result.inserted_id})
            print("✅ 删除测试数据成功")
            
            client.close()
        except Exception as e:
            print(f"⚠️  数据库操作测试失败: {e}")
    
    print()
    print("=" * 70)
    
    if connection_ok:
        print("🎉 MongoDB运行正常！")
        print()
        print("服务可以正常使用MongoDB功能")
    else:
        print("⚠️  MongoDB连接有问题")
        print()
        print("建议:")
        print("1. 检查MongoDB服务是否运行")
        print("2. 检查配置文件中的连接信息")
        print("3. 尝试不使用认证连接")
    
    print("=" * 70)
    
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print()
    print("请安装pymongo:")
    print("  pip install pymongo")
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
