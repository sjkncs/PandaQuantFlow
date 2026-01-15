"""
PandaAI QuantFlow - 量化工作流平台主服务
集成工作流编排、机器学习、数据分析和可视化
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

# 添加项目路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# FastAPI相关
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

# 创建应用
app = FastAPI(
    title="PandaAI QuantFlow",
    description="量化交易和机器学习工作流平台",
    version="1.0.0"
)

# CORS配置 - 完全开放本地访问（仅开发环境）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_credentials=False,  # 关闭凭证要求
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# ==================== 数据模型 ====================

class WorkflowNode(BaseModel):
    """工作流节点"""
    id: str
    type: str
    name: str
    position: Dict[str, float]
    data: Dict[str, Any]
    inputs: List[str] = []
    outputs: List[str] = []

class WorkflowConnection(BaseModel):
    """工作流连接"""
    id: str
    source: str
    target: str
    sourcePort: str
    targetPort: str

class Workflow(BaseModel):
    """工作流"""
    id: str
    name: str
    description: str = ""
    nodes: List[WorkflowNode]
    connections: List[WorkflowConnection]
    created_at: str
    updated_at: str
    status: str = "draft"  # draft, running, completed, failed

class ExecutionRequest(BaseModel):
    """执行请求"""
    workflow_id: str
    parameters: Dict[str, Any] = {}

# ==================== 工作流管理 ====================

# 内存存储（实际应用应使用数据库）
workflows_store: Dict[str, Workflow] = {}
executions_store: Dict[str, Dict] = {}
connected_clients: List[WebSocket] = []

@app.get("/")
async def root():
    """根路径重定向到工作流界面"""
    return HTMLResponse("""
    <html>
        <head>
            <title>PandaAI QuantFlow</title>
            <meta http-equiv="refresh" content="0; url=/quantflow/">
        </head>
        <body>
            <p>Redirecting to QuantFlow...</p>
        </body>
    </html>
    """)

@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "PandaAI QuantFlow",
        "timestamp": datetime.now().isoformat()
    }

# ==================== 工作流API ====================

@app.get("/api/workflows")
async def get_workflows():
    """获取所有工作流"""
    return list(workflows_store.values())

@app.get("/api/workflows/{workflow_id}")
async def get_workflow(workflow_id: str):
    """获取单个工作流"""
    if workflow_id not in workflows_store:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflows_store[workflow_id]

@app.post("/api/workflows")
async def create_workflow(workflow: Workflow):
    """创建工作流"""
    workflow_id = workflow.id or f"wf_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    workflow.id = workflow_id
    workflow.created_at = datetime.now().isoformat()
    workflow.updated_at = workflow.created_at
    workflows_store[workflow_id] = workflow
    
    # 通知所有连接的客户端
    await notify_clients({"type": "workflow_created", "workflow": workflow.dict()})
    
    return workflow

@app.put("/api/workflows/{workflow_id}")
async def update_workflow(workflow_id: str, workflow: Workflow):
    """更新工作流"""
    if workflow_id not in workflows_store:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow.id = workflow_id
    workflow.updated_at = datetime.now().isoformat()
    workflows_store[workflow_id] = workflow
    
    # 通知所有连接的客户端
    await notify_clients({"type": "workflow_updated", "workflow": workflow.dict()})
    
    return workflow

@app.delete("/api/workflows/{workflow_id}")
async def delete_workflow(workflow_id: str):
    """删除工作流"""
    if workflow_id not in workflows_store:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    del workflows_store[workflow_id]
    
    # 通知所有连接的客户端
    await notify_clients({"type": "workflow_deleted", "workflow_id": workflow_id})
    
    return {"message": "Workflow deleted successfully"}

# ==================== 工作流执行 ====================

@app.post("/api/workflows/{workflow_id}/execute")
async def execute_workflow(workflow_id: str, request: ExecutionRequest):
    """执行工作流"""
    if workflow_id not in workflows_store:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = workflows_store[workflow_id]
    execution_id = f"exec_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # 创建执行记录
    execution = {
        "id": execution_id,
        "workflow_id": workflow_id,
        "status": "running",
        "started_at": datetime.now().isoformat(),
        "parameters": request.parameters,
        "results": {}
    }
    
    executions_store[execution_id] = execution
    
    # 异步执行工作流
    asyncio.create_task(run_workflow(workflow, execution))
    
    # 通知客户端
    await notify_clients({
        "type": "execution_started",
        "execution_id": execution_id,
        "workflow_id": workflow_id
    })
    
    return execution

async def run_workflow(workflow: Workflow, execution: Dict):
    """异步执行工作流"""
    try:
        # 模拟执行过程
        for i, node in enumerate(workflow.nodes):
            await asyncio.sleep(1)  # 模拟节点执行
            
            # 更新执行状态
            execution["results"][node.id] = {
                "status": "completed",
                "output": f"Node {node.name} executed successfully"
            }
            
            # 通知客户端进度
            await notify_clients({
                "type": "node_executed",
                "execution_id": execution["id"],
                "node_id": node.id,
                "progress": (i + 1) / len(workflow.nodes)
            })
        
        # 完成执行
        execution["status"] = "completed"
        execution["completed_at"] = datetime.now().isoformat()
        
        # 通知客户端完成
        await notify_clients({
            "type": "execution_completed",
            "execution_id": execution["id"],
            "results": execution["results"]
        })
        
    except Exception as e:
        execution["status"] = "failed"
        execution["error"] = str(e)
        
        await notify_clients({
            "type": "execution_failed",
            "execution_id": execution["id"],
            "error": str(e)
        })

@app.get("/api/executions")
async def get_executions():
    """获取所有执行记录"""
    return list(executions_store.values())

@app.get("/api/executions/{execution_id}")
async def get_execution(execution_id: str):
    """获取单个执行记录"""
    if execution_id not in executions_store:
        raise HTTPException(status_code=404, detail="Execution not found")
    return executions_store[execution_id]

# ==================== 节点库API ====================

@app.get("/api/nodes")
async def get_available_nodes():
    """获取可用的工作流节点"""
    nodes = [
        {
            "type": "data_source",
            "category": "数据",
            "name": "数据源",
            "description": "加载市场数据",
            "icon": "📊"
        },
        {
            "type": "factor_compute",
            "category": "因子",
            "name": "因子计算",
            "description": "计算技术因子",
            "icon": "🧮"
        },
        {
            "type": "ml_model",
            "category": "机器学习",
            "name": "ML模型",
            "description": "机器学习模型训练",
            "icon": "🤖"
        },
        {
            "type": "backtest",
            "category": "回测",
            "name": "策略回测",
            "description": "历史数据回测",
            "icon": "📈"
        },
        {
            "type": "visualization",
            "category": "可视化",
            "name": "图表展示",
            "description": "生成分析图表",
            "icon": "📉"
        },
        {
            "type": "risk_analysis",
            "category": "风控",
            "name": "风险分析",
            "description": "计算风险指标",
            "icon": "⚠️"
        },
        {
            "type": "portfolio_optimizer",
            "category": "优化",
            "name": "组合优化",
            "description": "投资组合优化",
            "icon": "🎯"
        },
        {
            "type": "alert",
            "category": "通知",
            "name": "预警通知",
            "description": "发送交易信号",
            "icon": "🔔"
        }
    ]
    return nodes

# ==================== WebSocket支持 ====================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket连接"""
    await websocket.accept()
    connected_clients.append(websocket)
    
    try:
        while True:
            # 接收客户端消息
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # 处理消息
            if message["type"] == "ping":
                await websocket.send_json({"type": "pong"})
            
            # 广播给所有客户端
            await notify_clients(message)
            
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

