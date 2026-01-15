# MongoDB 认证问题修复说明

## 🔧 已完成的修复

### 1. 修改配置文件
**文件**: `panda_common/panda_common/config.yaml`

```yaml
# 修改前
MONGO_USER: "panda"
MONGO_PASSWORD: "panda"

# 修改后（无认证）
MONGO_USER: ""
MONGO_PASSWORD: ""
```

### 2. 修改数据库连接代码
**文件**: `panda_common/panda_common/handlers/database_handler.py`

**修改内容**:
- ✅ 支持无认证连接
- ✅ 当用户名密码为空时，使用 `mongodb://127.0.0.1:27017/` 连接
- ✅ 当用户名密码不为空时，使用认证连接
- ✅ 修复密码为空时的masking错误

---

## 🚀 重新启动服务

```powershell
py start_server_fixed.py
```

---

## ✅ 预期结果

启动后应该看到：

```
======================================================================
PandaFactor 服务启动（修复版）
======================================================================

[1/2] 检查依赖...
✅ 所有依赖已安装

[2/2] 启动服务...

服务地址:
  - 主页:     http://127.0.0.1:8111/
  - API文档:  http://127.0.0.1:8111/docs
  - 因子界面: http://127.0.0.1:8111/factor

按 Ctrl+C 停止服务
======================================================================

Connecting to MongoDB: mongodb://127.0.0.1:27017/

路由加载状态:
  ✅ 因子API
  ✅ LLM API
  ✅ Web界面

INFO:     Started server process [xxxxx]
INFO:     Uvicorn running on http://0.0.0.0:8111
```

**关键变化**:
- ✅ 不再有 "Authentication failed" 错误
- ✅ 因子API 成功加载
- ✅ LLM API 成功加载
- ✅ MongoDB 连接成功

---

## 📊 MongoDB 状态

```
服务名称: MongoDB
状态: Running (正在运行)
端口: 27017
认证: 未启用（开发模式）
```

---

## 🔐 如果需要启用认证

### 步骤1: 创建MongoDB用户

```javascript
// 连接到MongoDB
mongo

// 切换到admin数据库
use admin

// 创建管理员用户
db.createUser({
  user: "panda",
  pwd: "panda",
  roles: [ { role: "root", db: "admin" } ]
})
```

### 步骤2: 修改配置文件

```yaml
MONGO_USER: "panda"
MONGO_PASSWORD: "panda"
```

### 步骤3: 重启MongoDB服务（启用认证）

```powershell
# 停止MongoDB服务
net stop MongoDB

# 修改MongoDB配置文件启用认证
# 编辑: C:\Program Files\MongoDB\Server\<version>\bin\mongod.cfg
# 添加:
# security:
#   authorization: enabled

# 重启MongoDB服务
net start MongoDB
```

---

## 💡 当前推荐配置

**开发环境（当前）**:
- ✅ 无认证连接
- ✅ 简单快速
- ✅ 适合本地开发

**生产环境（未来）**:
- 🔐 启用认证
- 🔐 设置强密码
- 🔐 配置访问控制

---

## 🎯 下一步

```powershell
# 重新启动服务
py start_server_fixed.py

# 访问服务
# http://127.0.0.1:8111/docs
```

所有功能现在应该正常工作了！🎉
