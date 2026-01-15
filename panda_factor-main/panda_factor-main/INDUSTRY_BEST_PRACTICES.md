# 🏆 PandaQuantFlow - 对标行业顶尖的量化因子平台

## 📊 行业对标分析

### 对标产品
1. **Bloomberg Terminal** - 金融数据终端标杆
2. **QuantConnect** - 量化策略平台
3. **Alphalens** - 因子分析工具
4. **WorldQuant** - 因子挖掘平台
5. **Tableau/Power BI** - 数据可视化

### 核心差异化优势
- ✅ **AI驱动** - 集成4个免费LLM模型辅助因子开发
- ✅ **多密钥负载均衡** - 3个API密钥保证高可用
- ✅ **实时计算** - 流式数据处理
- ✅ **现代化UI** - 参考最新设计趋势
- ✅ **开源免费** - 降低使用门槛

---

## 🎨 前端架构 - 对标行业最佳实践

### 技术栈选型

```typescript
// 核心框架
React 18.2+ (或 Vue 3.3+)     // 主流框架，生态成熟
TypeScript 5.0+                // 类型安全
Vite 4.0+                      // 极速构建

// UI组件库
Ant Design 5.0+ / Material-UI  // 企业级组件
TailwindCSS 3.0+               // 原子化CSS
Framer Motion                  // 高性能动画

// 数据可视化
ECharts 5.4+ / Apache ECharts  // 强大的图表库
D3.js 7.0+                     // 自定义可视化
Plotly.js                      // 金融图表

// 状态管理
Zustand / Jotai               // 轻量级状态管理
React Query / SWR             // 服务端状态

// 实时通信
Socket.IO / WebSocket         // 实时数据推送
```

### 设计系统

```typescript
// Design Tokens (设计令牌)
const designTokens = {
  // 色彩系统 - 参考 Material Design 3.0
  colors: {
    primary: {
      50: '#E8EAF6',
      100: '#C5CAE9',
      500: '#667eea',  // 主色
      700: '#764ba2',  // 深色
      gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    },
    semantic: {
      success: '#4CAF50',
      warning: '#FF9800',
      error: '#F44336',
      info: '#2196F3'
    },
    neutral: {
      0: '#FFFFFF',
      50: '#F8F9FA',
      100: '#F5F5F5',
      900: '#1A1A1A'
    }
  },
  
  // 间距系统 - 8px 基准
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    '2xl': '48px'
  },
  
  // 字体系统
  typography: {
    fontFamily: {
      sans: '-apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei"',
      mono: '"JetBrains Mono", "Fira Code", monospace'
    },
    fontSize: {
      xs: '12px',
      sm: '14px',
      base: '16px',
      lg: '18px',
      xl: '20px',
      '2xl': '24px',
      '3xl': '30px'
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700
    }
  },
  
  // 阴影系统
  shadows: {
    sm: '0 2px 4px rgba(0, 0, 0, 0.05)',
    md: '0 4px 12px rgba(0, 0, 0, 0.08)',
    lg: '0 8px 24px rgba(0, 0, 0, 0.12)',
    xl: '0 12px 32px rgba(0, 0, 0, 0.15)'
  },
  
  // 圆角系统
  borderRadius: {
    sm: '6px',
    md: '12px',
    lg: '16px',
    xl: '20px',
    full: '9999px'
  },
  
  // 动画系统
  transitions: {
    fast: '150ms cubic-bezier(0.4, 0, 0.2, 1)',
    base: '300ms cubic-bezier(0.4, 0, 0.2, 1)',
    slow: '500ms cubic-bezier(0.4, 0, 0.2, 1)'
  }
}
```

---

## 🏗️ 组件架构 - 原子设计模式

### 1. Atoms (原子组件)