async def notify_clients(message: Dict):
    """通知所有连接的客户端"""
    for client in connected_clients:
        try:
            await client.send_json(message)
        except:
            connected_clients.remove(client)

# ==================== 市场数据API ====================

@app.get("/api/market/overview")
async def get_market_overview():
    """获取市场概况"""
    return {
        "indices": [
            {"name": "上证指数", "code": "000001.SH", "value": 3089.26, "change": -0.52},
            {"name": "深证成指", "code": "399001.SZ", "value": 9684.33, "change": -0.73},
            {"name": "创业板指", "code": "399006.SZ", "value": 1887.45, "change": -1.12}
        ],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/factors/list")
async def get_factors():
    """获取因子列表"""
    return {
        "factors": [
            {"id": "momentum_20", "name": "20日动量", "category": "动量类"},
            {"id": "rsi", "name": "RSI", "category": "技术指标"},
            {"id": "macd", "name": "MACD", "category": "技术指标"},
            {"id": "pe_ratio", "name": "市盈率", "category": "估值类"}
        ]
    }

# ==================== 静态文件服务 ====================

# 挂载静态文件目录
static_dir = Path(__file__).parent.parent / "static"
if not static_dir.exists():
    static_dir.mkdir(parents=True, exist_ok=True)

# 工作流UI静态文件
quantflow_dir = static_dir / "quantflow"
if not quantflow_dir.exists():
    quantflow_dir.mkdir(parents=True, exist_ok=True)

# 图表UI静态文件
charts_dir = static_dir / "charts"
if not charts_dir.exists():
    charts_dir.mkdir(parents=True, exist_ok=True)

# 挂载静态目录
app.mount("/quantflow", StaticFiles(directory=str(quantflow_dir), html=True), name="quantflow")
app.mount("/charts", StaticFiles(directory=str(charts_dir), html=True), name="charts")
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# ==================== 主程序入口 ====================

def main():
    """主程序入口"""
    print("=" * 80)
    print("🐼 PandaAI QuantFlow - 量化工作流平台")
    print("=" * 80)
    print()
    print("🚀 正在启动服务...")
    print()
    print("📊 服务地址:")
    print("   工作流: http://127.0.0.1:8000/quantflow/")
    print("   图表: http://127.0.0.1:8000/charts/")
    print("   API文档: http://127.0.0.1:8000/docs")
    print()
    print("=" * 80)
    
    # 启动服务
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,  # 改为False避免reload错误
        log_level="info"
    )

if __name__ == "__main__":
    main()
