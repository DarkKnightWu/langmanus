from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import MessagesState

from src.config import TEAM_MEMBERS

# 定义路由选项
# 选项包括所有团队成员名称和一个FINISH标记，表示工作流结束
OPTIONS = TEAM_MEMBERS + ["FINISH"]


class Router(TypedDict):
    """
    路由器类型，用于确定下一个处理节点
    
    当工作流需要选择下一个执行的代理时，使用此类型指定目标
    如果不需要继续执行，可以路由到FINISH标记结束工作流
    """

    next: Literal[*OPTIONS]  # 下一个执行节点的名称，必须是OPTIONS中的一个值


class State(MessagesState):
    """
    代理系统的状态类型，继承自MessagesState并添加额外字段
    
    MessagesState基类提供了消息历史管理功能
    State类添加了系统运行所需的各种状态变量
    """

    # 常量配置
    TEAM_MEMBERS: list[str]  # 团队成员列表，从配置中获取

    # 运行时变量
    next: str                # 下一个执行节点的名称
    full_plan: str           # 完整执行计划
    deep_thinking_mode: bool # 是否启用深度思考模式
    search_before_planning: bool  # 是否在规划前进行搜索
