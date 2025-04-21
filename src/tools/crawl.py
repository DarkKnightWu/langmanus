"""
网页爬取工具模块 - 提供网页内容爬取功能

该模块实现了网页爬取工具，允许代理获取和处理网页内容：
1. 支持从给定URL爬取网页
2. 清理和格式化网页内容为可读的Markdown格式
3. 处理潜在的错误并提供有用的错误信息

该工具对于搜集网页信息、分析在线内容非常有用。
"""

import logging
from typing import Annotated

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from .decorators import log_io

from src.crawler import Crawler

# 初始化日志记录器
logger = logging.getLogger(__name__)


@tool  # 将函数注册为LangChain工具
@log_io  # 记录输入和输出
def crawl_tool(
    url: Annotated[str, "The url to crawl."],  # 要爬取的URL
) -> HumanMessage:
    """
    爬取指定URL并获取可读的Markdown格式内容
    
    该工具使用Crawler类爬取指定网页，提取主要内容，
    并将其转换为结构化的Markdown格式，便于LLM理解和处理。
    
    Args:
        url: 要爬取的网页URL
        
    Returns:
        包含格式化内容的HumanMessage对象，或错误信息字符串
    """
    try:
        # 创建爬虫实例
        crawler = Crawler()
        # 爬取指定URL
        article = crawler.crawl(url)
        # 返回格式化的消息
        return {"role": "user", "content": article.to_message()}
    except BaseException as e:
        # 捕获并记录所有异常
        error_msg = f"Failed to crawl. Error: {repr(e)}"
        logger.error(error_msg)
        return error_msg
