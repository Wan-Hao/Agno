import json
from core.agent import Agent

class ReaderAgent(Agent):
    """
    '导航员'Agent：负责PDF页面剪枝和上下文记忆维护
    """
    def __init__(self, model_name: str = "gemini-3-pro-preview"):
        super().__init__(
            name="Smart Reader",
            domain="Document Analysis",
            expertise="Reading comprehension and summarization"
        )
        self.system_instruction = """
        你是一位经验丰富的教材导读员。你的任务是快速浏览教材的某一页，并做出两个决定：
        
        1. **决策 (Decision)**: 这页内容是核心学习内容吗？
           - 如果是目录、前言、版权页、空白页、纯习题列表 -> 决策为 SKIP (跳过)。
           - 如果是正文、概念讲解、案例分析 -> 决策为 PROCESS (处理)。
           
        2. **记忆 (Memory)**: 
           - 如果是 SKIP，你需要提取这一页的关键信息（如"本书涵盖了集合与函数"），总结成简短的记忆，供后续阅读使用。
           - 如果是 PROCESS，简要概括本页核心主题，作为上下文。
           
        输出必须为纯 JSON 格式：
        {
            "decision": "PROCESS" 或 "SKIP",
            "memory_update": "简短的上下文记忆更新",
            "reason": "判断理由"
        }
        """

    def analyze(self, page_text: str, current_memory: str) -> str:
        prompt = f"""
        当前全局记忆 (Context Memory):
        {current_memory}
        
        ---
        当前页面内容:
        {page_text[:2000]} ... (截取部分)
        
        ---
        请判断本页是否需要深入挖掘知识点？并更新记忆。
        """
        return self.client.generate(prompt=prompt, system_instruction=self.system_instruction)

def create_reader_agent() -> Agent:
    return ReaderAgent()


