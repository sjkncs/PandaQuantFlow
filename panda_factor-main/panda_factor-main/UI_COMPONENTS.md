# 🎨 PandaFactor UI组件设计 - 参考现代化界面

## 📋 参考UI分析

根据您提供的参考界面，我们提取了以下设计元素：

### 1. 渐变色背景
- 主色调：蓝色到紫色渐变
- 背景：`linear-gradient(135deg, #667eea 0%, #764ba2 100%)`

### 2. 卡片设计
- 白色背景
- 圆角：12-16px
- 阴影：柔和的投影效果
- 悬停效果：轻微上浮

### 3. 标签样式
- 小圆角标签
- 彩色背景
- 白色文字
- 多种颜色分类

### 4. 字体
- 标题：16-18px，加粗
- 正文：14px，常规
- 标签：12px，中等粗细

---

## 🎨 完整CSS样式表

### 基础样式和变量

```css
/* ==================== 全局变量 ==================== */
:root {
  /* 主题色 */
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --primary-color: #667eea;
  --secondary-color: #764ba2;
  
  /* 标签颜色 */
  --tag-tech: #2196F3;
  --tag-finance: #4CAF50;
  --tag-news: #FF9800;
  --tag-analysis: #9C27B0;
  --tag-hot: #F44336;
  
  /* 中性色 */
  --bg-primary: #ffffff;
  --bg-secondary: #f8f9fa;
  --bg-dark: #1a1a1a;
  --text-primary: #333333;
  --text-secondary: #666666;
  --text-muted: #999999;
  --border-color: #e0e0e0;
  
  /* 阴影 */
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
  --shadow-xl: 0 12px 32px rgba(0, 0, 0, 0.15);
  
  /* 圆角 */
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;
  
  /* 字体 */
  --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
}

/* ==================== 全局样式 ==================== */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-family);
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-primary);
  background: var(--bg-secondary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* ==================== 渐变背景容器 ==================== */
.app-container {
  min-height: 100vh;
  background: var(--primary-gradient);
  padding: 20px;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
}

/* ==================== 顶部导航栏 ==================== */
.top-navbar {
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  padding: 16px 24px;
  margin-bottom: 24px;
  box-shadow: var(--shadow-md);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.navbar-logo {
  width: 40px;
  height: 40px;
  border-radius: 8px;
}

.navbar-title {
  font-size: 20px;
  font-weight: 600;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.navbar-menu {
  display: flex;
  gap: 8px;
}

.nav-item {
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  text-decoration: none;
  color: var(--text-secondary);
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
}

.nav-item:hover {
  background: var(--bg-secondary);
  color: var(--primary-color);
}

.nav-item.active {
  background: var(--primary-gradient);
  color: white;
}

/* ==================== 标签样式 ==================== */
.tag {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  line-height: 1.5;
  white-space: nowrap;
  transition: all 0.3s ease;
}

/* 标签颜色变体 */
.tag-tech {
  background: var(--tag-tech);
  color: white;
}

.tag-finance {
  background: var(--tag-finance);
  color: white;
}

.tag-news {
  background: var(--tag-news);
  color: white;
}

.tag-analysis {
  background: var(--tag-analysis);
  color: white;
}

.tag-hot {
  background: var(--tag-hot);
  color: white;
}

.tag-primary {
  background: var(--primary-gradient);
  color: white;
}

/* 标签带星标 */
.tag-starred::before {
  content: "⭐ ";
}

/* 标签悬停效果 */
.tag:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

/* ==================== 卡片样式 ==================== */
.card {
  background: var(--bg-primary);
  border-radius: var(--radius-md);
  padding: 20px;
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--primary-gradient);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.card:hover::before {
  transform: scaleX(1);
}

/* 卡片头部 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
  margin: 0;
  flex: 1;
}

.card-meta {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-shrink: 0;
}

/* 卡片内容 */
.card-content {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 卡片底部 */
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--border-color);
}

.card-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.card-time {
  font-size: 12px;
  color: var(--text-muted);
}

/* ==================== 因子卡片网格 ==================== */
.factor-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

/* 因子卡片特殊样式 */
.factor-card {
  background: var(--bg-primary);
  border-radius: var(--radius-md);
  padding: 24px;
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.factor-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--primary-gradient);
}

.factor-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-xl);
}

.factor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.factor-name {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.factor-status {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.factor-status.running {
  background: linear-gradient(135deg, #2196F3, #21CBF3);
  color: white;
}

.factor-status.completed {
  background: linear-gradient(135deg, #4CAF50, #8BC34A);
  color: white;
}

.factor-status.error {
  background: linear-gradient(135deg, #F44336, #E91E63);
  color: white;
}

/* 因子描述 */
.factor-description {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 16px;
  min-height: 60px;
}

/* 因子指标 */
.factor-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.metric-item {
  text-align: center;
  padding: 12px;
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
  transition: all 0.3s ease;
}

.metric-item:hover {
  background: var(--primary-gradient);
  color: white;
}

.metric-item:hover .metric-label {
  color: rgba(255, 255, 255, 0.9);
}

.metric-label {
  display: block;
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.metric-value {
  display: block;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.metric-item:hover .metric-value {
  color: white;
}

/* 因子操作按钮 */
.factor-actions {
  display: flex;
  gap: 10px;
}

.btn {
  flex: 1;
  padding: 10px 16px;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background: var(--primary-gradient);
  color: white;
}

.btn-primary:hover {
  opacity: 0.9;
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.btn-outline {
  background: transparent;
  color: var(--primary-color);
  border: 2px solid var(--primary-color);
}

.btn-outline:hover {
  background: var(--primary-gradient);
  color: white;
  border-color: transparent;
}

/* ==================== 新闻卡片样式（参考UI） ==================== */
.news-card {
  background: var(--bg-primary);
  border-radius: var(--radius-md);
  padding: 20px;
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.news-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: var(--primary-gradient);
  transform: scaleY(0);
  transition: transform 0.3s ease;
}

.news-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.news-card:hover::before {
  transform: scaleY(1);
}

.news-header {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.news-category {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  background: var(--tag-tech);
  color: white;
}

.news-badge {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  background: var(--tag-hot);
  color: white;
}

.news-badge::before {
  content: "⭐ ";
}

.news-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.5;
  margin-bottom: 12px;
}

.news-content {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 16px;
}

.news-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.news-source {
  font-size: 12px;
  color: var(--text-muted);
}

.news-link {
  font-size: 12px;
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.news-link:hover {
  text-decoration: underline;
}

.news-link::after {
  content: "→";
}

/* ==================== 响应式设计 ==================== */
@media (max-width: 1200px) {
  .factor-grid {
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  }
}

@media (max-width: 768px) {
  .app-container {
    padding: 12px;
  }
  
  .top-navbar {
    flex-direction: column;
    gap: 12px;
  }
  
  .factor-grid {
    grid-template-columns: 1fr;
  }
  
  .factor-metrics {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* ==================== 动画效果 ==================== */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.fade-in {
  animation: fadeIn 0.5s ease;
}

.slide-in {
  animation: slideIn 0.5s ease;
}

/* ==================== 加载状态 ==================== */
.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* ==================== 空状态 ==================== */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-muted);
}

.empty-state-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state-text {
  font-size: 16px;
  margin-bottom: 8px;
}

.empty-state-hint {
  font-size: 14px;
  color: var(--text-muted);
}
```

