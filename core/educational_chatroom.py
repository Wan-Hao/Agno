"""
教育知识关联聊天室

专门用于发现景点与教学知识点的关联
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import json
import re

from agents.scenic_agent import ScenicSpotAgent
from agents.domain_agents import PhysicsAgent, MathAgent
from core.educational_edge import EducationalEdge, EducationalEdgeBuilder, KnowledgePoint
from agents.meta_agent import MetaAgent


class EducationalChatroom:
    """
    教育知识关联聊天室
    
    目标：从景点特征中提取可用于教学的知识点关联
    """
    
    def __init__(
        self,
        scenic_agent: Optional[ScenicSpotAgent] = None,
        physics_agent: Optional[PhysicsAgent] = None,
        math_agent: Optional[MathAgent] = None,
        meta_agent: Optional[MetaAgent] = None
    ):
        self.scenic_agent = scenic_agent or ScenicSpotAgent()
        self.physics_agent = physics_agent or PhysicsAgent()
        self.math_agent = math_agent or MathAgent()
        self.meta_agent = meta_agent or MetaAgent()
        
        self.edge_builder = EducationalEdgeBuilder()
        self.discussion_history = []
        
        print(f"✓ 教育知识关联聊天室已创建")
    
    def load_scenic_spots(self, json_path: str) -> bool:
        """加载景点数据"""
        return self.scenic_agent.load_scenic_spots_from_json(json_path)
    
    def discover_educational_edges(
        self,
        spot_index: int,
        target_stage: str = "高中",
        target_subjects: Optional[List[str]] = None,
        rounds: int = 2
    ) -> List[EducationalEdge]:
        """
        发现教育知识边
        
        Args:
            spot_index: 景点索引
            target_stage: 目标学段（小学/初中/高中/大学）
            target_subjects: 目标学科列表
            rounds: 讨论轮次
            
        Returns:
            教育知识边列表
        """
        if target_subjects is None:
            target_subjects = ["数学", "物理"]
        
        spot = self.scenic_agent.get_spot_by_index(spot_index)
        if not spot:
            print(f"✗ 无效的景点索引: {spot_index}")
            return []
        
        spot_name = spot.get("scenic_spot", "")
        city = spot.get("province_city", "")
        description = spot.get("description", "")
        
        print(f"\n{'='*70}")
        print(f"分析景点: {spot_name} ({city})")
        print(f"目标学段: {target_stage}")
        print(f"目标学科: {', '.join(target_subjects)}")
        print(f"{'='*70}\n")
        
        # 第一步：景点专家提取教学潜力点
        print(f"[{self.scenic_agent.name}] 正在分析教学潜力...")
        teaching_analysis = self._analyze_teaching_potential(
            spot, target_stage, target_subjects
        )
        print(f"✓ 教学潜力分析完成\n")
        
        # 第二步：各学科专家分析具体知识点
        edges = []
        
        for subject in target_subjects:
            print(f"\n--- 分析学科: {subject} ---\n")
            
            if subject == "物理":
                agent = self.physics_agent
            elif subject == "数学":
                agent = self.math_agent
            else:
                print(f"✗ 暂不支持学科: {subject}")
                continue
            
            # 专家分析
            print(f"[{agent.name}] 正在提取知识点...")
            knowledge_points = self._extract_knowledge_points(
                spot, agent, target_stage, teaching_analysis
            )
            
            print(f"✓ 发现 {len(knowledge_points)} 个潜在知识点\n")
            
            # 为每个知识点创建教育边
            for kp_data in knowledge_points:
                try:
                    edge = self._create_educational_edge(
                        city=city,
                        spot_name=spot_name,
                        stage=target_stage,
                        subject=subject,
                        kp_data=kp_data
                    )
                    if edge:
                        edges.append(edge)
                        self.edge_builder.edges.append(edge)
                except Exception as e:
                    print(f"警告：创建教育边失败 - {e}")
        
        print(f"\n{'='*70}")
        print(f"✓ 共发现 {len(edges)} 个教育知识点关联")
        print(f"{'='*70}\n")
        
        # 显示结果
        self._display_edges(edges)
        
        return edges
    
    def discover_all_spots(
        self,
        target_stage: str = "高中",
        target_subjects: Optional[List[str]] = None,
        max_spots: Optional[int] = None
    ) -> List[EducationalEdge]:
        """
        发现所有景点的教育知识边
        
        Args:
            target_stage: 目标学段
            target_subjects: 目标学科
            max_spots: 最大景点数量（None表示全部）
            
        Returns:
            所有教育知识边
        """
        all_edges = []
        spots_count = len(self.scenic_agent.scenic_spots)
        
        if max_spots:
            spots_count = min(spots_count, max_spots)
        
        for i in range(spots_count):
            print(f"\n\n{'#'*70}")
            print(f"# 景点 {i+1}/{spots_count}")
            print(f"{'#'*70}")
            
            edges = self.discover_educational_edges(
                spot_index=i,
                target_stage=target_stage,
                target_subjects=target_subjects
            )
            all_edges.extend(edges)
        
        print(f"\n\n{'='*70}")
        print(f"总计: {len(all_edges)} 个教育知识点关联")
        print(f"{'='*70}\n")
        
        return all_edges
    
    def _analyze_teaching_potential(
        self,
        spot: Dict,
        target_stage: str,
        target_subjects: List[str]
    ) -> str:
        """分析景点的教学潜力"""
        spot_name = spot.get("scenic_spot", "")
        description = spot.get("description", "")
        
        prompt = f"""
你是一位教育专家，正在分析景点的教学价值。

景点：{spot_name}
描述：{description}

目标学段：{target_stage}
目标学科：{', '.join(target_subjects)}

