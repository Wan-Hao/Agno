import json
from core.agent import Agent

class MinerAgent(Agent):
    """
    '矿工'Agent：负责从文本中挖掘所有可能的知识点
    """
    def __init__(self, model_name: str = "gemini-3-pro-preview"):
        super().__init__(
            name="Knowledge Miner",
            domain="Data Mining",
            expertise="Text extraction and concept mining"
        )
        # 覆盖默认的系统指令
        self.system_instruction = """
        你是一位不知疲倦的知识矿工，负责从原始文本中挖掘出所有可能的知识概念。
        你的任务是阅读给定的文本，结合提供的全局上下文记忆，尽可能全面地提取出其中包含的知识概念。
        
        提取标准（宁滥勿缺）：
        1. 核心概念（如：动能、重力势能）
        2. 定律与原理（如：机械能守恒定律）
        3. 重要公式（如：Ek = 1/2mv^2）
        4. 跨学科联系（如：动能与二次函数的关系）
        
        输出要求：
        必须且只能输出纯 JSON 格式，不要包含 Markdown 代码块标记（```json）。
        格式如下：
        [
            {
                "concept_name": "概念名称",
                "concept_type": "定义/定律/公式/现象",
                "raw_definition": "原文描述",
                "source_context": "上下文片段"
            },
            ...
        ]
        """

    def analyze(self, text: str, context_memory: str = "") -> str:
        """
        挖掘知识点，支持上下文记忆
        """
        prompt = f"""
        全局上下文记忆:
        {context_memory}
        
        ---
        请从以下文本中挖掘知识点，返回JSON列表：
        
        {text}
        """
        return self.client.generate(prompt=prompt, system_instruction=self.system_instruction)

def create_miner_agent() -> Agent:
    return MinerAgent()
