"""
PDF 数据处理器
"""
from pathlib import Path
from typing import Dict, Any, List
import pypdf


class PDFProcessor:
    """PDF 数据处理器"""
    
    @staticmethod
    def process(file_path: Path) -> Dict[str, Any]:
        """
        处理 PDF 文件
        
        Args:
            file_path: PDF 文件路径
            
        Returns:
            处理后的数据字典
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        # 读取 PDF
        reader = pypdf.PdfReader(str(file_path))
        
        # 提取所有页面的文本
        pages_text = []
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            pages_text.append({
                "page_number": page_num + 1,
                "text": text
            })
        
        # 合并所有文本
        full_text = "\n\n".join([page["text"] for page in pages_text])
        
        return {
            "type": "pdf",
            "source": str(file_path),
            "content": full_text,
            "pages": pages_text,
            "metadata": {
                "num_pages": len(reader.pages),
                "file_size": file_path.stat().st_size,
                "file_name": file_path.name
            }
        }
    
    @staticmethod
    def extract_page(file_path: Path, page_number: int) -> str:
        """
        提取指定页面的文本
        
        Args:
            file_path: PDF 文件路径
            page_number: 页码（从1开始）
            
        Returns:
            页面文本
        """
        reader = pypdf.PdfReader(str(file_path))
        
        if page_number < 1 or page_number > len(reader.pages):
            raise ValueError(f"Invalid page number: {page_number}")
        
        page = reader.pages[page_number - 1]
        return page.extract_text()
    
    @staticmethod
    def get_metadata(file_path: Path) -> Dict[str, Any]:
        """
        获取 PDF 元数据
        
        Args:
            file_path: PDF 文件路径
            
        Returns:
            元数据字典
        """
        reader = pypdf.PdfReader(str(file_path))
        metadata = reader.metadata
        
        return {
            "title": metadata.get("/Title", ""),
            "author": metadata.get("/Author", ""),
            "subject": metadata.get("/Subject", ""),
            "creator": metadata.get("/Creator", ""),
            "producer": metadata.get("/Producer", ""),
            "num_pages": len(reader.pages)
        }


if __name__ == "__main__":
    # 测试 PDF 处理器
    print("PDF Processor module loaded successfully")
    # 实际测试需要提供 PDF 文件路径