```typescript
// Button 组件 - 参考 Ant Design
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'outline' | 'ghost'
  size: 'sm' | 'md' | 'lg'
  loading?: boolean
  icon?: React.ReactNode
  onClick?: () => void
}

const Button: React.FC<ButtonProps> = ({ 
  variant = 'primary', 
  size = 'md',
  loading,
  icon,
  children,
  onClick 
}) => {
  return (
    <motion.button
      className={cn(
        'inline-flex items-center justify-center gap-2',
        'font-medium rounded-lg transition-all',
        'focus:outline-none focus:ring-2 focus:ring-offset-2',
        variants[variant],
        sizes[size]
      )}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      disabled={loading}
    >
      {loading && <Spinner size="sm" />}
      {icon && <span>{icon}</span>}
      {children}
    </motion.button>
  )
}

// Tag 组件 - 多彩标签
interface TagProps {
  color: 'tech' | 'finance' | 'news' | 'hot'
  starred?: boolean
  children: React.ReactNode
}

const Tag: React.FC<TagProps> = ({ color, starred, children }) => {
  return (
    <span className={cn(
      'inline-flex items-center gap-1',
      'px-3 py-1 rounded text-xs font-medium',
      'transition-transform hover:-translate-y-0.5',
      tagColors[color]
    )}>
      {starred && <Star className="w-3 h-3" />}
      {children}
    </span>
  )
}
```

### 2. Molecules (分子组件)

```typescript
// MetricCard - 指标卡片
interface MetricCardProps {
  label: string
  value: string | number
  trend?: 'up' | 'down' | 'neutral'
  trendValue?: string
}

const MetricCard: React.FC<MetricCardProps> = ({ 
  label, 
  value, 
  trend,
  trendValue 
}) => {
  return (
    <motion.div
      className="p-4 bg-gray-50 rounded-lg hover:bg-gradient-to-br hover:from-primary-500 hover:to-primary-700 hover:text-white transition-all group"
      whileHover={{ scale: 1.05 }}
    >
      <div className="text-xs text-gray-500 group-hover:text-white/80 mb-1">
        {label}
      </div>
      <div className="flex items-baseline gap-2">
        <div className="text-2xl font-semibold">{value}</div>
        {trend && (
          <div className={cn(
            'text-xs flex items-center gap-1',
            trend === 'up' && 'text-green-500',
            trend === 'down' && 'text-red-500'
          )}>
            {trend === 'up' ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
            {trendValue}
          </div>
        )}
      </div>
    </motion.div>
  )
}

// StatusBadge - 状态徽章
const StatusBadge: React.FC<{ status: 'running' | 'completed' | 'error' }> = ({ status }) => {
  const config = {
    running: { 
      label: '运行中', 
      gradient: 'from-blue-500 to-cyan-500',
      icon: <Activity className="w-3 h-3 animate-pulse" />
    },
    completed: { 
      label: '已完成', 
      gradient: 'from-green-500 to-emerald-500',
      icon: <CheckCircle className="w-3 h-3" />
    },
    error: { 
      label: '错误', 
      gradient: 'from-red-500 to-pink-500',
      icon: <AlertCircle className="w-3 h-3" />
    }
  }
  
  return (
    <span className={cn(
      'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full',
      'text-xs font-medium text-white',
      'bg-gradient-to-r',
      config[status].gradient
    )}>
      {config[status].icon}
      {config[status].label}
    </span>
  )
}
```

### 3. Organisms (有机体组件)

