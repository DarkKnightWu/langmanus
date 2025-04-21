import logging
from src.config import TEAM_MEMBERS
from src.graph import build_graph

# 配置日志系统
# 设置基本日志格式和默认日志级别为INFO
logging.basicConfig(
    level=logging.INFO,  # 默认日志级别为INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def enable_debug_logging():
    """
    启用调试级别日志，提供更详细的执行信息
    此函数将src包的日志级别设置为DEBUG
    """
    logging.getLogger("src").setLevel(logging.DEBUG)


# 获取当前模块的日志记录器
logger = logging.getLogger(__name__)

# 创建工作流图实例
# 通过build_graph函数构建整个系统的工作流图
graph = build_graph()


def run_agent_workflow(user_input: str, debug: bool = False):
    """
    运行代理工作流，处理用户输入并返回结果
    
    工作流程:
    1. 验证用户输入
    2. 根据需要启用调试日志
    3. 调用图执行器处理用户请求
    4. 返回最终结果状态
    
    Args:
        user_input: 用户的查询或请求文本
        debug: 如果为True，启用调试级别的日志记录
        
    Returns:
        工作流完成后的最终状态
        
    Raises:
        ValueError: 当用户输入为空时抛出
    """
    if not user_input:
        raise ValueError("Input could not be empty")

    if debug:
        enable_debug_logging()

    logger.info(f"Starting workflow with user input: {user_input}")
    result = graph.invoke(
        {
            # 常量
            "TEAM_MEMBERS": TEAM_MEMBERS,  # 团队成员配置
            # 运行时变量
            "messages": [{"role": "user", "content": user_input}],  # 用户消息
            "deep_thinking_mode": True,  # 启用深度思考模式
            "search_before_planning": True,  # 在规划前进行搜索
        }
    )
    logger.debug(f"Final workflow state: {result}")
    logger.info("Workflow completed successfully")
    return result


if __name__ == "__main__":
    # 以Mermaid图表格式打印工作流图结构
    print(graph.get_graph().draw_mermaid())
