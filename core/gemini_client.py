"""
Gemini API 客户端封装
"""
import google.generativeai as genai
from typing import Optional, Dict, Any, List
from pathlib import Path
import base64
from config import Config


class GeminiClient:
    """Gemini API 客户端"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ):
        """
        初始化 Gemini 客户端
        
        Args:
            api_key: API 密钥（默认从配置读取）
            model_name: 模型名称（默认从配置读取）
            temperature: 温度参数（默认从配置读取）
            max_tokens: 最大 token 数（默认从配置读取）
        """
        self.api_key = api_key or Config.GEMINI_API_KEY
        self.model_name = model_name or Config.GEMINI_MODEL
        self.temperature = temperature or Config.TEMPERATURE
        self.max_tokens = max_tokens or Config.MAX_TOKENS
        
        # 配置 API
        genai.configure(api_key=self.api_key)
        
        # 初始化模型
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "temperature": self.temperature,
                "max_output_tokens": self.max_tokens,
            }
        )
    
    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        生成文本响应
        
        Args:
            prompt: 提示词
            system_instruction: 系统指令
            **kwargs: 其他生成参数
            
        Returns:
            生成的文本
        """
        try:
            if system_instruction:
                # 创建带系统指令的模型
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    generation_config={
                        "temperature": kwargs.get("temperature", self.temperature),
                        "max_output_tokens": kwargs.get("max_tokens", self.max_tokens),
                    },
                    system_instruction=system_instruction
                )
                response = model.generate_content(prompt)
            else:
                response = self.model.generate_content(prompt)
            
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def generate_with_image(
        self,
        prompt: str,
        image_path: Path,
        system_instruction: Optional[str] = None
    ) -> str:
        """
        使用图片生成响应（多模态）
        
        Args:
            prompt: 提示词
            image_path: 图片路径
            system_instruction: 系统指令
            
        Returns:
            生成的文本
        """
        try:
            # 读取图片
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            # 上传图片
            image_part = {
                "mime_type": self._get_mime_type(image_path),
                "data": image_data
            }
            
            if system_instruction:
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=system_instruction
                )
                response = model.generate_content([prompt, image_part])
            else:
                response = self.model.generate_content([prompt, image_part])
            
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error with image: {str(e)}")
    
    def generate_with_files(
        self,
        prompt: str,
        file_paths: List[Path],
        system_instruction: Optional[str] = None
    ) -> str:
        """
        使用多个文件生成响应（多模态）
        
        Args:
            prompt: 提示词
            file_paths: 文件路径列表
            system_instruction: 系统指令
            
        Returns:
            生成的文本
        """
        try:
            # 准备内容列表
            content_parts = [prompt]
            
            for file_path in file_paths:
                # 上传文件到 Gemini
                uploaded_file = genai.upload_file(str(file_path))
                content_parts.append(uploaded_file)
            
            if system_instruction:
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=system_instruction
                )
                response = model.generate_content(content_parts)
            else:
                response = self.model.generate_content(content_parts)
            
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error with files: {str(e)}")
    
    def _get_mime_type(self, file_path: Path) -> str:
        """获取文件的 MIME 类型"""
        suffix = file_path.suffix.lower()
        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp",
            ".mp4": "video/mp4",
            ".avi": "video/avi",
            ".mov": "video/quicktime",
            ".mp3": "audio/mpeg",
            ".wav": "audio/wav",
            ".pdf": "application/pdf",
        }
        return mime_types.get(suffix, "application/octet-stream")
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        system_instruction: Optional[str] = None
    ) -> str:
        """
        对话模式
        
        Args:
            messages: 消息历史列表，格式为 [{"role": "user", "content": "..."}, ...]
            system_instruction: 系统指令
            
        Returns:
            生成的回复
        """
        try:
            if system_instruction:
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=system_instruction
                )
            else:
                model = self.model
            
            # 创建聊天会话
            chat = model.start_chat(history=[])
            
            # 发送消息
            for msg in messages[:-1]:  # 除了最后一条
                if msg["role"] == "user":
                    chat.send_message(msg["content"])
            
            # 发送最后一条并获取响应
            response = chat.send_message(messages[-1]["content"])
            return response.text
        except Exception as e:
            raise Exception(f"Gemini chat error: {str(e)}")


if __name__ == "__main__":
    # 测试 Gemini 客户端
    try:
        client = GeminiClient()
        response = client.generate("Hello, how are you?")
        print(f"✓ Gemini client test successful")
        print(f"  Response: {response[:100]}...")
    except Exception as e:
        print(f"✗ Gemini client test failed: {e}")

