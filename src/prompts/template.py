import os
import re
from datetime import datetime

from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt.chat_agent_executor import AgentState


def get_prompt_template(prompt_name: str) -> str:
    """
    获取指定名称的提示模板内容
    
    该函数从prompts目录下读取对应名称的Markdown文件，并进行模板格式处理：
    1. 将普通花括号转义，以避免与模板变量冲突
    2. 将特殊标记 <<VAR>> 转换为模板变量格式 {VAR}
    
    Args:
        prompt_name: 提示模板名称（不包含.md后缀）
        
    Returns:
        处理后的模板字符串
    """
    # 读取模板文件
    template = open(os.path.join(os.path.dirname(__file__), f"{prompt_name}.md")).read()
    # 转义花括号，避免与模板变量冲突
    template = template.replace("{", "{{").replace("}", "}}")
    # 将 <<VAR>> 格式替换为模板变量格式 {VAR}
    template = re.sub(r"<<([^>>]+)>>", r"{\1}", template)
    return template


def apply_prompt_template(prompt_name: str, state: AgentState) -> list:
    """
    应用提示模板，将当前状态填充到模板中并构建完整的消息列表
    
    该函数执行以下步骤：
    1. 获取模板内容
    2. 将当前时间和状态变量填充到模板中
    3. 创建系统提示消息
    4. 将系统提示与历史消息合并
    
    Args:
        prompt_name: 提示模板名称
        state: 代理的当前状态，包含消息历史和其他状态变量
        
    Returns:
        完整的消息列表，包含系统提示和历史消息
    """
    # 使用PromptTemplate进行变量替换
    system_prompt = PromptTemplate(
        input_variables=["CURRENT_TIME"],  # 定义模板中的变量
        template=get_prompt_template(prompt_name),  # 获取模板内容
    ).format(
        CURRENT_TIME=datetime.now().strftime("%a %b %d %Y %H:%M:%S %z"),  # 当前时间格式化
        **state  # 展开状态中的所有变量
    )
    # 返回系统提示消息和历史消息的组合
    return [{"role": "system", "content": system_prompt}] + state["messages"]
