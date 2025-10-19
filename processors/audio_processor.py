"""
音频数据处理器
"""
from pathlib import Path
from typing import Dict, Any


class AudioProcessor:
    """音频数据处理器"""
    
    @staticmethod
    def process(file_path: Path) -> Dict[str, Any]:
        """
        处理音频文件
        
        Args:
            file_path: 音频文件路径
            
        Returns:
            处理后的数据字典
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        # 获取基本信息
        file_size = file_path.stat().st_size
        
        # 尝试获取音频元数据（需要额外的库如 mutagen）
        # 这里先返回基本信息
        return {
            "type": "audio",
            "source": str(file_path),
            "file_path": str(file_path),  # 保留文件路径供 Gemini 使用
            "metadata": {
                "file_size": file_size,
                "file_name": file_path.name,
                "format": file_path.suffix.lstrip('.'),
            }
        }
    
    @staticmethod
    def get_audio_analysis_prompt() -> str:
        """
        获取音频分析提示词
        
        Returns:
            提示词
        """
        return (
            "请分析这段音频的内容。包括：\n"
            "1. 音频的主要内容（如果是语音，请转录）\n"
            "2. 音频的特征（音调、节奏、情绪等）\n"
            "3. 可能的含义或主题\n"
            "4. 与你的专业领域相关的见解\n"
        )
    
    @staticmethod
    def supported_formats() -> list:
        """
        支持的音频格式
        
        Returns:
            格式列表
        """
        return ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a']


if __name__ == "__main__":
    # 测试音频处理器
    print("Audio Processor module loaded successfully")
    print(f"Supported formats: {AudioProcessor.supported_formats()}")

