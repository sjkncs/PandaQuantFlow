#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自动修复因子用户ID问题（无需确认）
将用户ID从0改为1
"""

from panda_common.handlers.database_handler import DatabaseHandler
from panda_common.config import config
from datetime import datetime

def fix_user_id_auto():
    """自动修复用户ID"""
    
    print("=" * 60)
    print("🔧 自动修复因子用户ID")
    print("=" * 60)
    print()
    
    db_handler = DatabaseHandler(config)
    
    # 1. 查看当前状态
    print("📋 步骤1: 查看当前因子状态...")
    
    factors_with_zero = db_handler.mongo_find("panda", "user_factors", {"user_id": "0"})
    factors_with_one = db_handler.mongo_find("panda", "user_factors", {"user_id": "1"})
    
    print(f"  用户ID为0的因子: {len(factors_with_zero)} 个")
    print(f"  用户ID为1的因子: {len(factors_with_one)} 个")
    print()
    
    if len(factors_with_zero) == 0:
        print("✅ 没有需要修复的因子（用户ID都不为0）")
        print()
        print("=" * 60)
        return
    
    # 2. 显示需要修复的因子
    print("📋 步骤2: 需要修复的因子列表...")
    print("-" * 60)
    
    for i, factor in enumerate(factors_with_zero, 1):
        print(f"{i}. {factor.get('factor_name', '未命名')}")
        print(f"   ID: {factor.get('_id')}")
        print(f"   当前用户ID: {factor.get('user_id')}")
    
    print("-" * 60)
    print()
    
    # 3. 自动执行修复
    print("📋 步骤3: 自动执行修复...")
    
    try:
        result = db_handler.mongo_client["panda"]["user_factors"].update_many(
            {"user_id": "0"},
            {
                "$set": {
                    "user_id": "1",
                    "updated_at": datetime.now().isoformat()
                }
            }
        )
        
        print(f"✅ 成功更新 {result.modified_count} 个因子的用户ID")
        print()
        
        # 4. 验证修复结果
        print("📋 步骤4: 验证修复结果...")
        
        factors_with_zero_after = db_handler.mongo_find("panda", "user_factors", {"user_id": "0"})
        factors_with_one_after = db_handler.mongo_find("panda", "user_factors", {"user_id": "1"})
        
        print(f"  修复后用户ID为0的因子: {len(factors_with_zero_after)} 个")
        print(f"  修复后用户ID为1的因子: {len(factors_with_one_after)} 个")
        print()
        
        if len(factors_with_zero_after) == 0:
            print("✅ 修复成功！所有因子的用户ID都已更新为1")
        else:
            print("⚠️  仍有部分因子的用户ID为0")
        
    except Exception as e:
        print(f"❌ 修复失败: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)
    print("✅ 修复完成！")
    print()
    print("💡 下一步:")
    print("   1. 刷新浏览器页面: http://127.0.0.1:8111/factor/")
    print("   2. 尝试运行因子")
    print("   3. 如果还有问题，请查看 FACTOR_ERROR_SOLUTION.md")
    print("=" * 60)

if __name__ == "__main__":
    try:
        fix_user_id_auto()
    except Exception as e:
        print(f"❌ 执行过程出错: {e}")
        import traceback
        traceback.print_exc()
