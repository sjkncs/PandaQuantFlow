#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复因子运行问题 - 添加示例因子和项目数据
"""

from panda_common.handlers.database_handler import DatabaseHandler
from panda_common.config import config
from datetime import datetime
from bson import ObjectId

def fix_factor_issue():
    """修复因子运行问题"""
    
    print("=" * 60)
    print("🔧 修复因子运行问题")
    print("=" * 60)
    print()
    
    db_handler = DatabaseHandler(config)
    
    # 1. 检查并添加示例项目
    print("📋 步骤1: 检查项目数据...")
    
    # 查找所有用户因子
    factors = db_handler.mongo_find("panda", "user_factors", {})
    
    if not factors or len(factors) == 0:
        print("⚠️  未找到任何因子，创建示例因子...")
        
        # 创建示例因子
        sample_factor = {
            "user_id": "1",
            "factor_name": "示例动量因子",
            "factor_code": """class MomentumFactor(Factor):
    def calculate(self, context, factor):
        # 计算20日收益率
        returns = RETURN(close, period=20)
        return returns""",
            "description": "基于20日收益率的动量因子",
            "status": 0,  # 0: 未运行, 1: 运行中, 2: 已完成
            "params": {
                "start_date": "2020-01-01",
                "end_date": "2023-12-31",
                "benchmark": "000300.SH",
                "quantiles": 5,
                "periods": [1, 5, 10],
                "filter_extremum": True,
                "long_short": False,
                "group_adjust": False,
                "equal_weight": True,
                "max_loss": 0.25
            },
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "result": None
        }
        
        result = db_handler.mongo_insert("panda", "user_factors", sample_factor)
        print(f"✅ 已创建示例因子，ID: {result.inserted_id}")
        
        # 获取新创建的因子
        factors = [db_handler.mongo_find_one("panda", "user_factors", {"_id": result.inserted_id})]
    else:
        print(f"✅ 找到 {len(factors)} 个因子")
    
    print()
    
    # 2. 检查并创建项目数据（如果需要）
    print("📋 步骤2: 检查项目配置...")
    
    # 检查是否有项目配置集合
    try:
        # 尝试查找项目配置
        projects = db_handler.mongo_find("panda", "projects", {})
        
        if not projects or len(projects) == 0:
            print("⚠️  未找到项目配置，创建默认项目...")
            
            # 为每个用户创建项目
            user_ids = set([f.get("user_id") for f in factors if f.get("user_id")])
            
            for user_id in user_ids:
                project = {
                    "user_id": user_id,
                    "project_name": f"用户{user_id}的默认项目",
                    "description": "自动创建的默认项目",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "status": 1  # 激活状态
                }
                
                result = db_handler.mongo_insert("panda", "projects", project)
                print(f"✅ 为用户 {user_id} 创建项目，ID: {result.inserted_id}")
        else:
            print(f"✅ 找到 {len(projects)} 个项目配置")
    except Exception as e:
        print(f"⚠️  项目配置检查出错（可能不需要）: {e}")
    
    print()
    
    # 3. 更新因子状态
    print("📋 步骤3: 重置因子状态...")
    
    # 将所有运行中的因子状态重置为未运行
    result = db_handler.mongo_client["panda"]["user_factors"].update_many(
        {"status": 1},  # 运行中
        {"$set": {
            "status": 0,  # 重置为未运行
            "updated_at": datetime.now().isoformat(),
            "current_task_id": None
        }}
    )
    
    if result.modified_count > 0:
        print(f"✅ 重置了 {result.modified_count} 个运行中的因子")
    else:
        print("✅ 没有需要重置的因子")
    
    print()
    
    # 4. 显示当前因子列表
    print("📋 步骤4: 当前因子列表")
    print("-" * 60)
    
    factors = db_handler.mongo_find("panda", "user_factors", {})
    
    for i, factor in enumerate(factors, 1):
        status_map = {0: "未运行", 1: "运行中", 2: "已完成", 3: "失败"}
        status = status_map.get(factor.get("status", 0), "未知")
        
        print(f"{i}. {factor.get('factor_name', '未命名')}")
        print(f"   ID: {factor.get('_id')}")
        print(f"   用户: {factor.get('user_id')}")
        print(f"   状态: {status}")
        print(f"   创建时间: {factor.get('created_at', 'N/A')}")
        print()
    
    print("=" * 60)
    print("✅ 修复完成！")
    print()
    print("💡 下一步:")
    print("   1. 刷新浏览器页面")
    print("   2. 尝试运行因子")
    print("   3. 如果还有问题，请检查因子代码是否正确")
    print("=" * 60)

if __name__ == "__main__":
    try:
        fix_factor_issue()
    except Exception as e:
        print(f"❌ 修复过程出错: {e}")
        import traceback
        traceback.print_exc()
