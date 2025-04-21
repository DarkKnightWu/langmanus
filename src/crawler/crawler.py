import sys

from .article import Article
from .jina_client import JinaClient
from .readability_extractor import ReadabilityExtractor


class Crawler:
    """
    爬虫类：用于从URL爬取网页内容并提取文章
    """
    def crawl(self, url: str) -> Article:
        """
        爬取指定URL的内容并提取为结构化文章
        
        参数:
            url: 要爬取的网页URL
            
        返回:
            Article: 提取的文章对象
        """
        # To help LLMs better understand content, we extract clean
        # articles from HTML, convert them to markdown, and split
        # them into text and image blocks for one single and unified
        # LLM message.
        #
        # Jina is not the best crawler on readability, however it's
        # much easier and free to use.
        #
        # Instead of using Jina's own markdown converter, we'll use
        # our own solution to get better readability results.
        
        # 为了帮助LLM更好地理解内容，我们从HTML中提取干净的
        # 文章，将其转换为markdown格式，并将其分割为文本和图片块，
        # 形成单一统一的LLM消息。
        #
        # Jina在可读性上不是最好的爬虫，但它更容易使用且免费。
        #
        # 我们不使用Jina自带的markdown转换器，而是使用
        # 自己的解决方案以获得更好的可读性结果。
        
        jina_client = JinaClient()
        html = jina_client.crawl(url, return_format="html")
        extractor = ReadabilityExtractor()
        article = extractor.extract_article(html)
        article.url = url
        return article


if __name__ == "__main__":
    """主函数：用于直接运行模块进行测试"""
    if len(sys.argv) == 2:
        url = sys.argv[1]
    else:
        url = "https://fintel.io/zh-hant/s/br/nvdc34"
    crawler = Crawler()
    article = crawler.crawl(url)
    print(article.to_markdown())