```typescript
// FactorCard - 因子卡片（完整版）
interface FactorCardProps {
  factor: {
    id: string
    name: string
    description: string
    status: 'running' | 'completed' | 'error'
    metrics: {
      sharpe: number
      annualReturn: number
      maxDrawdown: number
    }
    tags: Array<{ label: string; color: string; starred?: boolean }>
    createdAt: string
    updatedAt: string
  }
  onView?: (id: string) => void
  onEdit?: (id: string) => void
  onDelete?: (id: string) => void
}

const FactorCard: React.FC<FactorCardProps> = ({ factor, onView, onEdit, onDelete }) => {
  return (
    <motion.div
      className="relative bg-white rounded-xl p-6 shadow-md hover:shadow-xl transition-all overflow-hidden group"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -6 }}
    >
      {/* 顶部渐变条 */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-primary-500 to-primary-700" />
      
      {/* 头部 */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-1">
            {factor.name}
          </h3>
          <p className="text-sm text-gray-500">
            更新于 {formatRelativeTime(factor.updatedAt)}
          </p>
        </div>
        <StatusBadge status={factor.status} />
      </div>
      
      {/* 描述 */}
      <p className="text-sm text-gray-600 mb-4 line-clamp-2">
        {factor.description}
      </p>
      
      {/* 指标网格 */}
      <div className="grid grid-cols-3 gap-3 mb-4">
        <MetricCard 
          label="夏普比率" 
          value={factor.metrics.sharpe.toFixed(2)}
          trend={factor.metrics.sharpe > 1.5 ? 'up' : 'neutral'}
        />
        <MetricCard 
          label="年化收益" 
          value={`${factor.metrics.annualReturn.toFixed(1)}%`}
          trend={factor.metrics.annualReturn > 15 ? 'up' : 'down'}
          trendValue={`${factor.metrics.annualReturn > 0 ? '+' : ''}${factor.metrics.annualReturn.toFixed(1)}%`}
        />
        <MetricCard 
          label="最大回撤" 
          value={`${factor.metrics.maxDrawdown.toFixed(1)}%`}
          trend={Math.abs(factor.metrics.maxDrawdown) < 15 ? 'up' : 'down'}
        />
      </div>
      
      {/* 标签 */}
      <div className="flex flex-wrap gap-2 mb-4">
        {factor.tags.map((tag, idx) => (
          <Tag key={idx} color={tag.color} starred={tag.starred}>
            {tag.label}
          </Tag>
        ))}
      </div>
      
      {/* 操作按钮 */}
      <div className="flex gap-2">
        <Button 
          variant="primary" 
          size="sm" 
          icon={<Eye size={16} />}
          onClick={() => onView?.(factor.id)}
        >
          查看详情
        </Button>
        <Button 
          variant="outline" 
          size="sm" 
          icon={<Edit size={16} />}
          onClick={() => onEdit?.(factor.id)}
        >
          编辑
        </Button>
        <Button 
          variant="ghost" 
          size="sm" 
          icon={<Trash2 size={16} />}
          onClick={() => onDelete?.(factor.id)}
        >
          删除
        </Button>
      </div>
      
      {/* 悬停效果 - 渐变光晕 */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary-500/0 to-primary-700/0 group-hover:from-primary-500/5 group-hover:to-primary-700/5 transition-all pointer-events-none" />
    </motion.div>
  )
}
```

---

## 📊 数据可视化 - 对标 Bloomberg/Tableau

### 1. 因子表现图表

