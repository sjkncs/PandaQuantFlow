"""金融数据分析路由"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import io
import base64
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime, timedelta
import warnings

# 配置matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 支持中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
warnings.filterwarnings('ignore')

router = APIRouter()

class StockAnalysisRequest(BaseModel):
    """股票分析请求"""
    code: str
    period: Optional[int] = 30
    analysis_type: str = "technical"  # technical, fundamental, volume
    indicators: Optional[List[str]] = ["MA", "MACD", "RSI"]

class ChartGenerateRequest(BaseModel):
    """图表生成请求"""
    data: List[Dict[str, Any]]
    chart_type: str = "line"  # line, bar, candlestick, scatter
    title: Optional[str] = "数据分析图"
    x_label: Optional[str] = "时间"
    y_label: Optional[str] = "数值"

class FactorAnalysisRequest(BaseModel):
    """因子分析请求"""
    factor_code: str
    backtest_period: Optional[int] = 180
    stock_pool: Optional[List[str]] = []

@router.post("/analysis/stock")
async def analyze_stock(request: StockAnalysisRequest):
    """股票技术分析"""
    try:
        # 模拟数据生成
        dates = pd.date_range(end=datetime.now(), periods=request.period, freq='D')
        
        # 生成模拟价格数据
        np.random.seed(42)
        price_base = 100
        returns = np.random.randn(request.period) * 0.02
        prices = price_base * np.exp(np.cumsum(returns))
        
        # 计算技术指标
        df = pd.DataFrame({
            'date': dates,
            'close': prices,
            'volume': np.random.randint(1000000, 5000000, request.period),
            'high': prices * (1 + np.abs(np.random.randn(request.period) * 0.01)),
            'low': prices * (1 - np.abs(np.random.randn(request.period) * 0.01))
        })
        
        # 计算移动平均
        df['MA5'] = df['close'].rolling(window=5).mean()
        df['MA20'] = df['close'].rolling(window=20).mean()
        
        # 计算RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # 计算MACD
        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        # 转换日期为字符串以便 JSON 序列化
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        
        # 生成分析结果
        result = {
            "code": request.code,
            "period": request.period,
            "latest_price": float(df['close'].iloc[-1]),
            "change_pct": float((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0] * 100),
            "indicators": {
                "MA5": float(df['MA5'].iloc[-1]) if not pd.isna(df['MA5'].iloc[-1]) else None,
                "MA20": float(df['MA20'].iloc[-1]) if not pd.isna(df['MA20'].iloc[-1]) else None,
                "RSI": float(df['RSI'].iloc[-1]) if not pd.isna(df['RSI'].iloc[-1]) else None,
                "MACD": float(df['MACD'].iloc[-1]) if not pd.isna(df['MACD'].iloc[-1]) else None,
            },
            "signals": {
                "trend": "上升" if df['close'].iloc[-1] > df['MA20'].iloc[-1] else "下降",
                "rsi_signal": "超买" if df['RSI'].iloc[-1] > 70 else ("超卖" if df['RSI'].iloc[-1] < 30 else "中性"),
                "macd_signal": "买入" if df['MACD'].iloc[-1] > df['Signal'].iloc[-1] else "卖出"
            },
            "data": df.fillna(0).to_dict('records')[-30:]  # 返回最近30条数据
        }
        
        return JSONResponse(content=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analysis/chart")
async def generate_chart(request: ChartGenerateRequest):
    """生成数据图表"""
    try:
        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 准备数据
        df = pd.DataFrame(request.data)
        
        # 根据类型生成不同图表
        if request.chart_type == "line":
            if 'x' in df.columns and 'y' in df.columns:
                ax.plot(df['x'], df['y'], marker='o', linewidth=2)
            else:
                ax.plot(df.index, df.iloc[:, 0], marker='o', linewidth=2)
                
        elif request.chart_type == "bar":
            if 'x' in df.columns and 'y' in df.columns:
                ax.bar(df['x'], df['y'])
            else:
                ax.bar(df.index, df.iloc[:, 0])
                
        elif request.chart_type == "scatter":
            if 'x' in df.columns and 'y' in df.columns:
                ax.scatter(df['x'], df['y'])
            else:
                ax.scatter(df.index, df.iloc[:, 0])
                
        elif request.chart_type == "candlestick":
            # K线图需要特殊处理
            if all(col in df.columns for col in ['open', 'high', 'low', 'close']):
                from matplotlib.patches import Rectangle
                
                for i in range(len(df)):
                    row = df.iloc[i]
                    color = 'g' if row['close'] >= row['open'] else 'r'
                    
                    # 画影线
                    ax.plot([i, i], [row['low'], row['high']], color=color, linewidth=0.5)
                    
                    # 画实体
                    height = abs(row['close'] - row['open'])
                    bottom = min(row['close'], row['open'])
                    rect = Rectangle((i - 0.3, bottom), 0.6, height, 
                                   facecolor=color, edgecolor=color, alpha=0.7)
                    ax.add_patch(rect)
        
        # 设置标题和标签
        ax.set_title(request.title, fontsize=16, fontweight='bold')
        ax.set_xlabel(request.x_label, fontsize=12)
        ax.set_ylabel(request.y_label, fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # 调整布局
        plt.tight_layout()
        
        # 转换为base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        plt.close()
        
        return {
            "success": True,
            "image": f"data:image/png;base64,{image_base64}",
            "chart_type": request.chart_type
        }
        
    except Exception as e:
        plt.close()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analysis/factor")
async def analyze_factor(request: FactorAnalysisRequest):
    """因子分析与回测"""
    try:
        # 模拟因子回测
        dates = pd.date_range(end=datetime.now(), periods=request.backtest_period, freq='D')
        
        # 生成模拟收益率
        np.random.seed(42)
        factor_returns = np.random.randn(request.backtest_period) * 0.01 + 0.0005  # 日均0.05%收益
        cumulative_returns = np.cumprod(1 + factor_returns)
        
        # 计算统计指标
        sharpe_ratio = np.mean(factor_returns) / np.std(factor_returns) * np.sqrt(252)
        max_drawdown = np.min(cumulative_returns / np.maximum.accumulate(cumulative_returns) - 1)
        win_rate = np.mean(factor_returns > 0)
        
        # 生成图表
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 累计收益曲线
        axes[0, 0].plot(dates, cumulative_returns, linewidth=2, color='#667eea')
        axes[0, 0].set_title('累计收益曲线', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('日期')
        axes[0, 0].set_ylabel('累计收益')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 日收益分布
        axes[0, 1].hist(factor_returns, bins=50, edgecolor='black', alpha=0.7, color='#764ba2')
        axes[0, 1].set_title('日收益分布', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('收益率')
        axes[0, 1].set_ylabel('频次')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 滚动夏普率
        rolling_sharpe = pd.Series(factor_returns).rolling(30).apply(
            lambda x: x.mean() / x.std() * np.sqrt(252) if x.std() > 0 else 0
        )
        axes[1, 0].plot(dates, rolling_sharpe, linewidth=2, color='#4ade80')
        axes[1, 0].set_title('30日滚动夏普率', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('日期')
        axes[1, 0].set_ylabel('夏普率')
        axes[1, 0].axhline(y=0, color='r', linestyle='--', alpha=0.5)
        axes[1, 0].grid(True, alpha=0.3)
        
        # 回撤图
        drawdowns = cumulative_returns / np.maximum.accumulate(cumulative_returns) - 1
        axes[1, 1].fill_between(dates, 0, drawdowns, color='#ff6b6b', alpha=0.5)
        axes[1, 1].set_title('回撤曲线', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('日期')
        axes[1, 1].set_ylabel('回撤比例')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle(f'因子回测分析 - {request.factor_code}', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # 转换为base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        plt.close()
        
        return {
            "success": True,
            "factor_code": request.factor_code,
            "statistics": {
                "total_return": float((cumulative_returns[-1] - 1) * 100),
                "annual_return": float((cumulative_returns[-1] ** (252 / request.backtest_period) - 1) * 100),
                "sharpe_ratio": float(sharpe_ratio),
                "max_drawdown": float(max_drawdown * 100),
                "win_rate": float(win_rate * 100),
                "volatility": float(np.std(factor_returns) * np.sqrt(252) * 100)
            },
            "chart": f"data:image/png;base64,{image_base64}"
        }
        
    except Exception as e:
        plt.close()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analysis/market_overview")
async def get_market_overview():
    """获取市场概况"""
    try:
        # 模拟市场数据
        indices = [
            {"name": "上证指数", "code": "000001.SH", "price": 3089.26, "change": -0.52, "volume": "2890亿"},
            {"name": "深证成指", "code": "399001.SZ", "price": 9684.33, "change": -0.73, "volume": "3560亿"},
            {"name": "创业板指", "code": "399006.SZ", "price": 1887.45, "change": -1.12, "volume": "1230亿"},
            {"name": "科创50", "code": "000688.SH", "price": 876.23, "change": 0.35, "volume": "580亿"}
        ]
        
        sectors = [
            {"name": "银行", "change": 1.23, "leader": "招商银行"},
            {"name": "新能源", "change": -2.15, "leader": "宁德时代"},
            {"name": "半导体", "change": 0.87, "leader": "中芯国际"},
            {"name": "医药", "change": -0.45, "leader": "恒瑞医药"},
            {"name": "消费", "change": 0.68, "leader": "贵州茅台"}
        ]
        
        hot_stocks = [
            {"name": "比亚迪", "code": "002594.SZ", "price": 258.32, "change": 3.45},
            {"name": "中国平安", "code": "601318.SH", "price": 44.28, "change": -1.23},
            {"name": "隆基绿能", "code": "601012.SH", "price": 24.56, "change": 2.18}
        ]
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "indices": indices,
            "sectors": sectors,
            "hot_stocks": hot_stocks,
            "market_sentiment": "中性偏多"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
