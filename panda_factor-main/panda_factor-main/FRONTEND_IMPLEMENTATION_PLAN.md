# 🚀 PandaQuantFlow 前端实现方案

## 📋 实施路线图

### Phase 1: 基础架构搭建 (Week 1-2)
- ✅ 项目初始化 (Vite + React + TypeScript)
- ✅ 设计系统建立 (Design Tokens)
- ✅ 组件库开发 (Atomic Design)
- ✅ 路由配置
- ✅ 状态管理设置

### Phase 2: 核心功能开发 (Week 3-5)
- ✅ 因子列表页面
- ✅ 因子详情页面
- ✅ 因子编辑器 (Monaco Editor)
- ✅ 回测分析页面
- ✅ 数据可视化组件

### Phase 3: AI功能集成 (Week 6-7)
- ✅ LLM聊天组件
- ✅ 代码生成功能
- ✅ 智能建议系统
- ✅ 模型切换功能

### Phase 4: 优化与测试 (Week 8)
- ✅ 性能优化
- ✅ 单元测试
- ✅ E2E测试
- ✅ 文档完善

---

## 🛠️ 技术栈详细说明

### 核心框架
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "typescript": "^5.0.0",
  "vite": "^4.3.0"
}
```

### UI组件库
```json
{
  "@headlessui/react": "^1.7.0",
  "@heroicons/react": "^2.0.0",
  "framer-motion": "^10.12.0",
  "tailwindcss": "^3.3.0",
  "clsx": "^1.2.1",
  "tailwind-merge": "^1.12.0"
}
```

### 数据可视化
```json
{
  "echarts": "^5.4.0",
  "echarts-for-react": "^3.0.2",
  "d3": "^7.8.0",
  "plotly.js": "^2.20.0",
  "react-plotly.js": "^2.6.0"
}
```

### 状态管理与数据获取
```json
{
  "zustand": "^4.3.0",
  "@tanstack/react-query": "^4.29.0",
  "axios": "^1.4.0",
  "socket.io-client": "^4.6.0"
}
```

### 代码编辑器
```json
{
  "@monaco-editor/react": "^4.5.0",
  "monaco-editor": "^0.38.0"
}
```

### 工具库
```json
{
  "date-fns": "^2.30.0",
  "lodash-es": "^4.17.21",
  "react-markdown": "^8.0.7",
  "react-syntax-highlighter": "^15.5.0",
  "dompurify": "^3.0.3"
}
```

---

## 📁 项目结构（详细版）

```
frontend/
├── public/
│   ├── favicon.ico
│   └── assets/
│       ├── images/
│       └── fonts/
├── src/
│   ├── main.tsx                    # 入口文件
│   ├── App.tsx                     # 根组件
│   ├── vite-env.d.ts              # Vite类型声明
│   │
│   ├── components/                 # 组件库
│   │   ├── atoms/                 # 原子组件
│   │   │   ├── Button/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Button.test.tsx
│   │   │   │   └── index.ts
│   │   │   ├── Tag/
│   │   │   ├── Badge/
│   │   │   ├── Input/
│   │   │   ├── Select/
│   │   │   └── Spinner/
│   │   │
│   │   ├── molecules/             # 分子组件
│   │   │   ├── MetricCard/
│   │   │   ├── StatusBadge/
│   │   │   ├── SearchBar/
│   │   │   └── ModelSelector/
│   │   │
│   │   ├── organisms/             # 有机体组件
│   │   │   ├── FactorCard/
│   │   │   ├── FactorGrid/
│   │   │   ├── AIChat/
│   │   │   ├── CodeEditor/
│   │   │   ├── ChartPanel/
│   │   │   └── Navbar/
│   │   │
│   │   ├── templates/             # 模板组件
│   │   │   ├── DashboardLayout/
│   │   │   ├── FactorDetailLayout/
│   │   │   └── EditorLayout/
│   │   │
│   │   └── charts/                # 图表组件
│   │       ├── PerformanceChart/
│   │       ├── DrawdownChart/
│   │       ├── ICChart/
│   │       └── TurnoverChart/
│   │
│   ├── pages/                     # 页面组件
│   │   ├── Dashboard/
│   │   │   ├── index.tsx
│   │   │   └── Dashboard.module.css
│   │   ├── FactorList/
│   │   ├── FactorDetail/
│   │   ├── FactorEditor/
│   │   ├── Backtest/
│   │   ├── DataManagement/
│   │   └── Settings/
│   │
│   ├── hooks/                     # 自定义Hooks
│   │   ├── useFactorData.ts
│   │   ├── useRealtimeData.ts
│   │   ├── useAIChat.ts
│   │   ├── useResponsive.ts
│   │   └── useTheme.ts
│   │
│   ├── services/                  # API服务
│   │   ├── api.ts                # Axios配置
│   │   ├── factorService.ts
│   │   ├── llmService.ts
│   │   ├── backtestService.ts
│   │   └── websocket.ts
│   │
│   ├── stores/                    # 状态管理
│   │   ├── useFactorStore.ts
│   │   ├── useUserStore.ts
│   │   ├── useThemeStore.ts
│   │   └── useAIStore.ts
│   │
│   ├── utils/                     # 工具函数
│   │   ├── format.ts             # 格式化函数
│   │   ├── validation.ts         # 验证函数
│   │   ├── calculation.ts        # 计算函数
│   │   └── constants.ts          # 常量定义
│   │
│   ├── types/                     # TypeScript类型
│   │   ├── factor.ts
│   │   ├── backtest.ts
│   │   ├── chart.ts
│   │   └── api.ts
│   │
│   ├── styles/                    # 样式文件
│   │   ├── globals.css           # 全局样式
│   │   ├── variables.css         # CSS变量
│   │   └── tailwind.css          # Tailwind配置
│   │
│   └── config/                    # 配置文件
│       ├── routes.tsx            # 路由配置
│       ├── theme.ts              # 主题配置
│       └── env.ts                # 环境变量
│
├── .env.development               # 开发环境变量
├── .env.production                # 生产环境变量
├── tailwind.config.js             # Tailwind配置
├── tsconfig.json                  # TypeScript配置
├── vite.config.ts                 # Vite配置
├── package.json
└── README.md
```

---

## 🎨 核心组件实现

### 1. 主题配置 (theme.ts)

```typescript
export const theme = {
  colors: {
    primary: {
      50: '#E8EAF6',
      100: '#C5CAE9',
      200: '#9FA8DA',
      300: '#7986CB',
      400: '#5C6BC0',
      500: '#667eea',
      600: '#5568D3',
      700: '#764ba2',
      800: '#283593',
      900: '#1A237E',
    },
    semantic: {
      success: {
        light: '#81C784',
        main: '#4CAF50',
        dark: '#388E3C',
      },
      warning: {
        light: '#FFB74D',
        main: '#FF9800',
        dark: '#F57C00',
      },
      error: {
        light: '#E57373',
        main: '#F44336',
        dark: '#D32F2F',
      },
      info: {
        light: '#64B5F6',
        main: '#2196F3',
        dark: '#1976D2',
      },
    },
  },
  
  spacing: (multiplier: number) => `${multiplier * 8}px`,
  
  borderRadius: {
    sm: '6px',
    md: '12px',
    lg: '16px',
    xl: '20px',
    full: '9999px',
  },
  
  shadows: {
    sm: '0 2px 4px rgba(0, 0, 0, 0.05)',
    md: '0 4px 12px rgba(0, 0, 0, 0.08)',
    lg: '0 8px 24px rgba(0, 0, 0, 0.12)',
    xl: '0 12px 32px rgba(0, 0, 0, 0.15)',
  },
  
  transitions: {
    fast: '150ms cubic-bezier(0.4, 0, 0.2, 1)',
    base: '300ms cubic-bezier(0.4, 0, 0.2, 1)',
    slow: '500ms cubic-bezier(0.4, 0, 0.2, 1)',
  },
}
```

### 2. API服务 (factorService.ts)

```typescript
import axios from 'axios'
import type { Factor, FactorAnalysis, BacktestResult } from '@/types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8111',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      // 处理未授权
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const factorService = {
  // 获取因子列表
  getFactors: async (params?: {
    page?: number
    pageSize?: number
    status?: string
    search?: string
  }): Promise<{ data: Factor[]; total: number }> => {
    return api.get('/api/v1/factors', { params })
  },
  
  // 获取因子详情
  getFactorById: async (id: string): Promise<Factor> => {
    return api.get(`/api/v1/factors/${id}`)
  },
  
  // 创建因子
  createFactor: async (data: Partial<Factor>): Promise<Factor> => {
    return api.post('/api/v1/factors', data)
  },
  
  // 更新因子
  updateFactor: async (id: string, data: Partial<Factor>): Promise<Factor> => {
    return api.put(`/api/v1/factors/${id}`, data)
  },
  
  // 删除因子
  deleteFactor: async (id: string): Promise<void> => {
    return api.delete(`/api/v1/factors/${id}`)
  },
  
  // 获取因子分析
  getFactorAnalysis: async (id: string): Promise<FactorAnalysis> => {
    return api.get(`/api/v1/factors/${id}/analysis`)
  },
  
  // 运行回测
  runBacktest: async (id: string, params: any): Promise<BacktestResult> => {
    return api.post(`/api/v1/factors/${id}/backtest`, params)
  },
}
```

### 3. 状态管理 (useFactorStore.ts)

```typescript
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import type { Factor } from '@/types'

