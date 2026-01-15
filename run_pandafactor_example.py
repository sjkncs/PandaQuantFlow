"""
PandaFactor 快速示例
演示如何使用PandaFactor编写和计算因子
"""

import sys
import os

# 添加项目路径
project_root = r"c:\Users\Lenovo\Desktop\PandaQuantFlow\panda_factor-main\panda_factor-main"
sys.path.insert(0, project_root)

# 同时添加我们自己的因子库路径
lightweight_path = r"c:\Users\Lenovo\Desktop\PandaQuantFlow\lightweight"
sys.path.insert(0, lightweight_path)

print("="*70)
print("PandaFactor 快速示例")
print("="*70)
print()

# ==================== 示例1: 使用我们的轻量级因子库 ====================
print("[示例 1/3] 使用轻量级因子库计算技术指标...")
print()

try:
    from factor_library import FactorLibrary
    import pandas as pd
    import numpy as np
    
    # 创建模拟市场数据
    dates = pd.date_range('2024-01-01', periods=100)
    np.random.seed(42)
    
    data = pd.DataFrame({
        'close': np.random.randn(100).cumsum() + 100,
        'open': np.random.randn(100).cumsum() + 100,
        'high': np.random.randn(100).cumsum() + 102,
        'low': np.random.randn(100).cumsum() + 98,
        'volume': np.random.randint(1000000, 10000000, 100)
    }, index=dates)
    
    print(f"数据范围: {data.index[0]} 至 {data.index[-1]}")
    print(f"数据条数: {len(data)}")
    print()
    
    # 计算各种技术指标
    close = FactorLibrary.CLOSE(data)
    volume = FactorLibrary.VOLUME(data)
    
    # 趋势指标
    ma5 = FactorLibrary.MA(close, 5)
    ma20 = FactorLibrary.MA(close, 20)
    ma60 = FactorLibrary.MA(close, 60)
    
    # 动量指标
    rsi14 = FactorLibrary.RSI(close, 14)
    roc10 = FactorLibrary.ROC(close, 10)
    
    # 波动率指标
    std20 = FactorLibrary.STD(close, 20)
    atr14 = FactorLibrary.ATR(data, 14)
    
    # MACD指标
    macd = FactorLibrary.MACD(close, 12, 26, 9)
    
    # 布林带
    boll_upper = FactorLibrary.BOLL_UPPER(close, 20, 2)
    boll_lower = FactorLibrary.BOLL_LOWER(close, 20, 2)
    
    # 量价相关性
    corr_pv = FactorLibrary.CORRELATION(close, volume, 20)
    
    print("✅ 技术指标计算完成:")
    print(f"   MA(5)   = {ma5.iloc[-1]:.2f}")
    print(f"   MA(20)  = {ma20.iloc[-1]:.2f}")
    print(f"   MA(60)  = {ma60.iloc[-1]:.2f}")
    print(f"   RSI(14) = {rsi14.iloc[-1]:.2f}")
    print(f"   ROC(10) = {roc10.iloc[-1]:.2f}%")
    print(f"   STD(20) = {std20.iloc[-1]:.2f}")
    print(f"   ATR(14) = {atr14.iloc[-1]:.2f}")
    print(f"   MACD    = {macd.iloc[-1]:.4f}")
    print(f"   布林上轨 = {boll_upper.iloc[-1]:.2f}")
    print(f"   布林下轨 = {boll_lower.iloc[-1]:.2f}")
    print(f"   量价相关 = {corr_pv.iloc[-1]:.4f}")
    
except Exception as e:
    print(f"❌ 示例1失败: {e}")
    import traceback
    traceback.print_exc()

print()
print("-"*70)
print()

# ==================== 示例2: 编写自定义因子 (Python方式) ====================
print("[示例 2/3] 编写自定义复合因子...")
print()

