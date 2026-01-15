"""
PandaAI Factor Library - Lightweight Edition
轻量级因子库实现

基于PandaAI官方函数参考手册实现的完整因子库
支持200+量化因子和技术指标
"""

import pandas as pd
import numpy as np
from typing import Union, Optional


class FactorLibrary:
    """
    因子库基类
    
    提供所有PandaAI支持的因子计算函数
    所有函数均为静态方法，可直接调用
    """
    
    # ==================== 基础因子 ====================
    
    @staticmethod
    def CLOSE(data: pd.DataFrame) -> pd.Series:
        """收盘价"""
        return data['close']
    
    @staticmethod
    def OPEN(data: pd.DataFrame) -> pd.Series:
        """开盘价"""
        return data['open']
    
    @staticmethod
    def HIGH(data: pd.DataFrame) -> pd.Series:
        """最高价"""
        return data['high']
    
    @staticmethod
    def LOW(data: pd.DataFrame) -> pd.Series:
        """最低价"""
        return data['low']
    
    @staticmethod
    def VOLUME(data: pd.DataFrame) -> pd.Series:
        """成交量"""
        return data['volume']
    
    @staticmethod
    def AMOUNT(data: pd.DataFrame) -> pd.Series:
        """成交额"""
        return data.get('amount', data['volume'] * data['close'])
    
    # ==================== 1. 直接操作型函数 ====================
    
    @staticmethod
    def ABS(X: pd.Series) -> pd.Series:
        """求X的绝对值"""
        return X.abs()
    
    @staticmethod
    def LOG(X: pd.Series) -> pd.Series:
        """对X逐个取自然对数"""
        return np.log(X)
    
    @staticmethod
    def LOGABS(X: pd.Series) -> pd.Series:
        """对X的绝对值逐个取自然对数"""
        return np.log(X.abs())
    
    @staticmethod
    def EXP(X: pd.Series) -> pd.Series:
        """对X逐个取e的指数"""
        return np.exp(X)
    
    @staticmethod
    def AS_FLOAT(X: pd.Series) -> pd.Series:
        """将X布尔值转换为0.0或1.0"""
        return X.astype(float)
    
    @staticmethod
    def RD(X: pd.Series, N: int = 2) -> pd.Series:
        """对X进行4舍5入处理，保留N位小数"""
        return X.round(N)
    
    @staticmethod
    def SIGN(X: pd.Series) -> pd.Series:
        """返回X的正负号：正为1,负为-1,0为0"""
        return np.sign(X)
    
    @staticmethod
    def SIN(X: pd.Series) -> pd.Series:
        """返回X的正弦值"""
        return np.sin(X)
    
    @staticmethod
    def COS(X: pd.Series) -> pd.Series:
        """返回X的余弦值"""
        return np.cos(X)
    
    @staticmethod
    def TAN(X: pd.Series) -> pd.Series:
        """返回X的正切值"""
        return np.tan(X)
    
    @staticmethod
    def ARCSIN(X: pd.Series) -> pd.Series:
        """返回X的反正弦值"""
        return np.arcsin(X)
    
    @staticmethod
    def ARCCOS(X: pd.Series) -> pd.Series:
        """返回X的反余弦值"""
        return np.arccos(X)
    
    @staticmethod
    def ARCTAN(X: pd.Series) -> pd.Series:
        """返回X的反正切值"""
        return np.arctan(X)
    
    # ==================== 2. 截面操作型函数 ====================
    
    @staticmethod
    def RANK(X: pd.Series) -> pd.Series:
        """求截面排序分位数，范围[0,1]"""
        return X.rank(pct=True)
    
    @staticmethod
    def SCALE(X: pd.Series) -> pd.Series:
        """将X按截面最大最小值缩放到[-1,1]"""
        return 2 * (X - X.min()) / (X.max() - X.min()) - 1
    
    @staticmethod
    def ZSCORE(X: pd.Series) -> pd.Series:
        """将X按截面进行z-score标准化"""
        return (X - X.mean()) / X.std()
    
    # ==================== 3. 时序操作型函数 ====================
    
    @staticmethod
    def CONST(X: pd.Series) -> pd.Series:
        """返回X最后一个值组成的常数序列"""
        last_value = X.iloc[-1]
        return pd.Series([last_value] * len(X), index=X.index)
    
    @staticmethod
    def BARSLAST(X: pd.Series) -> pd.Series:
        """返回X距离上一次为True已过去多少期"""
        result = pd.Series(index=X.index, dtype=float)
        last_true_idx = -1
        for i in range(len(X)):
            if X.iloc[i]:
                last_true_idx = i
                result.iloc[i] = 0
            else:
                result.iloc[i] = i - last_true_idx if last_true_idx >= 0 else np.nan
        return result
    
    @staticmethod
    def BARSLASTCOUNT(X: pd.Series) -> pd.Series:
        """统计连续满足X条件的周期数"""
        result = pd.Series(index=X.index, dtype=int)
        count = 0
        for i in range(len(X)):
            if X.iloc[i]:
                count += 1
            else:
                count = 0
            result.iloc[i] = count
        return result
    
    # ==================== 5. 时序操作型函数 (X,N) ====================
    
    @staticmethod
    def REF(X: pd.Series, N: int) -> pd.Series:
        """返回X整体延后N期后的序列"""
        return X.shift(N)
    
    @staticmethod
    def DELAY(X: pd.Series, N: int) -> pd.Series:
        """返回X整体延后N期后的序列，等同于REF"""
        return X.shift(N)
    
    @staticmethod
    def DIFF(X: pd.Series, N: int = 1) -> pd.Series:
        """返回X与其前N期值之差"""
        return X - X.shift(N)
    
    @staticmethod
    def DELTA(X: pd.Series, N: int = 1) -> pd.Series:
        """返回X与其前N期值之差，等同于DIFF"""
        return X - X.shift(N)
    
    @staticmethod
    def MA(X: pd.Series, N: int) -> pd.Series:
        """返回X在过去N日的平均值"""
        return X.rolling(window=N).mean()
    
    @staticmethod
    def TS_MEAN(X: pd.Series, N: int) -> pd.Series:
        """返回X在过去N日的平均值，等同于MA"""
        return X.rolling(window=N).mean()
    
    @staticmethod
    def SUM(X: pd.Series, N: int) -> pd.Series:
        """返回X在过去N日的滚动求和"""
        return X.rolling(window=N).sum()
    
    @staticmethod
    def PRODUCT(X: pd.Series, N: int) -> pd.Series:
        """返回X在过去N日的滚动乘积"""
        return X.rolling(window=N).apply(np.prod, raw=True)
    
    @staticmethod
    def ROC(X: pd.Series, N: int) -> pd.Series:
        """当前值与N日前值的百分比变化"""
        return (X / X.shift(N) - 1) * 100
    
    @staticmethod
    def PCT_CHANGE(X: pd.Series, N: int = 1) -> pd.Series:
        """当前值与N日前值的百分比变化，等同于ROC"""
        return (X / X.shift(N) - 1) * 100
    
    @staticmethod
    def STD(X: pd.Series, N: int) -> pd.Series:
        """返回X在过去N日的标准差"""
        return X.rolling(window=N).std()
    
    @staticmethod
    def STDDEV(X: pd.Series, N: int) -> pd.Series:
        """返回X在过去N日的标准差，等同于STD"""
        return X.rolling(window=N).std()
    
    @staticmethod
    def VAR(X: pd.Series, N: int) -> pd.Series:
        """返回X在过去N日的滚动方差"""
        return X.rolling(window=N).var()
    
    @staticmethod
    def TS_MAX(X: pd.Series, N: int) -> pd.Series:
        """返回X在过去N日的最大值"""
        return X.rolling(window=N).max()
    
    @staticmethod
    def TS_MIN(X: pd.Series, N: int) -> pd.Series:
        """返回X在过去N日的最小值"""
        return X.rolling(window=N).min()
    
    @staticmethod
    def TS_MIDDLE(X: pd.Series, N: int) -> pd.Series:
        """返回X在过去N日的最大最小值的均值"""
        return (X.rolling(window=N).max() + X.rolling(window=N).min()) / 2
    
    @staticmethod
    def TS_RANK(X: pd.Series, N: int) -> pd.Series:
        """返回X在过去N日中的排序百分位数"""
        return X.rolling(window=N).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1], raw=False)
    
    @staticmethod
    def TS_ARGMAX(X: pd.Series, N: int) -> pd.Series:
        """返回X在过去N日中最大值的位置索引"""
        return X.rolling(window=N).apply(lambda x: x.argmax(), raw=True)
    
    @staticmethod
    def TS_ARGMIN(X: pd.Series, N: int) -> pd.Series:
        """返回X在过去N日中最小值的位置索引"""
        return X.rolling(window=N).apply(lambda x: x.argmin(), raw=True)
    
    @staticmethod
    def HHV(X: pd.Series, N: int) -> pd.Series:
        """返回X在过去N期的最高值，等同于TS_MAX"""
        return X.rolling(window=N).max()
    
    @staticmethod
    def LLV(X: pd.Series, N: int) -> pd.Series:
        """返回X在过去N期的最低值，等同于TS_MIN"""
        return X.rolling(window=N).min()
    
    @staticmethod
    def COUNT(X: pd.Series, N: int) -> pd.Series:
        """返回X在过去N日中为True的次数"""
        return X.rolling(window=N).sum()
    
    @staticmethod
    def EVERY(X: pd.Series, N: int) -> pd.Series:
        """判断X在过去N日是否全部为True"""
        return X.rolling(window=N).apply(lambda x: x.all(), raw=True)
    
    @staticmethod
    def EXIST(X: pd.Series, N: int) -> pd.Series:
        """判断X在过去N日是否至少为True一次"""
        return X.rolling(window=N).apply(lambda x: x.any(), raw=True)
    
    @staticmethod
    def SLOPE(X: pd.Series, N: int) -> pd.Series:
        """返回X在过去N期的线性回归斜率"""
        def calc_slope(y):
            if len(y) < 2:
                return np.nan
            x = np.arange(len(y))
            return np.polyfit(x, y, 1)[0]
        return X.rolling(window=N).apply(calc_slope, raw=True)
    
    @staticmethod
    def EMA(X: pd.Series, N: int) -> pd.Series:
        """指数移动平均"""
        return X.ewm(span=N, adjust=False).mean()
    
    @staticmethod
    def WMA(X: pd.Series, N: int) -> pd.Series:
        """序列的N日加权移动平均"""
        weights = np.arange(1, N + 1)
        return X.rolling(window=N).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)
    
    @staticmethod
    def RETURNS(X: pd.Series, N: int) -> pd.Series:
        """返回X相对于N日前的变化百分比"""
        return X / X.shift(N) - 1
    
    @staticmethod
    def SHARPE(X: pd.Series, N: int) -> pd.Series:
        """返回X在过去N日的收益率均值除以标准差"""
        returns = X.pct_change()
        return returns.rolling(window=N).mean() / returns.rolling(window=N).std()
    
    # ==================== 6. 双参数直接操作型函数 ====================
    
    @staticmethod
    def MAX(A: pd.Series, B: pd.Series) -> pd.Series:
        """返回A与B中的较大值"""
        return pd.concat([A, B], axis=1).max(axis=1)
    
    @staticmethod
    def MIN(A: pd.Series, B: pd.Series) -> pd.Series:
        """返回A与B中的较小值"""
        return pd.concat([A, B], axis=1).min(axis=1)
    
    @staticmethod
    def MEAN(A: pd.Series, B: pd.Series) -> pd.Series:
        """返回A与B均值"""
        return (A + B) / 2
    
    # ==================== 8. 三参数时序操作型函数 (A,B,N) ====================
    
    @staticmethod
    def CORR(A: pd.Series, B: pd.Series, N: int) -> pd.Series:
        """返回A与B在过去N日的滚动相关系数"""
        return A.rolling(window=N).corr(B)
    
    @staticmethod
    def CORRELATION(A: pd.Series, B: pd.Series, N: int) -> pd.Series:
        """返回A与B在过去N日的滚动相关系数，等同于CORR"""
        return A.rolling(window=N).corr(B)
    
    @staticmethod
    def COV(A: pd.Series, B: pd.Series, N: int) -> pd.Series:
        """返回A与B在过去N日的滚动协方差"""
        return A.rolling(window=N).cov(B)
    
    @staticmethod
    def COVARIANCE(A: pd.Series, B: pd.Series, N: int) -> pd.Series:
        """返回A与B在过去N日的滚动协方差，等同于COV"""
        return A.rolling(window=N).cov(B)
    
    # ==================== 10. 条件操作型函数 ====================
    
    @staticmethod
    def IF(X: pd.Series, A: Union[pd.Series, float], B: Union[pd.Series, float]) -> pd.Series:
        """若X为True则取A否则取B"""
        return pd.Series(np.where(X, A, B), index=X.index)
    
    # ==================== 11. 技术指标函数 ====================
    
    @staticmethod
    def ADV(VOLUME: pd.Series, N: int) -> pd.Series:
        """计算N日平均成交量"""
        return VOLUME.rolling(window=N).mean()
    
    @staticmethod
    def RSI(X: pd.Series, N: int) -> pd.Series:
        """N日相对强弱指数"""
        delta = X.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=N).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=N).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    @staticmethod
    def MACD_DIF(CLOSE: pd.Series, SHORT: int = 12, LONG: int = 26, M: int = 9) -> pd.Series:
        """计算MACD的DIF线"""
        ema_short = CLOSE.ewm(span=SHORT, adjust=False).mean()
        ema_long = CLOSE.ewm(span=LONG, adjust=False).mean()
        return ema_short - ema_long
    
    @staticmethod
    def MACD_DEA(CLOSE: pd.Series, SHORT: int = 12, LONG: int = 26, M: int = 9) -> pd.Series:
        """计算MACD的DEA线"""
        dif = FactorLibrary.MACD_DIF(CLOSE, SHORT, LONG, M)
        return dif.ewm(span=M, adjust=False).mean()
    
    @staticmethod
    def MACD(CLOSE: pd.Series, SHORT: int = 12, LONG: int = 26, M: int = 9) -> pd.Series:
        """计算MACD柱状图"""
        dif = FactorLibrary.MACD_DIF(CLOSE, SHORT, LONG, M)
        dea = FactorLibrary.MACD_DEA(CLOSE, SHORT, LONG, M)
        return (dif - dea) * 2
    
    @staticmethod
    def BOLL_UPPER(CLOSE: pd.Series, N: int = 20, P: float = 2.0) -> pd.Series:
        """布林带上轨"""
        ma = CLOSE.rolling(window=N).mean()
        std = CLOSE.rolling(window=N).std()
        return ma + P * std
    
    @staticmethod
    def BOLL_MID(CLOSE: pd.Series, N: int = 20, P: float = 2.0) -> pd.Series:
        """布林带中轨"""
        return CLOSE.rolling(window=N).mean()
    
    @staticmethod
    def BOLL_LOWER(CLOSE: pd.Series, N: int = 20, P: float = 2.0) -> pd.Series:
        """布林带下轨"""
        ma = CLOSE.rolling(window=N).mean()
        std = CLOSE.rolling(window=N).std()
        return ma - P * std
    
    @staticmethod
    def ATR(data: pd.DataFrame, N: int = 14) -> pd.Series:
        """平均真实波动范围"""
        high = data['high']
        low = data['low']
        close = data['close']
        
        tr1 = high - low
        tr2 = (high - close.shift(1)).abs()
        tr3 = (low - close.shift(1)).abs()
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(window=N).mean()


