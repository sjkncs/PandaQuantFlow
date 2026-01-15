"""
添加示例因子到数据库
"""

import sys
import os
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, "panda_common"))

print("=" * 70)
print("添加示例因子")
print("=" * 70)
print()

try:
    from pymongo import MongoClient
    from panda_common.config import config
    
    # 连接MongoDB
    mongo_uri = config.get('MONGO_URI', '127.0.0.1:27017')
    client = MongoClient(f'mongodb://{mongo_uri}/')
    db = client['panda']
    collection = db['user_factors']
    
    print("[1/3] 连接MongoDB...")
    print(f"✅ 已连接到 {mongo_uri}")
    print()
    
    # 检查现有因子
    print("[2/3] 检查现有因子...")
    existing_count = collection.count_documents({})
    print(f"当前因子数量: {existing_count}")
    print()
    
    # 添加示例因子
    print("[3/3] 添加示例因子...")
    
    sample_factors = [
        {
            "user_id": "0",
            "factor_name": "MA20",
            "factor_code": "# 20日移动平均线\nclose.rolling(20).mean()",
            "factor_desc": "20日移动平均线，用于判断趋势",
            "status": "completed",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "return_ratio": 0.15,
            "sharpe_ratio": 1.2,
            "maximum_drawdown": -0.08,
            "IC": 0.05,
            "IR": 0.8
        },
        {
            "user_id": "0",
            "factor_name": "RSI14",
            "factor_code": "# 14日相对强弱指标\n# RSI计算\ndelta = close.diff()\ngain = delta.where(delta > 0, 0)\nloss = -delta.where(delta < 0, 0)\navg_gain = gain.rolling(14).mean()\navg_loss = loss.rolling(14).mean()\nrs = avg_gain / avg_loss\nrsi = 100 - (100 / (1 + rs))\nrsi",
            "factor_desc": "相对强弱指标，用于判断超买超卖",
            "status": "completed",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "return_ratio": 0.12,
            "sharpe_ratio": 1.0,
            "maximum_drawdown": -0.10,
            "IC": 0.04,
            "IR": 0.7
        },
        {
            "user_id": "0",
            "factor_name": "MACD",
            "factor_code": "# MACD指标\nema12 = close.ewm(span=12).mean()\nema26 = close.ewm(span=26).mean()\nmacd = ema12 - ema26\nmacd",
            "factor_desc": "移动平均收敛散度指标",
            "status": "completed",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "return_ratio": 0.18,
            "sharpe_ratio": 1.5,
            "maximum_drawdown": -0.06,
            "IC": 0.06,
            "IR": 0.9
        },
        {
            "user_id": "0",
            "factor_name": "成交量比率",
            "factor_code": "# 成交量比率\nvolume / volume.rolling(20).mean()",
            "factor_desc": "当日成交量与20日平均成交量的比率",
            "status": "completed",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "return_ratio": 0.10,
            "sharpe_ratio": 0.8,
            "maximum_drawdown": -0.12,
            "IC": 0.03,
            "IR": 0.6
        },
        {
            "user_id": "0",
            "factor_name": "布林带宽度",
            "factor_code": "# 布林带宽度\nma = close.rolling(20).mean()\nstd = close.rolling(20).std()\nupper = ma + 2 * std\nlower = ma - 2 * std\nwidth = (upper - lower) / ma\nwidth",
            "factor_desc": "布林带宽度，衡量波动率",
            "status": "completed",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "return_ratio": 0.14,
            "sharpe_ratio": 1.1,
            "maximum_drawdown": -0.09,
            "IC": 0.045,
            "IR": 0.75
        }
    ]
    
    inserted_count = 0
    for factor in sample_factors:
        # 检查是否已存在
        existing = collection.find_one({
            "user_id": factor["user_id"],
            "factor_name": factor["factor_name"]
        })
        
        if not existing:
            result = collection.insert_one(factor)
            print(f"  ✅ 添加因子: {factor['factor_name']}")
            inserted_count += 1
        else:
            print(f"  ⚠️  因子已存在: {factor['factor_name']}")
    
    print()
    print("=" * 70)
    print(f"🎉 完成！添加了 {inserted_count} 个新因子")
    print(f"总因子数: {collection.count_documents({})}")
    print()
    print("现在刷新因子界面，您应该能看到这些示例因子了！")
    print("访问: http://127.0.0.1:8111/factor")
    print("=" * 70)
    
    client.close()
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