interface FactorState {
  factors: Factor[]
  selectedFactor: Factor | null
  loading: boolean
  error: string | null
  
  // Actions
  setFactors: (factors: Factor[]) => void
  setSelectedFactor: (factor: Factor | null) => void
  addFactor: (factor: Factor) => void
  updateFactor: (id: string, updates: Partial<Factor>) => void
  removeFactor: (id: string) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
}

export const useFactorStore = create<FactorState>()(
  devtools(
    persist(
      (set) => ({
        factors: [],
        selectedFactor: null,
        loading: false,
        error: null,
        
        setFactors: (factors) => set({ factors }),
        
        setSelectedFactor: (factor) => set({ selectedFactor: factor }),
        
        addFactor: (factor) => 
          set((state) => ({ 
            factors: [...state.factors, factor] 
          })),
        
        updateFactor: (id, updates) =>
          set((state) => ({
            factors: state.factors.map((f) =>
              f.id === id ? { ...f, ...updates } : f
            ),
          })),
        
        removeFactor: (id) =>
          set((state) => ({
            factors: state.factors.filter((f) => f.id !== id),
          })),
        
        setLoading: (loading) => set({ loading }),
        
        setError: (error) => set({ error }),
      }),
      {
        name: 'factor-storage',
        partialize: (state) => ({ 
          factors: state.factors,
          selectedFactor: state.selectedFactor 
        }),
      }
    )
  )
)
```

### 4. 自定义Hook (useFactorData.ts)

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { factorService } from '@/services/factorService'
import { useFactorStore } from '@/stores/useFactorStore'
import type { Factor } from '@/types'

export const useFactorData = (factorId?: string) => {
  const queryClient = useQueryClient()
  const { setLoading, setError } = useFactorStore()
  
  // 获取因子列表
  const { data: factors, isLoading: isLoadingList } = useQuery({
    queryKey: ['factors'],
    queryFn: () => factorService.getFactors(),
    onSuccess: (data) => {
      setLoading(false)
    },
    onError: (error: any) => {
      setError(error.message)
      setLoading(false)
    },
  })
  
  // 获取单个因子
  const { data: factor, isLoading: isLoadingDetail } = useQuery({
    queryKey: ['factor', factorId],
    queryFn: () => factorService.getFactorById(factorId!),
    enabled: !!factorId,
  })
  
  // 创建因子
  const createMutation = useMutation({
    mutationFn: (data: Partial<Factor>) => factorService.createFactor(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['factors'] })
    },
  })
  
  // 更新因子
  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Factor> }) =>
      factorService.updateFactor(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['factors'] })
      if (factorId) {
        queryClient.invalidateQueries({ queryKey: ['factor', factorId] })
      }
    },
  })
  
  // 删除因子
  const deleteMutation = useMutation({
    mutationFn: (id: string) => factorService.deleteFactor(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['factors'] })
    },
  })
  
  return {
    factors: factors?.data || [],
    factor,
    isLoading: isLoadingList || isLoadingDetail,
    createFactor: createMutation.mutate,
    updateFactor: updateMutation.mutate,
    deleteFactor: deleteMutation.mutate,
    isCreating: createMutation.isLoading,
    isUpdating: updateMutation.isLoading,
    isDeleting: deleteMutation.isLoading,
  }
}
```

