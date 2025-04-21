"""
代理实现模块 - 定义系统中的各类专业代理

该模块创建并配置系统中的各种专用代理，每个代理负责特定类型的任务：
1. 研究代理：负责信息收集和分析
2. 编码代理：负责代码编写和执行
3. 浏览器代理：负责网页浏览和交互

每个代理都配备了：
- 特定的大语言模型，根据任务复杂度选择
- 专用工具集，提供执行任务所需的功能
- 定制提示模板，引导代理行为方式
"""

from langgraph.prebuilt import create_react_agent

from src.prompts import apply_prompt_template
from src.tools import (
    bash_tool,
    browser_tool,
    crawl_tool,
    python_repl_tool,
    tavily_tool,
)

from .llm import get_llm_by_type
from src.config.agents import AGENT_LLM_MAP

# 创建各种专用代理，每种代理使用不同的LLM配置和工具集

# 研究代理
# 职责：负责收集和分析信息，执行网络搜索和网站爬取任务
research_agent = create_react_agent(
    get_llm_by_type(AGENT_LLM_MAP["researcher"]),  # 根据配置获取研究员代理对应的LLM模型
    tools=[tavily_tool, crawl_tool],               # 提供搜索和网页爬取工具
    prompt=lambda state: apply_prompt_template("researcher", state),  # 应用研究员专用提示模板
)

# 编码代理
# 职责：负责代码实现，执行代码编写、测试和调试任务
coder_agent = create_react_agent(
    get_llm_by_type(AGENT_LLM_MAP["coder"]),       # 根据配置获取编码代理对应的LLM模型
    tools=[python_repl_tool, bash_tool],           # 提供Python解释器和Bash命令行工具
    prompt=lambda state: apply_prompt_template("coder", state),  # 应用编码专用提示模板
)

# 浏览器代理
# 职责：负责浏览网页，模拟用户浏览行为，处理网页交互
browser_agent = create_react_agent(
    get_llm_by_type(AGENT_LLM_MAP["browser"]),     # 根据配置获取浏览器代理对应的LLM模型
    tools=[browser_tool],                           # 提供浏览器模拟工具
    prompt=lambda state: apply_prompt_template("browser", state),  # 应用浏览器专用提示模板
)
