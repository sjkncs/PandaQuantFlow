# SCGU-PandaFactor 快速入门指南

## 🎯 30分钟上手指南

本指南帮助您在30分钟内完成SCGU方法在PandaFactor中的集成和基础使用。

---

## 第一步: 环境准备 (10分钟)

### 1.1 安装依赖

```bash
# 创建环境
conda create -n scgu_panda python=3.9 -y
conda activate scgu_panda

# 安装核心依赖
pip install torch==2.0.0 torchvision torchaudio
pip install torch_geometric
pip install pandas numpy scikit-learn tqdm matplotlib
```

### 1.2 验证安装

```python
import torch
import torch_geometric
print(f"PyTorch: {torch.__version__}")
print(f"PyG: {torch_geometric.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
```

---

## 第二步: 运行示例 (10分钟)

### 2.1 训练因子图模型

```bash
cd PandaQuantFlow
python examples/scgu_factor_example.py --mode train --epochs 50
```

**预期输出**:
```
Training Factor Graph Model
Graph created: 2120 nodes, 8456 edges
Training for 50 epochs...
Epoch 10/50, Loss: 0.6234
Epoch 20/50, Loss: 0.4521
...
Model saved to factor_graph_model.pt
```

### 2.2 执行因子遗忘

```bash
python examples/scgu_factor_example.py --mode unlearn --factors "FACTOR_00,FACTOR_01" --unlearn-epochs 30
```

**预期输出**:
```
Unlearning Factors using SCGU
Factors to forget: ['FACTOR_00', 'FACTOR_01']
Marked 156 edges for deletion
Epoch 10/30, Total Loss: 0.3421, Random Loss: 0.2134, Locality Loss: 0.1287
...
Unlearned model saved to factor_graph_model_unlearned.pt
```

---

## 第三步: 集成到您的项目 (10分钟)

### 3.1 基础集成代码

```python
# 导入模块
import sys
sys.path.append('panda_factor-main/panda_factor-main/panda_factor/panda_factor')
from models.scgu_integration import (
    FactorGraphConfig, FactorRGCN, FactorGNNDelete,
    create_factor_graph_from_panda, unlearn_factors
)

# 准备数据
import pandas as pd
factor_data = pd.DataFrame({
    'date': ['2024-01-01'] * 100,
    'symbol': [f'STOCK_{i}' for i in range(100)],
    'factor_name': ['MOMENTUM'] * 100,
    'value': np.random.randn(100)
})

# 创建图并训练
config = FactorGraphConfig()
graph = create_factor_graph_from_panda(factor_data, config)
model = FactorRGCN(config, graph.num_nodes, 4)

# 训练模型 (简化版)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
for epoch in range(50):
    z = model(graph.x, graph.edge_index, graph.edge_type)
    # ... 训练逻辑

# 遗忘因子
model = unlearn_factors(model, graph, ['MOMENTUM'], epochs=30)
```

### 3.2 与PandaFactor数据对接

```python
import panda_data

# 初始化
panda_data.init()

# 获取因子数据
factor_df = panda_data.get_factor_by_name(
    factor_name="VH03cc651",
    start_date='20230101',
    end_date='20240101'
)

# 转换格式
factor_df = factor_df.reset_index()
factor_df['factor_name'] = 'VH03cc651'

# 创建图
graph = create_factor_graph_from_panda(factor_df)
```

---

## 常见使用场景

### 场景1: 删除失效因子

```python
# 识别失效因子 (基于回测)
failed_factors = ['FACTOR_A', 'FACTOR_B']

# 加载模型
checkpoint = torch.load('factor_graph_model.pt')
model = FactorRGCN(...)
model.load_state_dict(checkpoint['model_state_dict'])

# 遗忘
model = unlearn_factors(model, graph, failed_factors, epochs=50)

# 保存
torch.save(model.state_dict(), 'model_updated.pt')
```

### 场景2: 隐私数据删除

```python
# 删除特定股票的所有因子数据
sensitive_stocks = ['STOCK_001', 'STOCK_002']

# 标记相关边
builder = FactorGraphBuilder(config)
edges_to_delete = []
for stock in sensitive_stocks:
    stock_idx = graph.node_to_idx[f'stock_{stock}']
    edges_to_delete.extend(
        get_edges_for_node(graph, stock_idx)
    )

# 执行遗忘
deletion_mask = create_deletion_mask(graph, edges_to_delete)
model = unlearn_with_mask(model, graph, deletion_mask)
```

### 场景3: 增量更新

```python
# 定期遗忘过时因子
import schedule

def daily_unlearning():
    # 识别过时因子
    outdated = identify_outdated_factors()
    
    # 加载当前模型
    model = load_current_model()
    
    # 遗忘
    model = unlearn_factors(model, graph, outdated)
    
    # 保存
    save_model(model)

# 每天执行
schedule.every().day.at("02:00").do(daily_unlearning)
```

---

## 性能优化建议

### 1. 使用GPU加速

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
graph = graph.to(device)
```

### 2. 批处理大规模数据

```python
from torch_geometric.loader import NeighborLoader

loader = NeighborLoader(
    graph,
    num_neighbors=[10, 5],
    batch_size=256
)

for batch in loader:
    # 批处理训练
    pass
```

### 3. 降低模型复杂度

```python
# 使用较小的嵌入维度
config = FactorGraphConfig(
    in_dim=32,
    hidden_dim=64,
    out_dim=32
)
```

---

## 故障排查

### 问题1: CUDA out of memory

**解决方案**:
```python
# 减小批次大小
batch_size = 64  # 从128降低到64

# 或使用CPU
device = torch.device('cpu')
```

### 问题2: 图构建失败

**解决方案**:
```python
# 检查数据格式
assert 'date' in factor_data.columns
assert 'symbol' in factor_data.columns
assert 'factor_name' in factor_data.columns
assert 'value' in factor_data.columns

# 处理缺失值
factor_data = factor_data.dropna()
```

### 问题3: 遗忘效果不明显

**解决方案**:
```python
# 增加遗忘轮数
epochs = 100  # 从50增加到100

# 调整学习率
lr = 0.0001  # 降低学习率

# 增加alpha权重
alpha = 0.7  # 增加随机性损失权重
```

---

## 下一步学习

### 📚 深入文档
- [INTEGRATION_README.md](INTEGRATION_README.md) - 完整集成指南
- [RESEARCH_DIRECTIONS_2026_2027.md](RESEARCH_DIRECTIONS_2026_2027.md) - 研究方向

### 🔬 高级功能
- 多模态融合
- 联邦遗忘
- 在线学习与遗忘

### 📊 实验与评估
- 遗忘效果评估
- 性能基准测试
- 可视化分析

### 🎯 研究方向
- 多模态金融智能
- 机器人技能遗忘
- 视觉模型遗忘
- LLM知识遗忘
- 医疗AI遗忘

---

## 获取帮助

- **文档**: 查看完整文档
- **示例**: 运行 `examples/` 目录下的示例
- **问题**: 提交GitHub Issue
- **讨论**: 加入技术交流群

---

**恭喜！您已完成快速入门。现在可以开始使用SCGU方法进行因子图分析了！** 🎉
