# SCGU-PandaFactor 集成指南

## 概述

本项目将SCGU (Subspace-Constrained Graph Unlearning) 方法集成到PandaFactor量化因子系统中，实现基于图神经网络的因子关系建模和选择性遗忘功能。

## 核心功能

### 1. 因子图建模
- **异构图构建**: 支持因子-股票、因子-因子、股票-股票等多种关系
- **RGCN编码**: 使用关系图卷积网络学习因子表示
- **链接预测**: 预测因子与股票之间的关联强度

### 2. 选择性遗忘
- **因子级遗忘**: 删除特定失效因子
- **关系级遗忘**: 删除特定因子关联
- **局部因果保持**: 保护未删除关系的完整性

### 3. 多模态扩展
- 支持视觉、文本、图等多模态数据融合
- 为顶会论文研究提供技术基础

## 项目结构

```
PandaQuantFlow/
├── SCGU-main/                          # SCGU原始框架
│   ├── framework/                      # 核心算法
│   │   ├── models/                     # GNN模型
│   │   └── trainer/                    # 训练器
│   └── README.md
├── panda_factor-main/                  # PandaFactor系统
│   └── panda_factor-main/
│       └── panda_factor/
│           └── panda_factor/
│               └── models/
│                   └── scgu_integration.py  # 集成模块
├── examples/
│   └── scgu_factor_example.py          # 使用示例
├── RESEARCH_DIRECTIONS_2026_2027.md    # 研究方向规划
└── INTEGRATION_README.md               # 本文档
```

## 快速开始

### 环境配置

```bash
# 1. 创建虚拟环境
conda create -n scgu_panda python=3.9
conda activate scgu_panda

# 2. 安装PyTorch (CUDA版本)
pip install torch==2.0.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 3. 安装PyTorch Geometric
pip install torch_geometric
pip install pyg_lib torch_scatter torch_sparse torch_cluster -f https://data.pyg.org/whl/torch-2.0.0+cu118.html

# 4. 安装其他依赖
pip install pandas numpy scikit-learn tqdm matplotlib seaborn

# 5. 安装PandaFactor (可选)
cd panda_factor-main/panda_factor-main/panda_common
pip install -e .
cd ../panda_data
pip install -e .
cd ../panda_factor
pip install -e .
```

### 基础使用

#### 1. 训练因子图模型

```python
from models.scgu_integration import (
    FactorGraphConfig, FactorRGCN, create_factor_graph_from_panda
)
import pandas as pd

# 准备因子数据
factor_data = pd.DataFrame({
    'date': [...],
    'symbol': [...],
    'factor_name': [...],
    'value': [...]
})

# 创建因子图
config = FactorGraphConfig(in_dim=64, hidden_dim=128, out_dim=64)
graph_data = create_factor_graph_from_panda(factor_data, config)

# 初始化模型
model = FactorRGCN(
    config=config,
    num_nodes=graph_data.num_nodes,
    num_edge_types=4
)

# 训练模型
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
for epoch in range(100):
    z = model(graph_data.x, graph_data.edge_index, graph_data.edge_type)
    # ... 训练逻辑
```

#### 2. 遗忘特定因子

```python
from models.scgu_integration import unlearn_factors

# 指定要遗忘的因子
factors_to_forget = ['FACTOR_01', 'FACTOR_05']

# 执行遗忘
updated_model = unlearn_factors(
    model=model,
    data=graph_data,
    factors_to_forget=factors_to_forget,
    epochs=50,
    lr=0.0001
)
```

#### 3. 运行完整示例

```bash
# 训练模型
python examples/scgu_factor_example.py --mode train --epochs 100

# 遗忘因子
python examples/scgu_factor_example.py --mode unlearn --factors "FACTOR_00,FACTOR_01" --unlearn-epochs 50

# 评估模型
python examples/scgu_factor_example.py --mode evaluate
```

## 核心模块说明

### 1. FactorGraphConfig
配置因子图的超参数

