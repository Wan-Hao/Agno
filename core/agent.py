"""
智能体基类
"""
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
from pathlib import Path
from core.openai_client import OpenAIClient
from core.edge import KnowledgeEdge


class Agent(ABC):
    """
    智能体基类
    
    所有智能体都应继承此类并实现相应方法
    """
    
    def __init__(
        self,
        name: str,
        domain: str,
        expertise: str,
        system_instruction: Optional[str] = None,
        api_client: Optional[OpenAIClient] = None
    ):
        """
        初始化智能体
        
        Args:
            name: 智能体名称
            domain: 所属领域
            expertise: 专业描述
            system_instruction: 系统指令（可选）
            api_client: API 客户端（可选，默认创建新实例）
        """
        self.name = name
        self.domain = domain
        self.expertise = expertise
        self.system_instruction = system_instruction or self._default_system_instruction()
        self.client = api_client or OpenAIClient()
        
        # 知识库：存储该智能体处理的数据和知识
        self.knowledge_base: List[Dict[str, Any]] = []
        
        # 对话历史
        self.conversation_history: List[Dict[str, str]] = []
    
    def _default_system_instruction(self) -> str:
        """默认系统指令"""
        return (
            f"你是一位{self.domain}领域的专家，名字是{self.name}。"
            f"你的专长是：{self.expertise}。"
            f"你正在参与一个跨学科的学术讨论，目标是发现不同领域之间的潜在联系。"
            f"请基于你的专业知识，与其他领域的专家进行深入对话，"
            f"寻找可能的跨领域关联、类比、隐喻或因果关系。"
        )
    
    def load_knowledge(self, data: Any, data_type: str, source: str):
        """
        加载知识到智能体的知识库
        
        Args:
            data: 数据内容
            data_type: 数据类型（text, image, pdf, audio, video, web）
            source: 数据来源
        """
        self.knowledge_base.append({
            "data": data,
            "type": data_type,
            "source": source,
            "domain": self.domain
        })
    
    def get_knowledge_summary(self) -> str:
        """获取知识库摘要"""
        if not self.knowledge_base:
            return f"{self.name} 的知识库为空。"
        
        summary = f"{self.name} 的知识库包含 {len(self.knowledge_base)} 条知识：\n"
        for i, kb in enumerate(self.knowledge_base, 1):
            summary += f"{i}. 类型: {kb['type']}, 来源: {kb['source']}\n"
        return summary
    
    @abstractmethod
    def analyze(self, prompt: str) -> str:
        """
        分析给定的提示并生成响应
        
        Args:
            prompt: 分析提示
            
        Returns:
            分析结果
        """
        pass
    
    def discuss(self, topic: str, context: Optional[str] = None) -> str:
        """
        针对特定主题进行讨论
        
        Args:
            topic: 讨论主题
            context: 上下文信息（如其他智能体的发言）
            
        Returns:
            讨论内容
        """
        prompt = f"讨论主题：{topic}\n\n"
        
        if context:
            prompt += f"当前讨论上下文：\n{context}\n\n"
        
        prompt += (
            f"请从{self.domain}的角度，结合你的知识库内容，"
            f"对这个主题进行深入分析。特别注意：\n"
            f"1. 寻找与其他领域可能的联系点\n"
            f"2. 提出具有启发性的观点\n"
            f"3. 使用具体的概念和例子\n"
        )
        
        response = self.client.generate(
            prompt=prompt,
            system_instruction=self.system_instruction
        )
        
        # 记录对话历史
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
    def propose_edge(
        self,
        target_agent: "Agent",
        topic: str,
        discussion_context: str
    ) -> Optional[KnowledgeEdge]:
        """
        提议一个知识边
        
        Args:
            target_agent: 目标智能体
            topic: 讨论主题
            discussion_context: 讨论上下文
            
        Returns:
            提议的知识边，如果没有发现关联则返回 None
        """
        prompt = (
            f"基于以下讨论内容，尝试在{self.domain}和{target_agent.domain}之间"
            f"发现潜在的知识关联。\n\n"
            f"讨论主题：{topic}\n\n"
            f"讨论内容：\n{discussion_context}\n\n"
            f"请分析是否存在跨领域的关联，如果存在，请描述：\n"
            f"1. 源概念（来自{self.domain}）\n"
            f"2. 目标概念（来自{target_agent.domain}）\n"
            f"3. 关系类型（如：类比、因果、隐喻、结构相似等）\n"
            f"4. 关系描述\n"
            f"5. 推理过程\n"
            f"6. 置信度（0-1之间的数值）\n\n"
            f"如果不存在明确的关联，请回复'无关联'。\n"
            f"如果存在关联，请以JSON格式回复。"
        )
        
        response = self.client.generate(
            prompt=prompt,
            system_instruction=self.system_instruction
        )
        
        # 解析响应（简化版本，实际应用中需要更复杂的解析）
        if "无关联" in response or "无明确关联" in response:
            return None
        
        # 这里应该解析 JSON，为了简化，我们先返回 None
        # 在实际应用中，需要使用 JSON 解析或结构化输出
        return None
    
    def reflect(self) -> str:
        """
        对自己的讨论进行反思
        
        Returns:
            反思内容
        """
        if not self.conversation_history:
            return "暂无讨论历史。"
        
        prompt = (
            f"请回顾你在讨论中的发言，进行反思：\n"
            f"1. 你提出了哪些关键观点？\n"
            f"2. 发现了哪些潜在的跨领域联系？\n"
            f"3. 还有哪些角度可以进一步探讨？\n"
        )
        
        return self.client.generate(
            prompt=prompt,
            system_instruction=self.system_instruction
        )
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"Agent({self.name}, domain={self.domain})"
    
    def __repr__(self) -> str:
        """详细表示"""
        return (
            f"Agent(name='{self.name}', domain='{self.domain}', "
            f"knowledge_items={len(self.knowledge_base)}, "
            f"conversations={len(self.conversation_history)})"
        )


class BasicAgent(Agent):
    """
    基础智能体实现
    
    可以直接使用的简单智能体
    """
    
    def analyze(self, prompt: str) -> str:
        """分析给定的提示"""
        full_prompt = (
            f"作为{self.domain}领域的专家，请分析以下内容：\n\n"
            f"{prompt}\n\n"
            f"请提供专业的见解和分析。"
        )
        
        return self.client.generate(
            prompt=full_prompt,
            system_instruction=self.system_instruction
        )


if __name__ == "__main__":
    # 测试基础智能体
    agent = BasicAgent(
        name="测试专家",
        domain="测试领域",
        expertise="测试相关的专业知识"
    )
    
    print(agent)
    print(f"\n系统指令：\n{agent.system_instruction[:200]}...")
    
    # 加载一些知识
    agent.load_knowledge("测试数据", "text", "test.txt")
    print(f"\n{agent.get_knowledge_summary()}")

