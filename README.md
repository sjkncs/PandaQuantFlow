# 🐼 PandaQuantFlow - AI驱动的量化因子平台

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**基于 FastAPI + LLM 的智能量化因子开发与回测平台**

[功能特点](#-功能特点) • [快速开始](#-快速开始) • [架构设计](#-架构设计) • [文档](#-文档) • [贡献](#-贡献)

</div>

---

## 📖 项目简介

PandaQuantFlow 是一个集成了大语言模型（LLM）的量化交易平台，旨在通过 AI 辅助量化策略开发、因子分析和回测。平台提供友好的 Web 界面，支持自然语言交互，让量化研究更加高效。

### 🎯 核心优势

- 🤖 **AI 助手**: 集成 DeepSeek V3、Qwen 等多个 LLM 模型，支持智能对话和代码生成
- 📊 **因子分析**: 完整的因子开发、测试、回测工作流
- 🎨 **现代 UI**: 基于 Web 的专业界面，支持实时市场数据展示
- 🔧 **高可扩展**: 模块化设计，易于扩展和定制
- 🚀 **高性能**: 基于 FastAPI 异步框架，支持高并发

---

## ✨ 功能特点

### 1. 智能对话系统
- 🗣️ 支持多模型切换（DeepSeek、Qwen、GLM-4 等）
- 💬 自然语言因子开发
- 📝 代码生成与优化建议
- 🔄 上下文记忆与多轮对话

### 2. 因子分析
- 📈 技术指标计算（MA、MACD、RSI 等）
- 📊 因子回测与评估
- 📉 可视化图表生成
- 💾 因子库管理

### 3. 数据分析
- 🌐 实时市场概览
- 📑 股票技术分析
- 📊 自定义图表生成
- 🔍 数据探索与洞察

### 4. 系统特性
- 🔐 多 API 密钥轮询与负载均衡
- 🛡️ 自动故障转移与重试机制
- 📝 完整的日志与监控
- 🔧 灵活的配置管理

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- MongoDB 4.0+（可选）
- 8GB+ RAM
- Windows/Linux/MacOS

### 安装步骤

#### 1. 克隆仓库
```bash
git clone https://github.com/your-username/PandaQuantFlow.git
cd PandaQuantFlow
```

#### 2. 安装依赖
```bash
# 安装 PandaFactor 依赖
cd panda_factor-main/panda_factor-main
pip install -r requirements.txt

# 安装 QuantFlow 依赖
cd ../../
pip install -e .
```

#### 3. 配置 LLM API
编辑配置文件，添加你的 API 密钥：

```yaml
# config.yaml
LLM_API_KEYS:
  - "your-api-key-1"
  - "your-api-key-2"
  - "your-api-key-3"

LLM_BASE_URL: "https://api.siliconflow.cn/v1"
LLM_MODEL: "deepseek-ai/DeepSeek-V3"
```

#### 4. 启动服务

**Windows**:
```bash
# 启动所有服务
restart_all.bat
```

**Linux/MacOS**:
```bash
# 启动 PandaFactor
cd panda_factor-main/panda_factor-main
python start_complete.py

# 启动 QuantFlow
cd ../../src
python -m panda_server.main
```

#### 5. 访问界面
打开浏览器访问：
- **主界面**: http://127.0.0.1:8111/
- **API 文档**: http://127.0.0.1:8111/docs
- **QuantFlow**: http://127.0.0.1:8000/docs

---

## 🏗️ 架构设计

### 系统架构

```
PandaQuantFlow
├── panda_factor-main/          # 因子平台主服务
│   ├── panda_web/              # Web 前端
│   ├── panda_llm/              # LLM 集成
│   ├── panda_factor/           # 因子分析
│   └── panda_common/           # 公共组件
├── src/                        # QuantFlow 服务
│   └── panda_server/           # 数据服务
├── tests/                      # 测试脚本
└── docs/                       # 文档
```

### 技术栈

**后端**:
- FastAPI - 异步 Web 框架
- OpenAI SDK - LLM 集成
- Pandas/NumPy - 数据处理
- Matplotlib - 图表生成
- MongoDB - 数据存储（可选）

**前端**:
- 原生 JavaScript
- CSS3 动画
- 响应式设计

**部署**:
- Uvicorn - ASGI 服务器
- 多进程支持
- 自动重启机制

---

## 📚 文档

### API 文档

#### LLM 接口
```python
# 简单聊天
POST /llm/chat/simple
{
    "message": "帮我生成一个动量因子",
    "model": "deepseek",
    "history": []
}

# 获取模型列表
GET /llm/models

# 查看 LLM 状态
GET /llm/status
```

#### 分析接口
```python
# 市场概览
GET /analysis/market_overview

# 股票分析
POST /analysis/stock
{
    "code": "000001",
    "period": 30,
    "analysis_type": "technical"
}

# 因子回测
POST /analysis/factor
{
    "factor_code": "momentum_20d",
    "backtest_period": 180
}
```

### 配置说明

详细配置文档请参考：
- [快速开始指南](QUICK_START.md)
- [研究方向](RESEARCH_DIRECTIONS_2026_2027.md)
- [问题修复报告](问题修复完成报告.md)

---

## 🧪 测试

### 运行测试
```bash
# 测试所有 API
python test_all_apis.py

# 测试 LLM 功能
python test_llm_api.py

# 测试 CORS
python test_cors_simple.py
```

### 测试覆盖
- ✅ LLM 对话功能
- ✅ 市场数据接口
- ✅ 因子分析功能
- ✅ 图表生成
- ✅ CORS 配置

---

## 🔧 开发指南

### 添加新模型

1. 在配置中添加模型信息：
```yaml
LLM_MODELS:
  custom_model:
    name: "自定义模型"
    model_id: "provider/model-name"
    description: "模型描述"
```

2. 前端调用：
```javascript
const response = await fetch('/llm/chat/simple', {
    method: 'POST',
    body: JSON.stringify({
        message: "你好",
        model: "custom_model"
    })
});
```

### 添加新因子

1. 创建因子类：
```python
from panda_factor import BaseFactor

class MyFactor(BaseFactor):
    def calculate(self, data):
        # 计算逻辑
        return result
```

2. 注册因子：
```python
factor_manager.register("my_factor", MyFactor)
```

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

### 贡献流程
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范
- 遵循 PEP 8 Python 代码规范
- 添加必要的注释和文档字符串
- 编写单元测试
- 确保所有测试通过

---

## 📋 待办事项

- [ ] 支持更多 LLM 模型（Claude、GPT-4 等）
- [ ] 实现流式响应
- [ ] 添加因子可视化
- [ ] 支持多用户系统
- [ ] 实现策略回测引擎
- [ ] 优化性能和并发
- [ ] 完善文档和教程
- [ ] Docker 容器化部署

---

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

感谢以下开源项目：
- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI](https://github.com/openai/openai-python)
- [Pandas](https://pandas.pydata.org/)
- [DeepSeek](https://www.deepseek.com/)
- [Qwen](https://github.com/QwenLM/Qwen)

---

## 📞 联系方式

- 项目主页: https://github.com/your-username/PandaQuantFlow
- 问题反馈: https://github.com/your-username/PandaQuantFlow/issues
- 邮箱:zhiwaisong@gmail.com

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个 Star！⭐**

Made with ❤️ by PandaQuantFlow Team

</div>
