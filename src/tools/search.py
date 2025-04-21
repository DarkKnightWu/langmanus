"""
搜索工具模块 - 提供网络搜索功能

该模块集成了Tavily搜索API，为代理提供互联网搜索能力：
1. 使用Tavily搜索引擎进行网络搜索
2. 限制返回结果数量，提高效率
3. 集成日志记录功能，便于调试和监控

搜索工具是代理获取最新信息和外部知识的重要手段。
"""

import logging
from langchain_community.tools.tavily_search import TavilySearchResults
from src.config import TAVILY_MAX_RESULTS
from .decorators import create_logged_tool

# 初始化日志记录器
logger = logging.getLogger(__name__)

# 初始化带日志记录的Tavily搜索工具
# 使用装饰器为搜索工具添加日志功能
LoggedTavilySearch = create_logged_tool(TavilySearchResults)

# 创建搜索工具实例，设置最大结果数量
# 该工具将在使用时自动从环境变量获取TAVILY_API_KEY
tavily_tool = LoggedTavilySearch(name="tavily_search", max_results=TAVILY_MAX_RESULTS)
