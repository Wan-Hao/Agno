"""
配置管理模块
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    """系统配置类"""
    
    # API 配置
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    API_BASE_URL = os.getenv("API_BASE_URL", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "8192"))
    
    # 系统配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./output"))
    
    # 确保输出目录存在
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    
    # 对话配置
    MAX_DISCUSSION_ROUNDS = 10
    MIN_AGENTS = 2
    MAX_AGENTS = 10
    
    # 评估配置
    SEMANTIC_SIMILARITY_THRESHOLD = 0.6
    NOVELTY_THRESHOLD = 0.5
    CONFIDENCE_THRESHOLD = 0.7
    
    @classmethod
    def validate(cls):
        """验证配置是否完整"""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found. "
                "Please set it in .env file or environment variables."
            )
        return True


if __name__ == "__main__":
    # 测试配置
    try:
        Config.validate()
        print("✓ Configuration validated successfully")
        print(f"  Model: {Config.GEMINI_MODEL}")
        print(f"  Output directory: {Config.OUTPUT_DIR}")
    except Exception as e:
        print(f"✗ Configuration error: {e}")

