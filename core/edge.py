"""
知识边定义
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class KnowledgeEdge(BaseModel):
    """
    知识边：表示两个不同领域概念之间的关联关系
    """
    
    # 基本信息
    source_domain: str = Field(..., description="源领域名称")
    source_concept: str = Field(..., description="源概念")
    target_domain: str = Field(..., description="目标领域名称")
    target_concept: str = Field(..., description="目标概念")
    
    # 关系信息
    relation_type: str = Field(..., description="关系类型（如：类比、因果、隐喻等）")
    relation_description: str = Field(..., description="关系描述")
    
    # 评估指标
    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="置信度 (0-1)"
    )
    semantic_similarity: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="语义相似度 (0-1)"
    )
    novelty_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="新颖度评分 (0-1)"
    )
    rarity_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="稀有度评分 (0-1)"
    )
    
    # 生成信息
    reasoning: str = Field(..., description="生成该边的推理过程")
    generated_by: str = Field(..., description="生成该边的 Agent 或 Agent 组合")
    generated_at: datetime = Field(
        default_factory=datetime.now,
        description="生成时间"
    )
    
    # 验证状态
    validated: bool = Field(default=False, description="是否已验证")
    validation_notes: Optional[str] = Field(default=None, description="验证备注")
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "source": {
                "domain": self.source_domain,
                "concept": self.source_concept
            },
            "target": {
                "domain": self.target_domain,
                "concept": self.target_concept
            },
            "relation": {
                "type": self.relation_type,
                "description": self.relation_description
            },
            "evaluation": {
                "confidence": self.confidence,
                "semantic_similarity": self.semantic_similarity,
                "novelty_score": self.novelty_score,
                "rarity_score": self.rarity_score
            },
            "metadata": {
                "reasoning": self.reasoning,
                "generated_by": self.generated_by,
                "generated_at": self.generated_at.isoformat(),
                "validated": self.validated,
                "validation_notes": self.validation_notes
            }
        }
    
    def get_overall_score(self) -> float:
        """
        计算综合评分
        
        综合考虑置信度、语义相似度、新颖度和稀有度
        """
        scores = [self.confidence]
        
        if self.semantic_similarity is not None:
            scores.append(self.semantic_similarity)
        if self.novelty_score is not None:
            scores.append(self.novelty_score)
        if self.rarity_score is not None:
            scores.append(self.rarity_score)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def __str__(self) -> str:
        """字符串表示"""
        return (
            f"[{self.source_domain}:{self.source_concept}] "
            f"--[{self.relation_type}]--> "
            f"[{self.target_domain}:{self.target_concept}] "
            f"(score: {self.get_overall_score():.2f})"
        )
    
    def __repr__(self) -> str:
        """详细表示"""
        return f"KnowledgeEdge({str(self)})"


if __name__ == "__main__":
    # 测试知识边
    edge = KnowledgeEdge(
        source_domain="物理学",
        source_concept="熵增原理",
        target_domain="文学",
        target_concept="时间流逝的不可逆性",
        relation_type="隐喻映射",
        relation_description="物理学中的熵增描述系统的不可逆演化，与文学中对时间单向流逝的描写存在深层隐喻关系",
        confidence=0.85,
        reasoning="两者都强调了某种不可逆的过程，熵增是热力学层面的，时间流逝是感知层面的",
        generated_by="PhysicsAgent + LiteratureAgent"
    )
    
    print(edge)
    print("\nDetailed info:")
    print(edge.model_dump_json(indent=2))