```typescript
// 使用 ECharts 创建专业金融图表
import * as echarts from 'echarts'

const FactorPerformanceChart: React.FC<{ data: FactorData }> = ({ data }) => {
  const chartRef = useRef<HTMLDivElement>(null)
  
  useEffect(() => {
    if (!chartRef.current) return
    
    const chart = echarts.init(chartRef.current)
    
    const option: echarts.EChartsOption = {
      // 主题配置
      backgroundColor: 'transparent',
      
      // 标题
      title: {
        text: '因子累计收益曲线',
        textStyle: {
          color: '#333',
          fontSize: 18,
          fontWeight: 600
        }
      },
      
      // 工具箱
      toolbox: {
        feature: {
          dataZoom: { show: true },
          restore: { show: true },
          saveAsImage: { show: true }
        }
      },
      
      // 提示框
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#667eea',
        borderWidth: 1,
        textStyle: { color: '#333' },
        formatter: (params: any) => {
          const date = params[0].axisValue
          const value = params[0].value
          const change = params[0].data.change
          return `
            <div class="p-2">
              <div class="text-xs text-gray-500">${date}</div>
              <div class="text-lg font-semibold">${value.toFixed(2)}%</div>
              <div class="text-xs ${change >= 0 ? 'text-green-500' : 'text-red-500'}">
                ${change >= 0 ? '↑' : '↓'} ${Math.abs(change).toFixed(2)}%
              </div>
            </div>
          `
        }
      },
      
      // 图例
      legend: {
        data: ['因子收益', '基准收益', '超额收益'],
        top: 40,
        textStyle: { fontSize: 12 }
      },
      
      // 网格
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      
      // X轴
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: data.dates,
        axisLine: { lineStyle: { color: '#E0E0E0' } },
        axisLabel: { color: '#666' }
      },
      
      // Y轴
      yAxis: {
        type: 'value',
        axisLine: { lineStyle: { color: '#E0E0E0' } },
        axisLabel: { 
          color: '#666',
          formatter: '{value}%'
        },
        splitLine: { lineStyle: { color: '#F5F5F5' } }
      },
      
      // 数据系列
      series: [
        {
          name: '因子收益',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 6,
          lineStyle: {
            width: 3,
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#667eea' },
              { offset: 1, color: '#764ba2' }
            ])
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(102, 126, 234, 0.3)' },
              { offset: 1, color: 'rgba(118, 75, 162, 0.1)' }
            ])
          },
          data: data.factorReturns
        },
        {
          name: '基准收益',
          type: 'line',
          smooth: true,
          lineStyle: { width: 2, color: '#999', type: 'dashed' },
          data: data.benchmarkReturns
        },
        {
          name: '超额收益',
          type: 'line',
          smooth: true,
          lineStyle: { width: 2, color: '#4CAF50' },
          data: data.excessReturns
        }
      ],
      
      // 数据区域缩放
      dataZoom: [
        {
          type: 'inside',
          start: 0,
          end: 100
        },
        {
          start: 0,
          end: 100,
          handleStyle: {
            color: '#667eea'
          }
        }
      ]
    }
    
    chart.setOption(option)
    
    // 响应式
    const handleResize = () => chart.resize()
    window.addEventListener('resize', handleResize)
    
    return () => {
      window.removeEventListener('resize', handleResize)
      chart.dispose()
    }
  }, [data])
  
  return <div ref={chartRef} className="w-full h-96" />
}
```

### 2. 因子分析仪表盘

```typescript
// 多维度分析仪表盘
const FactorDashboard: React.FC<{ factorId: string }> = ({ factorId }) => {
  const { data, isLoading } = useFactorAnalysis(factorId)
  
  if (isLoading) return <LoadingSkeleton />
  
  return (
    <div className="space-y-6">
      {/* 概览卡片 */}
      <div className="grid grid-cols-4 gap-4">
        <StatCard
          icon={<TrendingUp className="text-green-500" />}
          label="累计收益"
          value={`${data.totalReturn.toFixed(2)}%`}
          trend="up"
          trendValue="+12.5%"
        />
        <StatCard
          icon={<Activity className="text-blue-500" />}
          label="夏普比率"
          value={data.sharpeRatio.toFixed(2)}
          trend={data.sharpeRatio > 1.5 ? 'up' : 'neutral'}
        />
        <StatCard
          icon={<BarChart3 className="text-purple-500" />}
          label="信息比率"
          value={data.informationRatio.toFixed(2)}
        />
        <StatCard
          icon={<AlertTriangle className="text-orange-500" />}
          label="最大回撤"
          value={`${data.maxDrawdown.toFixed(2)}%`}
          trend="down"
        />
      </div>
      
      {/* 主图表区域 */}
      <div className="grid grid-cols-2 gap-6">
        {/* 收益曲线 */}
        <Card title="累计收益曲线">
          <FactorPerformanceChart data={data.performance} />
        </Card>
        
        {/* 回撤曲线 */}
        <Card title="回撤分析">
          <DrawdownChart data={data.drawdown} />
        </Card>
      </div>
      
      {/* 分层分析 */}
      <Card title="分层收益分析">
        <LayeredReturnsChart data={data.layeredReturns} />
      </Card>
      
      {/* IC分析 */}
      <div className="grid grid-cols-2 gap-6">
        <Card title="IC时间序列">
          <ICTimeSeriesChart data={data.ic} />
        </Card>
        <Card title="IC分布">
          <ICDistributionChart data={data.icDistribution} />
        </Card>
      </div>
      
      {/* 换手率分析 */}
      <Card title="换手率分析">
        <TurnoverChart data={data.turnover} />
      </Card>
    </div>
  )
}
```

