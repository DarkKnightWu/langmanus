from readabilipy import simple_json_from_html_string

from .article import Article


class ReadabilityExtractor:
    """
    可读性提取器：使用readabilipy库从HTML内容中提取干净的文章内容
    """
    def extract_article(self, html: str) -> Article:
        """
        从HTML内容中提取文章
        
        参数:
            html: HTML字符串内容
            
        返回:
            Article: 提取的文章对象
        """
        article = simple_json_from_html_string(html, use_readability=True)
        return Article(
            title=article.get("title"),
            html_content=article.get("content"),
        )
