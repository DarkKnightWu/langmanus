"""
代理模块 - 管理系统中的各种智能代理

该模块导出系统使用的主要代理：
- research_agent: 研究代理，负责搜索和信息收集
- coder_agent: 编码代理，负责代码生成和执行
- browser_agent: 浏览器代理，负责网页浏览和交互
"""

from .agents import research_agent, coder_agent, browser_agent

__all__ = ["research_agent", "coder_agent", "browser_agent"]