---

## 🔄 实时数据流 - WebSocket集成

```typescript
// WebSocket Hook - 实时数据推送
const useRealtimeFactorData = (factorId: string) => {
  const [data, setData] = useState<FactorData | null>(null)
  const [status, setStatus] = useState<'connecting' | 'connected' | 'disconnected'>('connecting')
  
  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8111/ws/factor/${factorId}`)
    
    ws.onopen = () => {
      setStatus('connected')
      console.log('✅ WebSocket connected')
    }
    
    ws.onmessage = (event) => {
      const update = JSON.parse(event.data)
      setData(prev => ({
        ...prev,
        ...update,
        // 增量更新
        performance: [...(prev?.performance || []), update.newDataPoint]
      }))
    }
    
    ws.onerror = (error) => {
      console.error('❌ WebSocket error:', error)
      setStatus('disconnected')
    }
    
    ws.onclose = () => {
      setStatus('disconnected')
      console.log('🔌 WebSocket disconnected')
    }
    
    return () => ws.close()
  }, [factorId])
  
  return { data, status }
}

// 实时因子监控组件
const RealtimeFactorMonitor: React.FC = () => {
  const { data, status } = useRealtimeFactorData('factor-123')
  
  return (
    <div className="relative">
      {/* 连接状态指示器 */}
      <div className="absolute top-4 right-4">
        <StatusIndicator status={status} />
      </div>
      
      {/* 实时数据展示 */}
      {data && (
        <motion.div
          key={data.timestamp}
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="p-6 bg-white rounded-xl shadow-lg"
        >
          <div className="text-sm text-gray-500 mb-2">
            实时更新 • {formatTime(data.timestamp)}
          </div>
          <div className="text-3xl font-bold">
            {data.currentReturn.toFixed(2)}%
          </div>
          <div className={cn(
            'text-sm font-medium',
            data.change >= 0 ? 'text-green-500' : 'text-red-500'
          )}>
            {data.change >= 0 ? '↑' : '↓'} {Math.abs(data.change).toFixed(2)}%
          </div>
        </motion.div>
      )}
    </div>
  )
}
```

---

## 🤖 AI辅助功能 - LLM集成

```typescript
// AI因子助手
const AIFactorAssistant: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [selectedModel, setSelectedModel] = useState<'deepseek' | 'qwen' | 'qwen_coder' | 'glm'>('deepseek')
  
  const sendMessage = async () => {
    if (!input.trim()) return
    
    // 添加用户消息
    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date()
    }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsTyping(true)
    
    try {
      // 调用LLM API
      const response = await fetch('/llm/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: [...messages, userMessage],
          model: selectedModel
        })
      })
      
      const data = await response.json()
      
      // 添加AI回复
      const aiMessage: Message = {
        role: 'assistant',
        content: data.content,
        timestamp: new Date(),
        model: selectedModel
      }
      setMessages(prev => [...prev, aiMessage])
      
      // 如果是代码生成，自动插入编辑器
      if (data.code) {
        insertCodeToEditor(data.code)
      }
    } catch (error) {
      console.error('AI调用失败:', error)
    } finally {
      setIsTyping(false)
    }
  }
  
  return (
    <div className="flex flex-col h-full bg-white rounded-xl shadow-lg overflow-hidden">
      {/* 头部 */}
      <div className="flex items-center justify-between p-4 border-b bg-gradient-to-r from-primary-500 to-primary-700">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center">
            <Sparkles className="text-white" size={20} />
          </div>
          <div>
            <h3 className="text-white font-semibold">AI因子助手</h3>
            <p className="text-white/80 text-xs">由 {selectedModel.toUpperCase()} 驱动</p>
          </div>
        </div>
        
        {/* 模型选择器 */}
        <select
          value={selectedModel}
          onChange={(e) => setSelectedModel(e.target.value as any)}
          className="px-3 py-1.5 rounded-lg bg-white/20 text-white text-sm border border-white/30"
        >
          <option value="deepseek">DeepSeek V3 (代码)</option>
          <option value="qwen">Qwen 2.5 (分析)</option>
          <option value="qwen_coder">Qwen Coder (算法)</option>
          <option value="glm">GLM-4 (通用)</option>
        </select>
      </div>
      
      {/* 消息列表 */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={cn(
              'flex gap-3',
              msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'
            )}
          >
            {/* 头像 */}
            <div className={cn(
              'w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0',
              msg.role === 'user' 
                ? 'bg-gradient-to-br from-blue-500 to-cyan-500' 
                : 'bg-gradient-to-br from-purple-500 to-pink-500'
            )}>
              {msg.role === 'user' ? <User size={16} className="text-white" /> : <Bot size={16} className="text-white" />}
            </div>
            
            {/* 消息内容 */}
            <div className={cn(
              'max-w-[70%] rounded-2xl px-4 py-3',
              msg.role === 'user'
                ? 'bg-gradient-to-br from-primary-500 to-primary-700 text-white'
                : 'bg-gray-100 text-gray-900'
            )}>
              <ReactMarkdown className="prose prose-sm max-w-none">
                {msg.content}
              </ReactMarkdown>
              <div className="text-xs opacity-70 mt-2">
                {formatTime(msg.timestamp)}
              </div>
            </div>
          </motion.div>
        ))}
        
        {/* 输入中指示器 */}
        {isTyping && (
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
              <Bot size={16} className="text-white" />
            </div>
            <div className="bg-gray-100 rounded-2xl px-4 py-3">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}
      </div>
      
      {/* 输入框 */}
      <div className="p-4 border-t bg-gray-50">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="输入您的问题，例如：帮我写一个RSI因子..."
            className="flex-1 px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
          <Button
            variant="primary"
            onClick={sendMessage}
            disabled={!input.trim() || isTyping}
            icon={<Send size={18} />}
          >
            发送
          </Button>
        </div>
        
        {/* 快捷操作 */}
        <div className="flex gap-2 mt-2">
          <button className="text-xs px-3 py-1 rounded-full bg-gray-200 hover:bg-gray-300 transition-colors">
            💡 生成动量因子
          </button>
          <button className="text-xs px-3 py-1 rounded-full bg-gray-200 hover:bg-gray-300 transition-colors">
            📊 分析因子表现
          </button>
          <button className="text-xs px-3 py-1 rounded-full bg-gray-200 hover:bg-gray-300 transition-colors">
            🔧 优化代码
          </button>
        </div>
      </div>
    </div>
  )
}
```

---

## 📱 响应式设计 - 移动端优化

```typescript
// 响应式布局 Hook
const useResponsive = () => {
  const [breakpoint, setBreakpoint] = useState<'mobile' | 'tablet' | 'desktop'>('desktop')
  
  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth
      if (width < 768) setBreakpoint('mobile')
      else if (width < 1024) setBreakpoint('tablet')
      else setBreakpoint('desktop')
    }
    
    handleResize()
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])
  
  return {
    breakpoint,
    isMobile: breakpoint === 'mobile',
    isTablet: breakpoint === 'tablet',
    isDesktop: breakpoint === 'desktop'
  }
}

