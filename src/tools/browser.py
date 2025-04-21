"""
浏览器工具模块 - 提供网页浏览和交互功能

该模块实现了浏览器操作工具，允许代理模拟用户浏览网页：
1. 创建和管理浏览器实例
2. 执行导航、点击、搜索等操作
3. 支持同步和异步操作模式
4. 处理浏览器交互可能的错误

浏览器工具极大扩展了代理与网络内容交互的能力，使其能够执行复杂的网页任务。
"""

import asyncio

from pydantic import BaseModel, Field
from typing import Optional, ClassVar, Type
from langchain.tools import BaseTool
from browser_use import AgentHistoryList, Browser, BrowserConfig
from browser_use import Agent as BrowserAgent
from src.agents.llm import vl_llm
from src.tools.decorators import create_logged_tool
from src.config import CHROME_INSTANCE_PATH

# 全局浏览器实例
expected_browser = None

# 如果配置了Chrome实例路径，则创建浏览器实例
if CHROME_INSTANCE_PATH:
    expected_browser = Browser(
        config=BrowserConfig(chrome_instance_path=CHROME_INSTANCE_PATH)
    )


class BrowserUseInput(BaseModel):
    """浏览器工具的输入模型"""

    instruction: str = Field(..., description="The instruction to use browser")


class BrowserTool(BaseTool):
    """
    浏览器工具类，用于执行网页浏览和交互任务
    
    该工具创建一个浏览器代理，能够理解自然语言指令并执行相应的
    浏览器操作，如导航到网站、搜索内容、点击元素等。
    """
    
    name: ClassVar[str] = "browser"  # 工具名称
    args_schema: Type[BaseModel] = BrowserUseInput  # 输入模式
    description: ClassVar[str] = (
        "Use this tool to interact with web browsers. Input should be a natural language description of what you want to do with the browser, such as 'Go to google.com and search for browser-use', or 'Navigate to Reddit and find the top post about AI'."
    )

    _agent: Optional[BrowserAgent] = None  # 浏览器代理实例

    def _run(self, instruction: str) -> str:
        """
        同步执行浏览器任务
        
        创建一个浏览器代理，并在同步上下文中运行异步操作，
        处理可能的异常并返回执行结果。
        
        Args:
            instruction: 用自然语言描述的浏览器操作指令
            
        Returns:
            浏览器操作的结果或错误信息
        """
        # 创建浏览器代理实例
        self._agent = BrowserAgent(
            task=instruction,  # 设置任务指令
            llm=vl_llm,  # 使用视觉语言模型
            browser=expected_browser,  # 使用预先配置的浏览器
        )
        try:
            # 创建新的事件循环来运行异步代码
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                # 执行浏览器操作
                result = loop.run_until_complete(self._agent.run())
                # 处理结果格式
                return (
                    str(result)
                    if not isinstance(result, AgentHistoryList)
                    else result.final_result
                )
            finally:
                # 确保事件循环关闭
                loop.close()
        except Exception as e:
            # 捕获并返回任何异常
            return f"Error executing browser task: {str(e)}"

    async def _arun(self, instruction: str) -> str:
        """
        异步执行浏览器任务
        
        创建一个浏览器代理并异步运行，便于在异步环境中使用。
        
        Args:
            instruction: 用自然语言描述的浏览器操作指令
            
        Returns:
            浏览器操作的结果或错误信息
        """
        # 创建浏览器代理实例
        self._agent = BrowserAgent(
            task=instruction, 
            llm=vl_llm,  # 使用视觉语言模型
            browser=expected_browser,  # 使用预先配置的浏览器
        )
        try:
            # 异步执行浏览器操作
            result = await self._agent.run()
            # 处理结果格式
            return (
                str(result)
                if not isinstance(result, AgentHistoryList)
                else result.final_result
            )
        except Exception as e:
            # 捕获并返回任何异常
            return f"Error executing browser task: {str(e)}"


# 创建带日志功能的浏览器工具
BrowserTool = create_logged_tool(BrowserTool)
# 实例化浏览器工具
browser_tool = BrowserTool()
