// 全局变量
let currentModel = 'deepseek';
let messages = [];
let isTyping = false;
const API_BASE = 'http://127.0.0.1:8111';

// 模型配置
const models = {
    deepseek: { name: 'DeepSeek V3', desc: '代码生成专家' },
    qwen: { name: 'Qwen 2.5 72B', desc: '中文理解专家' },
    qwen_coder: { name: 'Qwen Coder 32B', desc: '专业编程模型' },
    glm: { name: 'GLM-4 9B', desc: '通用对话模型' }
};

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    setupInputHandlers();
    adjustTextareaHeight();
    loadMarketData();
    checkAPIStatus();
    loadFunctions();
});

// 加载功能列表
function loadFunctions() {
    const functionList = document.getElementById('functionList');
    const functions = [
        { icon: '📊', title: '因子生成', desc: '智能生成量化因子', action: 'factor' },
        { icon: '📈', title: '策略回测', desc: '历史数据回测分析', action: 'backtest' },
        { icon: '🔍', title: '技术分析', desc: 'MACD, RSI, 布林带等', action: 'technical' },
        { icon: '⚠️', title: '风险管理', desc: 'VaR, 夏普率计算', action: 'risk' }
    ];
    
    functionList.innerHTML = functions.map(func => `
        <div class="function-item" onclick="selectFunction('${func.action}')">
            <div class="function-icon">${func.icon}</div>
            <div class="function-info">
                <div class="function-title">${func.title}</div>
                <div class="function-desc">${func.desc}</div>
            </div>
        </div>
    `).join('');
}

// 设置输入处理
function setupInputHandlers() {
    const input = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    
    input.addEventListener('input', function() {
        const hasContent = this.value.trim().length > 0;
        sendBtn.disabled = !hasContent || isTyping;
        adjustTextareaHeight();
    });
    
    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

// 自动调整输入框高度
function adjustTextareaHeight() {
    const textarea = document.getElementById('messageInput');
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
}

// 切换模型下拉菜单
function toggleModelDropdown() {
    const dropdown = document.getElementById('modelDropdown');
    dropdown.classList.toggle('show');
    
    // 点击外部关闭
    document.addEventListener('click', function closeDropdown(e) {
        if (!e.target.closest('.model-selector')) {
            dropdown.classList.remove('show');
            document.removeEventListener('click', closeDropdown);
        }
    });
}

// 选择模型
async function selectModel(model) {
    currentModel = model;
    
    // 更新UI
    document.getElementById('currentModelName').textContent = models[model].name;
    document.querySelectorAll('.model-option').forEach(opt => {
        opt.classList.remove('selected');
    });
    event.target.closest('.model-option').classList.add('selected');
    
    // 关闭下拉菜单
    document.getElementById('modelDropdown').classList.remove('show');
    
    // 调用后端切换模型
    try {
        const response = await fetch(`${API_BASE}/llm/switch_model`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ model_type: model })
        });
        
        if (response.ok) {
            const data = await response.json();
            showNotification(`已切换到 ${models[model].name}`, 'success');
        }
    } catch (error) {
        showNotification('模型切换失败', 'error');
    }
}

// 发送消息
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message || isTyping) return;
    
    // 添加用户消息
    addMessage('user', message);
    input.value = '';
    adjustTextareaHeight();
    
    // 显示输入中
    isTyping = true;
    document.getElementById('sendBtn').disabled = true;
    const typingId = addTypingIndicator();
    
    try {
        // 检查是否是分析命令
        if (message.startsWith('/analyze') || message.includes('分析')) {
            await handleAnalysisCommand(message, typingId);
        } else if (message.startsWith('/chart') || message.includes('图表')) {
            await handleChartCommand(message, typingId);
        } else {
            // 普通对话
            const response = await fetch(`${API_BASE}/llm/chat/simple`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    model: currentModel,
                    history: messages.slice(-10)
                })
            });
            
            removeTypingIndicator(typingId);
            
            if (response.ok) {
                const data = await response.json();
                
                // 检查 API 返回的 success 字段
                if (data.success === false) {
                    // API 调用失败，显示错误信息
                    const errorMsg = data.error || data.message || '调用失败';
                    addMessage('assistant', `❌ 错误: ${errorMsg}\n\n请检查：\n1. LLM API 密钥是否配置正确\n2. 网络连接是否正常\n3. API 服务是否可用`);
                } else {
                    // API 调用成功
                    const reply = data.response || data.data || '抱歉，我没有收到回复。';
                    addMessage('assistant', reply);
                }
            } else {
                throw new Error('API请求失败');
            }
        }
    } catch (error) {
        removeTypingIndicator(typingId);
        addMessage('assistant', '抱歉，处理失败：' + error.message);
    } finally {
        isTyping = false;
        document.getElementById('sendBtn').disabled = false;
    }
}

