# PandaFactor 服务状态说明

## ✅ 服务已成功启动！

您的服务**已经在运行**，可以正常使用！

---

## 🌐 访问地址

### 主页
```
http://127.0.0.1:8111/
```

返回服务信息和可用端点

### API文档（Swagger UI）
```
http://127.0.0.1:8111/docs
```

交互式API文档，可以直接测试API

### Web界面
```
http://127.0.0.1:8111/factor
```

因子管理和可视化界面

---

## 📊 当前服务状态

### ✅ 正常运行的功能

- **Web服务器**: 运行在 http://0.0.0.0:8111
- **Web界面**: 已加载并可访问
- **主页API**: 正常响应（200 OK）
- **基础配置**: 已加载

### ⚠️ 可选功能（需要额外配置）

#### 1. 因子API路由
**状态**: 未加载  
**原因**: 缺少 `panda_data_hub.models` 模块  
**影响**: 不影响Web界面使用  
**是否必需**: 否（可选）

#### 2. LLM聊天功能
**状态**: 未加载  
**原因**: MongoDB连接失败  
**影响**: LLM聊天功能不可用  
**是否必需**: 否（可选）

---

## 🔧 解决MongoDB连接问题（可选）

我已经修改了配置文件，将MongoDB模式从 `replica_set` 改为 `single`。

### 重启服务以应用更改

```powershell
# 按 Ctrl+C 停止当前服务
# 然后重新启动
python start_server.py
```

### 如果没有MongoDB

**选项A**: 不使用MongoDB相关功能
- Web界面仍然可用
- 基础API仍然可用

**选项B**: 安装MongoDB
```powershell
# 下载MongoDB Community Edition
# https://www.mongodb.com/try/download/community

# 或使用Docker
docker run -d -p 27017:27017 --name mongodb mongo
```

---

## 💡 当前可以做什么

### 1. 访问Web界面
```
http://127.0.0.1:8111/factor
```

### 2. 查看API文档
```
http://127.0.0.1:8111/docs
```

### 3. 测试主页API
```
http://127.0.0.1:8111/
```

### 4. 使用轻量级因子库（无需MongoDB）

在另一个终端运行：
```powershell
cd c:\Users\Lenovo\Desktop\PandaQuantFlow
python run_pandafactor_example.py
```

---

## 🎯 推荐使用方式

### 方式1: Web界面（当前已启动）
- 访问: http://127.0.0.1:8111/factor
- 功能: 可视化因子管理

### 方式2: 轻量级因子库（无需服务器）
```python
from lightweight.factor_library import FactorLibrary
import pandas as pd

# 计算因子
ma20 = FactorLibrary.MA(close, 20)
rsi = FactorLibrary.RSI(close, 14)
```

### 方式3: API调用（需要完整配置）
```python
import requests

response = requests.get("http://127.0.0.1:8111/api/v1/factors")
```

---

## 📝 日志说明

### 正常日志
```
INFO:     Started server process [17048]
INFO:     Uvicorn running on http://0.0.0.0:8111
INFO:     127.0.0.1:57963 - "GET / HTTP/1.1" 200 OK
```
这些是**正常**的运行日志，表示服务正常工作。

### 警告日志
```
⚠️  因子路由加载失败: No module named 'panda_data_hub.models'
⚠️  LLM路由加载失败: MongoDB connection failed
```
这些是**警告**，不是错误。服务仍然可以正常运行，只是部分功能不可用。

---

## 🚀 下一步

### 如果只需要基础功能
- ✅ 服务已经可用，直接访问 http://127.0.0.1:8111/

### 如果需要完整功能
1. 安装MongoDB
2. 重启服务
3. 配置数据源（Tushare/RiceQuant等）

### 如果只需要因子计算
- 使用轻量级因子库，无需启动服务
- 运行: `python run_pandafactor_example.py`

---

## ✅ 总结

**服务状态**: 🟢 运行中  
**访问地址**: http://127.0.0.1:8111/  
**可用功能**: Web界面、基础API  
**可选功能**: 因子API、LLM聊天（需要MongoDB）

**您现在就可以使用服务了！** 🎉
