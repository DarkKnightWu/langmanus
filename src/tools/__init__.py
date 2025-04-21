"""
工具模块 - 为代理系统提供各种功能工具

该模块集成了多种工具，使代理能够执行各种操作：
- 执行Bash命令
- 进行网页爬取
- 执行网络搜索
- 运行Python代码
- 文件操作
- 浏览器模拟

每个工具都设计为可被代理调用的函数，并通过langchain_core.tools装饰器暴露给LLM。
"""

# 导入各种工具
from .crawl import crawl_tool  # 网页爬取工具
from .file_management import write_file_tool  # 文件写入工具
from .python_repl import python_repl_tool  # Python代码执行工具
from .search import tavily_tool  # Tavily搜索工具
from .bash_tool import bash_tool  # Bash命令执行工具
from .browser import browser_tool  # 浏览器模拟工具

# 定义公开的工具列表
__all__ = [
    "bash_tool",  # 执行系统命令
    "crawl_tool",  # 爬取网页内容
    "tavily_tool",  # 进行互联网搜索
    "python_repl_tool",  # 执行Python代码
    "write_file_tool",  # 写入文件内容
    "browser_tool",  # 模拟浏览器操作
]
