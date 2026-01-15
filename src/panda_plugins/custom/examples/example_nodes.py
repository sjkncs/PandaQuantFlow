"""
示例自定义节点
展示如何创建量化分析相关的工作流节点
"""

from typing import Optional, Type, List, Dict, Any
from pydantic import BaseModel
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# 导入基类和装饰器
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from panda_plugins.base import BaseWorkNode, work_node

# ==================== 数据节点 ====================

class StockDataInput(BaseModel):
    """股票数据输入"""
    symbol: str
    start_date: str
    end_date: str
    frequency: str = "1d"  # 1d, 1h, 5m

class StockDataOutput(BaseModel):
    """股票数据输出"""
    symbol: str
    data: List[Dict[str, Any]]
    columns: List[str]
    count: int

@work_node(name="股票数据加载", group="数据获取", icon="📊")
class StockDataLoader(BaseWorkNode):
    """
    加载股票历史数据
    支持多种数据源和时间频率
    """
    
    @classmethod
    def input_model(cls) -> Optional[Type[BaseModel]]:
        return StockDataInput
    
    @classmethod
    def output_model(cls) -> Optional[Type[BaseModel]]:
        return StockDataOutput
    
    def run(self, input: StockDataInput) -> StockDataOutput:
        # 模拟数据生成（实际应用应连接真实数据源）
        days = 30
        dates = pd.date_range(end=datetime.now(), periods=days)
        
        # 生成模拟价格数据
        np.random.seed(42)
        price_base = 100
        returns = np.random.randn(days) * 0.02
        prices = price_base * np.exp(np.cumsum(returns))
        
        data = []
        for i, date in enumerate(dates):
            data.append({
                "date": date.isoformat(),
                "open": float(prices[i] * (1 - np.random.rand() * 0.01)),
                "high": float(prices[i] * (1 + np.random.rand() * 0.02)),
                "low": float(prices[i] * (1 - np.random.rand() * 0.02)),
                "close": float(prices[i]),
                "volume": int(np.random.randint(1000000, 5000000))
            })
        
        return StockDataOutput(
            symbol=input.symbol,
            data=data,
            columns=["date", "open", "high", "low", "close", "volume"],
            count=len(data)
        )

# ==================== 因子计算节点 ====================

class FactorInput(BaseModel):
    """因子计算输入"""
    data: List[Dict[str, Any]]
    factor_type: str  # momentum, rsi, macd, bollinger
    period: int = 20

class FactorOutput(BaseModel):
    """因子计算输出"""
    factor_name: str
    values: List[float]
    statistics: Dict[str, float]

@work_node(name="技术因子计算", group="因子分析", icon="🧮")
class TechnicalFactorCalculator(BaseWorkNode):
    """
    计算各类技术因子
    支持动量、RSI、MACD、布林带等
    """
    
    @classmethod
    def input_model(cls) -> Optional[Type[BaseModel]]:
        return FactorInput
    
    @classmethod
    def output_model(cls) -> Optional[Type[BaseModel]]:
        return FactorOutput
    
    def run(self, input: FactorInput) -> FactorOutput:
        # 转换为DataFrame
        df = pd.DataFrame(input.data)
        df['close'] = pd.to_numeric(df['close'])
        
        values = []
        factor_name = ""
        
        if input.factor_type == "momentum":
            # 动量因子
            factor_name = f"Momentum_{input.period}"
            momentum = df['close'].pct_change(input.period)
            values = momentum.fillna(0).tolist()
            
        elif input.factor_type == "rsi":
            # RSI指标
            factor_name = f"RSI_{input.period}"
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=input.period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=input.period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            values = rsi.fillna(50).tolist()
            
        elif input.factor_type == "macd":
            # MACD指标
            factor_name = "MACD"
            exp1 = df['close'].ewm(span=12, adjust=False).mean()
            exp2 = df['close'].ewm(span=26, adjust=False).mean()
            macd = exp1 - exp2
            values = macd.fillna(0).tolist()
            
        else:
            # 默认返回价格
            factor_name = "Price"
            values = df['close'].tolist()
        
        # 计算统计指标
        values_array = np.array(values)
        statistics = {
            "mean": float(np.mean(values_array)),
            "std": float(np.std(values_array)),
            "min": float(np.min(values_array)),
            "max": float(np.max(values_array)),
            "sharpe": float(np.mean(values_array) / np.std(values_array)) if np.std(values_array) > 0 else 0
        }
        
        return FactorOutput(
            factor_name=factor_name,
            values=values,
            statistics=statistics
        )

