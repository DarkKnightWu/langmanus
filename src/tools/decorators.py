"""
工具装饰器模块 - 提供日志记录和工具增强功能

该模块实现了用于增强工具功能的装饰器和混入类：
1. 提供函数级装饰器，记录工具输入和输出
2. 提供类级混入，增强工具类的日志能力
3. 提供工具类转换工厂，创建带日志的工具类

这些装饰器使代理工具的使用更加透明，便于调试和监控。
"""

import logging
import functools
from typing import Any, Callable, Type, TypeVar

# 初始化日志记录器
logger = logging.getLogger(__name__)

# 定义泛型类型变量，用于类型提示
T = TypeVar("T")


def log_io(func: Callable) -> Callable:
    """
    记录工具函数输入参数和输出结果的装饰器
    
    此装饰器包装工具函数，在函数执行前记录输入参数，
    执行后记录返回结果，便于跟踪工具的使用情况。
    
    Args:
        func: 要装饰的工具函数
        
    Returns:
        带有日志功能的包装函数
    """

    @functools.wraps(func)  # 保留原函数的元数据（名称、文档等）
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # 记录输入参数
        func_name = func.__name__
        params = ", ".join(
            [*(str(arg) for arg in args), *(f"{k}={v}" for k, v in kwargs.items())]
        )
        logger.debug(f"Tool {func_name} called with parameters: {params}")

        # 执行原函数
        result = func(*args, **kwargs)

        # 记录输出结果
        logger.debug(f"Tool {func_name} returned: {result}")

        return result

    return wrapper


class LoggedToolMixin:
    """
    为工具类添加日志功能的混入类
    
    此混入类可以与任何工具类组合，为其添加自动日志记录功能。
    它重写了工具类的_run方法，在执行前后添加日志记录。
    """

    def _log_operation(self, method_name: str, *args: Any, **kwargs: Any) -> None:
        """
        记录工具操作的辅助方法
        
        Args:
            method_name: 被调用的方法名
            *args, **kwargs: 方法的参数
        """
        tool_name = self.__class__.__name__.replace("Logged", "")
        params = ", ".join(
            [*(str(arg) for arg in args), *(f"{k}={v}" for k, v in kwargs.items())]
        )
        logger.debug(f"Tool {tool_name}.{method_name} called with parameters: {params}")

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """
        重写_run方法，添加日志记录
        
        In the execution of the original _run method before and after adding logging.
        
        Returns:
            工具执行结果
        """
        self._log_operation("_run", *args, **kwargs)
        result = super()._run(*args, **kwargs)
        logger.debug(
            f"Tool {self.__class__.__name__.replace('Logged', '')} returned: {result}"
        )
        return result


def create_logged_tool(base_tool_class: Type[T]) -> Type[T]:
    """
    创建带日志功能的工具类的工厂函数
    
    此函数接收一个基础工具类，返回一个新类，该新类同时继承
    LoggedToolMixin和基础工具类，从而具备日志功能。
    
    Args:
        base_tool_class: 原始工具类
        
    Returns:
        带有日志功能的新工具类
    """

    class LoggedTool(LoggedToolMixin, base_tool_class):
        """带有日志功能的工具类"""
        pass

    # 设置更具描述性的类名
    LoggedTool.__name__ = f"Logged{base_tool_class.__name__}"
    return LoggedTool
