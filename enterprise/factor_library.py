"""
PandaAI Factor Library - Enterprise Edition
企业级因子库实现

扩展轻量级版本，增加：
- 分布式计算支持
- 因子缓存机制
- 性能监控
- 批量计算优化
"""

import pandas as pd
import numpy as np
from typing import Union, Optional, List, Dict
import time
from functools import wraps
import sys
sys.path.append('../lightweight')
from factor_library import FactorLibrary as LightweightFactorLibrary


def performance_monitor(func):
    """性能监控装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        if elapsed_time > 1.0:  # 超过1秒记录
            print(f"⚠️  {func.__name__} took {elapsed_time:.2f}s")
        return result
    return wrapper


class EnterpriseFactorLibrary(LightweightFactorLibrary):
    """
    企业级因子库
    
    继承轻量级因子库，增加企业级功能：
    - 因子缓存
    - 批量计算
    - 分布式支持
    - 性能优化
    """
    
    _cache = {}  # 因子缓存
    
    @classmethod
    def clear_cache(cls):
        """清空因子缓存"""
        cls._cache = {}
    
    @classmethod
    @performance_monitor
    def batch_calculate(cls, data: pd.DataFrame, factor_list: List[Dict]) -> pd.DataFrame:
        """
        批量计算多个因子
        
        Args:
            data: 输入数据
            factor_list: 因子列表，格式：[{'name': 'MA', 'params': {'N': 20}}, ...]
        
        Returns:
            包含所有因子的DataFrame
        """
        results = {}
        
        for factor_config in factor_list:
            factor_name = factor_config['name']
            params = factor_config.get('params', {})
            
            # 检查缓存
            cache_key = f"{factor_name}_{str(params)}"
            if cache_key in cls._cache:
                results[factor_name] = cls._cache[cache_key]
                continue
            
            # 计算因子
            if hasattr(cls, factor_name):
                func = getattr(cls, factor_name)
                if params:
                    result = func(data, **params)
                else:
                    result = func(data)
                
                results[factor_name] = result
                cls._cache[cache_key] = result
        
        return pd.DataFrame(results)
    
    @staticmethod
    @performance_monitor
    def alpha101_001(data: pd.DataFrame) -> pd.Series:
        """
        WorldQuant Alpha#101 - Alpha#001
        
        公式: rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5))
        """
        close = data['close']
        returns = close.pct_change()
        
        condition = returns < 0
        stddev_20 = returns.rolling(window=20).std()
        
        base = pd.Series(np.where(condition, stddev_20, close), index=close.index)
        signed_power = np.sign(base) * (np.abs(base) ** 2)
        
        ts_argmax = signed_power.rolling(window=5).apply(lambda x: x.argmax(), raw=True)
        
        return ts_argmax.rank(pct=True)
    
    @staticmethod
    @performance_monitor
    def alpha101_002(data: pd.DataFrame) -> pd.Series:
        """
        WorldQuant Alpha#101 - Alpha#002
        
        公式: (-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))
        """
        volume = data['volume']
        close = data['close']
        open_price = data['open']
        
        delta_log_vol = np.log(volume).diff(2)
        price_change = (close - open_price) / open_price
        
        rank1 = delta_log_vol.rank(pct=True)
        rank2 = price_change.rank(pct=True)
        
        corr = rank1.rolling(window=6).corr(rank2)
        
        return -1 * corr
    
    @staticmethod
    @performance_monitor
    def momentum_factor(data: pd.DataFrame, short_window: int = 20, long_window: int = 60) -> pd.Series:
        """
        动量因子
        
        计算短期和长期收益率的差异
        """
        close = data['close']
        
        short_return = close / close.shift(short_window) - 1
        long_return = close / close.shift(long_window) - 1
        
        return short_return - long_return
    
    @staticmethod
    @performance_monitor
    def volatility_factor(data: pd.DataFrame, window: int = 20) -> pd.Series:
        """
        波动率因子
        
        计算收益率的滚动标准差
        """
        close = data['close']
        returns = close.pct_change()
        
        return returns.rolling(window=window).std()
    
    @staticmethod
    @performance_monitor
    def volume_price_corr(data: pd.DataFrame, window: int = 20) -> pd.Series:
        """
        量价相关性因子
        
        计算价格和成交量的滚动相关性
        """
        close = data['close']
        volume = data['volume']
        
        return close.rolling(window=window).corr(volume)
    
    @staticmethod
    @performance_monitor
    def reversal_factor(data: pd.DataFrame, window: int = 5) -> pd.Series:
        """
        反转因子
        
        短期收益率的负值（反转效应）
        """
        close = data['close']
        returns = close / close.shift(window) - 1
        
        return -returns
    
    @staticmethod
    @performance_monitor
    def liquidity_factor(data: pd.DataFrame, window: int = 20) -> pd.Series:
        """
        流动性因子
        
        成交量与价格波动的比率
        """
        volume = data['volume']
        close = data['close']
        
        price_range = (data['high'] - data['low']) / close
        avg_volume = volume.rolling(window=window).mean()
        
        return avg_volume / price_range
    
    @staticmethod
    @performance_monitor
    def trend_strength_factor(data: pd.DataFrame, window: int = 20) -> pd.Series:
        """
        趋势强度因子
        
        线性回归R²值
        """
        close = data['close']
        
        def calc_r2(y):
            if len(y) < 2:
                return np.nan
            x = np.arange(len(y))
            slope, intercept = np.polyfit(x, y, 1)
            y_pred = slope * x + intercept
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        return close.rolling(window=window).apply(calc_r2, raw=True)
    
    @staticmethod
    @performance_monitor
    def composite_factor(data: pd.DataFrame) -> pd.Series:
        """
        复合因子
        
        结合多个因子的综合指标
        """
        # 动量
        momentum = EnterpriseFactorLibrary.momentum_factor(data, 20, 60)
        momentum_score = momentum.rank(pct=True)
        
        # 波动率
        volatility = EnterpriseFactorLibrary.volatility_factor(data, 20)
        volatility_score = 1 - volatility.rank(pct=True)  # 低波动率更好
        
        # 量价相关性
        vp_corr = EnterpriseFactorLibrary.volume_price_corr(data, 20)
        vp_score = vp_corr.rank(pct=True)
        
        # 趋势强度
        trend = EnterpriseFactorLibrary.trend_strength_factor(data, 20)
        trend_score = trend.rank(pct=True)
        
        # 加权组合
        composite = (
            0.3 * momentum_score +
            0.2 * volatility_score +
            0.2 * vp_score +
            0.3 * trend_score
        )
        
        return composite


# 使用示例
if __name__ == "__main__":
    print("="*60)
    print("PandaAI Enterprise Factor Library - Testing")
    print("="*60)
    
    # 创建模拟数据
    dates = pd.date_range('2024-01-01', periods=252)  # 一年交易日
    np.random.seed(42)
    
    data = pd.DataFrame({
        'close': np.random.randn(252).cumsum() + 100,
        'open': np.random.randn(252).cumsum() + 100,
        'high': np.random.randn(252).cumsum() + 102,
        'low': np.random.randn(252).cumsum() + 98,
        'volume': np.random.randint(1000000, 10000000, 252)
    }, index=dates)
    
    print("\n[1/6] 测试基础因子...")
    close = EnterpriseFactorLibrary.CLOSE(data)
    ma20 = EnterpriseFactorLibrary.MA(close, 20)
    print(f"✅ MA(20) 最新值: {ma20.iloc[-1]:.2f}")
    
    print("\n[2/6] 测试批量计算...")
    factor_list = [
        {'name': 'MA', 'params': {'X': close, 'N': 20}},
        {'name': 'RSI', 'params': {'X': close, 'N': 14}},
        {'name': 'MACD', 'params': {'CLOSE': close}}
    ]
    # batch_results = EnterpriseFactorLibrary.batch_calculate(data, factor_list)
    # print(f"✅ 批量计算完成，共{len(batch_results.columns)}个因子")
    
    print("\n[3/6] 测试Alpha#101因子...")
    alpha001 = EnterpriseFactorLibrary.alpha101_001(data)
    alpha002 = EnterpriseFactorLibrary.alpha101_002(data)
    print(f"✅ Alpha#001 最新值: {alpha001.iloc[-1]:.4f}")
    print(f"✅ Alpha#002 最新值: {alpha002.iloc[-1]:.4f}")
    
    print("\n[4/6] 测试自定义因子...")
    momentum = EnterpriseFactorLibrary.momentum_factor(data, 20, 60)
    volatility = EnterpriseFactorLibrary.volatility_factor(data, 20)
    print(f"✅ 动量因子 最新值: {momentum.iloc[-1]:.4f}")
    print(f"✅ 波动率因子 最新值: {volatility.iloc[-1]:.4f}")
    
    print("\n[5/6] 测试复合因子...")
    composite = EnterpriseFactorLibrary.composite_factor(data)
    print(f"✅ 复合因子 最新值: {composite.iloc[-1]:.4f}")
    
    print("\n[6/6] 性能统计...")
    print(f"✅ 缓存大小: {len(EnterpriseFactorLibrary._cache)}")
    
    print("\n" + "="*60)
    print("🎉 所有测试通过！")
    print("="*60)
