"""
配置模块 - 管理系统的全局配置和常量

该模块负责：
1. 汇总和导出环境配置变量
2. 定义团队成员和代理结构
3. 设置工具参数和限制

主要分为以下几类配置：
- LLM配置：不同类型语言模型的参数
- 团队配置：定义系统中的代理成员
- 工具配置：各工具的参数设置
- 其他系统配置：浏览器路径等
"""

from .env import (
    # 推理型LLM配置
    REASONING_MODEL,
    REASONING_BASE_URL,
    REASONING_API_KEY,
    # 基础LLM配置
    BASIC_MODEL,
    BASIC_BASE_URL,
    BASIC_API_KEY,
    # 视觉-语言LLM配置
    VL_MODEL,
    VL_BASE_URL,
    VL_API_KEY,
    # 其他配置
    CHROME_INSTANCE_PATH,
)
from .tools import TAVILY_MAX_RESULTS

# 团队成员配置 - 定义系统中的代理角色
TEAM_MEMBERS = ["researcher", "coder", "browser", "reporter"]

__all__ = [
    # 推理型LLM配置
    "REASONING_MODEL",
    "REASONING_BASE_URL",
    "REASONING_API_KEY",
    # 基础LLM配置
    "BASIC_MODEL",
    "BASIC_BASE_URL",
    "BASIC_API_KEY",
    # 视觉-语言LLM配置
    "VL_MODEL",
    "VL_BASE_URL",
    "VL_API_KEY",
    # 其他配置
    "TEAM_MEMBERS",
    "TAVILY_MAX_RESULTS",
    "CHROME_INSTANCE_PATH",
]
