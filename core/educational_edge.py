"""
教育知识边 - 景点与学科知识点的关联
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import json


@dataclass
class KnowledgePoint:
    """知识点数据结构"""
    chapter_number: int
    chapter_title: str
    section_number: str
    section_title: str
    point_name: str
    description: str
    formula: Optional[str] = None
    difficulty: str = "基础"
    applications: list = None
    
    def __post_init__(self):
        if self.applications is None:
            self.applications = []
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


@dataclass
class EducationalEdge:
    """
    教育知识边
    
    连接景点场景与具体教学知识点
    """
    province_city: str
    scenic_spot: str
    name: str  # 具体场景描述
    stage: str  # 学段：小学/初中/高中/大学
    subject: str  # 学科：数学/物理/化学等
    knowledge_point: KnowledgePoint
    
    # 可选字段
    reasoning: Optional[str] = None  # 关联推理
    confidence: float = 0.8  # 置信度
    reference: Optional[list] = None  # 参考文献页码
    images: Optional[list] = None  # 相关图片
    
    def __post_init__(self):
        if self.reference is None:
            self.reference = []
        if self.images is None:
            self.images = []
        
        # 确保knowledge_point是KnowledgePoint实例
        if isinstance(self.knowledge_point, dict):
            self.knowledge_point = KnowledgePoint(**self.knowledge_point)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（符合用户期望的输出格式）"""
        result = {
            "province_city": self.province_city,
            "scenic_spot": self.scenic_spot,
            "name": self.name,
            "stage": self.stage,
            "subject": self.subject,
            "knowledge_point": self.knowledge_point.to_dict()
        }
        
        # 添加可选字段
        if self.reasoning:
            result["reasoning"] = self.reasoning
        if self.confidence != 0.8:
            result["confidence"] = self.confidence
        if self.reference:
            result["reference"] = self.reference
        if self.images:
            result["images"] = self.images
        
        return result
    
    def to_json(self, indent: int = 2) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EducationalEdge":
        """从字典创建"""
        return cls(**data)
    
    def __str__(self) -> str:
        """字符串表示"""
        return (
            f"[{self.scenic_spot}] {self.name[:50]}... "
            f"→ [{self.subject}] {self.knowledge_point.point_name}"
        )


class EducationalEdgeBuilder:
    """教育知识边构建器"""
    
    def __init__(self):
        self.edges = []
    
    def add_edge(
        self,
        province_city: str,
        scenic_spot: str,
        scene_description: str,
        stage: str,
        subject: str,
        chapter_number: int,
        chapter_title: str,
        section_number: str,
        section_title: str,
        point_name: str,
        point_description: str,
        formula: Optional[str] = None,
        difficulty: str = "基础",
        applications: Optional[list] = None,
        reasoning: Optional[str] = None,
        confidence: float = 0.8,
        reference: Optional[list] = None
    ) -> EducationalEdge:
        """
        添加教育知识边
        
        Args:
            province_city: 城市
            scenic_spot: 景点名称
            scene_description: 具体场景描述
            stage: 学段
            subject: 学科
            chapter_number: 章节号
            chapter_title: 章节标题
            section_number: 小节号
            section_title: 小节标题
            point_name: 知识点名称
            point_description: 知识点描述
            formula: 公式（可选）
            difficulty: 难度
            applications: 应用场景
            reasoning: 推理过程
            confidence: 置信度
            reference: 参考文献
            
        Returns:
            创建的教育知识边
        """
        knowledge_point = KnowledgePoint(
            chapter_number=chapter_number,
            chapter_title=chapter_title,
            section_number=section_number,
            section_title=section_title,
            point_name=point_name,
            description=point_description,
            formula=formula,
            difficulty=difficulty,
            applications=applications or []
        )
        
        edge = EducationalEdge(
            province_city=province_city,
            scenic_spot=scenic_spot,
            name=scene_description,
            stage=stage,
            subject=subject,
            knowledge_point=knowledge_point,
            reasoning=reasoning,
            confidence=confidence,
            reference=reference
        )
        
        self.edges.append(edge)
        return edge
    
    def get_edges(self) -> list:
        """获取所有边"""
        return self.edges
    
    def to_json_list(self) -> list:
        """转换为JSON列表"""
        return [edge.to_dict() for edge in self.edges]
    
    def export_to_file(self, output_path: str):
        """导出到文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_json_list(), f, ensure_ascii=False, indent=2)
        print(f"✓ 已导出 {len(self.edges)} 个教育知识边到: {output_path}")
    
    def filter_by_subject(self, subject: str) -> list:
        """按学科筛选"""
        return [edge for edge in self.edges if edge.subject == subject]
    
    def filter_by_stage(self, stage: str) -> list:
        """按学段筛选"""
        return [edge for edge in self.edges if edge.stage == stage]
    
    def filter_by_scenic_spot(self, scenic_spot: str) -> list:
        """按景点筛选"""
        return [edge for edge in self.edges if edge.scenic_spot == scenic_spot]


if __name__ == "__main__":
    # 测试示例
    builder = EducationalEdgeBuilder()
    
    # 添加一个示例边
    edge = builder.add_edge(
        province_city="扬州",
        scenic_spot="瘦西湖",
        scene_description="瘦西湖的钓鱼台是园林\"框景\"艺术的典范。其墙上设有多个月洞门，从特定角度通过圆形的门洞，恰好能将远处的五亭桥和白塔框入\"画\"中，形成一幅完美的构图。",
        stage="高中",
        subject="数学",
        chapter_number=2,
        chapter_title="圆锥曲线",
        section_number="2.1",
        section_title="圆",
        point_name="点与圆的位置关系",
        point_description="掌握判断点与圆的位置关系的方法，理解点在圆内、圆上、圆外的判定条件",
        formula="点P(x₀,y₀)到圆心C(a,b)的距离d = √[(x₀-a)² + (y₀-b)²]",
        difficulty="基础",
        applications=["几何分析", "位置判断", "实际问题"],
        confidence=0.9,
        reference=[18, 23]
    )
    
    print("✓ 教育知识边创建成功")
    print(f"\n{edge}")
    print(f"\nJSON格式:\n{edge.to_json()}")


