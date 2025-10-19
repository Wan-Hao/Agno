"""
元协调智能体
"""
from typing import List, Dict, Any, Optional
from core.agent import Agent
from core.openai_client import OpenAIClient
from core.edge import KnowledgeEdge
import json
import re


class MetaAgent(Agent):
    """
    元协调智能体
    
    负责：
    1. 监控和引导讨论方向
    2. 识别潜在的跨领域关联
    3. 提取和生成知识边
    4. 协调各领域智能体的互动
    """
    
    def __init__(
        self,
        name: str = "元协调者",
        api_client: Optional[OpenAIClient] = None
    ):
        super().__init__(
            name=name,
            domain="跨学科协调",
            expertise=(
                "跨学科知识整合、关联发现、对话管理、"
                "概念映射、系统思维"
            ),
            api_client=api_client
        )
    
    def _default_system_instruction(self) -> str:
        return (
            f"你是一位跨学科研究的元协调者，名字是{self.name}。"
            f"你的职责是观察和引导不同领域专家之间的对话，"
            f"识别他们讨论中可能存在的跨领域知识关联。"
            f"你需要：\n"
            f"1. 保持中立和客观，不偏向任何特定领域\n"
            f"2. 敏锐地捕捉不同领域概念之间的相似性、对应关系或隐喻联系\n"
            f"3. 提出引导性问题，促进更深入的跨领域对话\n"
            f"4. 总结和提炼讨论中的关键洞见\n"
            f"5. 识别潜在的创新性跨领域关联\n"
        )
    
    def analyze(self, prompt: str) -> str:
        """分析跨学科讨论"""
        full_prompt = (
            f"作为跨学科元协调者，请分析以下内容：\n\n"
            f"{prompt}\n\n"
            f"请识别其中的关键概念和潜在的跨领域联系。"
        )
        return self.client.generate(full_prompt, self.system_instruction)
    
    def moderate_discussion(
        self,
        topic: str,
        agent_responses: Dict[str, str]
    ) -> str:
        """
        主持讨论
        
        Args:
            topic: 讨论主题
            agent_responses: 各智能体的发言 {agent_name: response}
            
        Returns:
            主持评论和引导
        """
        # 构建讨论内容
        discussion_text = f"讨论主题：{topic}\n\n"
        discussion_text += "各领域专家的观点：\n\n"
        
        for agent_name, response in agent_responses.items():
            discussion_text += f"【{agent_name}】：\n{response}\n\n"
        
        prompt = (
            f"{discussion_text}\n"
            f"作为元协调者，请：\n"
            f"1. 总结各领域专家提出的核心观点\n"
            f"2. 指出你观察到的潜在跨领域联系\n"
            f"3. 提出2-3个引导性问题，促进更深入的讨论\n"
            f"4. 建议下一轮讨论可以重点探讨的方向\n"
        )
        
        return self.client.generate(prompt, self.system_instruction)
    
    def extract_edges(
        self,
        topic: str,
        discussion_history: List[Dict[str, Any]]
    ) -> List[KnowledgeEdge]:
        """
        从讨论历史中提取知识边
        
        Args:
            topic: 讨论主题
            discussion_history: 讨论历史
            
        Returns:
            知识边列表
        """
        # 构建讨论内容
        discussion_text = f"讨论主题：{topic}\n\n"
        discussion_text += "讨论历史：\n\n"
        
        for i, turn in enumerate(discussion_history, 1):
            agent_name = turn.get("agent", "未知")
            content = turn.get("content", "")
            discussion_text += f"轮次 {i} - {agent_name}：\n{content}\n\n"
        
        # 请求 Gemini 提取边
        prompt = (
            f"{discussion_text}\n"
            f"请分析以上讨论，提取所有可能的跨领域知识关联。\n"
            f"对于每一个关联，请提供以下信息（以JSON格式）：\n"
            f"{{\n"
            f'  "source_domain": "源领域名称",\n'
            f'  "source_concept": "源概念",\n'
            f'  "target_domain": "目标领域名称",\n'
            f'  "target_concept": "目标概念",\n'
            f'  "relation_type": "关系类型（如：类比、因果、隐喻、结构相似等）",\n'
            f'  "relation_description": "关系的详细描述",\n'
            f'  "reasoning": "发现此关联的推理过程",\n'
            f'  "confidence": 0.0到1.0之间的置信度数值\n'
            f"}}\n\n"
            f"请以JSON数组的形式返回所有发现的关联，格式为：\n"
            f'[{{...}}, {{...}}]\n\n'
            f"如果没有发现明确的关联，返回空数组 []"
        )
        
        try:
            response = self.client.generate(prompt, self.system_instruction)
            
            # 提取 JSON 数组
            edges_data = self._extract_json_from_response(response)
            
            if not edges_data:
                return []
            
            # 转换为 KnowledgeEdge 对象
            edges = []
            for edge_dict in edges_data:
                try:
                    edge = KnowledgeEdge(
                        source_domain=edge_dict.get("source_domain", ""),
                        source_concept=edge_dict.get("source_concept", ""),
                        target_domain=edge_dict.get("target_domain", ""),
                        target_concept=edge_dict.get("target_concept", ""),
                        relation_type=edge_dict.get("relation_type", ""),
                        relation_description=edge_dict.get("relation_description", ""),
                        reasoning=edge_dict.get("reasoning", ""),
                        confidence=float(edge_dict.get("confidence", 0.5)),
                        generated_by=self.name
                    )
                    edges.append(edge)
                except Exception as e:
                    print(f"警告：无法创建知识边 - {e}")
                    continue
            
            return edges
        
        except Exception as e:
            print(f"提取边时出错：{e}")
            return []
    
    def _extract_json_from_response(self, response: str) -> List[Dict]:
        """从响应中提取 JSON 数组"""
        try:
            # 尝试直接解析
            return json.loads(response)
        except:
            pass
        
        # 尝试查找 JSON 数组
        json_pattern = r'\[[\s\S]*?\]'
        matches = re.findall(json_pattern, response)
        
        for match in matches:
            try:
                data = json.loads(match)
                if isinstance(data, list):
                    return data
            except:
                continue
        
        # 尝试查找 JSON 对象并包装成数组
        json_obj_pattern = r'\{[\s\S]*?\}'
        matches = re.findall(json_obj_pattern, response)
        
        result = []
        for match in matches:
            try:
                obj = json.loads(match)
                if isinstance(obj, dict):
                    result.append(obj)
            except:
                continue
        
        return result
    
    def synthesize_insights(
        self,
        topic: str,
        edges: List[KnowledgeEdge]
    ) -> str:
        """
        综合洞见
        
        Args:
            topic: 讨论主题
            edges: 发现的知识边
            
        Returns:
            综合洞见报告
        """
        if not edges:
            return "暂未发现明确的跨领域关联。"
        
        # 构建边的描述
        edges_text = "\n".join([
            f"{i+1}. [{edge.source_domain}:{edge.source_concept}] "
            f"--{edge.relation_type}--> "
            f"[{edge.target_domain}:{edge.target_concept}] "
            f"(置信度: {edge.confidence:.2f})"
            for i, edge in enumerate(edges)
        ])
        
        prompt = (
            f"讨论主题：{topic}\n\n"
            f"发现的跨领域关联：\n{edges_text}\n\n"
            f"请综合分析这些跨领域关联，撰写一份洞见报告：\n"
            f"1. 这些关联反映了什么样的深层结构或模式？\n"
            f"2. 哪些关联最具创新性或启发性？\n"
            f"3. 这些发现对于理解'{topic}'有什么新的贡献？\n"
            f"4. 还有哪些值得进一步探索的方向？\n"
        )
        
        return self.client.generate(prompt, self.system_instruction)


if __name__ == "__main__":
    # 测试元协调智能体
    meta_agent = MetaAgent()
    print(f"✓ {meta_agent.name} initialized")
    print(f"  Domain: {meta_agent.domain}")
    print(f"  Expertise: {meta_agent.expertise}")

