# PandaFactor 配置与运行指南

## 📋 环境要求

- Python 3.8+
- MongoDB 4.0+ (用于数据存储)
- Windows/Linux/MacOS

---

## 🚀 快速配置步骤

### 步骤1: 安装依赖

```bash
# 进入PandaFactor项目目录
cd c:\Users\Lenovo\Desktop\PandaQuantFlow\panda_factor-main\panda_factor-main

# 安装基础依赖
pip install -r requirements.txt
```

### 步骤2: 配置各个子模块 (VSCode/Cursor方式)

按照README说明，需要在每个子模块目录下执行 `pip install -e .`

```bash
# 1. 配置 panda_common
cd panda_common
pip install -e .
cd ..

# 2. 配置 panda_data
cd panda_data
pip install -e .
cd ..

# 3. 配置 panda_data_hub
cd panda_data_hub
pip install -e .
cd ..

# 4. 配置 panda_factor
cd panda_factor
pip install -e .
cd ..

# 5. 配置 panda_llm
cd panda_llm
pip install -e .
cd ..

# 6. 配置 panda_factor_server
cd panda_factor_server
pip install -e .
cd ..
```

### 步骤3: 配置MongoDB连接

编辑配置文件 `panda_common/config.yaml`：

```yaml
mongodb:
  host: localhost
  port: 27017
  database: panda_factor
  username: ""  # 如果有认证，填写用户名
  password: ""  # 如果有认证，填写密码
```

### 步骤4: 启动数据库

如果您下载了官方数据库包：
```bash
# 解压数据库包后，执行
bin/db_start.bat
```

如果使用自己的MongoDB：
```bash
# 确保MongoDB服务已启动
# Windows: 
net start MongoDB

# Linux/Mac:
sudo systemctl start mongod
```

---

## 💻 运行方式

### 方式1: 在代码中引用因子

```python
import panda_data

# 初始化
panda_data.init()

# 获取因子数据
factor = panda_data.get_factor_by_name(
    factor_name="VH03cc651", 
    start_date='20240320',
    end_date='20250325'
)

print(factor.head())
```

### 方式2: 启动Web服务器

```bash
# 启动因子服务器
cd panda_factor_server
python -m panda_factor_server

# 或者直接运行
python __main__.py
```

访问: http://localhost:8000

### 方式3: 启动数据自动更新

```bash
# 启动数据更新任务
cd panda_data_hub
python -m panda_data_hub

# 或者直接运行
python __main__.py
```

---

## 📝 编写自定义因子

### Python方式 (推荐)

```python
from panda_factor import Factor
from panda_factor.operators import *

class MyCustomFactor(Factor):
    """自定义因子示例"""
    
    def calculate(self, factors):
        close = factors['close']
        volume = factors['volume']
        high = factors['high']
        low = factors['low']
        
        # 计算20日收益率
        returns = (close / DELAY(close, 20)) - 1
        
        # 计算20日波动率
        volatility = STDDEV((close / DELAY(close, 1)) - 1, 20)
        
        # 计算价格区间
        price_range = (high - low) / close
        
        # 计算成交量比率
        volume_ratio = volume / DELAY(volume, 1)
        
        # 计算20日成交量均值
        volume_ma = SUM(volume, 20) / 20
        
        # 计算动量信号
        momentum = RANK(returns)
        
        # 计算波动率信号
        vol_signal = IF(volatility > DELAY(volatility, 1), 1, -1)
        
        # 合成最终因子
        result = momentum * vol_signal * SCALE(volume_ratio / volume_ma)
        
        return result

# 使用因子
factor = MyCustomFactor()
result = factor.calculate(data)
```

### 公式方式

```python
# 简单因子
formula = "RANK((CLOSE / DELAY(CLOSE, 20)) - 1)"

# 复杂因子
formula = """
returns = (CLOSE / DELAY(CLOSE, 20)) - 1
volatility = STDDEV((CLOSE / DELAY(CLOSE, 1)) - 1, 20)
momentum = RANK(returns)
vol_signal = IF(volatility > DELAY(volatility, 1), 1, -1)
result = momentum * vol_signal
"""
```

---

## 🔧 常见问题

### Q1: 找不到模块 panda_data
**解决**: 确保已在各子模块目录执行 `pip install -e .`

### Q2: MongoDB连接失败
**解决**: 
1. 检查MongoDB服务是否启动
2. 检查 `panda_common/config.yaml` 配置是否正确
3. 检查防火墙设置

### Q3: 缺少数据
**解决**: 
1. 下载官方数据库包
2. 或配置数据源(Tushare/RiceQuant等)自动更新

### Q4: 依赖安装失败
**解决**:
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 📞 获取帮助

- 官方文档: https://www.pandaai.online
- 函数参考: https://www.pandaai.online/community/article/72
- 加群答疑: 见README中的二维码

---

## ✅ 验证安装

运行以下测试脚本验证安装是否成功：

```python
# test_installation.py
import sys

print("Testing PandaFactor installation...")

# 测试1: 导入模块
try:
    import panda_common
    print("✅ panda_common imported successfully")
except ImportError as e:
    print(f"❌ panda_common import failed: {e}")

try:
    import panda_data
    print("✅ panda_data imported successfully")
except ImportError as e:
    print(f"❌ panda_data import failed: {e}")

try:
    import panda_factor
    print("✅ panda_factor imported successfully")
except ImportError as e:
    print(f"❌ panda_factor import failed: {e}")

# 测试2: 检查配置
try:
    from panda_common import config
    print(f"✅ Config loaded: {config}")
except Exception as e:
    print(f"❌ Config load failed: {e}")

print("\nInstallation test completed!")
```

保存为 `test_installation.py` 并运行：
```bash
python test_installation.py
```