---

## 📄 HTML示例

### 因子列表页面

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PandaAI 因子平台</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <!-- 主容器 -->
  <div class="app-container">
    <div class="content-wrapper">
      
      <!-- 顶部导航 -->
      <nav class="top-navbar">
        <div class="navbar-brand">
          <img src="/logo.png" alt="Logo" class="navbar-logo">
          <h1 class="navbar-title">PandaAI 因子平台</h1>
        </div>
        
        <div class="navbar-menu">
          <a href="#" class="nav-item active">因子开发</a>
          <a href="#" class="nav-item">回测分析</a>
          <a href="#" class="nav-item">策略优化</a>
          <a href="#" class="nav-item">数据管理</a>
        </div>
      </nav>
      
      <!-- 因子网格 -->
      <div class="factor-grid">
        
        <!-- 因子卡片 1 -->
        <div class="factor-card fade-in">
          <div class="factor-header">
            <h3 class="factor-name">动量因子 v2.0</h3>
            <span class="factor-status running">运行中</span>
          </div>
          
          <p class="factor-description">
            基于20日收益率的动量因子，结合成交量加权，适用于中短期趋势跟踪策略。
          </p>
          
          <div class="factor-metrics">
            <div class="metric-item">
              <span class="metric-label">夏普比率</span>
              <span class="metric-value">1.85</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">年化收益</span>
              <span class="metric-value">23.5%</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">最大回撤</span>
              <span class="metric-value">-12.3%</span>
            </div>
          </div>
          
          <div class="card-tags">
            <span class="tag tag-tech tag-starred">技术指标</span>
            <span class="tag tag-finance">动量策略</span>
          </div>
          
          <div class="factor-actions" style="margin-top: 16px;">
            <button class="btn btn-primary">查看详情</button>
            <button class="btn btn-outline">编辑代码</button>
          </div>
        </div>
        
        <!-- 因子卡片 2 -->
        <div class="factor-card fade-in" style="animation-delay: 0.1s;">
          <div class="factor-header">
            <h3 class="factor-name">价值因子 v1.5</h3>
            <span class="factor-status completed">已完成</span>
          </div>
          
          <p class="factor-description">
            综合市盈率、市净率、股息率的多维度价值评估因子，适用于长期价值投资。
          </p>
          
          <div class="factor-metrics">
            <div class="metric-item">
              <span class="metric-label">夏普比率</span>
              <span class="metric-value">1.52</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">年化收益</span>
              <span class="metric-value">18.2%</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">最大回撤</span>
              <span class="metric-value">-15.7%</span>
            </div>
          </div>
          
          <div class="card-tags">
            <span class="tag tag-finance tag-starred">价值投资</span>
            <span class="tag tag-analysis">基本面</span>
          </div>
          
          <div class="factor-actions" style="margin-top: 16px;">
            <button class="btn btn-primary">查看详情</button>
            <button class="btn btn-outline">编辑代码</button>
          </div>
        </div>
        
        <!-- 因子卡片 3 -->
        <div class="factor-card fade-in" style="animation-delay: 0.2s;">
          <div class="factor-header">
            <h3 class="factor-name">波动率因子</h3>
            <span class="factor-status running">运行中</span>
          </div>
          
          <p class="factor-description">
            基于历史波动率和隐含波动率的复合因子，捕捉市场情绪变化。
          </p>
          
          <div class="factor-metrics">
            <div class="metric-item">
              <span class="metric-label">夏普比率</span>
              <span class="metric-value">1.68</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">年化收益</span>
              <span class="metric-value">20.1%</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">最大回撤</span>
              <span class="metric-value">-10.5%</span>
            </div>
          </div>
          
          <div class="card-tags">
            <span class="tag tag-hot tag-starred">热门因子</span>
            <span class="tag tag-tech">波动率</span>
          </div>
          
          <div class="factor-actions" style="margin-top: 16px;">
            <button class="btn btn-primary">查看详情</button>
            <button class="btn btn-outline">编辑代码</button>
          </div>
        </div>
        
      </div>
      
      <!-- 新闻卡片示例（参考UI风格） -->
      <div class="factor-grid">
        <div class="news-card fade-in">
          <div class="news-header">
            <span class="news-category">科技/AI</span>
            <span class="news-badge">重要提醒</span>
          </div>
          
          <h3 class="news-title">
            健康元：控股子公司获批NS-041片新药临床试验，达诺医药获批三款新药临床试验
          </h3>
          
          <p class="news-content">
            健康元公告称，公司控股子公司深圳市丽珠单抗生物技术有限公司收到国家药品监督管理局核准签发的《药物临床试验批准通知书》...
          </p>
          
          <div class="news-footer">
            <span class="news-source">READ SOURCE</span>
            <a href="#" class="news-link">阅读全文</a>
          </div>
        </div>
        
        <div class="news-card fade-in" style="animation-delay: 0.1s;">
          <div class="news-header">
            <span class="news-category">科技/AI</span>
            <span class="news-badge">重要提醒</span>
          </div>
          
          <h3 class="news-title">
            中信证券：推动AI民氏开放年度复盘，可关注三条线索年度机会
          </h3>
          
          <p class="news-content">
            中信证券研报指出，支持开源AI发展的政策文件密集出台，达诺医药获批三款新药临床试验，其中包括用于治疗肥胖症的新药...
          </p>
          
          <div class="news-footer">
            <span class="news-source">READ SOURCE</span>
            <a href="#" class="news-link">阅读全文</a>
          </div>
        </div>
      </div>
      
    </div>
  </div>
  
  <script src="app.js"></script>
