"""
因子库与自监督学习集成示例
Factor Library + Self-Supervised Learning Integration

展示如何将PandaAI因子库与自监督学习框架结合
实现端到端的量化因子挖掘流程
"""

import sys
sys.path.append('..')
import pandas as pd
import numpy as np
import torch
from factor_library import FactorLibrary
from ssl.contrastive import SimpleContrastiveLearning

print("="*70)
print("因子库 + 自监督学习 集成示例")
print("="*70)

# ==================== 1. 准备数据 ====================
print("\n[步骤 1/5] 准备市场数据...")

# 模拟一年的市场数据
dates = pd.date_range('2023-01-01', periods=252)
np.random.seed(42)

# 生成模拟价格数据（随机游走）
price_base = 100
prices = [price_base]
for _ in range(251):
    change = np.random.randn() * 2  # 每日波动
    prices.append(prices[-1] * (1 + change/100))

data = pd.DataFrame({
    'close': prices,
    'open': [p * (1 + np.random.randn()*0.01) for p in prices],
    'high': [p * (1 + abs(np.random.randn())*0.02) for p in prices],
    'low': [p * (1 - abs(np.random.randn())*0.02) for p in prices],
    'volume': np.random.randint(1000000, 10000000, 252)
}, index=dates)

print(f"✅ 数据准备完成: {len(data)} 个交易日")
print(f"   价格范围: {data['close'].min():.2f} - {data['close'].max():.2f}")
print(f"   平均成交量: {data['volume'].mean():.0f}")

# ==================== 2. 计算技术因子 ====================
print("\n[步骤 2/5] 计算技术因子...")

close = FactorLibrary.CLOSE(data)
volume = FactorLibrary.VOLUME(data)

# 计算多个技术因子
factors = pd.DataFrame({
    # 趋势因子
    'ma5': FactorLibrary.MA(close, 5),
    'ma10': FactorLibrary.MA(close, 10),
    'ma20': FactorLibrary.MA(close, 20),
    'ma60': FactorLibrary.MA(close, 60),
    
    # 动量因子
    'roc5': FactorLibrary.ROC(close, 5),
    'roc10': FactorLibrary.ROC(close, 10),
    'roc20': FactorLibrary.ROC(close, 20),
    
    # 波动率因子
    'std10': FactorLibrary.STD(close, 10),
    'std20': FactorLibrary.STD(close, 20),
    'atr14': FactorLibrary.ATR(data, 14),
    
    # 技术指标
    'rsi14': FactorLibrary.RSI(close, 14),
    'macd': FactorLibrary.MACD(close),
    
    # 量价因子
    'volume_ma20': FactorLibrary.MA(volume, 20),
    'volume_std20': FactorLibrary.STD(volume, 20),
    'corr_pv_20': FactorLibrary.CORRELATION(close, volume, 20),
    
    # 布林带
    'boll_upper': FactorLibrary.BOLL_UPPER(close, 20, 2),
    'boll_lower': FactorLibrary.BOLL_LOWER(close, 20, 2),
    
    # 价格位置
    'price_position': (close - FactorLibrary.MA(close, 20)) / FactorLibrary.STD(close, 20),
})

# 去除NaN值
factors = factors.fillna(method='bfill').fillna(0)

print(f"✅ 因子计算完成: {factors.shape[1]} 个因子")
print(f"   因子列表: {list(factors.columns[:5])}... (共{len(factors.columns)}个)")

# ==================== 3. 因子标准化 ====================
print("\n[步骤 3/5] 因子标准化...")

# Z-score标准化
factors_normalized = (factors - factors.mean()) / factors.std()
factors_normalized = factors_normalized.fillna(0)

print(f"✅ 标准化完成")
print(f"   均值: {factors_normalized.mean().mean():.4f}")
print(f"   标准差: {factors_normalized.std().mean():.4f}")

# ==================== 4. 自监督预训练 ====================
print("\n[步骤 4/5] 自监督预训练...")

# 转换为PyTorch张量
factor_tensor = torch.FloatTensor(factors_normalized.values)

# 创建自监督学习模型
input_dim = factors.shape[1]
ssl_model = SimpleContrastiveLearning(
    input_dim=input_dim,
    hidden_dim=64,
    output_dim=32
)

print(f"   模型架构: {input_dim} -> 64 -> 32")

# 训练参数
num_epochs = 50
batch_size = 32

