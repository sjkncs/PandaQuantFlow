# 🚀 LLM多密钥系统快速启动

## ✅ 已完成配置

### 3个API密钥 + 4个金融模型

```
✅ 卡密1: sk-ljllswzyhlrrskmolcxayvemftjuzrgbiuwnedfnfjckxnpu
✅ 卡密2: sk-ridvotghvcwjqormgutcojreigmszrrqhijbezbwhbvhcedw
✅ 卡密3: sk-kefpbqtbxodjvubcvoytodjsqtmaodriwtmreialxjbonstr

✅ DeepSeek V3 - 代码分析、因子生成
✅ Claude 4.5 - 策略推理、风险评估
✅ Kimi K2 - 长文本、财报分析
✅ Qwen 3 - 中文理解、市场解读
```

---

## 🎯 核心特性

1. **自动轮询** - 3个密钥轮流使用，负载均衡
2. **故障转移** - 单个密钥失败自动切换
3. **智能重试** - 每个密钥重试3次
4. **多模型** - 4种模型适配不同场景

---

## 🧪 立即测试

```powershell
# 测试多密钥负载均衡
py test_llm_multi_key.py
```

**测试内容**:
- ✅ 3个密钥轮询
- ✅ DeepSeek V3 测试
- ✅ Kimi K2 测试
- ✅ 密钥状态监控

---

## 💻 使用示例

### 基础用法

```python
from panda_common.llm_manager import get_llm_manager

# 获取管理器
llm = get_llm_manager()

# 调用LLM（自动轮询密钥）
response = llm.chat_completion(
    messages=[
        {"role": "user", "content": "分析这个因子"}
    ]
)

print(response['choices'][0]['message']['content'])
```

### 指定模型

```python
# 使用DeepSeek生成因子代码
response = llm.chat_completion(
    messages=[{"role": "user", "content": "写一个RSI因子"}],
    model=llm.get_model('deepseek')
)

# 使用Kimi分析长文本
response = llm.chat_completion(
    messages=[{"role": "user", "content": "分析这份财报"}],
    model=llm.get_model('kimi'),
    max_tokens=4000
)

# 使用Claude进行策略推理
response = llm.chat_completion(
    messages=[{"role": "user", "content": "设计量化策略"}],
    model=llm.get_model('claude')
)

# 使用Qwen解读市场
response = llm.chat_completion(
    messages=[{"role": "user", "content": "解读今日行情"}],
    model=llm.get_model('qwen')
)
```

---

## 🔄 工作原理

### 轮询机制

```
请求1 → 卡密1 → 成功 ✅
请求2 → 卡密2 → 成功 ✅
请求3 → 卡密3 → 成功 ✅
请求4 → 卡密1 → 成功 ✅ (循环)
```

### 故障转移

```
请求 → 卡密1 (尝试1) → 失败
     → 卡密1 (尝试2) → 失败
     → 卡密1 (尝试3) → 失败
     → 切换卡密2 (尝试1) → 成功 ✅
```

---

## 📊 模型选择指南

| 任务 | 推荐模型 | 命令 |
|------|---------|------|
| 因子代码 | DeepSeek V3 | `llm.get_model('deepseek')` |
| 财报分析 | Kimi K2 | `llm.get_model('kimi')` |
| 策略设计 | Claude 4.5 | `llm.get_model('claude')` |
| 市场解读 | Qwen 3 | `llm.get_model('qwen')` |

---

## 🚀 重启服务

```powershell
# 重启服务以应用LLM配置
py start_server_fixed.py
```

启动后应该看到：

```
路由加载状态:
  ✅ 因子API
  ✅ LLM API  ← 现在支持多密钥
  ✅ Web界面
```

---

## 📡 API端点

### 通过HTTP调用

```bash
curl -X POST http://127.0.0.1:8111/llm/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "分析因子"}
    ]
  }'
```

### 访问API文档

```
http://127.0.0.1:8111/docs
```

找到 `panda_llm` 标签测试。

---

## 💰 余额查询

访问: https://siliconflow.ly-y.cn/

输入API密钥查询余额。

---

## 🎯 下一步

```powershell
# 1. 测试多密钥系统
py test_llm_multi_key.py

# 2. 重启服务
py start_server_fixed.py

# 3. 开始使用
# - 因子代码生成
# - 财报分析
# - 策略设计
# - 市场解读
```

---

## ✅ 配置文件位置

- **配置**: `panda_common/panda_common/config.yaml`
- **管理器**: `panda_common/panda_common/llm_manager.py`
- **测试**: `test_llm_multi_key.py`
- **文档**: `MULTI_KEY_LLM_GUIDE.md`

---

## 🎉 完成！

您现在拥有：

✅ **3个API密钥** - 自动轮询，防止额度不足
✅ **4个金融模型** - 适配不同分析场景
✅ **自动故障转移** - 单个密钥失败自动切换
✅ **智能负载均衡** - 均衡分配请求负载

**开始使用强大的LLM金融分析能力！** 🚀
