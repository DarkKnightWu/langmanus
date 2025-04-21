"""
环境配置模块 - 管理系统环境变量和外部服务配置

该模块主要负责：
1. 加载.env文件中的环境变量
2. 为不同类型的LLM提供配置参数
3. 设置其他外部服务和工具的配置参数

通过环境变量管理配置，可以避免硬编码API密钥等敏感信息，
并支持不同部署环境（开发、测试、生产）使用不同配置。
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 推理型LLM配置（用于复杂推理任务）
REASONING_MODEL = os.getenv("REASONING_MODEL", "o1-mini")  # 默认使用DeepSeek的o1-mini模型
REASONING_BASE_URL = os.getenv("REASONING_BASE_URL")  # DeepSeek API的基础URL
REASONING_API_KEY = os.getenv("REASONING_API_KEY")  # DeepSeek API密钥

# 基础LLM配置（用于简单直接的任务）
BASIC_MODEL = os.getenv("BASIC_MODEL", "gpt-4o")  # 默认使用OpenAI的gpt-4o模型
BASIC_BASE_URL = os.getenv("BASIC_BASE_URL")  # OpenAI API的基础URL（可用于兼容API）
BASIC_API_KEY = os.getenv("BASIC_API_KEY")  # OpenAI API密钥

# 视觉-语言LLM配置（用于需要视觉理解的任务）
VL_MODEL = os.getenv("VL_MODEL", "gpt-4o")  # 默认使用OpenAI的gpt-4o模型（支持视觉）
VL_BASE_URL = os.getenv("VL_BASE_URL")  # 视觉模型API的基础URL
VL_API_KEY = os.getenv("VL_API_KEY")  # 视觉模型API密钥

# Chrome浏览器实例配置
CHROME_INSTANCE_PATH = os.getenv("CHROME_INSTANCE_PATH")  # Chrome可执行文件的路径