# 训练循环
losses = []
for epoch in range(num_epochs):
    epoch_losses = []
    
    # 随机采样批次
    indices = torch.randperm(len(factor_tensor))
    
    for i in range(0, len(indices), batch_size):
        batch_indices = indices[i:i+batch_size]
        if len(batch_indices) < 2:
            continue
        
        batch_data = factor_tensor[batch_indices]
        
        # 数据增强：添加噪声
        x1 = batch_data + torch.randn_like(batch_data) * 0.1
        x2 = batch_data + torch.randn_like(batch_data) * 0.1
        
        # 训练一步
        loss = ssl_model.train_step(x1, x2)
        epoch_losses.append(loss)
    
    avg_loss = np.mean(epoch_losses)
    losses.append(avg_loss)
    
    if (epoch + 1) % 10 == 0:
        print(f"   Epoch {epoch+1}/{num_epochs}, Loss: {avg_loss:.4f}")

print(f"✅ 预训练完成")
print(f"   最终损失: {losses[-1]:.4f}")
print(f"   损失下降: {(losses[0] - losses[-1])/losses[0]*100:.1f}%")

# ==================== 5. 因子表示学习 ====================
print("\n[步骤 5/5] 提取因子表示...")

# 使用训练好的编码器提取因子表示
with torch.no_grad():
    factor_embeddings = ssl_model.encode(factor_tensor)

print(f"✅ 因子表示提取完成")
print(f"   原始维度: {input_dim}")
print(f"   压缩维度: {factor_embeddings.shape[1]}")
print(f"   压缩比: {input_dim/factor_embeddings.shape[1]:.1f}x")

# ==================== 6. 结果分析 ====================
print("\n" + "="*70)
print("📊 结果分析")
print("="*70)

# 计算因子相关性
factor_corr = factors_normalized.corr()
avg_corr = factor_corr.abs().mean().mean()

print(f"\n1. 原始因子统计:")
print(f"   - 因子数量: {factors.shape[1]}")
print(f"   - 平均相关性: {avg_corr:.3f}")
print(f"   - 高相关因子对: {(factor_corr.abs() > 0.8).sum().sum() - len(factors.columns)}")

# 计算嵌入相关性
embedding_df = pd.DataFrame(factor_embeddings.numpy())
embedding_corr = embedding_df.corr()
avg_embedding_corr = embedding_corr.abs().mean().mean()

print(f"\n2. 学习到的表示统计:")
print(f"   - 表示维度: {factor_embeddings.shape[1]}")
print(f"   - 平均相关性: {avg_embedding_corr:.3f}")
print(f"   - 信息压缩: {(1 - avg_embedding_corr/avg_corr)*100:.1f}% 去相关")

# 计算收益预测能力（简单示例）
future_returns = (close.shift(-5) / close - 1).fillna(0)  # 未来5日收益

# 使用原始因子
factor_signal = factors_normalized.mean(axis=1)
signal_return_corr = np.corrcoef(factor_signal[:-5], future_returns[:-5])[0, 1]

# 使用学习到的表示
embedding_signal = pd.Series(factor_embeddings[:, 0].numpy(), index=factors.index)
embedding_return_corr = np.corrcoef(embedding_signal[:-5], future_returns[:-5])[0, 1]

print(f"\n3. 预测能力对比:")
print(f"   - 原始因子 vs 未来收益相关性: {signal_return_corr:.4f}")
print(f"   - 学习表示 vs 未来收益相关性: {embedding_return_corr:.4f}")
print(f"   - 改进: {(abs(embedding_return_corr) - abs(signal_return_corr))*100:.2f}%")

# ==================== 7. 应用建议 ====================
print("\n" + "="*70)
print("💡 应用建议")
print("="*70)

print("""
1. 因子挖掘流程:
   ✅ 计算大量技术因子 (100+)
   ✅ 使用自监督学习降维去噪
   ✅ 提取低维度高质量表示
   ✅ 用于下游预测任务

2. 优势:
   ✅ 无需标注数据
   ✅ 自动发现因子间关系
   ✅ 降低过拟合风险
   ✅ 提高计算效率

3. 下一步:
   ✅ 增加更多因子 (Alpha101, Alpha191等)
   ✅ 尝试不同自监督方法 (MaskedAE, Temporal)
   ✅ 加入少量标注数据微调
   ✅ 回测验证策略效果
""")

print("\n" + "="*70)
print("🎉 示例完成！")
print("="*70)
