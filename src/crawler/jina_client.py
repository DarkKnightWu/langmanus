import logging
import os

import requests

logger = logging.getLogger(__name__)


class JinaClient:
    """
    Jina API客户端：用于通过Jina AI的服务抓取网页内容
    """
    def crawl(self, url: str, return_format: str = "html") -> str:
        """
        抓取指定URL的网页内容
        
        参数:
            url: 要抓取的网页URL
            return_format: 返回格式，默认为"html"
            
        返回:
            str: 网页内容，格式由return_format参数指定
        """
        headers = {
            "Content-Type": "application/json",
            "X-Return-Format": return_format,
        }
        if os.getenv("JINA_API_KEY"):
            headers["Authorization"] = f"Bearer {os.getenv('JINA_API_KEY')}"
        else:
            logger.warning(
                "Jina API key is not set. Provide your own key to access a higher rate limit. See https://jina.ai/reader for more information."
                # Jina API密钥未设置。提供自己的密钥可以获得更高的请求限制。更多信息请访问https://jina.ai/reader
            )
        data = {"url": url}
        response = requests.post("https://r.jina.ai/", headers=headers, json=data)
        return response.text
