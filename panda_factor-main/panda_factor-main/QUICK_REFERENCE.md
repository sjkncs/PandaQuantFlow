# 🚀 PandaFactor快速参考

## ✅ 修复完成

- ✅ 移除付费模型（Kimi、Claude）
- ✅ 添加4个免费模型
- ✅ 更新API端点
- ✅ 修复测试脚本

---

## 🎯 4个免费模型

```
1. DeepSeek V3      → 因子代码生成
2. Qwen 2.5 (72B)   → 中文市场分析
3. Qwen Coder (32B) → 算法实现
4. GLM-4 (9B)       → 通用对话
```

---

## 🚀 立即开始

### 1. 重启服务
```powershell
py start_server_fixed.py
```

### 2. 测试模型
```powershell
py test_llm_multi_key.py
```

### 3. 访问界面
```
http://127.0.0.1:8111/factor/
```

---

## 📡 API端点

### 获取模型列表
```bash
GET http://127.0.0.1:8111/llm/models
```

### 切换模型
```bash
POST http://127.0.0.1:8111/llm/switch_model
Content-Type: application/json

{
  "model_type": "deepseek"  # 或 qwen, qwen_coder, glm
}
```

### 查看状态
```bash
GET http://127.0.0.1:8111/llm/status
```

---

## 💻 代码使用

### 基础用法
```python
from panda_common.llm_manager import get_llm_manager

llm = get_llm_manager()
response = llm.chat_completion(
    messages=[{"role": "user", "content": "你的问题"}]
)
```

### 指定模型
```python
# DeepSeek - 代码生成
response = llm.chat_completion(
    messages=[{"role": "user", "content": "写RSI因子"}],
    model=llm.get_model('deepseek')
)

# Qwen - 市场分析
response = llm.chat_completion(
    messages=[{"role": "user", "content": "分析市场"}],
    model=llm.get_model('qwen')
)
```

---

## 🎨 UI优化

详见 `UI_OPTIMIZATION_GUIDE.md`

主要改进：
- 卡片式布局
- 浮动聊天窗口
- 渐变色设计
- 实时状态指示

---

## 📚 完整文档

1. `FIXES_AND_UPDATES.md` - 修复总结
2. `UI_OPTIMIZATION_GUIDE.md` - UI优化指南
3. `FINAL_SUMMARY.md` - 完整总结
4. `QUICK_START_LLM.md` - LLM快速开始

---

## ✅ 核心特性

- ✅ 3个API密钥并联
- ✅ 4个免费模型
- ✅ 自动轮询
- ✅ 故障转移
- ✅ 完全免费

**🎉 开始使用免费LLM进行因子开发！**