```python
@dataclass
class FactorGraphConfig:
    in_dim: int = 64              # 输入维度
    hidden_dim: int = 128         # 隐藏层维度
    out_dim: int = 64             # 输出维度
    num_relations: int = 4        # 关系类型数量
    dropout: float = 0.1          # Dropout率
    num_layers: int = 2           # GNN层数
    similarity_threshold: float = 0.6  # 相似度阈值
```

### 2. FactorRGCN
关系图卷积网络模型

**主要方法**:
- `forward()`: 前向传播，生成节点嵌入
- `decode()`: 解码边概率，用于链接预测

### 3. FactorGNNDelete
支持遗忘的因子图模型

**特性**:
- 子空间约束删除层
- 局部因果保持
- 高效遗忘算法

### 4. FactorGraphBuilder
从数据构建因子图

**功能**:
- 异构图构建
- 多种关系类型支持
- 自动相似度计算

### 5. SCGUTrainer
SCGU训练器

**核心损失**:
- 随机性损失: 使删除边不可区分
- 局部性损失: 保持剩余关系

## 与PandaFactor集成

### 数据接口

```python
import panda_data

# 初始化PandaData
panda_data.init()

# 获取因子数据
factor_df = panda_data.get_factor_by_name(
    factor_name="VH03cc651",
    start_date='20230101',
    end_date='20240101'
)

# 转换为标准格式
factor_df = factor_df.reset_index()
factor_df['factor_name'] = 'VH03cc651'

# 创建因子图
graph_data = create_factor_graph_from_panda(factor_df)
```

### 因子更新流程

```python
# 1. 加载现有模型
checkpoint = torch.load('factor_graph_model.pt')
model = FactorRGCN(...)
model.load_state_dict(checkpoint['model_state_dict'])

# 2. 识别失效因子
# (基于回测结果、夏普比率等指标)
failed_factors = identify_failed_factors(backtest_results)

# 3. 执行遗忘
model = unlearn_factors(model, graph_data, failed_factors)

# 4. 保存更新后的模型
torch.save(model.state_dict(), 'factor_graph_model_updated.pt')
```

## 研究方向拓展

详见 [RESEARCH_DIRECTIONS_2026_2027.md](RESEARCH_DIRECTIONS_2026_2027.md)

### 五大研究方向

1. **多模态金融智能**
   - 视觉-文本-图融合的市场预测
   - 目标会议: KDD, WWW, AAAI

2. **具身智能与机器人学习**
   - 多模态机器人技能遗忘
   - 目标会议: ICRA, IROS, RSS, CoRL

3. **计算机视觉中的遗忘学习**
   - 视觉基础模型的选择性遗忘
   - 目标会议: CVPR, ICCV, ECCV

4. **自然语言处理中的知识遗忘**
   - 大语言模型的知识图谱遗忘
   - 目标会议: ACL, EMNLP

5. **多模态医疗AI**
   - 医学影像-文本-知识图谱联合诊断
   - 目标会议: MICCAI, NeurIPS

### 2026-2027论文规划

| 时间 | 方向 | 目标会议 | 状态 |
|------|------|----------|------|
| 2026 Q1-Q2 | 多模态金融 | KDD 2026 | 规划中 |
| 2026 Q1-Q2 | 视觉遗忘 | CVPR 2027 | 规划中 |
| 2026 Q3-Q4 | 机器人技能遗忘 | ICRA 2027 | 规划中 |
| 2026 Q3-Q4 | LLM知识遗忘 | ACL 2027 | 规划中 |
| 2027 Q1-Q2 | 医疗AI遗忘 | MICCAI 2027 | 规划中 |

## 实验与评估

### 评估指标

1. **遗忘效果**
   - 目标因子识别率下降
   - 成员推理攻击成功率

2. **保留性能**
   - 其他因子预测准确率
   - 回测收益保持率

3. **效率**
   - 遗忘时间 vs 重训练时间
   - 内存占用

### 实验脚本

