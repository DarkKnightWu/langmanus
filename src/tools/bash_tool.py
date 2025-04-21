import logging
import subprocess
from typing import Annotated
from langchain_core.tools import tool
from .decorators import log_io

# 初始化日志记录器
logger = logging.getLogger(__name__)


@tool  # 使用langchain_core的工具装饰器，将函数转换为可被代理调用的工具
@log_io  # 自定义装饰器，用于记录工具的输入和输出
def bash_tool(
    cmd: Annotated[str, "The bash command to be executed."],  # 使用Annotated提供参数说明
):
    """
    执行Bash命令并返回结果
    
    此工具允许代理执行系统命令，进行文件操作、安装软件、运行脚本等操作。
    工具会捕获命令的标准输出和错误输出，并返回给调用者。
    
    Args:
        cmd: 要执行的Bash命令
        
    Returns:
        命令执行的输出结果或错误信息
    """
    logger.info(f"Executing Bash Command: {cmd}")
    try:
        # 执行命令并捕获输出
        result = subprocess.run(
            cmd, shell=True, check=True, text=True, capture_output=True
        )
        # 返回标准输出作为结果
        return result.stdout
    except subprocess.CalledProcessError as e:
        # 如果命令执行失败，返回错误信息
        error_message = f"Command failed with exit code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}"
        logger.error(error_message)
        return error_message
    except Exception as e:
        # 捕获其他异常
        error_message = f"Error executing command: {str(e)}"
        logger.error(error_message)
        return error_message


if __name__ == "__main__":
    # 当脚本直接运行时的测试代码
    print(bash_tool.invoke("ls -all"))
