"""
文件管理工具模块 - 提供文件操作功能

该模块实现了文件管理相关工具，使代理能够操作文件系统：
1. 提供写入文件的功能
2. 为文件操作添加日志记录
3. 处理文件系统交互

文件管理工具使代理能够持久化存储数据、生成报告文件等。
"""

import logging
from langchain_community.tools.file_management import WriteFileTool
from .decorators import create_logged_tool

# 初始化日志记录器
logger = logging.getLogger(__name__)

# 初始化带日志记录的文件写入工具
# 使用装饰器包装原始的WriteFileTool，添加日志功能
LoggedWriteFile = create_logged_tool(WriteFileTool)

# 创建文件写入工具实例
# 此工具允许代理创建和写入文件，语法为：
# write_file_tool.invoke({"file_path": "path/to/file.txt", "text": "内容"})
write_file_tool = LoggedWriteFile()