// 自适应网格布局
const ResponsiveFactorGrid: React.FC = () => {
  const { breakpoint } = useResponsive()
  
  const gridCols = {
    mobile: 1,
    tablet: 2,
    desktop: 3
  }
  
  return (
    <div className={cn(
      'grid gap-6',
      `grid-cols-${gridCols[breakpoint]}`
    )}>
      {factors.map(factor => (
        <FactorCard key={factor.id} factor={factor} />
      ))}
    </div>
  )
}
```

---

## 🎯 性能优化策略

### 1. 虚拟滚动 - 大数据列表

```typescript
import { useVirtualizer } from '@tanstack/react-virtual'

const VirtualFactorList: React.FC<{ factors: Factor[] }> = ({ factors }) => {
  const parentRef = useRef<HTMLDivElement>(null)
  
  const virtualizer = useVirtualizer({
    count: factors.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 200,
    overscan: 5
  })
  
  return (
    <div ref={parentRef} className="h-screen overflow-auto">
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative'
        }}
      >
        {virtualizer.getVirtualItems().map(virtualItem => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualItem.size}px`,
              transform: `translateY(${virtualItem.start}px)`
            }}
          >
            <FactorCard factor={factors[virtualItem.index]} />
          </div>
        ))}
      </div>
    </div>
  )
}
```

### 2. 代码分割 - 按需加载

```typescript
// 路由懒加载
const FactorAnalysis = lazy(() => import('./pages/FactorAnalysis'))
const Backtest = lazy(() => import('./pages/Backtest'))
const DataManagement = lazy(() => import('./pages/DataManagement'))

// 组件懒加载
const HeavyChart = lazy(() => import('./components/HeavyChart'))

// 使用 Suspense
<Suspense fallback={<LoadingSpinner />}>
  <HeavyChart data={data} />
</Suspense>
```

### 3. 数据缓存 - React Query

```typescript
// 智能缓存和自动重新验证
const useFactorData = (factorId: string) => {
  return useQuery({
    queryKey: ['factor', factorId],
    queryFn: () => fetchFactorData(factorId),
    staleTime: 5 * 60 * 1000, // 5分钟
    cacheTime: 10 * 60 * 1000, // 10分钟
    refetchOnWindowFocus: true,
    refetchInterval: 30 * 1000 // 30秒自动刷新
  })
}
```

---

## 🔐 安全性最佳实践

```typescript
// 1. API密钥加密存储
const encryptApiKey = (key: string) => {
  // 使用 Web Crypto API
  return crypto.subtle.encrypt(...)
}

// 2. XSS防护
import DOMPurify from 'dompurify'

const SafeHTML: React.FC<{ html: string }> = ({ html }) => {
  const clean = DOMPurify.sanitize(html)
  return <div dangerouslySetInnerHTML={{ __html: clean }} />
}

// 3. CSRF保护
const api = axios.create({
  headers: {
    'X-CSRF-Token': getCsrfToken()
  }
})

// 4. 权限控制
const ProtectedRoute: React.FC<{ requiredRole: string }> = ({ requiredRole, children }) => {
  const { user } = useAuth()
  
  if (!user || !user.roles.includes(requiredRole)) {
    return <Navigate to="/unauthorized" />
  }
  
  return <>{children}</>
}
```

---

## 📦 项目结构

```
panda-quant-flow/
├── frontend/                    # 前端项目
│   ├── src/
│   │   ├── components/         # 组件库
│   │   │   ├── atoms/         # 原子组件
│   │   │   ├── molecules/     # 分子组件
│   │   │   ├── organisms/     # 有机体组件
│   │   │   └── templates/     # 模板组件
│   │   ├── pages/             # 页面
│   │   ├── hooks/             # 自定义Hooks
│   │   ├── utils/             # 工具函数
│   │   ├── services/          # API服务
│   │   ├── stores/            # 状态管理
│   │   ├── styles/            # 样式文件
│   │   └── types/             # TypeScript类型
│   ├── public/
│   └── package.json
├── backend/                    # 后端项目
│   ├── panda_factor/          # 因子服务
│   ├── panda_llm/             # LLM服务
│   ├── panda_common/          # 公共模块
│   └── panda_web/             # Web服务
└── docs/                      # 文档
```

---

**🎉 这是一个对标行业顶尖的完整架构方案！**

下一步我将创建具体的实现代码...
