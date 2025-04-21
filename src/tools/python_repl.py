"""
Python REPL工具模块 - 提供Python代码执行环境

该模块实现了Python代码执行工具，允许代理执行任意Python代码：
1. 创建安全的代码执行环境（REPL）
2. 执行代理提供的Python代码
3. 捕获和返回执行结果或错误信息

这个工具对于数据分析、算法实现、文件处理等任务非常重要，
为代理提供了通用的编程能力。
"""

import logging
from typing import Annotated
from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL
from .decorators import log_io

# 初始化Python REPL实例和日志记录器
repl = PythonREPL()  # 创建Python代码执行环境
logger = logging.getLogger(__name__)


@tool  # 将函数注册为LangChain工具
@log_io  # 记录输入和输出
def python_repl_tool(
    code: Annotated[
        str, "The python code to execute to do further analysis or calculation."
    ],
):
    """
    执行Python代码并返回结果
    
    该工具可用于执行Python代码进行数据分析或计算。
    如果需要查看变量的值，应使用`print(...)`函数将其打印出来。
    打印的内容会返回给用户，便于查看执行结果。
    
    Args:
        code: 要执行的Python代码字符串
        
    Returns:
        代码执行结果或错误信息
    """
    logger.info("Executing Python code")
    try:
        # 在REPL环境中执行代码
        result = repl.run(code)
        logger.info("Code execution successful")
    except BaseException as e:
        # 捕获所有可能的异常
        error_msg = f"Failed to execute. Error: {repr(e)}"
        logger.error(error_msg)
        return error_msg
    
    # 格式化执行结果，包含原始代码和输出
    result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
    return result_str
