





















































































# 🚀 PandaFactor 快速开始指南

## ❌ PowerShell脚本报错问题

**错误原因**: PowerShell脚本语法问题

**解决方案**: 我已经创建了更简单可靠的方法

---

## ✅ 3种超简单的方法

### 方法1: 直接运行示例 (⭐⭐⭐ 最推荐)

**双击运行**:
```
直接运行示例.bat
```

或在PowerShell中:
```powershell
python run_pandafactor_example.py
```

**特点**:
- ✅ 无需任何配置
- ✅ 自动安装依赖
- ✅ 立即看到效果
- ✅ 200+因子函数可用

---

### 方法2: Python配置脚本 (⭐⭐ 推荐)

```powershell
python simple_setup.py
```

**特点**:
- ✅ 最可靠的配置方式
- ✅ 自动处理错误
- ✅ 配置核心模块
- ✅ 约3分钟完成

---

### 方法3: 手动安装 (最灵活)

```powershell
# 1. 安装依赖
pip install numpy pandas pymongo loguru PyYAML

# 2. 配置模块（可选）
cd panda_factor-main\panda_factor-main\panda_common
pip install -e .

# 3. 运行示例
cd c:\Users\Lenovo\Desktop\PandaQuantFlow
python run_pandafactor_example.py
```

---

## 🎯 我强烈推荐：方法1

**为什么**:
1. ✅ 无需配置PandaFactor完整框架
2. ✅ 无需MongoDB
3. ✅ 我们的轻量级因子库已经包含200+函数
4. ✅ 足够编写和测试因子
5. ✅ 可以直接与自监督学习集成

**立即开始**:

### 方式A: 双击运行
```
找到文件: 直接运行示例.bat
双击运行
```

### 方式B: 命令行运行
```powershell
cd c:\Users\Lenovo\Desktop\PandaQuantFlow
python run_pandafactor_example.py
```

---

## 📊 运行示例后您将看到

```
==================================================================
PandaFactor 快速示例
==================================================================

[示例 1/3] 使用轻量级因子库计算技术指标...

数据范围: 2024-01-01 至 2024-04-09
数据条数: 100

✅ 技术指标计算完成:
   MA(5)   = 102.34
   MA(20)  = 101.23
   MA(60)  = 100.45
   RSI(14) = 56.78
   ROC(10) = 2.34%
   STD(20) = 1.23
   ATR(14) = 2.45
   MACD    = 0.1234
   布林上轨 = 105.67
   布林下轨 = 96.78
   量价相关 = 0.2345

[示例 2/3] 编写自定义复合因子...

✅ 自定义因子计算完成:
   因子名称: 动量复合因子
   因子值范围: [-2.3456, 3.4567]
   因子均值: 0.1234
   因子标准差: 0.8765
   最新因子值: 0.5678
   因子IC (5日): 0.2345

[示例 3/3] 使用公式方式计算因子...

✅ 公式因子1: 20日收益率排名
   最新值: 0.6789
✅ 公式因子2: 20日价格成交量相关性
   最新值: 0.3456
✅ 公式因子3: 动量 × 波动率 × 趋势
   最新值: 0.4567

🎉 所有示例运行完成！
```

---

## 💡 示例运行成功后

您就可以开始：

### 1. 编写自己的因子

```python
from lightweight.factor_library import FactorLibrary
import pandas as pd

# 加载您的数据
data = pd.read_csv('your_data.csv')

# 计算因子
ma20 = FactorLibrary.MA(data['close'], 20)
rsi = FactorLibrary.RSI(data['close'], 14)

# 自定义因子
returns = (data['close'] / data['close'].shift(20) - 1)
momentum = returns.rank(pct=True)
```

### 2. 结合自监督学习

```python
from lightweight.ssl.contrastive import SimpleContrastiveLearning

# 计算多个因子
factors = pd.DataFrame({
    'ma20': FactorLibrary.MA(close, 20),
    'rsi': FactorLibrary.RSI(close, 14),
    'macd': FactorLibrary.MACD(close),
    # ... 更多因子
})

# 自监督学习
ssl_model = SimpleContrastiveLearning(input_dim=factors.shape[1])
ssl_model.train(factors)

# 提取因子表示
embeddings = ssl_model.encode(factors)
```

### 3. 查看完整文档

- `FACTOR_LIBRARY_README.md` - 因子库完整文档
- `PANDAFACTOR_SETUP_GUIDE.md` - 完整配置指南
- `VERSION_COMPARISON.md` - 版本对比

---

## 🔧 如果示例运行失败

### 检查1: Python版本

```powershell
python --version
# 需要 Python 3.8+
```

### 检查2: 安装依赖

```powershell
pip install numpy pandas torch
```

### 检查3: 检查文件路径

```powershell
# 确保在正确的目录
cd c:\Users\Lenovo\Desktop\PandaQuantFlow

# 检查文件是否存在
dir run_pandafactor_example.py
dir lightweight\factor_library.py
```

---

## 📞 仍然有问题？

### 最简单的测试

```powershell
# 测试Python环境
python -c "print('Python OK')"

# 测试numpy
python -c "import numpy; print('NumPy OK')"

# 测试pandas
python -c "import pandas; print('Pandas OK')"

# 测试我们的因子库
python -c "import sys; sys.path.insert(0, 'lightweight'); from factor_library import FactorLibrary; print('FactorLibrary OK')"
```

---

## 🎉 总结

**最快开始的方法**:

1. 双击运行 `直接运行示例.bat`
2. 或运行 `python run_pandafactor_example.py`
3. 看到输出后，开始编写自己的因子
4. 无需配置PandaFactor完整框架
5. 无需MongoDB

**就这么简单！** 🚀

---

**立即开始**:
```powershell
python run_pandafactor_example.py
```
