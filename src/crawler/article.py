"""
文章模型模块 - 处理爬取的网页内容

该模块定义了Article类，用于表示从网页爬取的文章内容：
1. 存储文章标题和HTML内容
2. 提供HTML到Markdown的转换功能
3. 支持将内容转换为适合LLM处理的消息格式（包括文本和图像）

Article类是爬虫系统的核心数据结构，负责内容的表示和格式转换。
"""

import re
from urllib.parse import urljoin

from markdownify import markdownify as md


class Article:
    """
    文章类，表示从网页爬取的文章
    
    存储文章的标题、内容，并提供格式转换功能，
    使爬取的内容能够方便地被LLM理解和处理。
    """
    
    url: str  # 文章源URL

    def __init__(self, title: str, html_content: str):
        """
        初始化文章对象
        
        Args:
            title: 文章标题
            html_content: 文章HTML内容
        """
        self.title = title
        self.html_content = html_content

    def to_markdown(self, including_title: bool = True) -> str:
        """
        将文章内容转换为Markdown格式
        
        使用markdownify库将HTML内容转换为Markdown格式，
        可选择是否包含标题。
        
        Args:
            including_title: 是否在转换结果中包含标题
            
        Returns:
            转换后的Markdown格式文本
        """
        markdown = ""
        if including_title:
            markdown += f"# {self.title}\n\n"
        markdown += md(self.html_content)
        return markdown

    def to_message(self) -> list[dict]:
        """
        将文章内容转换为适合LLM处理的消息格式
        
        将Markdown内容转换为消息对象列表，其中：
        - 文本内容被转换为text类型消息
        - 图片被转换为image_url类型消息
        
        这种格式特别适合多模态LLM处理，可以同时理解文本和图像。
        
        Returns:
            消息对象列表，每个对象包含type和对应的内容
        """
        # 匹配Markdown格式的图片链接
        image_pattern = r"!\[.*?\]\((.*?)\)"

        content: list[dict[str, str]] = []
        # 按图片链接分割文本
        parts = re.split(image_pattern, self.to_markdown())

        for i, part in enumerate(parts):
            if i % 2 == 1:
                # 处理图片部分：将相对链接转为绝对链接
                image_url = urljoin(self.url, part.strip())
                content.append({"type": "image_url", "image_url": {"url": image_url}})
            else:
                # 处理文本部分
                content.append({"type": "text", "text": part.strip()})

        return content