# ==================== 机器学习节点 ====================

class MLInput(BaseModel):
    """机器学习输入"""
    features: List[List[float]]
    labels: List[float]
    model_type: str = "random_forest"  # random_forest, xgboost, linear
    train_ratio: float = 0.8

class MLOutput(BaseModel):
    """机器学习输出"""
    model_type: str
    train_score: float
    test_score: float
    predictions: List[float]
    feature_importance: List[float] = []

@work_node(name="ML模型训练", group="机器学习", icon="🤖")
class MLModelTrainer(BaseWorkNode):
    """
    训练机器学习模型
    支持随机森林、XGBoost、线性回归等
    """
    
    @classmethod
    def input_model(cls) -> Optional[Type[BaseModel]]:
        return MLInput
    
    @classmethod
    def output_model(cls) -> Optional[Type[BaseModel]]:
        return MLOutput
    
    def run(self, input: MLInput) -> MLOutput:
        # 模拟模型训练（实际应用应使用真实ML库）
        n_samples = len(input.labels)
        train_size = int(n_samples * input.train_ratio)
        
        # 模拟训练得分
        train_score = np.random.uniform(0.7, 0.95)
        test_score = train_score - np.random.uniform(0.05, 0.15)
        
        # 模拟预测
        predictions = [
            label + np.random.normal(0, 0.1) 
            for label in input.labels
        ]
        
        # 模拟特征重要性
        n_features = len(input.features[0]) if input.features else 0
        feature_importance = [
            np.random.uniform(0, 1) for _ in range(n_features)
        ]
        
        # 归一化特征重要性
        if feature_importance:
            total = sum(feature_importance)
            feature_importance = [f/total for f in feature_importance]
        
        return MLOutput(
            model_type=input.model_type,
            train_score=train_score,
            test_score=test_score,
            predictions=predictions,
            feature_importance=feature_importance
        )

# ==================== 回测节点 ====================

class BacktestInput(BaseModel):
    """回测输入"""
    signals: List[float]
    prices: List[float]
    initial_capital: float = 1000000
    position_size: float = 0.1
    commission: float = 0.001

class BacktestOutput(BaseModel):
    """回测输出"""
    total_return: float
    annual_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    trades_count: int