---

## 🎯 关键页面实现

### Dashboard页面

```typescript
import { useState } from 'react'
import { motion } from 'framer-motion'
import { FactorGrid } from '@/components/organisms/FactorGrid'
import { AIChat } from '@/components/organisms/AIChat'
import { SearchBar } from '@/components/molecules/SearchBar'
import { useFactorData } from '@/hooks/useFactorData'

export const Dashboard: React.FC = () => {
  const { factors, isLoading } = useFactorData()
  const [searchQuery, setSearchQuery] = useState('')
  const [showAIChat, setShowAIChat] = useState(false)
  
  const filteredFactors = factors.filter((factor) =>
    factor.name.toLowerCase().includes(searchQuery.toLowerCase())
  )
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-500 to-primary-700 p-6">
      <div className="max-w-7xl mx-auto">
        {/* 头部 */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold text-white mb-2">
            因子开发平台
          </h1>
          <p className="text-white/80">
            AI驱动的量化因子挖掘与分析
          </p>
        </motion.div>
        
        {/* 搜索栏 */}
        <div className="mb-6">
          <SearchBar
            value={searchQuery}
            onChange={setSearchQuery}
            placeholder="搜索因子..."
          />
        </div>
        
        {/* 因子网格 */}
        {isLoading ? (
          <LoadingSkeleton />
        ) : (
          <FactorGrid factors={filteredFactors} />
        )}
        
        {/* AI助手浮动按钮 */}
        <motion.button
          className="fixed bottom-6 right-6 w-14 h-14 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full shadow-xl flex items-center justify-center text-white"
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => setShowAIChat(true)}
        >
          <Sparkles size={24} />
        </motion.button>
        
        {/* AI聊天窗口 */}
        {showAIChat && (
          <AIChat onClose={() => setShowAIChat(false)} />
        )}
      </div>
    </div>
  )
}
```

