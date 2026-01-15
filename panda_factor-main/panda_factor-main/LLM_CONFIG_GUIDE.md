# LLM聊天功能配置指南

## ✅ 已完成配置

### 硅基流动API配置

**配置文件**: `panda_common/panda_common/config.yaml`

```yaml
# LLM配置 - 硅基流动API
LLM_API_KEY: "sk-ljllswzyhlrrskmolcxayvemftjuzrgbiuwnedfnfjckxnpu"
LLM_MODEL: "Pro/moonshotai/Kimi-K2-Thinking"
LLM_BASE_URL: "https://api.siliconflow.cn/v1"
```

---

## 🔑 可用的API密钥

您有3个API密钥可以使用：

### 卡密1（当前使用）
```
sk-ljllswzyhlrrskmolcxayvemftjuzrgbiuwnedfnfjckxnpu
```

### 卡密2（备用）
```
sk-ridvotghvcwjqormgutcojreigmszrrqhijbezbwhbvhcedw
```

### 卡密3（备用）
```
sk-kefpbqtbxodjvubcvoytodjsqtmaodriwtmreialxjbonstr
```

**查询余额**: https://siliconflow.ly-y.cn/

---

## 🤖 可用的模型

### 1. Kimi-K2-Thinking（当前使用）
```yaml
LLM_MODEL: "Pro/moonshotai/Kimi-K2-Thinking"
```
- 月之暗面Kimi模型
- 支持长文本
- 推理能力强

### 2. Claude 4.5 Thinking
```yaml
LLM_MODEL: "claude-4.5-thinking"
```
- Anthropic Claude模型
- 思维链推理
- 高质量输出

### 3. Qwen 3
```yaml
LLM_MODEL: "Qwen/Qwen2.5-72B-Instruct"
```
- 阿里通义千问
- 中文能力强
- 多任务支持

### 4. DeepSeek V3
```yaml
LLM_MODEL: "deepseek-ai/DeepSeek-V3"
```
- DeepSeek最新模型
- 代码能力强
- 推理性能优秀

---

## 🧪 测试LLM功能

### 运行测试脚本

```powershell
py test_llm.py
```

**测试内容**:
- ✅ 读取配置
- ✅ 测试API连接
- ✅ 发送测试消息
- ✅ 显示响应内容
- ✅ 显示Token使用情况

### 预期输出

```
======================================================================
测试LLM聊天功能
======================================================================

[1/3] 读取配置...
  API Key: sk-ljllswzyhlrrskmol...
  模型: Pro/moonshotai/Kimi-K2-Thinking
  Base URL: https://api.siliconflow.cn/v1

[2/3] 测试API连接...
  发送请求到: https://api.siliconflow.cn/v1/chat/completions
  使用模型: Pro/moonshotai/Kimi-K2-Thinking

✅ API连接成功！

[3/3] 响应内容:
----------------------------------------------------------------------
你好！我是Kimi，一个由月之暗面科技开发的AI助手...
----------------------------------------------------------------------

Token使用情况:
  输入: 15 tokens
  输出: 25 tokens
  总计: 40 tokens

======================================================================
🎉 LLM功能测试完成！
======================================================================
```

---

## 🚀 重启服务以应用配置

```powershell
# 停止当前服务（Ctrl+C）
# 重新启动
py start_server_fixed.py
```

启动后，LLM API应该成功加载：

```
路由加载状态:
  ✅ 因子API
  ✅ LLM API  ← 应该显示这个
  ✅ Web界面
```

---

## 📡 LLM API端点

### 聊天补全
```
POST /llm/chat/completions
```

**请求示例**:
```json
{
  "model": "Pro/moonshotai/Kimi-K2-Thinking",
  "messages": [
    {
      "role": "user",
      "content": "帮我分析一下这个因子的逻辑"
    }
  ],
  "max_tokens": 1000,
  "temperature": 0.7
}
```

### 访问API文档
```
http://127.0.0.1:8111/docs
```

在文档中找到 `panda_llm` 标签，可以直接测试LLM API。

---

## 🔄 切换模型

### 方法1: 修改配置文件

编辑 `panda_common/panda_common/config.yaml`:

```yaml
# 切换到DeepSeek V3
LLM_MODEL: "deepseek-ai/DeepSeek-V3"

# 或切换到Qwen
LLM_MODEL: "Qwen/Qwen2.5-72B-Instruct"

# 或切换到Claude
LLM_MODEL: "claude-4.5-thinking"
```

### 方法2: 通过API请求指定

在API请求中直接指定模型：

```json
{
  "model": "deepseek-ai/DeepSeek-V3",
  "messages": [...]
}
```

---

## 🔄 切换API密钥

如果当前密钥余额不足，修改配置文件：

```yaml
# 使用卡密2
LLM_API_KEY: "sk-ridvotghvcwjqormgutcojreigmszrrqhijbezbwhbvhcedw"

# 或使用卡密3
LLM_API_KEY: "sk-kefpbqtbxodjvubcvoytodjsqtmaodriwtmreialxjbonstr"
```

---

## 💰 查询余额

访问: https://siliconflow.ly-y.cn/

输入您的API密钥查询剩余额度。

---

## 🎯 使用场景

### 1. 因子分析
```
用户: "帮我分析这个因子的逻辑：close.rolling(20).mean()"
LLM: "这是一个20日移动平均线因子..."
```

### 2. 代码生成
```
用户: "帮我写一个RSI因子"
LLM: "以下是RSI因子的实现代码..."
```

### 3. 策略建议
```
用户: "这个因子的夏普比率是1.2，如何优化？"
LLM: "可以从以下几个方面优化..."
```

---

## 📊 模型对比

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| Kimi-K2-Thinking | 长文本、推理强 | 复杂分析、长文档 |
| Claude 4.5 | 思维链、高质量 | 深度推理、创意写作 |
| Qwen 3 | 中文优秀、多任务 | 中文对话、通用任务 |
| DeepSeek V3 | 代码能力强 | 代码生成、技术分析 |

---

## ✅ 配置完成检查清单

- [x] 配置API密钥
- [x] 配置Base URL
- [x] 选择模型
- [ ] 运行测试脚本 `py test_llm.py`
- [ ] 重启服务 `py start_server_fixed.py`
- [ ] 验证LLM API加载成功
- [ ] 测试聊天功能

---

## 🎉 下一步

```powershell
# 1. 测试LLM功能
py test_llm.py

# 2. 重启服务
py start_server_fixed.py

# 3. 访问API文档测试
# http://127.0.0.1:8111/docs
```

**LLM聊天功能已配置完成！** 🚀
