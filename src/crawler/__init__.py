"""
爬虫模块 - 提供网页内容爬取和处理功能

该模块实现了网页爬取和内容提取功能，包含以下组件：
1. Article类：表示爬取的文章，支持HTML到Markdown的转换
2. Crawler类：爬取网页并提取有意义的内容
3. 各种内容提取器：支持从HTML中提取结构化内容

爬虫模块为代理提供了获取和处理网页信息的能力，
使其能够分析和引用网络上的各种资源。
"""

from .article import Article
from .crawler import Crawler

__all__ = [
    "Article",
    "Crawler",
]