try:
    # 自定义因子类
    class MyMomentumFactor:
        """
        动量复合因子
        结合价格动量、成交量和波动率
        """
        
        @staticmethod
        def calculate(data):
            close = data['close']
            volume = data['volume']
            high = data['high']
            low = data['low']
            
            # 1. 计算20日收益率
            returns_20 = (close / close.shift(20) - 1) * 100
            
            # 2. 计算20日波动率
            returns_1 = close.pct_change()
            volatility_20 = returns_1.rolling(20).std() * 100
            
            # 3. 计算价格区间
            price_range = (high - low) / close * 100
            
            # 4. 计算成交量比率
            volume_ratio = volume / volume.shift(1)
            volume_ma20 = volume.rolling(20).mean()
            
            # 5. 计算动量信号
            momentum_rank = returns_20.rank(pct=True)
            
            # 6. 计算波动率信号
            vol_signal = (volatility_20 > volatility_20.shift(1)).astype(int) * 2 - 1
            
            # 7. 标准化成交量比率
            vol_ratio_scaled = (volume_ratio / volume_ma20 - 1) * 100
            vol_ratio_scaled = (vol_ratio_scaled - vol_ratio_scaled.mean()) / vol_ratio_scaled.std()
            
            # 8. 合成最终因子
            factor = momentum_rank * vol_signal * vol_ratio_scaled
            
            return factor
    
    # 计算因子
    my_factor = MyMomentumFactor.calculate(data)
    
    print("✅ 自定义因子计算完成:")
    print(f"   因子名称: 动量复合因子")
    print(f"   因子值范围: [{my_factor.min():.4f}, {my_factor.max():.4f}]")
    print(f"   因子均值: {my_factor.mean():.4f}")
    print(f"   因子标准差: {my_factor.std():.4f}")
    print(f"   最新因子值: {my_factor.iloc[-1]:.4f}")
    
    # 计算因子与未来收益的相关性
    future_returns = (close.shift(-5) / close - 1).fillna(0)
    ic = my_factor[:-5].corr(future_returns[:-5])
    print(f"   因子IC (5日): {ic:.4f}")
    
except Exception as e:
    print(f"❌ 示例2失败: {e}")
    import traceback
    traceback.print_exc()

print()
print("-"*70)
print()

# ==================== 示例3: 公式方式计算因子 ====================
print("[示例 3/3] 使用公式方式计算因子...")
print()

try:
    # 公式1: 简单动量因子
    formula1 = "20日收益率排名"
    returns_20 = (close / close.shift(20) - 1)
    factor1 = returns_20.rank(pct=True)
    
    print(f"✅ 公式因子1: {formula1}")
    print(f"   最新值: {factor1.iloc[-1]:.4f}")
    
    # 公式2: 价格-成交量相关性
    formula2 = "20日价格成交量相关性"
    factor2 = close.rolling(20).corr(volume)
    
    print(f"✅ 公式因子2: {formula2}")
    print(f"   最新值: {factor2.iloc[-1]:.4f}")
    
    # 公式3: 复合因子
    formula3 = "动量 × 波动率 × 趋势"
    momentum = returns_20.rank(pct=True)
    volatility = returns_1.rolling(20).std()
    vol_signal = (volatility > volatility.shift(1)).astype(int) * 2 - 1
    factor3 = momentum * vol_signal
    
    print(f"✅ 公式因子3: {formula3}")
    print(f"   最新值: {factor3.iloc[-1]:.4f}")
    
except Exception as e:
    print(f"❌ 示例3失败: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*70)
print("🎉 所有示例运行完成！")
print("="*70)
print()

# ==================== 下一步提示 ====================
print("📝 下一步:")
print()
print("1. 🔧 配置PandaFactor完整环境:")
print("   - 运行: setup_pandafactor.bat")
print("   - 或手动配置各子模块")
print()
print("2. 📊 连接真实数据源:")
print("   - 配置Tushare/RiceQuant等数据源")
print("   - 下载历史数据")
print()
print("3. 🚀 启动PandaFactor服务:")
print("   - 启动MongoDB")
print("   - 启动Web服务器")
print("   - 启动数据自动更新")
print()
print("4. 💡 编写更多因子:")
print("   - 参考Alpha#101/Alpha#191")
print("   - 结合自监督学习优化")
print("   - 回测验证效果")
print()
print("5. 📚 查看完整文档:")
print("   - PANDAFACTOR_SETUP_GUIDE.md")
print("   - FACTOR_LIBRARY_README.md")
print()
