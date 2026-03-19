"""
景点知识关联聊天室

三方协作模式：景点专家 + 物理专家 + 数学专家
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import json

from core.agent import Agent
from agents.scenic_agent import ScenicSpotAgent
from agents.domain_agents import PhysicsAgent, MathAgent
from core.edge import KnowledgeEdge
from agents.meta_agent import MetaAgent


class ScenicKnowledgeChatroom:
    """
    景点知识关联聊天室
    
    工作流程：
    1. 景点专家介绍景点，提出引导性问题
    2. 物理专家从物理学角度分析景点
    3. 数学专家从数学角度分析景点
    4. 景点专家促进讨论，提出新的引导
    5. 多轮对话后，提取知识关联边
    """
    
    def __init__(
        self,
        scenic_agent: Optional[ScenicSpotAgent] = None,
        physics_agent: Optional[PhysicsAgent] = None,
        math_agent: Optional[MathAgent] = None,
        meta_agent: Optional[MetaAgent] = None
    ):
        """
        初始化景点知识聊天室
        
        Args:
            scenic_agent: 景点智能体
            physics_agent: 物理智能体
            math_agent: 数学智能体
            meta_agent: 元协调者（用于提取知识边）
        """
        self.scenic_agent = scenic_agent or ScenicSpotAgent()
        self.physics_agent = physics_agent or PhysicsAgent()
        self.math_agent = math_agent or MathAgent()
        self.meta_agent = meta_agent or MetaAgent()
        
        # 讨论历史
        self.discussion_history: List[Dict[str, Any]] = []
        
        # 发现的知识边
        self.discovered_edges: List[KnowledgeEdge] = []
        
        print(f"✓ 景点知识关联聊天室已创建")
        print(f"  参与者:")
        print(f"    - {self.scenic_agent.name} (景点)")
        print(f"    - {self.physics_agent.name} (物理)")
        print(f"    - {self.math_agent.name} (数学)")
    
    def load_scenic_spots(self, json_path: str) -> bool:
        """
        加载景点数据
        
        Args:
            json_path: 景点JSON文件路径
            
        Returns:
            是否加载成功
        """
        return self.scenic_agent.load_scenic_spots_from_json(json_path)
    
    def discuss_spot(
        self,
        spot_index: int,
        rounds: int = 3,
        focus_aspects: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        讨论单个景点
        
        Args:
            spot_index: 景点索引（从0开始）
            rounds: 讨论轮次
            focus_aspects: 关注的方面（可选）
            
        Returns:
            讨论结果
        """
        # 获取景点
        spot = self.scenic_agent.get_spot_by_index(spot_index)
        if not spot:
            print(f"✗ 景点索引无效: {spot_index}")
            return {"success": False, "error": "invalid_index"}
        
        spot_name = spot.get("scenic_spot", "未知景点")
        
        print(f"\n{'='*70}")
        print(f"开始讨论景点: {spot_name}")
        print(f"{'='*70}\n")
        
        # 第一轮：景点专家介绍
        print(f"[{self.scenic_agent.name}] 正在介绍景点...")
        scenic_intro = self.scenic_agent.introduce_spot(spot, focus_aspects)
        
        self._record_discussion(
            round_num=0,
            agent=self.scenic_agent,
            content=scenic_intro,
            spot_name=spot_name
        )
        
        print(f"\n[{self.scenic_agent.name}]:\n{scenic_intro}\n")
        print(f"{'-'*70}\n")
        
        # 多轮讨论
        context = scenic_intro
        
        for round_num in range(1, rounds + 1):
            print(f"\n--- 第 {round_num} 轮讨论 ---\n")
            
            # 物理专家发言
            print(f"[{self.physics_agent.name}] 正在分析...")
            physics_prompt = self._build_physics_prompt(spot, context)
            physics_response = self.physics_agent.client.generate(
                physics_prompt,
                self.physics_agent.system_instruction
            )
            
            self._record_discussion(
                round_num=round_num,
                agent=self.physics_agent,
                content=physics_response,
                spot_name=spot_name
            )
            
            print(f"\n[{self.physics_agent.name}]:\n{physics_response[:400]}...\n")
            
            # 数学专家发言
            print(f"[{self.math_agent.name}] 正在分析...")
            math_prompt = self._build_math_prompt(spot, context, physics_response)
            math_response = self.math_agent.client.generate(
                math_prompt,
                self.math_agent.system_instruction
            )
            
            self._record_discussion(
                round_num=round_num,
                agent=self.math_agent,
                content=math_response,
                spot_name=spot_name
            )
            
            print(f"\n[{self.math_agent.name}]:\n{math_response[:400]}...\n")
            
            # 景点专家促进讨论
            if round_num < rounds:
                print(f"[{self.scenic_agent.name}] 正在促进讨论...")
                facilitation = self.scenic_agent.facilitate_discussion(
                    physics_response,
                    math_response
                )
                
                self._record_discussion(
                    round_num=round_num,
                    agent=self.scenic_agent,
                    content=facilitation,
                    spot_name=spot_name
                )
                
                print(f"\n[{self.scenic_agent.name}]:\n{facilitation}\n")
                print(f"{'-'*70}\n")
                
                # 更新上下文
                context = f"""
前情提要：
{facilitation}

上一轮讨论要点：
物理视角：{physics_response[:300]}
数学视角：{math_response[:300]}
"""
            else:
                print(f"{'-'*70}\n")
        
        # 提取知识边
        print(f"\n[{self.meta_agent.name}] 正在提取知识关联...")
        edges = self._extract_edges_for_spot(spot_name)
        self.discovered_edges.extend(edges)
        
        print(f"✓ 发现 {len(edges)} 个知识关联\n")
        
        # 显示边
        if edges:
            self._display_edges(edges)
        
        return {
            "success": True,
            "spot_name": spot_name,
            "rounds": rounds,
            "edges_count": len(edges),
            "edges": [edge.to_dict() for edge in edges]
        }
    
    def discuss_multiple_spots(
        self,
        spot_indices: List[int],
        rounds_per_spot: int = 2
    ) -> Dict[str, Any]:
        """
        讨论多个景点
        
        Args:
            spot_indices: 景点索引列表
            rounds_per_spot: 每个景点的讨论轮次
            
        Returns:
            总体讨论结果
        """
        results = []
        
        for i, spot_idx in enumerate(spot_indices, 1):
            print(f"\n\n{'#'*70}")
            print(f"# 景点 {i}/{len(spot_indices)}")
            print(f"{'#'*70}")
            
            result = self.discuss_spot(spot_idx, rounds=rounds_per_spot)
            results.append(result)
        
        # 总结
        total_edges = len(self.discovered_edges)
        successful = sum(1 for r in results if r.get("success"))
        
        print(f"\n\n{'='*70}")
        print(f"讨论总结")
        print(f"{'='*70}")
        print(f"- 讨论景点数: {len(spot_indices)}")
        print(f"- 成功讨论: {successful}")
        print(f"- 发现关联: {total_edges} 个")
        print(f"{'='*70}\n")
        
        return {
            "total_spots": len(spot_indices),
            "successful": successful,
            "total_edges": total_edges,
            "results": results
        }
    
    def _build_physics_prompt(self, spot: Dict, context: str) -> str:
        """构建物理专家的提示"""
        spot_name = spot.get("scenic_spot", "")
        description = spot.get("description", "")
        
        return f"""
你正在参与一个景点知识关联讨论。景点专家刚刚介绍了景点「{spot_name}」。

景点描述：
{description}

上下文：
{context}

请从物理学角度分析这个景点，思考：

1. **结构与力学**：建筑的支撑、平衡、稳定性涉及哪些物理原理？
2. **材料特性**：使用的材料有什么物理特性？
3. **光学现象**：视觉效果、倒影、灯光中有哪些光学原理？
4. **能量与热学**：是否涉及能量转换、温度、热传导等？
5. **流体力学**：如果有水体或气流，涉及哪些流体力学？
6. **其他物理概念**：还有哪些物理学概念可以与景点特征关联？

请具体分析，并明确指出物理概念与景点特征的对应关系。
"""
    
    def _build_math_prompt(
        self,
        spot: Dict,
        context: str,
        physics_response: str
    ) -> str:
        """构建数学专家的提示"""
        spot_name = spot.get("scenic_spot", "")
        description = spot.get("description", "")
        
        return f"""
你正在参与一个景点知识关联讨论。景点专家介绍了景点「{spot_name}」，物理专家已经发表了观点。

景点描述：
{description}

物理专家的观点：
{physics_response}

上下文：
{context}

请从数学角度分析这个景点，思考：

1. **几何结构**：建筑或景观的形状、对称性、比例关系
2. **空间关系**：布局、路径、拓扑结构
3. **数值特征**：高度、长度、面积、角度等测量值
4. **模式与规律**：重复、变化、序列、分形等
5. **优化原理**：设计中是否体现某种最优化思想（如黄金分割）
6. **数学建模**：如何用数学模型描述景点的某些特征

请具体分析，并尝试与物理专家的观点建立联系。
"""
    
    def _record_discussion(
        self,
        round_num: int,
        agent: Agent,
        content: str,
        spot_name: str
    ):
        """记录讨论"""
        self.discussion_history.append({
            "round": round_num,
            "agent": agent.name,
            "domain": agent.domain,
            "content": content,
            "spot_name": spot_name,
            "timestamp": datetime.now().isoformat()
        })
    
    def _extract_edges_for_spot(self, spot_name: str) -> List[KnowledgeEdge]:
        """提取单个景点的知识边"""
        # 构建讨论历史文本
        discussion_text = f"景点：{spot_name}\n\n"
        
        for turn in self.discussion_history:
            if turn.get("spot_name") == spot_name:
                discussion_text += f"\n[{turn['agent']}]:\n{turn['content']}\n"
        
        # 请求元协调者提取边
        prompt = f"""
以下是关于景点「{spot_name}」的跨学科讨论记录：

{discussion_text}

请提取所有明确的知识关联。对于每个关联，请以JSON格式提供：

{{
  "source_domain": "源领域（景点/物理学/数学）",
  "source_concept": "源概念（景点特征或学科概念）",
  "target_domain": "目标领域",
  "target_concept": "目标概念",
  "relation_type": "关系类型（体现/应用/类比/映射等）",
  "relation_description": "关系的详细描述",
  "reasoning": "发现此关联的推理过程",
  "confidence": 0.0到1.0之间的置信度
}}

返回JSON数组格式：[{{...}}, {{...}}]

重要：只提取明确讨论到的、有具体对应关系的关联！
"""
        
        try:
            response = self.meta_agent.client.generate(
                prompt,
                self.meta_agent.system_instruction
            )
            
            # 提取JSON
            edges_data = self.meta_agent._extract_json_from_response(response)
            
            if not edges_data:
                return []
            
            # 转换为KnowledgeEdge对象
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
                        generated_by=self.meta_agent.name,
                        metadata={"scenic_spot": spot_name}
                    )
                    edges.append(edge)
                except Exception as e:
                    print(f"警告：无法创建知识边 - {e}")
                    continue
            
            return edges
        
        except Exception as e:
            print(f"提取边时出错：{e}")
            return []
    
    def _display_edges(self, edges: List[KnowledgeEdge]):
        """显示知识边"""
        print(f"\n{'='*70}")
        print(f"发现的知识关联")
        print(f"{'='*70}\n")
        
        for i, edge in enumerate(edges, 1):
            print(f"{i}. [{edge.source_domain}] {edge.source_concept}")
            print(f"   --({edge.relation_type})--> ")
            print(f"   [{edge.target_domain}] {edge.target_concept}")
            print(f"   描述: {edge.relation_description[:100]}...")
            print(f"   置信度: {edge.confidence:.2f}")
            print()
    
    def export_results(
        self,
        output_dir: Path,
        prefix: str = "scenic_knowledge"
    ) -> bool:
        """
        导出结果
        
        Args:
            output_dir: 输出目录
            prefix: 文件名前缀
            
        Returns:
            是否导出成功
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            # 导出讨论日志
            log_file = output_dir / f"{prefix}_discussion_{timestamp}.json"
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "discussion_history": self.discussion_history,
                    "export_time": datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            
            print(f"✓ 讨论日志已导出: {log_file}")
            
            # 导出知识边
            edges_file = output_dir / f"{prefix}_edges_{timestamp}.json"
            with open(edges_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "edges": [edge.to_dict() for edge in self.discovered_edges],
                    "total_count": len(self.discovered_edges),
                    "export_time": datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            
            print(f"✓ 知识边已导出: {edges_file}")
            
            return True
        
        except Exception as e:
            print(f"✗ 导出失败: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        # 按景点统计
        spots = set(turn.get("spot_name") for turn in self.discussion_history)
        
        # 按领域统计边
        edge_by_domain = {}
        for edge in self.discovered_edges:
            pair = f"{edge.source_domain} -> {edge.target_domain}"
            edge_by_domain[pair] = edge_by_domain.get(pair, 0) + 1
        
        return {
            "total_turns": len(self.discussion_history),
            "spots_discussed": len(spots),
            "total_edges": len(self.discovered_edges),
            "edges_by_domain": edge_by_domain,
            "avg_confidence": sum(e.confidence for e in self.discovered_edges) / len(self.discovered_edges) if self.discovered_edges else 0
        }


if __name__ == "__main__":
    # 测试聊天室
    print("景点知识关联聊天室模块加载成功")
    
    # 创建聊天室
    chatroom = ScenicKnowledgeChatroom()
    
    # 加载景点数据（如果存在）
    test_json = Path("dataset/senarios/shanghai.json")
    if test_json.exists():
        chatroom.load_scenic_spots(str(test_json))
        print(f"\n可用景点: {len(chatroom.scenic_agent.list_all_spots())} 个")


