#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
诊断因子运行错误
"""

from panda_common.handlers.database_handler import DatabaseHandler
from panda_common.config import config
import panda_data

def diagnose_error():
    """诊断因子运行错误"""
    
    print("=" * 60)
    print("🔍 诊断因子运行错误")
    print("=" * 60)
    print()
    
    db_handler = DatabaseHandler(config)
    
    # 1. 检查因子数据
    print("📋 步骤1: 检查因子数据...")
    factors = db_handler.mongo_find("panda", "user_factors", {})
    
    if not factors or len(factors) == 0:
        print("❌ 未找到任何因子！")
        return
    
    print(f"✅ 找到 {len(factors)} 个因子")
    
    # 选择第一个因子进行测试
    test_factor = factors[0]
    factor_id = str(test_factor.get("_id"))
    user_id = test_factor.get("user_id")
    factor_name = test_factor.get("factor_name")
    
    print(f"\n测试因子:")
    print(f"  ID: {factor_id}")
    print(f"  名称: {factor_name}")
    print(f"  用户ID: {user_id}")
    print()
    
    # 2. 初始化panda_data
    print("📋 步骤2: 初始化panda_data...")
    try:
        panda_data.init()
        print("✅ panda_data初始化成功")
    except Exception as e:
        print(f"❌ panda_data初始化失败: {e}")
        return
    print()
    
    # 3. 测试获取因子数据
    print("📋 步骤3: 测试获取因子数据...")
    print(f"  调用: panda_data.get_custom_factor(")
    print(f"    user_id={user_id},")
    print(f"    factor_name='{factor_name}',")
    print(f"    start_date='20200101',")
    print(f"    end_date='20201231'")
    print(f"  )")
    print()
    
    try:
        # 尝试获取因子数据
        df = panda_data.get_custom_factor(
            factor_logger=None,
            user_id=int(user_id),
            factor_name=factor_name,
            start_date="20200101",
            end_date="20201231"
        )
        
        print(f"✅ 成功获取因子数据")
        print(f"  数据形状: {df.shape}")
        print(f"  列名: {list(df.columns)}")
        
        if not df.empty:
            print(f"\n前5行数据:")
            print(df.head())
        else:
            print("⚠️  数据为空！")
            
    except Exception as e:
        print(f"❌ 获取因子数据失败!")
        print(f"  错误类型: {type(e).__name__}")
        print(f"  错误信息: {str(e)}")
        
        # 检查是否是"没有本项目"错误
        if "没有本项目" in str(e) or "no project" in str(e).lower():
            print()
            print("🔍 检测到'没有本项目'错误！")
            print()
            print("💡 可能的原因:")
            print("  1. panda_data中没有为该用户创建项目")
            print("  2. 用户ID不正确")
            print("  3. 因子名称不存在")
            print()
            print("🔧 解决方案:")
            print("  方案1: 在panda_data中创建项目")
            print("  方案2: 修改因子代码，使用正确的用户ID")
            print("  方案3: 检查因子定义是否正确")
            print()
            
            # 尝试查找项目信息
            print("📋 检查项目信息...")
            try:
                # 检查panda_data中的项目
                from panda_data import get_user_projects
                projects = get_user_projects(int(user_id))
                
                if projects:
                    print(f"✅ 找到 {len(projects)} 个项目:")
                    for proj in projects:
                        print(f"  - {proj}")
                else:
                    print("❌ 该用户没有项目！")
                    print()
                    print("🔧 创建项目的方法:")
                    print("  1. 使用panda_data的管理界面创建项目")
                    print("  2. 或者修改用户ID为已有项目的用户")
                    
            except Exception as e2:
                print(f"⚠️  无法检查项目信息: {e2}")
        
        print()
        print("完整错误堆栈:")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)
    print("诊断完成")
    print("=" * 60)

if __name__ == "__main__":
    try:
        diagnose_error()
    except Exception as e:
        print(f"❌ 诊断过程出错: {e}")
        import traceback
        traceback.print_exc()
