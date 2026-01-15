# SCGU 部署指南

## 📁 项目结构

```
PandaQuantFlow/
├── enterprise/              # 企业级版本
│   ├── README.md
│   ├── requirements-enterprise.txt
│   ├── ssl/                # 自监督学习
│   ├── multimodal/         # 多模态融合
│   ├── brain/              # 类脑情感计算
│   ├── scgu/               # SCGU遗忘
│   ├── deployment/         # 生产部署
│   ├── k8s/                # Kubernetes配置
│   └── docs/               # 企业级文档
│
├── lightweight/            # 轻量级版本
│   ├── README.md
│   ├── requirements-lightweight.txt
│   ├── quick_start.py      # 快速开始
│   ├── ssl/                # 自监督学习
│   ├── examples/           # 示例代码
│   └── docs/               # 轻量级文档
│
├── VERSION_COMPARISON.md   # 版本对比
├── DEPLOYMENT_GUIDE.md     # 本文件
└── shared/                 # 共享代码
    ├── utils/
    └── data/
```

---

## 🚀 快速部署

### 轻量级版本 (个人/小团队)

```bash
# 1. 克隆项目
git clone https://github.com/PandaQuantFlow/SCGU.git
cd SCGU/lightweight

# 2. 创建环境
conda create -n scgu-light python=3.9 -y
conda activate scgu-light

# 3. 安装依赖
pip install -r requirements-lightweight.txt

# 4. 运行快速开始
python quick_start.py

# 5. 训练自己的模型
python train.py --data your_data.csv --epochs 50
```

### 企业级版本 (生产环境)

```bash
# 1. 克隆项目
git clone https://github.com/PandaQuantFlow/SCGU-Enterprise.git
cd SCGU-Enterprise/enterprise

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入配置

# 3. 使用Docker部署
docker-compose up -d

# 4. 或使用Kubernetes部署
kubectl apply -f k8s/

# 5. 验证部署
curl http://localhost:8000/health
```

---

## 💻 开发环境设置

### 轻量级版本

```bash
# 最小要求
- Python 3.8+
- 8GB RAM
- 可选: NVIDIA GPU (GTX 1060+)

# 推荐配置
- Python 3.9
- 16GB RAM
- NVIDIA GPU (RTX 3060+)
```

### 企业级版本

```bash
# 最小要求
- Python 3.9+
- 64GB RAM
- NVIDIA GPU (V100 × 4)
- Kubernetes集群

# 推荐配置
- Python 3.9
- 256GB RAM
- NVIDIA GPU (A100 × 8)
- Kubernetes集群 (3+ nodes)
```

---

## 📊 使用场景选择

### 使用轻量级版本

```python
# 场景1: 快速原型验证
from lightweight.ssl import SimpleContrastiveLearning

model = SimpleContrastiveLearning()
model.train(data, epochs=50)

# 场景2: 学术研究
model = SimpleContrastiveLearning()
results = model.evaluate(test_data)
publish_paper(results)

# 场景3: 个人项目
model = SimpleContrastiveLearning()
model.save('my_model.pt')
```

### 使用企业级版本

```python
# 场景1: 生产部署
from enterprise.deployment import ProductionDeployer

deployer = ProductionDeployer(
    model=model,
    replicas=10,
    auto_scaling=True
)
deployer.deploy()

# 场景2: 分布式训练
from enterprise.ssl import DistributedTrainer

trainer = DistributedTrainer(num_gpus=8)
model = trainer.train(large_dataset)

# 场景3: 实时监控
from enterprise.monitoring import ModelMonitor

monitor = ModelMonitor(model)
monitor.start()
```

---

## 🔄 版本升级

### 从轻量级升级到企业级

```bash
# 1. 导出轻量级模型
python lightweight/export_model.py --output model.pt

# 2. 转换为企业级格式
python enterprise/convert_model.py --input model.pt --output enterprise_model.pt

# 3. 部署企业级模型
python enterprise/deploy.py --model enterprise_model.pt
```

---

## 📞 技术支持

### 轻量级版本
- GitHub Issues: https://github.com/PandaQuantFlow/SCGU/issues
- 社区论坛: https://community.pandaquantflow.com
- 文档: https://docs.pandaquantflow.com/lightweight

### 企业级版本
- 邮件: enterprise@pandaquantflow.com
- 电话: +86-xxx-xxxx-xxxx
- 专属Slack频道
- 7×24小时技术支持

---

## 🎯 最佳实践

### 轻量级版本

1. **从小数据集开始**: 先用1000条数据验证
2. **使用预训练模型**: 节省训练时间
3. **定期保存检查点**: 避免训练中断
4. **监控GPU使用**: 避免OOM

### 企业级版本

1. **使用分布式训练**: 充分利用GPU集群
2. **启用模型监控**: 实时追踪性能
3. **配置自动扩缩容**: 应对流量波动
4. **定期备份**: 保护生产数据
5. **灰度发布**: 降低上线风险

---

## 📝 常见问题

### Q: 如何选择版本？
A: 
- 个人学习/研究 → 轻量级
- 小团队POC → 轻量级
- 生产环境 → 企业级
- 大规模数据 → 企业级

### Q: 轻量级版本有功能限制吗？
A: 核心算法完全相同，但缺少生产级功能（监控、分布式等）

### Q: 可以免费试用企业级版本吗？
A: 可以，联系sales@pandaquantflow.com申请30天试用

### Q: 如何获得技术支持？
A: 
- 轻量级: GitHub Issues
- 企业级: 专属技术支持团队

---

**祝您使用愉快！** 🎉