@work_node(name="策略回测", group="回测分析", icon="📈")
class StrategyBacktester(BaseWorkNode):
    """
    执行策略回测
    计算收益、风险和各种统计指标
    """
    
    @classmethod
    def input_model(cls) -> Optional[Type[BaseModel]]:
        return BacktestInput
    
    @classmethod
    def output_model(cls) -> Optional[Type[BaseModel]]:
        return BacktestOutput
    
    def run(self, input: BacktestInput) -> BacktestOutput:
        # 简单回测逻辑
        capital = input.initial_capital
        positions = 0
        trades = []
        
        for i in range(1, len(input.signals)):
            signal = input.signals[i]
            price = input.prices[i]
            
            # 买入信号
            if signal > 0 and positions == 0:
                positions = int(capital * input.position_size / price)
                capital -= positions * price * (1 + input.commission)
                trades.append({"type": "buy", "price": price})
            
            # 卖出信号
            elif signal < 0 and positions > 0:
                capital += positions * price * (1 - input.commission)
                trades.append({"type": "sell", "price": price})
                positions = 0
        
        # 清仓
        if positions > 0:
            capital += positions * input.prices[-1]
        
        # 计算统计指标
        total_return = (capital - input.initial_capital) / input.initial_capital
        annual_return = total_return * (252 / len(input.prices))  # 假设日数据
        
        # 计算每日收益率
        returns = np.diff(input.prices) / input.prices[:-1]
        sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
        
        # 计算最大回撤
        cumulative = np.cumprod(1 + returns)
        running_max = np.maximum.accumulate(cumulative)
        drawdowns = (cumulative - running_max) / running_max
        max_drawdown = np.min(drawdowns) if len(drawdowns) > 0 else 0
        
        # 计算胜率
        win_trades = 0
        for i in range(0, len(trades) - 1, 2):
            if i + 1 < len(trades):
                if trades[i + 1]["price"] > trades[i]["price"]:
                    win_trades += 1
        
        win_rate = win_trades / (len(trades) // 2) if len(trades) >= 2 else 0
        
        return BacktestOutput(
            total_return=float(total_return),
            annual_return=float(annual_return),
            sharpe_ratio=float(sharpe_ratio),
            max_drawdown=float(max_drawdown),
            win_rate=float(win_rate),
            trades_count=len(trades)
        )

# ==================== 数学运算节点 ====================

class MathInput(BaseModel):
    """数学运算输入"""
    number1: float
    number2: float
    operation: str = "add"  # add, subtract, multiply, divide

class MathOutput(BaseModel):
    """数学运算输出"""
    result: float

@work_node(name="数学运算", group="工具", icon="➕")
class MathOperator(BaseWorkNode):
    """
    基础数学运算节点
    支持加减乘除等运算
    """
    
    @classmethod
    def input_model(cls) -> Optional[Type[BaseModel]]:
        return MathInput
    
    @classmethod
    def output_model(cls) -> Optional[Type[BaseModel]]:
        return MathOutput
    
    def run(self, input: MathInput) -> MathOutput:
        result = 0
        
        if input.operation == "add":
            result = input.number1 + input.number2
        elif input.operation == "subtract":
            result = input.number1 - input.number2
        elif input.operation == "multiply":
            result = input.number1 * input.number2
        elif input.operation == "divide":
            result = input.number1 / input.number2 if input.number2 != 0 else 0
        
        return MathOutput(result=result)

# ==================== 示例：两数求和 ====================

class AdditionInput(BaseModel):
    """加法输入"""
    number1: int
    number2: int

class AdditionOutput(BaseModel):
    """加法输出"""
    result: int

@work_node(name="示例-两数求和", group="测试节点", icon="➕")
class ExamplePluginAddition(BaseWorkNode):
    """
    实现一个示例节点
    完成一个简单的加法运算
    """
    
    @classmethod
    def input_model(cls) -> Optional[Type[BaseModel]]:
        return AdditionInput
    
    @classmethod
    def output_model(cls) -> Optional[Type[BaseModel]]:
        return AdditionOutput
    
    def run(self, input: AdditionInput) -> AdditionOutput:
        result = input.number1 + input.number2
        return AdditionOutput(result=result)

# ==================== 测试代码 ====================

if __name__ == "__main__":
    # 测试股票数据加载
    print("测试股票数据加载节点...")
    data_loader = StockDataLoader()
    stock_input = StockDataInput(
        symbol="000001.SZ",
        start_date="2024-01-01",
        end_date="2024-01-31"
    )
    stock_output = data_loader.run(stock_input)
    print(f"加载 {stock_output.count} 条数据")
    
    # 测试因子计算
    print("\n测试技术因子计算节点...")
    factor_calc = TechnicalFactorCalculator()
    factor_input = FactorInput(
        data=stock_output.data,
        factor_type="momentum",
        period=5
    )
    factor_output = factor_calc.run(factor_input)
    print(f"因子: {factor_output.factor_name}")
    print(f"统计: {factor_output.statistics}")
    
    # 测试回测
    print("\n测试策略回测节点...")
    backtester = StrategyBacktester()
    signals = [1 if v > 0 else -1 for v in factor_output.values]
    prices = [d["close"] for d in stock_output.data]
    backtest_input = BacktestInput(
        signals=signals,
        prices=prices
    )
    backtest_output = backtester.run(backtest_input)
    print(f"总收益: {backtest_output.total_return:.2%}")
    print(f"夏普率: {backtest_output.sharpe_ratio:.2f}")
    print(f"最大回撤: {backtest_output.max_drawdown:.2%}")
    
    # 测试简单加法
    print("\n测试两数求和节点...")
    addition = ExamplePluginAddition()
    add_input = AdditionInput(number1=10, number2=20)
    add_output = addition.run(add_input)
    print(f"10 + 20 = {add_output.result}")
