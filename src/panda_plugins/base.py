"""
工作流节点基类和装饰器
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel
import inspect
import functools

# ==================== 基础模型 ====================

class NodeMetadata(BaseModel):
    """节点元数据"""
    name: str
    group: str = "默认"
    description: str = ""
    version: str = "1.0.0"
    author: str = "PandaAI"
    icon: str = "📦"
    tags: List[str] = []

class NodeInput(BaseModel):
    """节点输入基类"""
    pass

class NodeOutput(BaseModel):
    """节点输出基类"""
    pass

# ==================== 工作节点基类 ====================

class BaseWorkNode(ABC):
    """
    工作流节点基类
    所有自定义节点必须继承此类
    """
    
    def __init__(self):
        self.metadata = self._get_metadata()
        self._input_model = None
        self._output_model = None
    
    @classmethod
    @abstractmethod
    def input_model(cls) -> Optional[Type[BaseModel]]:
        """
        返回节点的输入模型
        使用Pydantic定义输入参数结构
        """
        pass
    
    @classmethod
    @abstractmethod
    def output_model(cls) -> Optional[Type[BaseModel]]:
        """
        返回节点的输出模型
        使用Pydantic定义输出结果结构
        """
        pass
    
    @abstractmethod
    def run(self, input: BaseModel) -> BaseModel:
        """
        节点执行逻辑
        接收输入模型，返回输出模型
        """
        pass
    
    def _get_metadata(self) -> NodeMetadata:
        """获取节点元数据"""
        if hasattr(self.__class__, '_metadata'):
            return self.__class__._metadata
        return NodeMetadata(name=self.__class__.__name__)
    
    def validate_input(self, input_data: Dict[str, Any]) -> BaseModel:
        """验证输入数据"""
        model = self.input_model()
        if model:
            return model(**input_data)
        return NodeInput()
    
    def validate_output(self, output_data: Any) -> BaseModel:
        """验证输出数据"""
        model = self.output_model()
        if model and isinstance(output_data, dict):
            return model(**output_data)
        return output_data if isinstance(output_data, BaseModel) else NodeOutput()
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行节点
        包含验证、执行、错误处理的完整流程
        """
        try:
            # 验证输入
            validated_input = self.validate_input(input_data)
            
            # 执行节点逻辑
            result = self.run(validated_input)
            
            # 验证输出
            validated_output = self.validate_output(result)
            
            # 转换为字典
            if isinstance(validated_output, BaseModel):
                return validated_output.dict()
            return {"result": validated_output}
            
        except Exception as e:
            return {
                "error": str(e),
                "type": type(e).__name__,
                "success": False
            }
    
    def get_info(self) -> Dict[str, Any]:
        """获取节点信息"""
        return {
            "metadata": self.metadata.dict(),
            "input_schema": self._get_model_schema(self.input_model()),
            "output_schema": self._get_model_schema(self.output_model()),
            "docstring": inspect.getdoc(self.__class__) or ""
        }
    
    def _get_model_schema(self, model: Optional[Type[BaseModel]]) -> Dict:
        """获取模型的JSON Schema"""
        if model:
            return model.schema()
        return {}

# ==================== 装饰器 ====================

def work_node(name: str, group: str = "默认", **kwargs):
    """
    工作节点装饰器
    用于注册和配置工作流节点
    
    参数:
        name: 节点显示名称
        group: 节点分组
        **kwargs: 其他元数据参数
    
    示例:
        @work_node(name="数据加载", group="数据处理")
        class DataLoaderNode(BaseWorkNode):
            ...
    """
    def decorator(cls):
        # 检查是否继承自BaseWorkNode
        if not issubclass(cls, BaseWorkNode):
            raise TypeError(f"{cls.__name__} 必须继承自 BaseWorkNode")
        
        # 创建元数据
        metadata = NodeMetadata(
            name=name,
            group=group,
            description=kwargs.get("description", inspect.getdoc(cls) or ""),
            version=kwargs.get("version", "1.0.0"),
            author=kwargs.get("author", "PandaAI"),
            icon=kwargs.get("icon", "📦"),
            tags=kwargs.get("tags", [])
        )
        
        # 附加元数据到类
        cls._metadata = metadata
        
        # 注册到全局节点库
        register_node(cls, metadata)
        
        return cls
    
    return decorator

# ==================== 节点注册表 ====================

class NodeRegistry:
    """节点注册表"""
    
    def __init__(self):
        self._nodes = {}
        self._groups = {}
    
    def register(self, node_class: Type[BaseWorkNode], metadata: NodeMetadata):
        """注册节点"""
        node_id = f"{metadata.group}.{metadata.name}"
        self._nodes[node_id] = {
            "class": node_class,
            "metadata": metadata
        }
        
        # 按组分类
        if metadata.group not in self._groups:
            self._groups[metadata.group] = []
        self._groups[metadata.group].append(node_id)
    
    def get_node(self, node_id: str) -> Optional[Type[BaseWorkNode]]:
        """获取节点类"""
        if node_id in self._nodes:
            return self._nodes[node_id]["class"]
        return None
    
    def get_all_nodes(self) -> Dict[str, Any]:
        """获取所有节点"""
        return self._nodes.copy()
    
    def get_groups(self) -> Dict[str, List[str]]:
        """获取所有分组"""
        return self._groups.copy()
    
    def create_instance(self, node_id: str) -> Optional[BaseWorkNode]:
        """创建节点实例"""
        node_class = self.get_node(node_id)
        if node_class:
            return node_class()
        return None

# 全局注册表
_registry = NodeRegistry()

def register_node(node_class: Type[BaseWorkNode], metadata: NodeMetadata):
    """注册节点到全局注册表"""
    _registry.register(node_class, metadata)

def get_registry() -> NodeRegistry:
    """获取全局注册表"""
    return _registry

# ==================== 内置节点类型 ====================

@work_node(name="输入节点", group="基础", icon="📥")
class InputNode(BaseWorkNode):
    """工作流输入节点"""
    
    class Input(BaseModel):
        data: Any
    
    class Output(BaseModel):
        data: Any
    
    @classmethod
    def input_model(cls):
        return cls.Input
    
    @classmethod
    def output_model(cls):
        return cls.Output
    
    def run(self, input: Input) -> Output:
        return self.Output(data=input.data)

@work_node(name="输出节点", group="基础", icon="📤")
class OutputNode(BaseWorkNode):
    """工作流输出节点"""
    
    class Input(BaseModel):
        data: Any
    
    class Output(BaseModel):
        result: Any
        success: bool = True
    
    @classmethod
    def input_model(cls):
        return cls.Input
    
    @classmethod
    def output_model(cls):
        return cls.Output
    
    def run(self, input: Input) -> Output:
        return self.Output(result=input.data, success=True)

@work_node(name="条件分支", group="控制", icon="🔀")
class ConditionNode(BaseWorkNode):
    """条件分支节点"""
    
    class Input(BaseModel):
        value: Any
        condition: str
        threshold: Any = None
    
    class Output(BaseModel):
        result: bool
        branch: str  # "true" or "false"
    
    @classmethod
    def input_model(cls):
        return cls.Input
    
    @classmethod
    def output_model(cls):
        return cls.Output
    
    def run(self, input: Input) -> Output:
        result = False
        
        if input.condition == "equals":
            result = input.value == input.threshold
        elif input.condition == "greater":
            result = input.value > input.threshold
        elif input.condition == "less":
            result = input.value < input.threshold
        elif input.condition == "not_null":
            result = input.value is not None
        
        return self.Output(
            result=result,
            branch="true" if result else "false"
        )
