"""
LLM模型管理模块

该模块提供了创建、管理和使用不同类型的大语言模型(LLM)的功能：
1. 创建OpenAI和DeepSeek模型实例
2. 按类型获取和缓存LLM实例
3. 提供通用接口访问不同的LLM提供商

模块支持三种主要的LLM类型：
- reasoning: 用于复杂推理任务的高能力模型
- basic: 用于基本任务的通用模型
- vision: 具有视觉能力的多模态模型
"""

from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from typing import Optional

from src.config import (
    REASONING_MODEL,
    REASONING_BASE_URL,
    REASONING_API_KEY,
    BASIC_MODEL,
    BASIC_BASE_URL,
    BASIC_API_KEY,
    VL_MODEL,
    VL_BASE_URL,
    VL_API_KEY,
)
from src.config.agents import LLMType


def create_openai_llm(
    model: str,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    temperature: float = 0.0,
    **kwargs,
) -> ChatOpenAI:
    """
    创建ChatOpenAI实例，配置特定参数
    
    该函数负责创建OpenAI模型实例，处理可选的基础URL和API密钥配置。
    适用于OpenAI兼容的API接口，包括官方API和兼容实现。
    
    Args:
        model: 模型名称，如"gpt-4o"、"gpt-3.5-turbo"等
        base_url: 可选的自定义API基础URL，用于自托管或兼容API
        api_key: 可选的API密钥
        temperature: 模型温度参数，控制输出随机性，默认为0.0（最确定性）
        **kwargs: 传递给ChatOpenAI构造函数的其他参数
        
    Returns:
        配置完成的ChatOpenAI实例
    """
    # 只有在base_url不为None或空字符串时才包含它
    llm_kwargs = {"model": model, "temperature": temperature, **kwargs}

    if base_url:  # 处理None或空字符串
        llm_kwargs["base_url"] = base_url

    if api_key:  # 处理None或空字符串
        llm_kwargs["api_key"] = api_key

    return ChatOpenAI(**llm_kwargs)


def create_deepseek_llm(
    model: str,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    temperature: float = 0.0,
    **kwargs,
) -> ChatDeepSeek:
    """
    创建ChatDeepSeek实例，配置特定参数
    
    该函数负责创建DeepSeek模型实例，处理可选的基础URL和API密钥配置。
    适用于DeepSeek API，提供另一种LLM选择。
    
    Args:
        model: 模型名称，如"o1-mini"等
        base_url: 可选的自定义API基础URL
        api_key: 可选的API密钥
        temperature: 模型温度参数，控制输出随机性，默认为0.0（最确定性）
        **kwargs: 传递给ChatDeepSeek构造函数的其他参数
        
    Returns:
        配置完成的ChatDeepSeek实例
    """
    # 只有在base_url不为None或空字符串时才包含它
    llm_kwargs = {"model": model, "temperature": temperature, **kwargs}

    if base_url:  # 处理None或空字符串
        llm_kwargs["api_base"] = base_url  # 注意DeepSeek使用api_base而非base_url

    if api_key:  # 处理None或空字符串
        llm_kwargs["api_key"] = api_key

    return ChatDeepSeek(**llm_kwargs)


# LLM实例缓存，避免重复创建相同类型的实例
_llm_cache: dict[LLMType, ChatOpenAI | ChatDeepSeek] = {}


def get_llm_by_type(llm_type: LLMType) -> ChatOpenAI | ChatDeepSeek:
    """
    根据类型获取LLM实例，如果可用则返回缓存的实例
    
    该函数是获取LLM实例的主要接口，它根据请求的类型返回适当的模型实例：
    - reasoning: 用于复杂推理任务的高能力模型（使用DeepSeek）
    - basic: 用于基本任务的通用模型（使用OpenAI）
    - vision: 具有视觉能力的多模态模型（使用OpenAI）
    
    Args:
        llm_type: LLM类型，定义于LLMType类型别名
        
    Returns:
        相应类型的LLM实例
        
    Raises:
        ValueError: 当请求的LLM类型未知时抛出
    """
    # 检查缓存中是否已有该类型的实例
    if llm_type in _llm_cache:
        return _llm_cache[llm_type]

    # 根据类型创建相应的LLM实例
    if llm_type == "reasoning":
        llm = create_deepseek_llm(
            model=REASONING_MODEL,
            base_url=REASONING_BASE_URL,
            api_key=REASONING_API_KEY,
        )
    elif llm_type == "basic":
        llm = create_openai_llm(
            model=BASIC_MODEL,
            base_url=BASIC_BASE_URL,
            api_key=BASIC_API_KEY,
        )
    elif llm_type == "vision":
        llm = create_openai_llm(
            model=VL_MODEL,
            base_url=VL_BASE_URL,
            api_key=VL_API_KEY,
        )
    else:
        raise ValueError(f"未知的LLM类型: {llm_type}")

    # 将创建的实例存入缓存
    _llm_cache[llm_type] = llm
    return llm


# 初始化不同用途的LLM - 现在这些实例将被缓存
reasoning_llm = get_llm_by_type("reasoning")  # 用于复杂推理
basic_llm = get_llm_by_type("basic")          # 用于基本任务
vl_llm = get_llm_by_type("vision")            # 用于视觉任务


if __name__ == "__main__":
    # 直接运行此模块时的测试代码
    stream = reasoning_llm.stream("what is mcp?")
    full_response = ""
    for chunk in stream:
        full_response += chunk.content
    print(full_response)

    basic_llm.invoke("Hello")
    vl_llm.invoke("Hello")
