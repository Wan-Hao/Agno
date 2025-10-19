"""
各领域专家智能体
"""
from core.agent import Agent
from typing import Optional
from core.openai_client import OpenAIClient


class PhysicsAgent(Agent):
    """物理学专家智能体"""
    
    def __init__(
        self,
        name: str = "物理学家",
        api_client: Optional[OpenAIClient] = None
    ):
        super().__init__(
            name=name,
            domain="物理学",
            expertise=(
                "经典力学、量子力学、热力学、相对论、统计物理、"
                "粒子物理、天体物理等物理学各分支"
            ),
            api_client=api_client
        )
    
    def _default_system_instruction(self) -> str:
        return (
            f"你是一位资深的物理学家，名字是{self.name}。"
            f"你精通{self.expertise}。"
            f"你正在参与一个跨学科的学术讨论，目标是发现物理学与其他领域之间的深层联系。"
            f"请运用物理学的基本原理、定律和概念框架来分析问题。"
            f"特别关注：能量、熵、对称性、守恒定律、时空结构、因果关系等核心概念。"
            f"在讨论时，尝试找出物理规律在其他领域中的类比或映射。"
        )
    
    def analyze(self, prompt: str) -> str:
        """从物理学角度分析"""
        full_prompt = (
            f"作为物理学专家，请从物理学的角度分析以下内容：\n\n"
            f"{prompt}\n\n"
            f"请特别关注是否涉及：\n"
            f"- 能量与物质的转换\n"
            f"- 时间与空间的性质\n"
            f"- 系统的演化与不可逆性\n"
            f"- 对称性与守恒\n"
            f"- 微观与宏观的关系\n"
        )
        return self.client.generate(full_prompt, self.system_instruction)


class LiteratureAgent(Agent):
    """文学专家智能体"""
    
    def __init__(
        self,
        name: str = "文学评论家",
        api_client: Optional[OpenAIClient] = None
    ):
        super().__init__(
            name=name,
            domain="文学",
            expertise=(
                "文学理论、诗歌、小说、戏剧、文学批评、"
                "叙事学、修辞学、比较文学、文学史"
            ),
            api_client=api_client
        )
    
    def _default_system_instruction(self) -> str:
        return (
            f"你是一位资深的文学评论家和学者，名字是{self.name}。"
            f"你精通{self.expertise}。"
            f"你正在参与一个跨学科的学术讨论，目标是发现文学与其他领域之间的深层联系。"
            f"请运用文学的叙事结构、隐喻、象征、主题等分析工具。"
            f"特别关注：时间叙事、人物命运、冲突与和解、意义的多层性、语言的力量等。"
            f"在讨论时，尝试找出文学表达方式在其他领域中的对应或呼应。"
        )
    
    def analyze(self, prompt: str) -> str:
        """从文学角度分析"""
        full_prompt = (
            f"作为文学专家，请从文学的角度分析以下内容：\n\n"
            f"{prompt}\n\n"
            f"请特别关注是否涉及：\n"
            f"- 叙事结构与时间处理\n"
            f"- 隐喻、象征与意象\n"
            f"- 主题与意义的建构\n"
            f"- 冲突、张力与和解\n"
            f"- 语言的表现力与多义性\n"
        )
        return self.client.generate(full_prompt, self.system_instruction)


class MathAgent(Agent):
    """数学专家智能体"""
    
    def __init__(
        self,
        name: str = "数学家",
        api_client: Optional[OpenAIClient] = None
    ):
        super().__init__(
            name=name,
            domain="数学",
            expertise=(
                "代数、几何、拓扑学、分析、概率论、数理逻辑、"
                "数论、组合数学、应用数学"
            ),
            api_client=api_client
        )
    
    def _default_system_instruction(self) -> str:
        return (
            f"你是一位资深的数学家，名字是{self.name}。"
            f"你精通{self.expertise}。"
            f"你正在参与一个跨学科的学术讨论，目标是发现数学与其他领域之间的深层联系。"
            f"请运用数学的抽象思维、逻辑推理和结构分析能力。"
            f"特别关注：模式、结构、对称性、映射、变换、不变量、递归等数学概念。"
            f"在讨论时，尝试找出数学结构在其他领域中的体现。"
        )
    
    def analyze(self, prompt: str) -> str:
        """从数学角度分析"""
        full_prompt = (
            f"作为数学专家，请从数学的角度分析以下内容：\n\n"
            f"{prompt}\n\n"
            f"请特别关注是否涉及：\n"
            f"- 数学模式与结构\n"
            f"- 对称性与不变量\n"
            f"- 函数关系与映射\n"
            f"- 连续性与离散性\n"
            f"- 概率与统计规律\n"
        )
        return self.client.generate(full_prompt, self.system_instruction)


