from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json

from panda_llm.services.chat_service import ChatService
from panda_common.llm_manager import get_llm_manager
from panda_common.config import get_config

router = APIRouter()
chat_service = ChatService()

class ChatRequest(BaseModel):
    user_id: str
    message: str
    session_id: Optional[str] = None

class SimpleChatRequest(BaseModel):
    message: str
    model: Optional[str] = "deepseek"
    history: Optional[List[Dict[str, str]]] = []
    conversation_id: Optional[str] = None

@router.post("/llm/chat")
async def chat(request: ChatRequest):
    """处理聊天请求"""
    try:
        # 使用流式处理
        async def generate():
            try:
                # async for chunk in chat_service.process_message_stream(
                async for chunk in chat_service.process_message_stream(
                    request.user_id,
                    request.message,
                    request.session_id
                ):
                    yield f"data: {json.dumps({'content': chunk})}\n\n"
            except ValueError as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': '处理消息时发生错误'})}\n\n"
            finally:
                yield "data: [DONE]\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/llm/chat/sessions")
async def get_sessions(user_id: str, limit: int = 10):
    """获取用户的聊天会话列表"""
    try:
        sessions = await chat_service.get_user_sessions(user_id, limit)
        return {"sessions": [session.dict() for session in sessions]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/llm/status")
async def get_llm_status():
    """获取LLM管理器状态（多密钥状态）"""
    from fastapi.responses import JSONResponse
    try:
        config = get_config()
        llm_manager = get_llm_manager(config)
        status = llm_manager.get_status()
        return JSONResponse(
            content={
                "success": True,
                "data": status
            },
            media_type="application/json; charset=utf-8"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/llm/models")
async def get_available_models():
    """获取可用的LLM模型列表"""
    try:
        config = get_config()
        llm_manager = get_llm_manager(config)
        
        models = {
            "deepseek": {
                "name": "DeepSeek V3",
                "model_id": llm_manager.get_model('deepseek'),
                "description": "代码生成和技术分析专家",
                "best_for": ["因子代码生成", "技术指标实现", "代码优化"],
                "status": "available",
                "free": True
            },
            "qwen": {
                "name": "Qwen 2.5 (72B)",
                "model_id": llm_manager.get_model('qwen'),
                "description": "中文理解和通用分析专家",
                "best_for": ["市场解读", "新闻分析", "中文对话"],
                "status": "available",
                "free": True
            },
            "qwen_coder": {
                "name": "Qwen 2.5 Coder (32B)",
                "model_id": llm_manager.get_model('qwen_coder'),
                "description": "专业代码生成模型",
                "best_for": ["因子代码", "算法实现", "代码调试"],
                "status": "available",
                "free": True
            },
            "glm": {
                "name": "GLM-4 (9B)",
                "model_id": llm_manager.get_model('glm'),
                "description": "智谱AI通用模型",
                "best_for": ["通用对话", "文本分析", "知识问答"],
                "status": "available",
                "free": True
            }
        }
        
        return {
            "success": True,
            "data": {
                "models": models,
                "default_model": config.get("LLM_MODEL"),
                "total_api_keys": len(config.get("LLM_API_KEYS", [])),
                "load_balance_strategy": config.get("LLM_LOAD_BALANCE_STRATEGY")
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ModelSwitchRequest(BaseModel):
    model_type: str  # deepseek, claude, kimi, qwen

@router.post("/llm/switch_model")
async def switch_model(request: ModelSwitchRequest):
    """切换LLM模型"""
    try:
        config = get_config()
        llm_manager = get_llm_manager(config)
        
        model_id = llm_manager.get_model(request.model_type)
        
        if not model_id:
            raise HTTPException(status_code=400, detail=f"未知的模型类型: {request.model_type}")
        
        return {
            "success": True,
            "data": {
                "model_type": request.model_type,
                "model_id": model_id,
                "message": f"已切换到 {request.model_type} 模型"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/llm/chat/simple")
async def simple_chat(request: SimpleChatRequest):
    """简化的聊天接口，不需要user_id"""
    try:
        config = get_config()
        llm_manager = get_llm_manager(config)
        
        # 构建消息历史
        messages = []
        for msg in request.history[-10:]:  # 只保留最近10条
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # 添加当前消息
        messages.append({
            "role": "user",
            "content": request.message
        })
        
        # 调用LLM（使用正确的方法名）
        model_id = llm_manager.get_model(request.model)
        response = llm_manager.chat_completion(
            messages=messages,
            model=model_id
        )
        
        # 提取回复文本
        reply_text = response['choices'][0]['message']['content']
        
        return {
            "success": True,
            "response": reply_text,
            "model": request.model,
            "usage": response.get('usage', {})
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"调用失败: {str(e)}"
        } 