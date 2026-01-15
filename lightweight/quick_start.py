"""
SCGU Lightweight Edition - Quick Start Example
快速开始示例 - 5分钟上手
"""

import torch
import numpy as np
from ssl.contrastive import SimpleContrastiveLearning
from ssl.masked_ae import SimpleMaskedAutoencoder

print("="*60)
print("SCGU Lightweight Edition - Quick Start")
print("="*60)

# 1. 准备数据 (使用模拟数据)
print("\n[1/4] 准备数据...")
num_samples = 1000
feature_dim = 64

# 模拟金融时序数据
data = torch.randn(num_samples, feature_dim)
print(f"✅ 数据准备完成: {data.shape}")

# 2. 自监督预训练 - 对比学习
print("\n[2/4] 自监督预训练 (对比学习)...")
ssl_model = SimpleContrastiveLearning(input_dim=feature_dim, hidden_dim=128)

# 训练10个epoch (实际应用建议50-100)
for epoch in range(10):
    # 数据增强生成正样本对
    x1 = data + torch.randn_like(data) * 0.1
    x2 = data + torch.randn_like(data) * 0.1
    
    # 前向传播
    z1 = ssl_model.encode(x1)
    z2 = ssl_model.encode(x2)
    
    # 对比损失
    loss = ssl_model.contrastive_loss(z1, z2)
    
    # 反向传播
    loss.backward()
    ssl_model.optimizer.step()
    ssl_model.optimizer.zero_grad()
    
    if (epoch + 1) % 5 == 0:
        print(f"  Epoch {epoch+1}/10, Loss: {loss.item():.4f}")

print("✅ 预训练完成")

# 3. 少量标注数据微调
print("\n[3/4] 少量标注数据微调...")

# 模拟100个标注样本 (实际建议500-1000)
labeled_data = data[:100]
labels = torch.randint(0, 2, (100,))

# 添加分类头
classifier = torch.nn.Linear(128, 2)
optimizer = torch.optim.Adam(classifier.parameters(), lr=0.001)

# 微调
for epoch in range(20):
    # 使用预训练的编码器
    with torch.no_grad():
        features = ssl_model.encode(labeled_data)
    
    # 分类
    logits = classifier(features)
    loss = torch.nn.functional.cross_entropy(logits, labels)
    
    # 更新
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    
    if (epoch + 1) % 10 == 0:
        acc = (logits.argmax(dim=1) == labels).float().mean()
        print(f"  Epoch {epoch+1}/20, Loss: {loss.item():.4f}, Acc: {acc.item():.2%}")

print("✅ 微调完成")

# 4. 评估
print("\n[4/4] 模型评估...")
test_data = data[100:200]
test_labels = torch.randint(0, 2, (100,))

with torch.no_grad():
    test_features = ssl_model.encode(test_data)
    test_logits = classifier(test_features)
    test_acc = (test_logits.argmax(dim=1) == test_labels).float().mean()

print(f"✅ 测试准确率: {test_acc.item():.2%}")

print("\n" + "="*60)
print("🎉 快速开始完成！")
print("="*60)
print("\n下一步:")
print("1. 使用真实数据替换模拟数据")
print("2. 调整超参数 (epochs, learning rate等)")
print("3. 尝试其他自监督方法 (MaskedAE, Temporal)")
print("4. 查看完整文档: docs/")