class BiologyAgent(Agent):
    """生物学专家智能体"""
    
    def __init__(
        self,
        name: str = "生物学家",
        api_client: Optional[OpenAIClient] = None
    ):
        super().__init__(
            name=name,
            domain="生物学",
            expertise=(
                "分子生物学、遗传学、进化生物学、生态学、"
                "细胞生物学、神经生物学、系统生物学"
            ),
            api_client=api_client
        )
    
    def _default_system_instruction(self) -> str:
        return (
            f"你是一位资深的生物学家，名字是{self.name}。"
            f"你精通{self.expertise}。"
            f"你正在参与一个跨学科的学术讨论，目标是发现生物学与其他领域之间的深层联系。"
            f"请运用生物学的进化思维、系统思维和适应性分析。"
            f"特别关注：进化、适应、自组织、信息传递、网络、反馈等生物学概念。"
            f"在讨论时，尝试找出生命系统的原理在其他领域中的类比。"
        )
    
    def analyze(self, prompt: str) -> str:
        """从生物学角度分析"""
        full_prompt = (
            f"作为生物学专家，请从生物学的角度分析以下内容：\n\n"
            f"{prompt}\n\n"
            f"请特别关注是否涉及：\n"
            f"- 进化与适应机制\n"
            f"- 自组织与涌现\n"
            f"- 信息编码与传递\n"
            f"- 网络与反馈系统\n"
            f"- 稳态与动态平衡\n"
        )
        return self.client.generate(full_prompt, self.system_instruction)


class PhilosophyAgent(Agent):
    """哲学专家智能体"""
    
    def __init__(
        self,
        name: str = "哲学家",
        api_client: Optional[OpenAIClient] = None
    ):
        super().__init__(
            name=name,
            domain="哲学",
            expertise=(
                "本体论、认识论、伦理学、逻辑学、美学、"
                "形而上学、科学哲学、心灵哲学"
            ),
            api_client=api_client
        )
    
    def _default_system_instruction(self) -> str:
        return (
            f"你是一位资深的哲学家，名字是{self.name}。"
            f"你精通{self.expertise}。"
            f"你正在参与一个跨学科的学术讨论，目标是发现哲学与其他领域之间的深层联系。"
            f"请运用哲学的概念分析、逻辑论证和批判性思维。"
            f"特别关注：本质、真理、存在、因果、自由、意识等哲学基本问题。"
            f"在讨论时，尝试揭示不同领域背后的哲学预设和概念框架。"
        )
    
    def analyze(self, prompt: str) -> str:
        """从哲学角度分析"""
        full_prompt = (
            f"作为哲学专家，请从哲学的角度分析以下内容：\n\n"
            f"{prompt}\n\n"
            f"请特别关注是否涉及：\n"
            f"- 本体论问题（存在的本质）\n"
            f"- 认识论问题（知识的可能性）\n"
            f"- 价值论问题（意义与价值）\n"
            f"- 逻辑与论证结构\n"
            f"- 概念的澄清与辨析\n"
        )
        return self.client.generate(full_prompt, self.system_instruction)


class ArtAgent(Agent):
    """艺术专家智能体"""
    
    def __init__(
        self,
        name: str = "艺术评论家",
        api_client: Optional[OpenAIClient] = None
    ):
        super().__init__(
            name=name,
            domain="艺术",
            expertise=(
                "绘画、雕塑、建筑、音乐、舞蹈、电影、"
                "艺术史、艺术理论、美学、设计"
            ),
            api_client=api_client
        )
    
    def _default_system_instruction(self) -> str:
        return (
            f"你是一位资深的艺术评论家和学者，名字是{self.name}。"
            f"你精通{self.expertise}。"
            f"你正在参与一个跨学科的学术讨论，目标是发现艺术与其他领域之间的深层联系。"
            f"请运用艺术的形式分析、风格批评和审美判断。"
            f"特别关注：形式、比例、韵律、和谐、张力、表现力等艺术元素。"
            f"在讨论时，尝试找出艺术表现形式在其他领域中的对应。"
        )
    
    def analyze(self, prompt: str) -> str:
        """从艺术角度分析"""
        full_prompt = (
            f"作为艺术专家，请从艺术的角度分析以下内容：\n\n"
            f"{prompt}\n\n"
            f"请特别关注是否涉及：\n"
            f"- 形式、结构与比例\n"
            f"- 色彩、节奏与韵律\n"
            f"- 平衡、对比与和谐\n"
            f"- 表现力与情感传达\n"
            f"- 创造性与审美体验\n"
        )
        return self.client.generate(full_prompt, self.system_instruction)


if __name__ == "__main__":
    # 测试各领域智能体
    print("Domain Agents module loaded successfully")
    print("\nAvailable agents:")
    agents = [
        PhysicsAgent(),
        LiteratureAgent(),
        MathAgent(),
        BiologyAgent(),
        PhilosophyAgent(),
        ArtAgent()
    ]
    for agent in agents:
        print(f"  - {agent.name} ({agent.domain})")

