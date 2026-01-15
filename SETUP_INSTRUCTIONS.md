# PandaFactor 配置说明

## ❌ 遇到的问题

在PowerShell中运行 `.bat` 文件时出现中文乱码错误：
```
'綍' 不是内部或外部命令，也不是可运行的程序或批处理文件。
```

**原因**: PowerShell对批处理文件的中文字符编码支持不佳。

---

## ✅ 解决方案

我已经为您创建了3个PowerShell版本的配置脚本：

### 方案1: 完整配置 (推荐)

```powershell
# 在PowerShell中运行
.\setup_pandafactor.ps1
```

**功能**:
- ✅ 安装所有依赖
- ✅ 配置所有6个子模块
- ✅ 完整的错误检查
- ✅ 彩色输出提示

**时间**: 约10分钟

---

### 方案2: 快速配置 (推荐新手)

```powershell
# 在PowerShell中运行
.\quick_setup.ps1
```

**功能**:
- ✅ 只安装核心依赖
- ✅ 只配置核心模块 (panda_common, panda_data, panda_factor)
- ✅ 跳过可选依赖
- ✅ 自动验证安装

**时间**: 约3分钟

---

### 方案3: 手动配置 (最灵活)

如果脚本运行失败，可以手动执行以下命令：

```powershell
# 1. 进入项目目录
cd c:\Users\Lenovo\Desktop\PandaQuantFlow\panda_factor-main\panda_factor-main

# 2. 安装核心依赖
pip install numpy pandas pymongo loguru PyYAML setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 配置核心模块
cd panda_common
pip install -e .
cd ..

cd panda_data
pip install -e .
cd ..

cd panda_factor
pip install -e .
cd ..

# 4. 验证安装
cd c:\Users\Lenovo\Desktop\PandaQuantFlow
python test_pandafactor.py
```

---

## 🚀 推荐流程

### 步骤1: 运行快速配置

```powershell
# 打开PowerShell
cd c:\Users\Lenovo\Desktop\PandaQuantFlow

# 如果遇到执行策略限制，先运行：
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 运行快速配置
.\quick_setup.ps1
```

### 步骤2: 运行测试

```powershell
python test_pandafactor.py
```

### 步骤3: 运行示例

```powershell
python run_pandafactor_example.py
```

---

## 🔧 常见问题

### Q1: PowerShell提示无法运行脚本

**错误信息**:
```
无法加载文件 setup_pandafactor.ps1，因为在此系统上禁止运行脚本
```

**解决**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q2: pip命令找不到

**解决**:
```powershell
# 检查Python是否在PATH中
python -m pip --version

# 如果可以，使用 python -m pip 代替 pip
python -m pip install numpy pandas
```

### Q3: 某个模块配置失败

**解决**:
```powershell
# 单独配置失败的模块
cd panda_factor-main\panda_factor-main\panda_common
python -m pip install -e .
```

### Q4: 依赖安装太慢

**解决**:
```powershell
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用阿里云镜像
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

---

## 📝 最简单的方式 (无需配置PandaFactor)

如果您只想快速使用因子库，可以直接使用我们的轻量级版本：

```powershell
# 1. 安装基础依赖
pip install numpy pandas torch -i https://pypi.tuna.tsinghua.edu.cn/simple

# 2. 直接运行示例
python run_pandafactor_example.py
```

这个方式：
- ✅ 无需配置PandaFactor
- ✅ 无需MongoDB
- ✅ 200+因子函数直接可用
- ✅ 5分钟即可开始

---

## 🎯 三种使用模式对比

| 模式 | 配置难度 | 功能 | 适合人群 |
|------|---------|------|---------|
| **轻量级因子库** | ⭐ 简单 | 200+函数 | 新手/快速开发 |
| **PandaFactor核心** | ⭐⭐ 中等 | 因子计算+数据管理 | 进阶用户 |
| **PandaFactor完整** | ⭐⭐⭐ 复杂 | 完整功能+Web界面 | 生产环境 |

---

## 💡 建议

**如果您是新手或想快速开始**:
```powershell
# 直接运行示例，无需配置
python run_pandafactor_example.py
```

**如果您想使用完整功能**:
```powershell
# 运行快速配置
.\quick_setup.ps1

# 然后测试
python test_pandafactor.py
```

**如果您要部署到生产环境**:
```powershell
# 运行完整配置
.\setup_pandafactor.ps1

# 配置MongoDB
# 启动服务器
```

---

## 📞 获取帮助

如果仍然遇到问题：

1. 查看详细日志
2. 检查Python版本 (需要3.8+)
3. 检查pip版本
4. 尝试手动配置
5. 使用轻量级版本

---

**现在就开始吧！** 🚀

推荐命令:
```powershell
.\quick_setup.ps1
```
