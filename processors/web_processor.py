"""
网页数据处理器
"""
from typing import Dict, Any
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class WebProcessor:
    """网页数据处理器"""
    
    @staticmethod
    def process(url: str) -> Dict[str, Any]:
        """
        处理网页 URL
        
        Args:
            url: 网页 URL
            
        Returns:
            处理后的数据字典
        """
        try:
            # 发送请求
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # 解析 HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取标题
            title = soup.title.string if soup.title else ""
            
            # 提取主要文本内容
            # 移除 script 和 style 标签
            for script in soup(["script", "style"]):
                script.decompose()
            
            # 获取文本
            text = soup.get_text()
            
            # 清理文本
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # 提取元数据
            meta_description = ""
            meta_tag = soup.find("meta", attrs={"name": "description"})
            if meta_tag and meta_tag.get("content"):
                meta_description = meta_tag["content"]
            
            # 提取链接
            links = []
            for link in soup.find_all('a', href=True):
                links.append({
                    "text": link.get_text().strip(),
                    "href": link['href']
                })
            
            return {
                "type": "web",
                "source": url,
                "content": text,
                "metadata": {
                    "url": url,
                    "title": title,
                    "description": meta_description,
                    "domain": urlparse(url).netloc,
                    "status_code": response.status_code,
                    "content_length": len(text),
                    "num_links": len(links)
                },
                "links": links[:50]  # 限制链接数量
            }
        
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch URL {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to process URL {url}: {str(e)}")
    
    @staticmethod
    def extract_summary(web_data: Dict[str, Any], max_length: int = 1000) -> str:
        """
        提取网页内容摘要
        
        Args:
            web_data: 网页数据字典
            max_length: 最大长度
            
        Returns:
            摘要文本
        """
        content = web_data.get("content", "")
        if len(content) <= max_length:
            return content
        return content[:max_length] + "..."
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        检查 URL 是否有效
        
        Args:
            url: URL 字符串
            
        Returns:
            是否有效
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False


if __name__ == "__main__":
    # 测试网页处理器
    processor = WebProcessor()
    
    # 测试 URL 验证
    test_url = "https://www.example.com"
    print(f"Is valid URL: {processor.is_valid_url(test_url)}")
    
    # 实际处理需要真实的 URL
    print("Web Processor module loaded successfully")

