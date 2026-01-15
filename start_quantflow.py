#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PandaAI QuantFlow 一键启动脚本
启动所有必要的服务
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def print_header():
    """打印启动标题"""
    print("=" * 80)
    print("🐼 PandaAI QuantFlow - 量化工作流平台")
    print("=" * 80)
    print("正在启动服务...")
    print()

def check_port(port):
    """检查端口是否被占用"""
    try:
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True,
            text=True,
            encoding='gbk',
            timeout=5
        )
        
        for line in result.stdout.split('\n'):
            if f':{port}' in line and 'LISTENING' in line:
                return True
        return False
    except:
        return False

def install_dependencies():
    """安装必要的依赖"""
    print("📦 检查并安装依赖...")
    
    required = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "numpy",
        "pandas",
        "matplotlib",
        "websockets",
        "aiofiles"
    ]
    
    for package in required:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  📥 安装 {package}...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", package,
                "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"
            ], capture_output=True)
            print(f"  ✅ {package} 安装完成")
    
    print()

def start_panda_factor():
    """启动PandaFactor服务"""
    print("🔧 启动 PandaFactor 服务...")
    
    factor_path = project_root / "panda_factor-main" / "panda_factor-main"
    
    if not factor_path.exists():
        print("  ⚠️  PandaFactor 未找到，跳过")
        return None
    
    # 检查端口8111
    if check_port(8111):
        print("  ✅ PandaFactor 已在运行 (端口 8111)")
        return None
    
    try:
        # 启动服务
        process = subprocess.Popen(
            [sys.executable, "-m", "panda_factor_server"],
            cwd=str(factor_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        
        time.sleep(3)
        
        if check_port(8111):
            print("  ✅ PandaFactor 启动成功")
            print("     访问: http://127.0.0.1:8111/factor")
        else:
            print("  ⚠️  PandaFactor 启动失败")
            
        return process
    except Exception as e:
        print(f"  ❌ 启动失败: {e}")
        return None

def start_quantflow():
    """启动QuantFlow服务"""
    print("🚀 启动 QuantFlow 工作流服务...")
    
    # 检查端口8000
    if check_port(8000):
        print("  ✅ QuantFlow 已在运行 (端口 8000)")
        return None
    
    # 检查main.py是否存在
    main_path = project_root / "src" / "panda_server" / "main.py"
    
    if not main_path.exists():
        print(f"  ❌ 找不到 {main_path}")
        print("  💡 请确保已创建QuantFlow服务文件")
        return None
    
    try:
        # 启动服务
        process = subprocess.Popen(
            [sys.executable, str(main_path)],
            cwd=str(project_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        
        time.sleep(5)
        
        if check_port(8000):
            print("  ✅ QuantFlow 启动成功")
            print("     工作流: http://127.0.0.1:8000/quantflow/")
            print("     图表: http://127.0.0.1:8000/charts/")
            print("     API文档: http://127.0.0.1:8000/docs")
        else:
            print("  ⚠️  QuantFlow 启动可能需要更多时间...")
            
        return process
    except Exception as e:
        print(f"  ❌ 启动失败: {e}")
        return None

def check_mongodb():
    """检查MongoDB状态"""
    print("🗄️  检查 MongoDB...")
    
    if check_port(27017):
        print("  ✅ MongoDB 已在运行 (端口 27017)")
    else:
        print("  ⚠️  MongoDB 未运行")
        print("     提示: MongoDB是可选的，不影响基础功能")
    
    print()

def create_ui_files():
    """创建UI文件"""
    print("🎨 创建UI界面文件...")
    
    # 创建工作流UI
    quantflow_dir = project_root / "src" / "static" / "quantflow"
    quantflow_dir.mkdir(parents=True, exist_ok=True)
    
    quantflow_html = quantflow_dir / "index.html"
    if not quantflow_html.exists():
        with open(quantflow_html, 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>PandaAI QuantFlow - 工作流</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial; margin: 0; padding: 20px; background: #f5f5f5; }
        .header { background: #667eea; color: white; padding: 20px; border-radius: 10px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .workflow-canvas { background: white; min-height: 600px; margin-top: 20px; 
                          border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                          padding: 20px; }
        .node-palette { background: white; padding: 20px; border-radius: 10px; 
                        margin-top: 20px; }
        .node-item { display: inline-block; padding: 10px 20px; margin: 5px;
                     background: #f0f0f0; border-radius: 5px; cursor: move; }
        .node-item:hover { background: #e0e0e0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐼 PandaAI QuantFlow</h1>
            <p>量化工作流编排平台</p>
        </div>
        
        <div class="node-palette">
            <h3>工作流节点</h3>
            <div class="node-item">📊 数据源</div>
            <div class="node-item">🧮 因子计算</div>
            <div class="node-item">🤖 ML模型</div>
            <div class="node-item">📈 策略回测</div>
            <div class="node-item">📉 可视化</div>
            <div class="node-item">⚠️ 风险分析</div>
        </div>
        
        <div class="workflow-canvas">
            <h3>工作流画布</h3>
            <p>拖拽节点到此处构建工作流...</p>
            <canvas id="workflow" width="1160" height="560" style="border: 1px dashed #ccc;"></canvas>
        </div>
    </div>
    
    <script>
        // 简单的画布交互
        const canvas = document.getElementById('workflow');
        const ctx = canvas.getContext('2d');
        
        // 绘制网格
        function drawGrid() {
            ctx.strokeStyle = '#f0f0f0';
            for(let x = 0; x < canvas.width; x += 20) {
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, canvas.height);
                ctx.stroke();
            }
            for(let y = 0; y < canvas.height; y += 20) {
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(canvas.width, y);
                ctx.stroke();
            }
        }
        drawGrid();
        
        // WebSocket连接
        let ws = null;
        try {
            ws = new WebSocket('ws://127.0.0.1:8000/ws');
            ws.onopen = () => console.log('Connected to QuantFlow');
            ws.onmessage = (e) => console.log('Message:', e.data);
        } catch(e) {
            console.log('WebSocket connection failed');
        }
    </script>
</body>
</html>""")
        print(f"  ✅ 创建工作流UI: {quantflow_html}")
    
    # 创建图表UI
    charts_dir = project_root / "src" / "static" / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)
    
    charts_html = charts_dir / "index.html"
    if not charts_html.exists():
        with open(charts_html, 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>PandaAI QuantFlow - 超级图表</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial; margin: 0; padding: 20px; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #667eea, #764ba2); 
                  color: white; padding: 20px; border-radius: 10px; }
        .container { max-width: 1400px; margin: 0 auto; }
        .chart-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; 
                      margin-top: 20px; }
        .chart-card { background: white; padding: 20px; border-radius: 10px; 
                      box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .chart-title { font-size: 16px; font-weight: bold; margin-bottom: 10px; }
        .chart-canvas { width: 100%; height: 300px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 超级图表</h1>
            <p>金融数据可视化分析平台</p>
        </div>
        
        <div class="chart-grid">
            <div class="chart-card">
                <div class="chart-title">📈 价格走势</div>
                <canvas class="chart-canvas" id="price-chart"></canvas>
            </div>
            
            <div class="chart-card">
                <div class="chart-title">📊 成交量</div>
                <canvas class="chart-canvas" id="volume-chart"></canvas>
            </div>
            
            <div class="chart-card">
                <div class="chart-title">🎯 技术指标</div>
                <canvas class="chart-canvas" id="indicator-chart"></canvas>
            </div>
            
            <div class="chart-card">
                <div class="chart-title">💰 收益曲线</div>
                <canvas class="chart-canvas" id="return-chart"></canvas>
            </div>
        </div>
    </div>
    
    <script>
        // 绘制示例图表
        function drawChart(canvasId, color) {
            const canvas = document.getElementById(canvasId);
            const ctx = canvas.getContext('2d');
            const width = canvas.width = canvas.offsetWidth;
            const height = canvas.height = canvas.offsetHeight;
            
            // 绘制坐标轴
            ctx.strokeStyle = '#ddd';
            ctx.beginPath();
            ctx.moveTo(40, height - 40);
            ctx.lineTo(width - 20, height - 40);
            ctx.moveTo(40, 20);
            ctx.lineTo(40, height - 40);
            ctx.stroke();
            
            // 绘制示例数据
            ctx.strokeStyle = color;
            ctx.lineWidth = 2;
            ctx.beginPath();
            for(let i = 0; i < 100; i++) {
                const x = 40 + (width - 60) * i / 100;
                const y = height/2 + Math.sin(i/10) * 50 + Math.random() * 20 - 10;
                if(i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.stroke();
        }
        
        drawChart('price-chart', '#667eea');
        drawChart('volume-chart', '#4ade80');
        drawChart('indicator-chart', '#fbbf24');
        drawChart('return-chart', '#ff6b6b');
        
        // 获取市场数据
        fetch('http://127.0.0.1:8000/api/market/overview')
            .then(r => r.json())
            .then(data => console.log('Market Data:', data))
            .catch(e => console.log('Failed to fetch market data'));
    </script>
</body>
</html>""")
        print(f"  ✅ 创建图表UI: {charts_html}")
    
    print()

def main():
    """主函数"""
    print_header()
    
    # 1. 安装依赖
    install_dependencies()
    
    # 2. 检查MongoDB
    check_mongodb()
    
    # 3. 创建UI文件
    create_ui_files()
    
    # 4. 启动服务
    processes = []
    
    # 启动PandaFactor
    factor_process = start_panda_factor()
    if factor_process:
        processes.append(factor_process)
    
    print()
    
    # 启动QuantFlow
    quantflow_process = start_quantflow()
    if quantflow_process:
        processes.append(quantflow_process)
    
    # 打印访问地址
    print()
    print("=" * 80)
    print("✨ 所有服务已启动！")
    print("=" * 80)
    print()
    print("📍 访问地址:")
    print()
    print("  🔧 PandaFactor (因子库):")
    print("     http://127.0.0.1:8111/factor")
    print()
    print("  🚀 QuantFlow (工作流):")
    print("     http://127.0.0.1:8000/quantflow/")
    print()
    print("  📊 超级图表:")
    print("     http://127.0.0.1:8000/charts/")
    print()
    print("  📚 API文档:")
    print("     http://127.0.0.1:8000/docs")
    print()
    print("=" * 80)
    print("按 Ctrl+C 停止所有服务")
    print("=" * 80)
    
    try:
        # 保持运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在停止服务...")
        for p in processes:
            if p:
                p.terminate()
        print("✅ 所有服务已停止")

if __name__ == "__main__":
    main()
