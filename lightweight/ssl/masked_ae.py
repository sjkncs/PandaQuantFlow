"""
Simple Masked Autoencoder for Lightweight Edition
轻量级掩码自编码器实现
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class SimpleMaskedAutoencoder(nn.Module):
    """
    简单的掩码自编码器
    
    核心思想:
    - 随机掩码部分输入
    - 从剩余部分重建完整输入
    - 学习数据的内在结构
    
    无需标注数据！
    """
    
    def __init__(self, input_dim=64, hidden_dim=128, mask_ratio=0.75):
        super().__init__()
        
        self.mask_ratio = mask_ratio
        
        # 编码器
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )
        
        # 解码器
        self.decoder = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim)
        )
        
        self.optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
    
    def random_mask(self, x):
        """
        随机掩码
        
        Args:
            x: 输入数据 [batch_size, feature_dim]
        
        Returns:
            masked_x: 掩码后的数据
            mask: 掩码位置 (True表示被掩码)
        """
        batch_size, feature_dim = x.shape
        num_masked = int(feature_dim * self.mask_ratio)
        
        # 随机选择掩码位置
        mask = torch.zeros(batch_size, feature_dim, dtype=torch.bool, device=x.device)
        for i in range(batch_size):
            masked_indices = torch.randperm(feature_dim)[:num_masked]
            mask[i, masked_indices] = True
        
        # 掩码数据 (用0替换)
        masked_x = x.clone()
        masked_x[mask] = 0
        
        return masked_x, mask
    
    def forward(self, x):
        """
        前向传播
        
        Args:
            x: 输入数据
        
        Returns:
            reconstructed: 重建的数据
        """
        # 编码
        latent = self.encoder(x)
        
        # 解码
        reconstructed = self.decoder(latent)
        
        return reconstructed
    
    def compute_loss(self, x, reconstructed, mask):
        """
        计算重建损失 (仅在掩码位置)
        
        Args:
            x: 原始数据
            reconstructed: 重建数据
            mask: 掩码位置
        
        Returns:
            损失值
        """
        # 仅计算掩码位置的损失
        loss = F.mse_loss(reconstructed[mask], x[mask])
        return loss
    
    def train_step(self, x):
        """
        单步训练
        
        Args:
            x: 输入数据
        
        Returns:
            损失值
        """
        self.optimizer.zero_grad()
        
        # 随机掩码
        masked_x, mask = self.random_mask(x)
        
        # 前向传播
        reconstructed = self.forward(masked_x)
        
        # 计算损失
        loss = self.compute_loss(x, reconstructed, mask)
        
        # 反向传播
        loss.backward()
        self.optimizer.step()
        
        return loss.item()
    
    def encode(self, x):
        """提取特征"""
        with torch.no_grad():
            return self.encoder(x)


if __name__ == "__main__":
    # 测试
    print("Testing SimpleMaskedAutoencoder...")
    
    model = SimpleMaskedAutoencoder(input_dim=64, hidden_dim=128, mask_ratio=0.75)
    
    # 模拟数据
    x = torch.randn(32, 64)
    
    # 训练一步
    loss = model.train_step(x)
    print(f"Loss: {loss:.4f}")
    
    # 编码
    z = model.encode(x)
    print(f"Encoded shape: {z.shape}")
    
    # 重建
    with torch.no_grad():
        reconstructed = model.forward(x)
    print(f"Reconstructed shape: {reconstructed.shape}")
    
    print("✅ Test passed!")
