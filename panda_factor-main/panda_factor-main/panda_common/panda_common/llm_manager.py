"""
LLM管理器 - 支持多API密钥负载均衡和故障转移
"""

import time
import random
import logging
from typing import List, Dict, Any, Optional
from openai import OpenAI

logger = logging.getLogger(__name__)


class LLMManager:
    """
    LLM管理器，支持：
    1. 多API密钥轮询
    2. 自动故障转移
    3. 负载均衡
    4. 重试机制
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化LLM管理器
        
        Args:
            config: 配置字典
        """
        # 获取API密钥列表
        self.api_keys = config.get('LLM_API_KEYS', [])
        if not self.api_keys:
            # 兼容旧配置
            single_key = config.get('LLM_API_KEY', '')
            if single_key:
                self.api_keys = [single_key]
        
        if not self.api_keys:
            raise ValueError("未配置LLM API密钥")
        
        self.base_url = config.get('LLM_BASE_URL', 'https://api.siliconflow.cn/v1')
        self.default_model = config.get('LLM_MODEL', 'deepseek-ai/DeepSeek-V3')
        self.models = config.get('LLM_MODELS', {})
        
        # 负载均衡策略
        self.strategy = config.get('LLM_LOAD_BALANCE_STRATEGY', 'round_robin')
        self.current_key_index = 0
        
        # 重试配置
        self.max_retries = config.get('LLM_MAX_RETRIES', 3)
        self.retry_delay = config.get('LLM_RETRY_DELAY', 1)
        
        # 密钥状态跟踪
        self.key_failures = {key: 0 for key in self.api_keys}
        self.key_last_success = {key: time.time() for key in self.api_keys}
        
        logger.info(f"LLM管理器初始化完成，共{len(self.api_keys)}个API密钥")
        logger.info(f"负载均衡策略: {self.strategy}")
        logger.info(f"默认模型: {self.default_model}")
    
    def _get_next_api_key(self) -> str:
        """
        根据策略获取下一个API密钥
        
        Returns:
            API密钥
        """
        if self.strategy == 'round_robin':
            # 轮询策略
            key = self.api_keys[self.current_key_index]
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            return key
        
        elif self.strategy == 'random':
            # 随机策略
            return random.choice(self.api_keys)
        
        elif self.strategy == 'failover':
            # 故障转移策略：优先使用失败次数少的
            sorted_keys = sorted(
                self.api_keys,
                key=lambda k: (self.key_failures[k], -self.key_last_success[k])
            )
            return sorted_keys[0]
        
        else:
            return self.api_keys[0]
    
    def _create_client(self, api_key: str) -> OpenAI:
        """
        创建OpenAI客户端
        
        Args:
            api_key: API密钥
            
        Returns:
            OpenAI客户端
        """
        return OpenAI(
            api_key=api_key,
            base_url=self.base_url
        )
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        聊天补全，支持自动重试和故障转移
        
        Args:
            messages: 消息列表
            model: 模型名称（可选）
            temperature: 温度参数
            max_tokens: 最大token数
            **kwargs: 其他参数
            
        Returns:
            响应字典
        """
        model = model or self.default_model
        
        # 尝试所有API密钥
        tried_keys = set()
        last_error = None
        
        while len(tried_keys) < len(self.api_keys):
            api_key = self._get_next_api_key()
            
            if api_key in tried_keys:
                continue
            
            tried_keys.add(api_key)
            
            # 重试当前密钥
            for attempt in range(self.max_retries):
                try:
                    logger.info(f"使用API密钥 {api_key[:20]}... 调用模型 {model} (尝试 {attempt + 1}/{self.max_retries})")
                    
                    client = self._create_client(api_key)
                    
                    response = client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        **kwargs
                    )
                    
                    # 成功
                    self.key_failures[api_key] = 0
                    self.key_last_success[api_key] = time.time()
                    
                    logger.info(f"API调用成功，使用密钥 {api_key[:20]}...")
                    
                    # 转换为字典
                    return {
                        'id': response.id,
                        'model': response.model,
                        'choices': [
                            {
                                'index': choice.index,
                                'message': {
                                    'role': choice.message.role,
                                    'content': choice.message.content
                                },
                                'finish_reason': choice.finish_reason
                            }
                            for choice in response.choices
                        ],
                        'usage': {
                            'prompt_tokens': response.usage.prompt_tokens,
                            'completion_tokens': response.usage.completion_tokens,
                            'total_tokens': response.usage.total_tokens
                        }
                    }
                
                except Exception as e:
                    last_error = e
                    logger.warning(f"API调用失败 (密钥 {api_key[:20]}..., 尝试 {attempt + 1}/{self.max_retries}): {e}")
                    
                    # 记录失败
                    self.key_failures[api_key] += 1
                    
                    # 如果不是最后一次尝试，等待后重试
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
            
            logger.warning(f"API密钥 {api_key[:20]}... 所有重试均失败，切换到下一个密钥")
        
        # 所有密钥都失败
        error_msg = f"所有API密钥均失败，最后错误: {last_error}"
        logger.error(error_msg)
        raise Exception(error_msg)
    
    def get_model(self, model_type: str) -> str:
        """
        获取指定类型的模型名称
        
        Args:
            model_type: 模型类型 (deepseek, claude, kimi, qwen)
            
        Returns:
            模型名称
        """
        return self.models.get(model_type, self.default_model)
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取管理器状态
        
        Returns:
            状态字典
        """
        return {
            'total_keys': len(self.api_keys),
            'strategy': self.strategy,
            'default_model': self.default_model,
            'available_models': self.models,
            'key_status': [
                {
                    'key': f"{key[:20]}...",
                    'failures': self.key_failures[key],
                    'last_success': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.key_last_success[key]))
                }
                for key in self.api_keys
            ]
        }


# 全局LLM管理器实例
_llm_manager: Optional[LLMManager] = None


def get_llm_manager(config: Optional[Dict[str, Any]] = None) -> LLMManager:
    """
    获取全局LLM管理器实例
    
    Args:
        config: 配置字典（首次调用时需要）
        
    Returns:
        LLM管理器实例
    """
    global _llm_manager
    
    if _llm_manager is None:
        if config is None:
            from panda_common.config import config as default_config
            config = default_config
        
        _llm_manager = LLMManager(config)
    
    return _llm_manager
