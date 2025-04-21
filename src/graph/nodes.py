import logging
import json
from copy import deepcopy
from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.graph import END

from src.agents import research_agent, coder_agent, browser_agent
from src.agents.llm import get_llm_by_type
from src.config import TEAM_MEMBERS
from src.config.agents import AGENT_LLM_MAP
from src.prompts.template import apply_prompt_template
from src.tools.search import tavily_tool
from .types import State, Router

# 初始化日志记录器
logger = logging.getLogger(__name__)

# 定义代理响应的格式模板
# 包含代理名称和响应内容，并添加执行下一步的提示
RESPONSE_FORMAT = "Response from {}:\n\n<response>\n{}\n</response>\n\n*Please execute the next step.*"


def research_node(state: State) -> Command[Literal["supervisor"]]:
    """
    研究节点 - 负责执行信息收集和研究任务
    
    该节点调用research_agent执行搜索和爬取操作，收集任务所需的信息。
    完成后，将结果添加到消息历史中，并将控制权交回给supervisor节点。
    
    Args:
        state: 当前工作流状态
        
    Returns:
        包含状态更新和下一节点信息的Command对象
    """
    logger.info("Research agent starting task")
    # 调用研究代理处理当前状态
    result = research_agent.invoke(state)
    logger.info("Research agent completed task")
    logger.debug(f"Research agent response: {result['messages'][-1].content}")
    # 将研究代理的响应添加到消息历史，并转到supervisor节点
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=RESPONSE_FORMAT.format(
                        "researcher", result["messages"][-1].content
                    ),
                    name="researcher",
                )
            ]
        },
        goto="supervisor",  # 返回supervisor进行下一步决策
    )


def code_node(state: State) -> Command[Literal["supervisor"]]:
    """
    代码节点 - 负责执行代码实现和测试任务
    
    该节点调用coder_agent执行Python代码和系统命令，实现和测试功能。
    完成后，将结果添加到消息历史中，并将控制权交回给supervisor节点。
    
    Args:
        state: 当前工作流状态
        
    Returns:
        包含状态更新和下一节点信息的Command对象
    """
    logger.info("Code agent starting task")
    # 调用代码代理处理当前状态
    result = coder_agent.invoke(state)
    logger.info("Code agent completed task")
    logger.debug(f"Code agent response: {result['messages'][-1].content}")
    # 将代码代理的响应添加到消息历史，并转到supervisor节点
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=RESPONSE_FORMAT.format(
                        "coder", result["messages"][-1].content
                    ),
                    name="coder",
                )
            ]
        },
        goto="supervisor",  # 返回supervisor进行下一步决策
    )


def browser_node(state: State) -> Command[Literal["supervisor"]]:
    """
    浏览器节点 - 负责执行网页浏览和交互任务
    
    该节点调用browser_agent模拟浏览器行为，访问网站和提取信息。
    完成后，将结果添加到消息历史中，并将控制权交回给supervisor节点。
    
    Args:
        state: 当前工作流状态
        
    Returns:
        包含状态更新和下一节点信息的Command对象
    """
    logger.info("Browser agent starting task")
    # 调用浏览器代理处理当前状态
    result = browser_agent.invoke(state)
    logger.info("Browser agent completed task")
    logger.debug(f"Browser agent response: {result['messages'][-1].content}")
    # 将浏览器代理的响应添加到消息历史，并转到supervisor节点
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=RESPONSE_FORMAT.format(
                        "browser", result["messages"][-1].content
                    ),
                    name="browser",
                )
            ]
        },
        goto="supervisor",  # 返回supervisor进行下一步决策
    )


def supervisor_node(state: State) -> Command[Literal[*TEAM_MEMBERS, "__end__"]]:
    """
    监督节点 - 决定下一步执行哪个代理
    
    该节点是工作流的核心决策点，负责评估当前状态，并决定：
    1. 将任务委派给特定的团队成员
    2. 结束工作流
    
    使用Router类型格式化输出，确保决策有效。
    
    Args:
        state: 当前工作流状态
        
    Returns:
        包含下一节点信息的Command对象
    """
    logger.info("Supervisor evaluating next action")
    # 应用supervisor提示模板
    messages = apply_prompt_template("supervisor", state)
    # 使用LLM进行结构化输出，决定下一步
    response = (
        get_llm_by_type(AGENT_LLM_MAP["supervisor"])
        .with_structured_output(Router)
        .invoke(messages)
    )
    goto = response["next"]
    logger.debug(f"Current state messages: {state['messages']}")
    logger.debug(f"Supervisor response: {response}")

    # 处理完成情况或继续委派任务
    if goto == "FINISH":
        goto = "__end__"  # 结束工作流
        logger.info("Workflow completed")
    else:
        logger.info(f"Supervisor delegating to: {goto}")

    # 返回下一步信息并更新状态
    return Command(goto=goto, update={"next": goto})


