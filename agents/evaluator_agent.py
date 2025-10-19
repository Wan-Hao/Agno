"""
评估智能体
"""
from typing import List, Dict, Any, Optional
from core.agent import Agent
from core.openai_client import OpenAIClient
from core.edge import KnowledgeEdge
import json


class EvaluatorAgent(Agent):
    """
    评估智能体
    
    负责：
    1. 评估知识边的有效性
    2. 计算各种评估指标
    3. 筛选高质量的关联
    4. 提供改进建议
    """
    
    def __init__(
        self,
        name: str = "评估专家",
        api_client: Optional[OpenAIClient] = None
    ):
        super().__init__(
            name=name,
            domain="知识质量评估",
            expertise=(
                "知识图谱评估、语义相似度分析、"
                "新颖性评估、学术价值判断"
            ),
            api_client=api_client
        )
    
    def _default_system_instruction(self) -> str:
        return (
            f"你是一位知识质量评估专家，名字是{self.name}。"
            f"你的职责是评估跨学科知识关联的质量和价值。"
            f"你需要从以下维度进行评估：\n"
            f"1. 语义合理性：关联在逻辑和语义上是否自洽\n"
            f"2. 知识稀有性：关联是否具有新颖性，在现有文献中较少被提及\n"
            f"3. 启发潜力：关联是否能够启发新的研究方向或理论\n"
            f"请保持客观、严谨，给出有依据的评分和建议。"
        )
    
    def analyze(self, prompt: str) -> str:
        """分析评估对象"""
        full_prompt = (
            f"作为知识质量评估专家，请分析以下内容：\n\n"
            f"{prompt}\n\n"
            f"请从学术价值和创新性角度提供评估。"
        )
        return self.client.generate(full_prompt, self.system_instruction)
    
    def evaluate_edge(
        self,
        edge: KnowledgeEdge,
        include_reasoning: bool = True
    ) -> Dict[str, Any]:
        """
        评估单个知识边
        
        Args:
            edge: 知识边
            include_reasoning: 是否包含详细推理
            
        Returns:
            评估结果字典
        """
        edge_description = (
            f"源领域：{edge.source_domain}\n"
            f"源概念：{edge.source_concept}\n"
            f"目标领域：{edge.target_domain}\n"
            f"目标概念：{edge.target_concept}\n"
            f"关系类型：{edge.relation_type}\n"
            f"关系描述：{edge.relation_description}\n"
            f"推理过程：{edge.reasoning}\n"
            f"原始置信度：{edge.confidence}"
        )
        
        prompt = (
            f"请评估以下跨领域知识关联：\n\n"
            f"{edge_description}\n\n"
            f"请从三个维度进行评估（每个维度给出0-1之间的分数）：\n"
            f"1. 语义合理性：关联在逻辑和语义层面是否合理、自洽\n"
            f"2. 知识稀有性：关联是否新颖，是否在现有文献中较少被提及\n"
            f"3. 启发潜力：关联是否能够启发新的研究思路或理论\n\n"
            f"请以JSON格式返回评估结果：\n"
            f"{{\n"
            f'  "semantic_similarity": 0.0到1.0之间的分数,\n'
            f'  "novelty_score": 0.0到1.0之间的分数,\n'
            f'  "inspiration_potential": 0.0到1.0之间的分数,\n'
            f'  "overall_score": 综合分数,\n'
            f'  "reasoning": "评估理由（简短）",\n'
            f'  "recommendation": "是否推荐（accept/review/reject）"\n'
            f"}}"
        )
        
        try:
            response = self.client.generate(prompt, self.system_instruction)
            eval_result = self._extract_json_from_response(response)
            
            if not eval_result:
                # 返回默认评估
                return {
                    "semantic_similarity": 0.5,
                    "novelty_score": 0.5,
                    "inspiration_potential": 0.5,
                    "overall_score": 0.5,
                    "reasoning": "评估失败，使用默认值",
                    "recommendation": "review"
                }
            
            # 更新边的评估指标
            edge.semantic_similarity = eval_result.get("semantic_similarity", 0.5)
            edge.novelty_score = eval_result.get("novelty_score", 0.5)
            edge.rarity_score = eval_result.get("novelty_score", 0.5)  # 使用novelty_score作为rarity_score
            
            return eval_result
        
        except Exception as e:
            print(f"评估边时出错：{e}")
            return {
                "semantic_similarity": 0.5,
                "novelty_score": 0.5,
                "inspiration_potential": 0.5,
                "overall_score": 0.5,
                "reasoning": f"评估失败：{str(e)}",
                "recommendation": "review"
            }
    
    def evaluate_edges_batch(
        self,
        edges: List[KnowledgeEdge]
    ) -> List[Dict[str, Any]]:
        """
        批量评估知识边
        
        Args:
            edges: 知识边列表
            
        Returns:
            评估结果列表
        """
        results = []
        for edge in edges:
            result = self.evaluate_edge(edge)
            result["edge"] = edge
            results.append(result)
        
        return results
    
    def filter_edges(
        self,
        edges: List[KnowledgeEdge],
        min_overall_score: float = 0.6
    ) -> List[KnowledgeEdge]:
        """
        筛选高质量的知识边
        
        Args:
            edges: 知识边列表
            min_overall_score: 最低综合分数阈值
            
        Returns:
            筛选后的知识边列表
        """
        eval_results = self.evaluate_edges_batch(edges)
        
        filtered = []
        for result in eval_results:
            if result.get("overall_score", 0) >= min_overall_score:
                filtered.append(result["edge"])
        
        return filtered
    
    def generate_evaluation_report(
        self,
        edges: List[KnowledgeEdge],
        eval_results: List[Dict[str, Any]]
    ) -> str:
        """
        生成评估报告
        
        Args:
            edges: 知识边列表
            eval_results: 评估结果列表
            
        Returns:
            评估报告文本
        """
        report = "# 跨学科知识关联评估报告\n\n"
        
        # 统计信息
        total = len(edges)
        accepted = sum(1 for r in eval_results if r.get("recommendation") == "accept")
        review = sum(1 for r in eval_results if r.get("recommendation") == "review")
        rejected = sum(1 for r in eval_results if r.get("recommendation") == "reject")
        
        report += f"## 总体统计\n\n"
        report += f"- 总关联数：{total}\n"
        report += f"- 推荐接受：{accepted} ({accepted/total*100:.1f}%)\n"
        report += f"- 需要审查：{review} ({review/total*100:.1f}%)\n"
        report += f"- 建议拒绝：{rejected} ({rejected/total*100:.1f}%)\n\n"
        
        # 详细评估
        report += "## 详细评估\n\n"
        
        for i, (edge, result) in enumerate(zip(edges, eval_results), 1):
            report += f"### {i}. {edge.source_domain} → {edge.target_domain}\n\n"
            report += f"**关联**：{edge.source_concept} --[{edge.relation_type}]--> {edge.target_concept}\n\n"
            report += f"**评分**：\n"
            report += f"- 语义合理性：{result.get('semantic_similarity', 0):.2f}\n"
            report += f"- 知识稀有性：{result.get('novelty_score', 0):.2f}\n"
            report += f"- 启发潜力：{result.get('inspiration_potential', 0):.2f}\n"
            report += f"- 综合分数：{result.get('overall_score', 0):.2f}\n\n"
            report += f"**建议**：{result.get('recommendation', 'review')}\n\n"
            report += f"**理由**：{result.get('reasoning', '无')}\n\n"
            report += "---\n\n"
        
        return report
    
    def _extract_json_from_response(self, response: str) -> Optional[Dict]:
        """从响应中提取 JSON 对象"""
        try:
            # 尝试直接解析
            return json.loads(response)
        except:
            pass
        
        # 尝试查找 JSON 对象
        import re
        json_pattern = r'\{[\s\S]*?\}'
        matches = re.findall(json_pattern, response)
        
        for match in matches:
            try:
                obj = json.loads(match)
                if isinstance(obj, dict):
                    return obj
            except:
                continue
        
        return None


if __name__ == "__main__":
    # 测试评估智能体
    evaluator = EvaluatorAgent()
    print(f"✓ {evaluator.name} initialized")
    print(f"  Domain: {evaluator.domain}")
    print(f"  Expertise: {evaluator.expertise}")