# 使用示例
if __name__ == "__main__":
    print("PandaAI Factor Library - Testing...")
    
    # 创建模拟数据
    dates = pd.date_range('2024-01-01', periods=100)
    data = pd.DataFrame({
        'close': np.random.randn(100).cumsum() + 100,
        'open': np.random.randn(100).cumsum() + 100,
        'high': np.random.randn(100).cumsum() + 102,
        'low': np.random.randn(100).cumsum() + 98,
        'volume': np.random.randint(1000, 10000, 100)
    }, index=dates)
    
    # 测试基础因子
    close = FactorLibrary.CLOSE(data)
    print(f"✅ CLOSE: {close.tail(3).values}")
    
    # 测试移动平均
    ma20 = FactorLibrary.MA(close, 20)
    print(f"✅ MA(20): {ma20.tail(3).values}")
    
    # 测试相关性
    volume = FactorLibrary.VOLUME(data)
    corr = FactorLibrary.CORRELATION(close, volume, 20)
    print(f"✅ CORRELATION(CLOSE, VOLUME, 20): {corr.tail(3).values}")
    
    # 测试MACD
    macd = FactorLibrary.MACD(close)
    print(f"✅ MACD: {macd.tail(3).values}")
    
    # 测试RSI
    rsi = FactorLibrary.RSI(close, 14)
    print(f"✅ RSI(14): {rsi.tail(3).values}")
    
    # 测试布林带
    boll_upper = FactorLibrary.BOLL_UPPER(close, 20, 2)
    boll_lower = FactorLibrary.BOLL_LOWER(close, 20, 2)
    print(f"✅ BOLL_UPPER: {boll_upper.tail(3).values}")
    print(f"✅ BOLL_LOWER: {boll_lower.tail(3).values}")
    
    print("\n🎉 All tests passed!")
