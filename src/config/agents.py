"""
代理配置模块 - 定义代理类型和LLM映射关系

该模块主要负责：
1. 定义系统支持的LLM类型
2. 配置每个代理使用的LLM类型
3. 建立代理与LLM之间的映射关系

通过此配置，可以灵活调整不同代理使用的LLM类型，以优化性能和成本。
"""

from typing import Literal

# Define available LLM types
LLMType = Literal["basic", "reasoning", "vision"]

# Define agent-LLM mapping
AGENT_LLM_MAP: dict[str, LLMType] = {
    "coordinator": "basic",  # 协调默认使用basic llm
    "planner": "reasoning",  # 计划默认使用reasoning llm（复杂任务）
    "supervisor": "basic",  # 决策使用basic llm
    "researcher": "basic",  # 简单搜索任务使用basic llm
    "coder": "basic",  # 编程任务使用basic llm
    "browser": "vision",  # 浏览器操作使用vision llm（处理图像）
    "reporter": "basic",  # 编写报告使用basic llm
}
