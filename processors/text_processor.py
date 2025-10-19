"""
文本数据处理器
"""
from pathlib import Path
from typing import Union, Dict, Any


class TextProcessor:
    """文本数据处理器"""
    
    @staticmethod
    def process(source: Union[str, Path]) -> Dict[str, Any]:
        """
        处理文本数据
        
        Args:
            source: 文本内容或文件路径
            
        Returns:
            处理后的数据字典
        """
        if isinstance(source, Path) or (isinstance(source, str) and Path(source).exists()):
            # 从文件读取
            file_path = Path(source)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "type": "text",
                "source": str(file_path),
                "content": content,
                "metadata": {
                    "file_size": file_path.stat().st_size,
                    "encoding": "utf-8"
                }
            }
        else:
            # 直接处理文本内容
            return {
                "type": "text",
                "source": "direct_input",
                "content": str(source),
                "metadata": {
                    "length": len(str(source))
                }
            }
    
    @staticmethod
    def extract_summary(text: str, max_length: int = 500) -> str:
        """
        提取文本摘要
        
        Args:
            text: 文本内容
            max_length: 最大长度
            
        Returns:
            文本摘要
        """
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> list:
        """
        将文本分块
        
        Args:
            text: 文本内容
            chunk_size: 块大小
            overlap: 重叠大小
            
        Returns:
            文本块列表
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap
        
        return chunks


if __name__ == "__main__":
    # 测试文本处理器
    processor = TextProcessor()
    
    # 测试直接文本
    result = processor.process("这是一段测试文本。")
    print("Direct text processing:")
    print(result)
    
    # 测试文本分块
    long_text = "这是一段很长的文本。" * 100
    chunks = processor.chunk_text(long_text, chunk_size=100, overlap=20)
    print(f"\nText chunking: {len(chunks)} chunks created")

