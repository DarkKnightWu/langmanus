from langgraph.graph import StateGraph, START

from .types import State
from .nodes import (
    supervisor_node,
    research_node,
    code_node,
    coordinator_node,
    browser_node,
    reporter_node,
    planner_node,
)


def build_graph():
    """
    构建并返回代理工作流图
    
    此函数创建了系统的核心工作流图，定义了各个代理节点及其连接关系：
    - coordinator: 协调者，负责任务分配和工作流程控制
    - planner: 规划者，负责制定任务执行计划
    - supervisor: 监督者，监控并评估任务执行质量
    - researcher: 研究员，负责信息收集和研究
    - coder: 编码者，负责代码实现
    - browser: 浏览器代理，处理网页交互
    - reporter: 报告者，汇总结果并生成报告
    
    Returns:
        编译后的可执行工作流图
    """
    # 创建基于State类型的状态图构建器
    builder = StateGraph(State)
    
    # 设置工作流起点为coordinator节点
    builder.add_edge(START, "coordinator")
    
    # 添加各个功能节点
    builder.add_node("coordinator", coordinator_node)  # 协调节点
    builder.add_node("planner", planner_node)          # 规划节点
    builder.add_node("supervisor", supervisor_node)    # 监督节点
    builder.add_node("researcher", research_node)      # 研究节点
    builder.add_node("coder", code_node)               # 代码节点
    builder.add_node("browser", browser_node)          # 浏览器节点
    builder.add_node("reporter", reporter_node)        # 报告节点
    
    # 编译并返回可执行图
    return builder.compile()