</body>
</html>
```

---

## 🎨 字体配置

### 推荐字体栈

```css
font-family: 
  -apple-system,                    /* macOS/iOS系统字体 */
  BlinkMacSystemFont,               /* macOS Chrome */
  "Segoe UI",                       /* Windows */
  "PingFang SC",                    /* macOS简体中文 */
  "Hiragino Sans GB",               /* macOS简体中文备选 */
  "Microsoft YaHei",                /* Windows简体中文 */
  "Helvetica Neue",                 /* macOS */
  Helvetica,                        /* 通用 */
  Arial,                            /* 通用 */
  sans-serif;                       /* 备选 */
```

### 字体大小规范

```css
/* 标题 */
--font-size-h1: 24px;
--font-size-h2: 20px;
--font-size-h3: 18px;
--font-size-h4: 16px;

/* 正文 */
--font-size-base: 14px;
--font-size-sm: 12px;
--font-size-xs: 11px;

/* 字重 */
--font-weight-light: 300;
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

---

## 📱 完整示例页面

将以上CSS保存为 `styles.css`，HTML保存为 `index.html`，即可看到完整效果！

**关键特性**：
- ✅ 蓝紫渐变背景
- ✅ 白色卡片设计
- ✅ 多彩标签系统
- ✅ 悬停动画效果
- ✅ 现代化字体
- ✅ 响应式布局

**立即使用这些样式优化您的PandaFactor界面！** 🎨
