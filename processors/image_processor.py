"""
图片数据处理器
"""
from pathlib import Path
from typing import Dict, Any
from PIL import Image
import io


class ImageProcessor:
    """图片数据处理器"""
    
    @staticmethod
    def process(file_path: Path) -> Dict[str, Any]:
        """
        处理图片文件
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            处理后的数据字典
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Image file not found: {file_path}")
        
        # 打开图片
        img = Image.open(file_path)
        
        return {
            "type": "image",
            "source": str(file_path),
            "file_path": str(file_path),  # 保留文件路径供 Gemini 使用
            "metadata": {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,  # (width, height)
                "width": img.width,
                "height": img.height,
                "file_size": file_path.stat().st_size,
                "file_name": file_path.name
            }
        }
    
    @staticmethod
    def resize_image(file_path: Path, max_size: tuple = (1024, 1024)) -> Path:
        """
        调整图片大小
        
        Args:
            file_path: 图片文件路径
            max_size: 最大尺寸 (width, height)
            
        Returns:
            调整后的图片路径
        """
        img = Image.open(file_path)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # 保存到临时文件
        output_path = file_path.parent / f"{file_path.stem}_resized{file_path.suffix}"
        img.save(output_path)
        
        return output_path
    
    @staticmethod
    def get_image_description_prompt() -> str:
        """
        获取图片描述提示词
        
        Returns:
            提示词
        """
        return (
            "请详细描述这张图片的内容。包括：\n"
            "1. 主要元素和对象\n"
            "2. 颜色和构图\n"
            "3. 可能的含义或主题\n"
            "4. 与你的专业领域相关的见解\n"
        )


if __name__ == "__main__":
    # 测试图片处理器
    print("Image Processor module loaded successfully")
    # 实际测试需要提供图片文件路径