// 处理分析命令
async function handleAnalysisCommand(message, typingId) {
    try {
        // 提取股票代码
        const codeMatch = message.match(/\d{6}/);
        const code = codeMatch ? codeMatch[0] : '000001';
        
        const response = await fetch(`${API_BASE}/analysis/stock`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                code: code,
                period: 30,
                analysis_type: 'technical'
            })
        });
        
        removeTypingIndicator(typingId);
        
        if (response.ok) {
            const data = await response.json();
            addAnalysisResult(data);
        }
    } catch (error) {
        removeTypingIndicator(typingId);
        addMessage('assistant', '分析失败：' + error.message);
    }
}

// 处理图表命令
async function handleChartCommand(message, typingId) {
    try {
        // 生成示例数据
        const data = [];
        for (let i = 0; i < 30; i++) {
            data.push({
                x: i,
                y: Math.sin(i / 5) * 10 + Math.random() * 5 + 50
            });
        }
        
        const response = await fetch(`${API_BASE}/analysis/chart`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                data: data,
                chart_type: 'line',
                title: '数据分析图表',
                x_label: '时间',
                y_label: '数值'
            })
        });
        
        removeTypingIndicator(typingId);
        
        if (response.ok) {
            const result = await response.json();
            addChartResult(result);
        }
    } catch (error) {
        removeTypingIndicator(typingId);
        addMessage('assistant', '图表生成失败：' + error.message);
    }
}

