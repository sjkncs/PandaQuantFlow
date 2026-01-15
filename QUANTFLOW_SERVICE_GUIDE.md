# PandaQuantFlow 服务启动指南

## 📋 当前项目状态分析

### ✅ 已有的服务

您的项目中已经包含了**PandaFactor服务**，但**不是**您提到的QuantFlow工作流服务。

#### 1. PandaFactor Web服务

**位置**: `panda_factor-main/panda_factor-main/panda_factor_server/`

**启动方式**:
```bash
# 方式1: 使用Python模块
cd c:\Users\Lenovo\Desktop\PandaQuantFlow\panda_factor-main\panda_factor-main
python -m panda_factor_server

# 方式2: 直接运行
cd panda_factor_server
python -m panda_factor_server.__main__
```

**服务端口**: `8111`

**访问地址**:
- 主页: http://127.0.0.1:8111/
- 因子界面: http://127.0.0.1:8111/factor
- API文档: http://127.0.0.1:8111/docs

**功能**:
- ✅ 因子管理
- ✅ 因子计算
- ✅ LLM集成
- ✅ Web界面

---

### ❌ 缺少的服务

您提到的**QuantFlow工作流服务**（包含超级图表和工作流UI）在当前项目中**不存在**。

**您提到的路径**:
- `src/panda_server/main.py` ❌ 不存在
- `src/panda_plugins/custom/` ❌ 不存在
- 超级图表: http://127.0.0.1:8000/charts/ ❌ 不存在
- 工作流: http://127.0.0.1:8000/quantflow/ ❌ 不存在

---

## 🚀 解决方案

### 方案1: 启动现有的PandaFactor服务 (推荐)

使用项目中已有的服务：

```bash
cd c:\Users\Lenovo\Desktop\PandaQuantFlow\panda_factor-main\panda_factor-main
python -m panda_factor_server
```

访问: http://127.0.0.1:8111/factor

---

### 方案2: 创建QuantFlow工作流服务 (新功能)

我可以为您创建一个完整的QuantFlow工作流系统，包括：

1. **工作流引擎**
   - 节点系统
   - 流程编排
   - 可视化编辑器

2. **超级图表**
   - 因子可视化
   - 回测结果展示
   - 实时监控

3. **插件系统**
   - 自定义节点
   - 动态加载
   - 热更新

---

## 📝 创建QuantFlow服务

让我为您创建一个完整的QuantFlow工作流系统：

### 目录结构

```
PandaQuantFlow/
├── src/
│   ├── panda_server/
│   │   └── main.py              # 主服务入口
│   ├── panda_plugins/
│   │   ├── base.py              # 基础节点类
│   │   └── custom/
│   │       ├── examples/        # 示例插件
│   │       └── __init__.py
│   ├── panda_workflow/
│   │   ├── engine.py            # 工作流引擎
│   │   ├── nodes.py             # 内置节点
│   │   └── executor.py          # 执行器
│   └── panda_charts/
│       ├── charts.py            # 图表生成
│       └── templates/           # 图表模板
```

### 核心功能

1. **BaseWorkNode** - 工作节点基类
2. **WorkflowEngine** - 工作流引擎
3. **ChartGenerator** - 图表生成器
4. **PluginLoader** - 插件加载器

---

## 🎯 您想要哪种方案？

### 选项A: 使用现有服务 (5分钟)

```bash
# 1. 配置依赖
cd panda_factor-main\panda_factor-main
pip install -e panda_common
pip install -e panda_data
pip install -e panda_factor
pip install -e panda_llm
pip install -e panda_factor_server

# 2. 启动服务
python -m panda_factor_server

# 3. 访问
# http://127.0.0.1:8111/factor
```

### 选项B: 创建完整QuantFlow系统 (30分钟)

我将为您创建：
- ✅ 完整的工作流引擎
- ✅ 可视化流程编辑器
- ✅ 超级图表系统
- ✅ 自定义插件框架
- ✅ 与现有因子库集成

---

## 💡 建议

**如果您想快速开始**:
- 使用方案A，启动现有的PandaFactor服务
- 已经包含因子管理和Web界面

**如果您需要工作流功能**:
- 选择方案B，我将创建完整的QuantFlow系统
- 包含您提到的所有功能（图表、工作流、插件）

---

## 🔧 快速启动脚本

我已经为您准备了启动脚本，请告诉我您想要：

1. **启动现有PandaFactor服务**
2. **创建新的QuantFlow工作流系统**

---

## 📞 下一步

请回复：
- "启动现有服务" - 我将帮您配置和启动PandaFactor
- "创建QuantFlow" - 我将创建完整的工作流系统

或者直接运行：

```bash
# 快速测试现有服务
cd c:\Users\Lenovo\Desktop\PandaQuantFlow
python -c "print('PandaFactor服务路径检查...')
import os
path = r'panda_factor-main\panda_factor-main\panda_factor_server'
print(f'服务存在: {os.path.exists(path)}')"
```
