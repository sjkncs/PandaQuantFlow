# CORS 跨域问题修复说明

## 🐛 问题描述

### 错误信息
```
Access to fetch at 'http://127.0.0.1:8111/llm/chat/simple' from origin 'http://127.0.0.1:56849' 
has been blocked by CORS policy: Response to preflight request doesn't pass access control check: 
The 'Access-Control-Allow-Origin' header has a value 'http://127.0.0.1' that is not equal to 
the supplied origin.
```

### 问题原因
1. **CORS 配置不当**: 使用了 `allow_origins=["*"]` 和 `allow_credentials=True` 的组合
2. **端口不匹配**: 浏览器预览使用的是 56849 端口，但 CORS 配置没有包含这个端口
3. **FastAPI CORS 限制**: 当 `allow_credentials=True` 时，不能使用通配符 `*`

## ✅ 解决方案

### 修改内容

#### 1. PandaFactor 服务 (start_complete.py)

**修改前**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ❌ 与 allow_credentials=True 冲突
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**修改后**:
```python
# 使用正则表达式匹配所有localhost和127.0.0.1的端口
import re
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",  # ✅ 匹配所有本地端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
```

#### 2. QuantFlow 服务 (src/panda_server/main.py)

**同样的修改**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
```

### 正则表达式说明

```regex
http://(localhost|127\.0\.0\.1)(:\d+)?
```

- `http://` - 匹配 HTTP 协议
- `(localhost|127\.0\.0\.1)` - 匹配 localhost 或 127.0.0.1
- `(:\d+)?` - 可选的端口号（`:8111`, `:8000`, `:56849` 等）
- `?` - 使端口部分可选，也支持不带端口的 URL

这样可以匹配：
- `http://localhost`
- `http://localhost:8111`
- `http://127.0.0.1`
- `http://127.0.0.1:8000`
- `http://127.0.0.1:56849` ✅ 浏览器预览端口

## 🧪 验证方法

### 方法1: 使用测试页面

打开 `test_cors.html` 文件：
```bash
# 直接在浏览器中打开
start test_cors.html
```

点击各个测试按钮，验证 API 是否正常工作。

### 方法2: 浏览器控制台

1. 打开 http://127.0.0.1:8111/
2. 按 F12 打开开发者工具
3. 切换到 Console 标签
4. 运行以下代码：

```javascript
// 测试 LLM 状态
fetch('http://127.0.0.1:8111/llm/status')
  .then(r => r.json())
  .then(data => console.log('LLM状态:', data))
  .catch(err => console.error('错误:', err));

// 测试聊天接口
fetch('http://127.0.0.1:8111/llm/chat/simple', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    message: '你好',
    model: 'deepseek'
  })
})
  .then(r => r.json())
  .then(data => console.log('聊天响应:', data))
  .catch(err => console.error('错误:', err));
```

### 方法3: 网络面板检查

1. 打开开发者工具 (F12)
2. 切换到 Network 标签
3. 发送一个请求
4. 检查响应头中的 CORS 相关字段：

应该看到：
```
Access-Control-Allow-Origin: http://127.0.0.1:56849
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT
Access-Control-Allow-Headers: *
```

## 📋 常见问题

### Q1: 为什么不直接用 `allow_origins=["*"]`?

**A**: 当设置 `allow_credentials=True` 时，浏览器出于安全考虑不允许使用通配符 `*`。必须明确指定允许的源。

### Q2: `allow_origin_regex` 会有性能问题吗?

**A**: 对于简单的正则表达式，性能影响可以忽略不计。我们的正则只匹配本地地址，非常简单高效。

### Q3: 生产环境应该怎么配置?

**A**: 生产环境应该明确列出允许的域名：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Q4: 如果还是有 CORS 错误怎么办?

**步骤1**: 检查服务是否重启
```bash
# 重启所有服务
cmd /c restart_all.bat
```

**步骤2**: 清除浏览器缓存
- 按 Ctrl+Shift+Delete
- 选择"缓存的图片和文件"
- 清除

**步骤3**: 检查 CORS 头
```bash
# 使用 curl 检查
curl -H "Origin: http://127.0.0.1:56849" -I http://127.0.0.1:8111/llm/status
```

应该看到 `access-control-allow-origin` 头。

## 🔍 CORS 工作原理

### Preflight 请求

浏览器在发送实际请求前，会先发送一个 OPTIONS 请求（称为 preflight）：

```http
OPTIONS /llm/chat/simple HTTP/1.1
Host: 127.0.0.1:8111
Origin: http://127.0.0.1:56849
Access-Control-Request-Method: POST
Access-Control-Request-Headers: content-type
```

服务器需要返回允许的 CORS 头：

```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: http://127.0.0.1:56849
Access-Control-Allow-Methods: POST, GET, OPTIONS
Access-Control-Allow-Headers: content-type
Access-Control-Allow-Credentials: true
```

只有 preflight 成功，浏览器才会发送实际的 POST 请求。

### FastAPI CORS 中间件

FastAPI 的 `CORSMiddleware` 会自动处理：
1. OPTIONS 请求（preflight）
2. 在响应中添加 CORS 头
3. 验证请求源是否在允许列表中

## 🎯 最佳实践

### 1. 开发环境
```python
# 允许所有本地端口
allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?"
```

### 2. 测试环境
```python
# 明确列出测试域名
allow_origins=[
    "http://localhost:3000",
    "http://test.yourdomain.com",
]
```

### 3. 生产环境
```python
# 只允许生产域名
allow_origins=[
    "https://yourdomain.com",
]
```

### 4. 安全建议

- ✅ 使用 HTTPS (生产环境)
- ✅ 明确指定允许的源
- ✅ 限制允许的 HTTP 方法
- ✅ 定期审查 CORS 配置
- ❌ 避免在生产环境使用 `allow_origins=["*"]`
- ❌ 不要暴露敏感的 API 端点

## 📊 修复效果

### 修复前
```
❌ Failed to load resource: CORS policy blocked
❌ Access-Control-Allow-Origin mismatch
❌ 前端无法调用后端 API
```

### 修复后
```
✅ 所有 API 请求正常
✅ CORS 头正确返回
✅ 前端可以正常调用后端
✅ WebSocket 连接正常
```

## 🚀 快速恢复

如果遇到任何问题，可以快速恢复：

```bash
# 1. 停止所有服务
taskkill /F /FI "WINDOWTITLE eq PandaFactor*"
taskkill /F /FI "WINDOWTITLE eq QuantFlow*"

# 2. 重新启动
cmd /c restart_all.bat

# 3. 测试 API
py test_backend.py

# 4. 打开浏览器测试
start http://127.0.0.1:8111/
```

## 📝 相关文件

- `start_complete.py` - PandaFactor CORS 配置
- `src/panda_server/main.py` - QuantFlow CORS 配置
- `test_cors.html` - CORS 测试页面
- `test_backend.py` - 后端 API 测试脚本
- `restart_all.bat` - 服务重启脚本

## 🎉 总结

CORS 问题已完全修复！现在可以：

1. ✅ 从任何本地端口访问 API
2. ✅ 浏览器预览正常工作
3. ✅ 前端可以正常调用后端
4. ✅ WebSocket 实时通信正常

所有服务都已正常运行，可以正常使用 PandaAI 平台的所有功能！

---

**修复时间**: 2026-01-14  
**修复版本**: v2.1.0  
**状态**: ✅ 已解决