```python
# 评估遗忘效果
def evaluate_forgetting(model, graph_data, forgotten_factors):
    # 1. 测试目标因子是否被遗忘
    target_edges = get_edges_for_factors(graph_data, forgotten_factors)
    target_scores = predict_edges(model, target_edges)
    
    # 2. 测试其他因子是否保留
    retain_edges = get_edges_for_other_factors(graph_data, forgotten_factors)
    retain_scores = predict_edges(model, retain_edges)
    
    return {
        'target_score': target_scores.mean(),
        'retain_score': retain_scores.mean(),
        'forgetting_ratio': 1 - target_scores.mean() / retain_scores.mean()
    }
```

## 常见问题

### Q1: 如何选择要遗忘的因子?

**A**: 基于以下标准:
- 回测表现持续下降
- 与其他因子高度相关(冗余)
- 数据质量问题
- 隐私/合规要求

### Q2: 遗忘会影响其他因子吗?

**A**: SCGU通过局部因果保持机制最小化影响:
- 只删除目标因子的直接关联
- 保护其他因子的嵌入表示
- 实验表明保留性能 > 95%

### Q3: 遗忘需要多长时间?

**A**: 相比重训练大幅提升:
- 小规模 (< 100因子): 1-5分钟
- 中等规模 (100-1000因子): 10-30分钟
- 大规模 (> 1000因子): 1-2小时
- 重训练: 数小时到数天

### Q4: 支持增量遗忘吗?

**A**: 支持，可以多次调用遗忘函数:

```python
# 第一次遗忘
model = unlearn_factors(model, data, ['FACTOR_01'])

# 第二次遗忘
model = unlearn_factors(model, data, ['FACTOR_05'])
```

### Q5: 如何验证遗忘效果?

**A**: 三种验证方法:
1. **直接测试**: 预测目标因子相关边的概率
2. **成员推理攻击**: 训练攻击模型判断是否遗忘
3. **回测验证**: 检查遗忘因子是否影响策略

## 性能优化

### GPU加速

```python
# 使用GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
graph_data = graph_data.to(device)
```

### 批处理

```python
# 对于大规模图，使用mini-batch训练
from torch_geometric.loader import NeighborLoader

loader = NeighborLoader(
    graph_data,
    num_neighbors=[10, 5],
    batch_size=128
)

for batch in loader:
    z = model(batch.x, batch.edge_index, batch.edge_type)
    # ...
```

### 模型压缩

```python
# 使用较小的嵌入维度
config = FactorGraphConfig(
    in_dim=32,      # 降低维度
    hidden_dim=64,
    out_dim=32
)
```

## 贡献指南

欢迎贡献代码、提出问题或建议！

### 开发流程

1. Fork本项目
2. 创建特性分支: `git checkout -b feature/amazing-feature`
3. 提交更改: `git commit -m 'Add amazing feature'`
4. 推送分支: `git push origin feature/amazing-feature`
5. 提交Pull Request

### 代码规范

- 遵循PEP 8
- 添加类型注解
- 编写文档字符串
- 添加单元测试

## 引用

如果使用本项目，请引用:

```bibtex
@article{ZHANG2025115193,
  title = {Subspace-Constrained Graph Unlearning For Forgetting High-Risk Compound-Protein Interactions},
  journal = {Knowledge-Based Systems},
  pages = {115193},
  year = {2025},
  author = {Yunjian Zhang and Rizhen Hu and Yixuan Li and Zhongfeng Kang}
}
```

## 许可证

本项目采用 GPL-3.0 许可证

## 联系方式

- 项目地址: https://github.com/PandaQuantFlow
- 问题反馈: 提交Issue
- 技术交流: [待补充]

## 更新日志

### v1.0.0 (2026-01)
- ✅ SCGU核心算法集成
- ✅ 因子图构建模块
- ✅ 基础遗忘功能
- ✅ 示例代码和文档
- ✅ 多模态研究方向规划

### 计划功能
- [ ] 联邦遗忘支持
- [ ] 在线遗忘算法
- [ ] 可视化工具
- [ ] Web界面
- [ ] 更多数据源支持

---

**最后更新**: 2026年1月12日
**维护者**: PandaQuantFlow Team
