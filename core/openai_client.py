"""
OpenAI 兼容 API 客户端封装
用于支持自定义 API 端点
"""
from openai import OpenAI
from typing import Optional, Dict, Any, List
from pathlib import Path
from config import Config


class OpenAIClient:
    """OpenAI 兼容 API 客户端"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ):
        """
        初始化 OpenAI 客户端
        
        Args:
            api_key: API 密钥（默认从配置读取）
            base_url: API 基础 URL（默认从配置读取）
            model_name: 模型名称（默认从配置读取）
            temperature: 温度参数（默认从配置读取）
            max_tokens: 最大 token 数（默认从配置读取）
        """
        self.api_key = api_key or Config.GEMINI_API_KEY
        self.base_url = base_url or Config.API_BASE_URL
        self.model_name = model_name or Config.GEMINI_MODEL
        self.temperature = temperature or Config.TEMPERATURE
        self.max_tokens = max_tokens or Config.MAX_TOKENS
        
        # 初始化 OpenAI 客户端
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url if self.base_url else None
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
            messages = []
            
            # 添加系统消息
            if system_instruction:
                messages.append({
                    "role": "system",
                    "content": system_instruction
                })
            
            # 添加用户消息
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # 调用 API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=kwargs.get("temperature", self.temperature),
                max_tokens=kwargs.get("max_tokens", self.max_tokens)
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
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
            import base64
            
            # 读取图片并编码为 base64
            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            messages = []
            
            # 添加系统消息
            if system_instruction:
                messages.append({
                    "role": "system",
                    "content": system_instruction
                })
            
            # 添加用户消息（包含图片）
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            })
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error with image: {str(e)}")
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        system_instruction: Optional[str] = None
    ) -> str:
        """
        对话模式
        
        Args:
            messages: 消息历史列表
            system_instruction: 系统指令
            
        Returns:
            生成的回复
        """
        try:
            chat_messages = []
            
            # 添加系统消息
            if system_instruction:
                chat_messages.append({
                    "role": "system",
                    "content": system_instruction
                })
            
            # 添加历史消息
            chat_messages.extend(messages)
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=chat_messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI chat error: {str(e)}")


if __name__ == "__main__":
    # 测试 OpenAI 客户端
    try:
        client = OpenAIClient()
        response = client.generate("Hello, how are you?")
        print(f"✓ OpenAI client test successful")
        print(f"  Response: {response[:100]}...")
    except Exception as e:
        print(f"✗ OpenAI client test failed: {e}")