请分析这个景点中哪些特征、场景、现象可以用于教学，特别是：

1. **物理教学**：结构力学、光学、热学、流体力学、能量等
2. **数学教学**：几何、对称、比例、测量、统计、函数等

对于每个潜在的教学点，请说明：
- 具体的场景或特征
- 可能关联的知识点
- 为什么适合{target_stage}学段

请详细列出所有可能的教学应用场景。
"""
        
        return self.scenic_agent.client.generate(
            prompt,
            self.scenic_agent.system_instruction
        )
    
    def _extract_knowledge_points(
        self,
        spot: Dict,
        agent: Any,
        target_stage: str,
        teaching_analysis: str
    ) -> List[Dict[str, Any]]:
        """提取具体的知识点"""
        spot_name = spot.get("scenic_spot", "")
        description = spot.get("description", "")
        
        # 根据学段确定难度级别
        difficulty_map = {
            "小学": "基础",
            "初中": "中等",
            "高中": "中等偏上",
            "大学": "高级"
        }
        target_difficulty = difficulty_map.get(target_stage, "中等")
        
        prompt = f"""
你是一位{agent.domain}教师，正在为{target_stage}学生设计基于景点的教学内容。

景点：{spot_name}
描述：{description}

教学潜力分析：
{teaching_analysis}

请提取3-5个**具体的、可操作的**{agent.domain}知识点，每个知识点必须：
1. 适合{target_stage}学段
2. 与景点特征有明确对应
3. 可以通过景点场景来讲解

对于每个知识点，请以JSON格式返回：

{{
  "scene_description": "景点中的具体场景描述（详细说明哪个特征体现了这个知识点，100-200字）",
  "chapter_number": 章节号（数字）,
  "chapter_title": "章节名称",
  "section_number": "小节号（如2.1）",
  "section_title": "小节名称",
  "point_name": "知识点名称",
  "point_description": "知识点的教学描述",
  "formula": "相关公式（如果有）",
  "difficulty": "基础/中等/中等偏上/高级",
  "applications": ["应用场景1", "应用场景2"],
  "reasoning": "为什么这个景点场景适合教学这个知识点"
}}

请返回JSON数组格式：[{{...}}, {{...}}, ...]

重要：
- scene_description要具体到景点的某个特征或现象
- 知识点要符合{target_stage}课标
- 难度建议为{target_difficulty}
- 每个知识点都要有清晰的教学价值
"""
        
        try:
            response = agent.client.generate(prompt, agent.system_instruction)
            
            # 提取JSON
            json_match = re.search(r'\[[\s\S]*\]', response)
            if json_match:
                data = json.loads(json_match.group())
                return data if isinstance(data, list) else []
        except Exception as e:
            print(f"提取知识点失败: {e}")
        
        return []
    
    def _create_educational_edge(
        self,
        city: str,
        spot_name: str,
        stage: str,
        subject: str,
        kp_data: Dict[str, Any]
    ) -> Optional[EducationalEdge]:
        """创建教育知识边"""
        try:
            knowledge_point = KnowledgePoint(
                chapter_number=int(kp_data.get("chapter_number", 1)),
                chapter_title=kp_data.get("chapter_title", ""),
                section_number=str(kp_data.get("section_number", "1.1")),
                section_title=kp_data.get("section_title", ""),
                point_name=kp_data.get("point_name", ""),
                description=kp_data.get("point_description", ""),
                formula=kp_data.get("formula"),
                difficulty=kp_data.get("difficulty", "基础"),
                applications=kp_data.get("applications", [])
            )
            
            edge = EducationalEdge(
                province_city=city,
                scenic_spot=spot_name,
                name=kp_data.get("scene_description", ""),
                stage=stage,
                subject=subject,
                knowledge_point=knowledge_point,
                reasoning=kp_data.get("reasoning"),
                confidence=kp_data.get("confidence", 0.8)
            )
            
            return edge
        except Exception as e:
            print(f"创建边失败: {e}")
            return None
    
    def _display_edges(self, edges: List[EducationalEdge]):
        """显示教育知识边"""
        for i, edge in enumerate(edges, 1):
            print(f"\n{i}. {edge.scenic_spot} → {edge.subject} ({edge.stage})")
            print(f"   知识点: {edge.knowledge_point.point_name}")
            print(f"   章节: {edge.knowledge_point.chapter_number}. {edge.knowledge_point.chapter_title}")
            print(f"   难度: {edge.knowledge_point.difficulty}")
            print(f"   场景: {edge.name[:80]}...")
            if edge.knowledge_point.formula:
                print(f"   公式: {edge.knowledge_point.formula}")
    
    def export_results(
        self,
        output_path: str,
        pretty_print: bool = True
    ):
        """
        导出结果
        
        Args:
            output_path: 输出文件路径
            pretty_print: 是否美化输出
        """
        self.edge_builder.export_to_file(output_path)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        edges = self.edge_builder.edges
        
        # 按学科统计
        by_subject = {}
        for edge in edges:
            by_subject[edge.subject] = by_subject.get(edge.subject, 0) + 1
        
        # 按景点统计
        by_spot = {}
        for edge in edges:
            by_spot[edge.scenic_spot] = by_spot.get(edge.scenic_spot, 0) + 1
        
        # 按难度统计
        by_difficulty = {}
        for edge in edges:
            diff = edge.knowledge_point.difficulty
            by_difficulty[diff] = by_difficulty.get(diff, 0) + 1
        
        return {
            "total_edges": len(edges),
            "by_subject": by_subject,
            "by_spot": by_spot,
            "by_difficulty": by_difficulty,
            "avg_confidence": sum(e.confidence for e in edges) / len(edges) if edges else 0
        }


if __name__ == "__main__":
    print("教育知识关联聊天室模块加载成功")


