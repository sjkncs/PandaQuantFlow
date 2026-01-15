"""
Simple Contrastive Learning for Lightweight Edition
轻量级对比学习实现
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class SimpleContrastiveLearning(nn.Module):
    """
    简单的对比学习模型
    
    核心思想:
    - 相似样本应该有相似的表示
    - 不同样本应该有不同的表示
    
    无需标注数据！
    """
    
    def __init__(self, input_dim=64, hidden_dim=128, output_dim=64, temperature=0.07):
        super().__init__()
        
        # 编码器
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )
        
        # 投影头 (用于对比学习)
        self.projection = nn.Sequential(
            nn.Linear(output_dim, output_dim),
            nn.ReLU(),
            nn.Linear(output_dim, output_dim // 2)
        )
        
        self.temperature = temperature
        self.optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
    
    def encode(self, x):
        """编码输入数据"""
        return self.encoder(x)
    
    def forward(self, x):
        """前向传播"""
        z = self.encode(x)
        p = self.projection(z)
        return F.normalize(p, dim=1)
    
    def contrastive_loss(self, z1, z2):
        """
        对比损失 (InfoNCE)
        
        Args:
            z1: 第一个视图的嵌入
            z2: 第二个视图的嵌入
        
        Returns:
            对比损失
        """
        # 归一化
        z1 = F.normalize(z1, dim=1)
        z2 = F.normalize(z2, dim=1)
        
        # 计算相似度矩阵
        similarity = torch.matmul(z1, z2.t()) / self.temperature
        
        # 对角线是正样本
        batch_size = z1.size(0)
        labels = torch.arange(batch_size, device=z1.device)
        
        # 对称损失
        loss_1 = F.cross_entropy(similarity, labels)
        loss_2 = F.cross_entropy(similarity.t(), labels)
        
        return (loss_1 + loss_2) / 2
    
    def train_step(self, x1, x2):
        """
        单步训练
        
        Args:
            x1: 第一个视图
            x2: 第二个视图 (通常是x1的增强版本)
        
        Returns:
            损失值
        """
        self.optimizer.zero_grad()
        
        # 前向传播
        z1 = self.forward(x1)
        z2 = self.forward(x2)
        
        # 计算损失
        loss = self.contrastive_loss(z1, z2)
        
        # 反向传播
        loss.backward()
        self.optimizer.step()
        
        return loss.item()


def data_augmentation(x, noise_level=0.1):
    """
    简单的数据增强
    
    Args:
        x: 输入数据
        noise_level: 噪声水平
    
    Returns:
        增强后的数据
    """
    return x + torch.randn_like(x) * noise_level


if __name__ == "__main__":
    # 测试
    print("Testing SimpleContrastiveLearning...")
    
    model = SimpleContrastiveLearning(input_dim=64, hidden_dim=128)
    
    # 模拟数据
    x = torch.randn(32, 64)
    x1 = data_augmentation(x)
    x2 = data_augmentation(x)
    
    # 训练一步
    loss = model.train_step(x1, x2)
    print(f"Loss: {loss:.4f}")
    
    # 编码
    with torch.no_grad():
        z = model.encode(x)
    print(f"Encoded shape: {z.shape}")
    
    print("✅ Test passed!")