---

## 📊 性能优化清单

- ✅ **代码分割**: 使用 React.lazy 和 Suspense
- ✅ **虚拟滚动**: 大列表使用 @tanstack/react-virtual
- ✅ **图片优化**: WebP格式 + 懒加载
- ✅ **缓存策略**: React Query 智能缓存
- ✅ **Tree Shaking**: Vite自动优化
- ✅ **CDN加速**: 静态资源CDN部署
- ✅ **Gzip压缩**: 服务端开启压缩
- ✅ **预加载**: 关键资源预加载

---

## 🧪 测试策略

### 单元测试 (Vitest + React Testing Library)

```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })
  
  it('handles click events', () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    fireEvent.click(screen.getByText('Click me'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
```

### E2E测试 (Playwright)

```typescript
import { test, expect } from '@playwright/test'

test('factor creation flow', async ({ page }) => {
  await page.goto('http://localhost:5173')
  
  // 点击创建按钮
  await page.click('text=创建因子')
  
  // 填写表单
  await page.fill('[name="name"]', 'Test Factor')
  await page.fill('[name="description"]', 'Test Description')
  
  // 提交
  await page.click('text=保存')
  
  // 验证
  await expect(page.locator('text=Test Factor')).toBeVisible()
})
```

---

## 🚀 部署方案

### 开发环境
```bash
npm run dev
```

### 生产构建
```bash
npm run build
npm run preview
```

### Docker部署
```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

**🎉 完整的前端实现方案已准备就绪！**

这是一个对标行业顶尖水平的现代化前端架构！