// 添加分析结果
function addAnalysisResult(data) {
    const container = document.getElementById('messagesContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="message-text">
                <p><strong>股票分析结果 - ${data.code}</strong></p>
                <div style="margin-top: 12px; padding: 12px; background: var(--bg-sidebar); border-radius: 8px;">
                    <p>📊 最新价格: ¥${data.latest_price.toFixed(2)}</p>
                    <p>📈 涨跌幅: ${data.change_pct > 0 ? '+' : ''}${data.change_pct.toFixed(2)}%</p>
                    <p style="margin-top: 8px;"><strong>技术指标:</strong></p>
                    <ul style="margin: 8px 0 0 20px;">
                        <li>MA5: ${data.indicators.MA5?.toFixed(2) || 'N/A'}</li>
                        <li>MA20: ${data.indicators.MA20?.toFixed(2) || 'N/A'}</li>
                        <li>RSI: ${data.indicators.RSI?.toFixed(2) || 'N/A'}</li>
                        <li>MACD: ${data.indicators.MACD?.toFixed(2) || 'N/A'}</li>
                    </ul>
                    <p style="margin-top: 8px;"><strong>信号建议:</strong></p>
                    <ul style="margin: 8px 0 0 20px;">
                        <li>趋势: ${data.signals.trend}</li>
                        <li>RSI: ${data.signals.rsi_signal}</li>
                        <li>MACD: ${data.signals.macd_signal}</li>
                    </ul>
                </div>
            </div>
        </div>
    `;
    
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

// 添加图表结果
function addChartResult(result) {
    const container = document.getElementById('messagesContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="message-text">
                <div class="chart-container">
                    <div class="chart-header">
                        <div class="chart-title">数据分析图表</div>
                        <div class="chart-actions">
                            <button class="chart-btn" onclick="downloadChart('${result.image}')">下载</button>
                            <button class="chart-btn" onclick="copyChart('${result.image}')">复制</button>
                        </div>
                    </div>
                    <img src="${result.image}" alt="Chart" class="chart-image">
                </div>
            </div>
        </div>
    `;
    
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

// 添加消息
function addMessage(role, content) {
    const container = document.getElementById('messagesContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatar = role === 'user' ? 'U' : '🤖';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-text">${formatMessage(content)}</div>
        </div>
    `;
    
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
    
    // 保存到历史
    messages.push({ role, content });
}

// 格式化消息
function formatMessage(content) {
    return content
        .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\n/g, '<br>');
}

// 添加输入指示器
function addTypingIndicator() {
    const container = document.getElementById('messagesContainer');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message assistant';
    typingDiv.id = 'typing-' + Date.now();
    
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="typing-indicator">
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>
    `;
    
    container.appendChild(typingDiv);
    container.scrollTop = container.scrollHeight;
    
    return typingDiv.id;
}

// 移除输入指示器
function removeTypingIndicator(id) {
    const indicator = document.getElementById(id);
    if (indicator) {
        indicator.remove();
    }
}

// 切换分析面板
function toggleAnalysisPanel() {
    const panel = document.getElementById('analysisPanel');
    panel.classList.toggle('show');
}

// 加载市场数据
async function loadMarketData() {
    try {
        const response = await fetch(`${API_BASE}/analysis/market_overview`);
        if (response.ok) {
            const data = await response.json();
            displayMarketData(data);
        }
    } catch (error) {
        console.error('加载市场数据失败:', error);
    }
}

// 显示市场数据
function displayMarketData(data) {
    // 显示指数
    const indicesList = document.getElementById('indicesList');
    indicesList.innerHTML = data.indices.map(index => `
        <div class="stock-card">
            <div class="stock-info">
                <div class="stock-name">${index.name}</div>
                <div class="stock-code">${index.code}</div>
            </div>
            <div class="stock-price">
                <div class="price-value">${index.price.toFixed(2)}</div>
                <div class="price-change ${index.change >= 0 ? 'positive' : 'negative'}">
                    ${index.change >= 0 ? '+' : ''}${index.change.toFixed(2)}%
                </div>
            </div>
        </div>
    `).join('');
    
    // 显示板块
    const sectorsList = document.getElementById('sectorsList');
    sectorsList.innerHTML = data.sectors.map(sector => `
        <div class="stock-card">
            <div class="stock-info">
                <div class="stock-name">${sector.name}</div>
                <div class="stock-code">${sector.leader}</div>
            </div>
            <div class="stock-price">
                <div class="price-change ${sector.change >= 0 ? 'positive' : 'negative'}">
                    ${sector.change >= 0 ? '+' : ''}${sector.change.toFixed(2)}%
                </div>
            </div>
        </div>
    `).join('');
    
    // 显示热门股票
    const stocksList = document.getElementById('stocksList');
    stocksList.innerHTML = data.hot_stocks.map(stock => `
        <div class="stock-card">
            <div class="stock-info">
                <div class="stock-name">${stock.name}</div>
                <div class="stock-code">${stock.code}</div>
            </div>
            <div class="stock-price">
                <div class="price-value">${stock.price.toFixed(2)}</div>
                <div class="price-change ${stock.change >= 0 ? 'positive' : 'negative'}">
                    ${stock.change >= 0 ? '+' : ''}${stock.change.toFixed(2)}%
                </div>
            </div>
        </div>
    `).join('');
}

// 检查API状态
async function checkAPIStatus() {
    try {
        const response = await fetch(`${API_BASE}/api/status`);
        const statusElement = document.getElementById('apiStatus');
        
        if (response.ok) {
            statusElement.textContent = 'API 已连接';
            statusElement.style.color = 'var(--success)';
        } else {
            throw new Error('API响应错误');
        }
    } catch (error) {
        const statusElement = document.getElementById('apiStatus');
        statusElement.textContent = 'API 未连接';
        statusElement.style.color = 'var(--danger)';
    }
}

// 运行分析
function runAnalysis() {
    const input = document.getElementById('messageInput');
    const message = input.value || '/analyze 000001';
    input.value = message;
    sendMessage();
}

// 插入图表命令
function insertChartCommand() {
    const input = document.getElementById('messageInput');
    input.value = '/chart 生成30日价格走势图';
    input.focus();
}

// 插入分析命令
function insertAnalysisCommand() {
    const input = document.getElementById('messageInput');
    input.value = '/analyze 000001 技术分析';
    input.focus();
}

// 插入回测命令
function insertBacktestCommand() {
    const input = document.getElementById('messageInput');
    input.value = '请帮我回测一个20日动量因子';
    input.focus();
}

// 选择功能
function selectFunction(action) {
    const commands = {
        factor: '请帮我生成一个动量因子',
        backtest: '请对MACD策略进行回测',
        technical: '/analyze 000001 技术分析',
        risk: '计算投资组合的VaR和夏普率'
    };
    
    const input = document.getElementById('messageInput');
    input.value = commands[action] || '';
    input.focus();
}

// 切换标签页
function switchTab(tab) {
    // 更新标签样式
    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
    event.target.classList.add('active');
    
    // 更新功能列表
    if (tab === 'analysis') {
        loadAnalysisFunctions();
    } else if (tab === 'tools') {
        loadToolsFunctions();
    } else {
        loadFunctions();
    }
}

// 加载分析功能
function loadAnalysisFunctions() {
    const functionList = document.getElementById('functionList');
    const functions = [
        { icon: '📊', title: '股票分析', desc: '个股技术分析', action: 'stock' },
        { icon: '📈', title: '板块分析', desc: '行业板块分析', action: 'sector' },
        { icon: '🔍', title: '因子分析', desc: '多因子分析', action: 'factors' },
        { icon: '💹', title: '市场概况', desc: '市场整体分析', action: 'market' }
    ];
    
    functionList.innerHTML = functions.map(func => `
        <div class="function-item" onclick="selectFunction('${func.action}')">
            <div class="function-icon">${func.icon}</div>
            <div class="function-info">
                <div class="function-title">${func.title}</div>
                <div class="function-desc">${func.desc}</div>
            </div>
        </div>
    `).join('');
}

// 加载工具功能
function loadToolsFunctions() {
    const functionList = document.getElementById('functionList');
    const functions = [
        { icon: '🛠️', title: 'Matplotlib绘图', desc: 'Python数据可视化', action: 'matplotlib' },
        { icon: '📉', title: '指标计算', desc: '技术指标计算', action: 'indicators' },
        { icon: '⚙️', title: '参数优化', desc: '策略参数优化', action: 'optimize' },
        { icon: '📝', title: '报告生成', desc: '分析报告生成', action: 'report' }
    ];
    
    functionList.innerHTML = functions.map(func => `
        <div class="function-item" onclick="selectFunction('${func.action}')">
            <div class="function-icon">${func.icon}</div>
            <div class="function-info">
                <div class="function-title">${func.title}</div>
                <div class="function-desc">${func.desc}</div>
            </div>
        </div>
    `).join('');
}

// 文件上传处理
function handleFileUpload(event) {
    const files = event.target.files;
    if (files.length > 0) {
        const fileNames = Array.from(files).map(f => f.name).join(', ');
        const input = document.getElementById('messageInput');
        input.value = `[已上传: ${fileNames}]\n` + input.value;
        adjustTextareaHeight();
    }
}

// 显示通知
function showNotification(message, type = 'info') {
    console.log(`${type}: ${message}`);
    // 可以添加更友好的通知UI
}

// 定期检查API状态
setInterval(checkAPIStatus, 30000);

// 打开 QuantFlow 工作流
function openQuantFlow() {
    window.open('http://127.0.0.1:8000/quantflow/', '_blank');
}

// 下载图表
function downloadChart(imageData) {
    const link = document.createElement('a');
    link.href = imageData;
    link.download = 'chart.png';
    link.click();
}

// 复制图表
function copyChart(imageData) {
    navigator.clipboard.writeText(imageData).then(() => {
        showNotification('图表已复制到剪贴板', 'success');
    });
}