def planner_node(state: State) -> Command[Literal["supervisor", "__end__"]]:
    """
    规划节点 - 生成完整的执行计划
    
    该节点负责分析任务并生成详细的执行计划，包括：
    1. 根据深度思考模式决定使用哪种LLM
    2. 可选地在规划前进行相关搜索
    3. 生成结构化的计划（JSON格式）
    
    Args:
        state: 当前工作流状态
        
    Returns:
        包含计划和下一节点信息的Command对象
    """
    logger.info("Planner generating full plan")
    # 应用planner提示模板
    messages = apply_prompt_template("planner", state)
    
    # 根据深度思考模式选择LLM类型
    llm = get_llm_by_type("basic")
    if state.get("deep_thinking_mode"):
        llm = get_llm_by_type("reasoning")
        
    # 如果启用了规划前搜索，执行相关搜索并将结果添加到消息中
    if state.get("search_before_planning"):
        searched_content = tavily_tool.invoke({"query": state["messages"][-1].content})
        messages = deepcopy(messages)
        # 确保searched_content是列表格式
        if isinstance(searched_content, str):
            searched_content = [{"title": "搜索结果", "content": searched_content}]
        elif not isinstance(searched_content, list):
            searched_content = [{"title": "搜索结果", "content": str(searched_content)}]
            
        messages[-1].content += f"\n\n# Relative Search Results\n\n{json.dumps([{'title': elem.get('title', '无标题'), 'content': elem.get('content', '无内容')} for elem in searched_content], ensure_ascii=False)}"
    
    # 流式处理LLM响应
    stream = llm.stream(messages)
    full_response = ""
    for chunk in stream:
        full_response += chunk.content
    logger.debug(f"Current state messages: {state['messages']}")
    logger.debug(f"Planner response: {full_response}")

    # 清理响应中的Markdown代码块标记
    if full_response.startswith("```json"):
        full_response = full_response.removeprefix("```json")

    if full_response.endswith("```"):
        full_response = full_response.removesuffix("```")

    # 设置默认下一步为supervisor
    goto = "supervisor"
    # 验证响应是否为有效的JSON
    try:
        json.loads(full_response)
    except json.JSONDecodeError:
        logger.warning("Planner response is not a valid JSON")
        goto = "__end__"  # 如果计划无效则结束工作流

    # 更新消息历史和完整计划
    return Command(
        update={
            "messages": [HumanMessage(content=full_response, name="planner")],
            "full_plan": full_response,
        },
        goto=goto,
    )


def coordinator_node(state: State) -> Command[Literal["planner", "__end__"]]:
    """
    协调节点 - 与用户沟通并决定是否启动规划
    
    该节点是工作流的入口点，负责：
    1. 与用户进行初步交流
    2. 确定是否需要进一步规划
    3. 决定是将控制权交给planner还是结束工作流
    
    Args:
        state: 当前工作流状态
        
    Returns:
        包含下一节点信息的Command对象
    """
    logger.info("Coordinator talking.")
    # 应用coordinator提示模板
    messages = apply_prompt_template("coordinator", state)
    # 获取LLM响应
    response = get_llm_by_type(AGENT_LLM_MAP["coordinator"]).invoke(messages)
    logger.debug(f"Current state messages: {state['messages']}")
    logger.debug(f"coordinator response: {response}")

    # 默认结束工作流
    goto = "__end__"
    # 如果响应中包含特定标记，则转到planner节点
    if "handoff_to_planner" in response.content:
        goto = "planner"

    # 返回下一步信息
    return Command(
        goto=goto,
    )


def reporter_node(state: State) -> Command[Literal["supervisor"]]:
    """
    报告节点 - 生成最终的任务报告
    
    该节点负责汇总工作流的执行结果，生成结构化的报告。
    完成后，将结果添加到消息历史中，并将控制权交回给supervisor节点。
    
    Args:
        state: 当前工作流状态
        
    Returns:
        包含状态更新和下一节点信息的Command对象
    """
    logger.info("Reporter write final report")
    # 应用reporter提示模板
    messages = apply_prompt_template("reporter", state)
    # 获取LLM响应
    response = get_llm_by_type(AGENT_LLM_MAP["reporter"]).invoke(messages)
    logger.debug(f"Current state messages: {state['messages']}")
    logger.debug(f"reporter response: {response}")

    # 将报告者的响应添加到消息历史，并转到supervisor节点
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=RESPONSE_FORMAT.format("reporter", response.content),
                    name="reporter",
                )
            ]
        },
        goto="supervisor",  # 返回supervisor进行下一步决策
    )
