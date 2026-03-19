import json
from core.agent import Agent

class CriticAgent(Agent):
    """
    '质检'Agent：负责审核候选概念，并进行标准化和布鲁姆层级填充
    """
    def __init__(self, model_name: str = "gemini-3-pro-preview"):
        super().__init__(
            name="Knowledge Critic",
            domain="Quality Assurance",
            expertise="Knowledge graph validation and educational taxonomy"
        )
        self.system_instruction = """
        你是一位严谨的百科全书编辑和教育专家，负责审核'矿工'提交的候选词条。
        你的任务是审核'知识矿工'提取的候选概念列表。你需要剔除低质量内容，并完善高质量内容。
        
        审核与优化步骤：
        1. **筛选 (Filter)**: 剔除琐碎、重复的概念。
        2. **标准化 (Standardize)**: 生成规范的 ID (snake_case) 和 Label。
        3. **布鲁姆深度填充 (Bloom Enrichment)**: 必须填充 'bloom_levels' 属性：
           - memory: 定义是什么？
           - understanding: 意义是什么？
           - application: 怎么用？
           
        输出要求：
        必须且只能输出纯 JSON 格式，不要包含 Markdown 代码块标记。
        格式如下：
        [
            {
                "id": "kinetic_energy",
                "label": "动能",
                "properties": {
                    "description": "...",
                    "category": "力学",
                    "theme": "机械能",
                    "bloom_levels": {
                        "remember": "...",
                        "understand": "...",
                        "apply": "..."
                    }
                },
                "status": "approved",
                "critique_comment": "通过"
            },
            ...
        ]
        """

    def analyze(self, candidates_json: str) -> str:
        """
        审核知识点
        """
        prompt = f"请审核以下候选知识点，并进行标准化和布鲁姆层级填充，返回JSON列表：\n\n{candidates_json}"
        return self.client.generate(prompt=prompt, system_instruction=self.system_instruction)

def create_critic_agent() -> Agent:
    return CriticAgent()
