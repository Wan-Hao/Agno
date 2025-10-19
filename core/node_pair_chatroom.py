"""
节点对节点聊天室

核心设计：
1. 每次对话聚焦一对节点（物理节点 ↔ 数学节点）
2. 每个agent携带该节点的学科内上下文
3. 讨论该节点对融合的可能性
4. 评估agent判断是否保留边
5. 通过function call写入JSON
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
from core.agent import Agent
from agents.meta_agent import MetaAgent
from agents.evaluator_agent import EvaluatorAgent
from datetime import datetime
import json
import re


class NodePairChatroom:
    """节点对节点的聊天室"""
    
    def __init__(
        self,
        physics_agent: Agent,
        math_agent: Agent,
        physics_graph: Dict[str, Any],
        math_graph: Dict[str, Any],
        meta_agent: Optional[MetaAgent] = None,
        evaluator: Optional[EvaluatorAgent] = None,
        output_file: Optional[Path] = None
    ):
        """
        初始化节点对聊天室
        
        Args:
            physics_agent: 物理专家
            math_agent: 数学专家
            physics_graph: 物理知识图谱
            math_graph: 数学知识图谱
            meta_agent: 元协调者（可选）
            evaluator: 评估agent（可选）
            output_file: 输出JSON文件路径
        """
        self.physics_agent = physics_agent
        self.math_agent = math_agent
        self.meta_agent = meta_agent or MetaAgent()
        self.evaluator = evaluator or EvaluatorAgent()
        
        # 知识图谱
        self.physics_graph = physics_graph
        self.math_graph = math_graph
        
        # 构建节点索引和邻接表
        self.physics_nodes = {n['id']: n for n in physics_graph['nodes']}
        self.math_nodes = {n['id']: n for n in math_graph['nodes']}
        
        self.physics_edges = self._build_adjacency_list(physics_graph['edges'])
        self.math_edges = self._build_adjacency_list(math_graph['edges'])
        
        # 输出文件
        self.output_file = output_file or Path("output/cross_domain_edges.json")
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 初始化输出文件
        self._init_output_file()
        
        print(f"✓ 节点对聊天室已创建")
        print(f"  物理节点: {len(self.physics_nodes)}")
        print(f"  数学节点: {len(self.math_nodes)}")
        print(f"  输出文件: {self.output_file}")
    
    def _build_adjacency_list(self, edges: List[Dict]) -> Dict[str, List[str]]:
        """构建邻接表（节点的相关节点）"""
        adj = {}
        for edge in edges:
            source = edge.get('source', '')
            target = edge.get('target', '')
            
            if source:
                if source not in adj:
                    adj[source] = []
                if target:
                    adj[source].append(target)
            
            if target:
                if target not in adj:
                    adj[target] = []
                if source:
                    adj[target].append(source)
        
        return adj
    
    def _init_output_file(self):
        """初始化输出文件"""
        if not self.output_file.exists():
            initial_data = {
                "metadata": {
                    "source_graphs": {
                        "physics": "physics_knowledge_graph_new.json",
                        "math": "math_knowledge_graph_new.json"
                    },
                    "created_at": datetime.now().isoformat(),
                    "total_edges": 0
                },
                "edges": []
            }
            write_edge_json(str(self.output_file), initial_data)
    
    def discuss_node_pair(
        self,
        physics_node_id: str,
        math_node_id: str,
        context_depth: int = 1
    ) -> Optional[Dict[str, Any]]:
        """
        讨论一对节点
        
        Args:
            physics_node_id: 物理节点ID
            math_node_id: 数学节点ID
            context_depth: 上下文深度（相关节点的层数）
            
        Returns:
            生成的边（如果评估通过），否则None
        """
        print(f"\n{'='*70}")
        print(f"讨论节点对: [{physics_node_id}] ↔ [{math_node_id}]")
        print(f"{'='*70}\n")
        
        # 验证节点存在
        if physics_node_id not in self.physics_nodes:
            print(f"✗ 物理节点不存在: {physics_node_id}")
            return None
        if math_node_id not in self.math_nodes:
            print(f"✗ 数学节点不存在: {math_node_id}")
            return None
        
        # 获取节点信息
        physics_node = self.physics_nodes[physics_node_id]
        math_node = self.math_nodes[math_node_id]
        
        # 构建学科内上下文
        physics_context = self._build_node_context(
            physics_node_id,
            self.physics_nodes,
            self.physics_edges,
            depth=context_depth
        )
        
        math_context = self._build_node_context(
            math_node_id,
            self.math_nodes,
            self.math_edges,
            depth=context_depth
        )
        
        # 物理agent发言
        print(f"[{self.physics_agent.name}] 正在分析物理节点...")
        physics_response = self._agent_discuss_node(
            self.physics_agent,
            physics_node,
            physics_context,
            math_node,
            "physics"
        )
        print(f"[{self.physics_agent.name}]: {physics_response[:300]}...\n")
        
        # 数学agent发言
        print(f"[{self.math_agent.name}] 正在分析数学节点...")
        math_response = self._agent_discuss_node(
            self.math_agent,
            math_node,
            math_context,
            physics_node,
            "math",
            other_response=physics_response
        )
        print(f"[{self.math_agent.name}]: {math_response[:300]}...\n")
        
        # 检查是否偏离
        if self._is_off_topic(physics_response, math_response, physics_node_id, math_node_id):
            print(f"[{self.meta_agent.name}] 检测到讨论偏离，进行矫正...")
            correction = self._correct_discussion(
                physics_node,
                math_node,
                physics_response,
                math_response
            )
            print(f"[{self.meta_agent.name}]: {correction[:200]}...\n")
            
            # 可以选择重新讨论，这里简化为跳过
            return None
        else:
            print(f"[{self.meta_agent.name}] 讨论聚焦良好\n")
        
        # 提取边
        edge = self._extract_edge(
            physics_node_id,
            math_node_id,
            physics_response,
            math_response
        )
        
        if not edge:
            print("✗ 未能从讨论中提取有效的边\n")
            return None
        
        # 评估边
        print(f"[{self.evaluator.name}] 正在评估边...")
        is_valid, reason = self._evaluate_edge(edge)
        
        if is_valid:
            print(f"[{self.evaluator.name}] ✓ 边评估通过: {reason}\n")
            
            # 写入文件
            self._write_edge_to_file(edge)
            
            return edge
        else:
            print(f"[{self.evaluator.name}] ✗ 边被拒绝: {reason}\n")
            return None
    
    def _build_node_context(
        self,
        node_id: str,
        nodes_dict: Dict[str, Dict],
        edges_dict: Dict[str, List[str]],
        depth: int = 1
    ) -> str:
        """构建节点的学科内上下文"""
        context = f"# 核心节点\n\n"
        
        # 核心节点信息
        node = nodes_dict[node_id]
        context += f"**[{node_id}]** {node.get('label', '')}\n\n"
        
        # 输出完整的properties
        properties = node.get('properties', {})
        if properties:
            context += "**属性信息**：\n"
            for key, value in properties.items():
                if isinstance(value, str):
                    context += f"- {key}: {value}\n"
                elif isinstance(value, list):
                    context += f"- {key}: {', '.join(str(v) for v in value)}\n"
                else:
                    context += f"- {key}: {value}\n"
            context += "\n"
        
        # 相关节点
        related_ids = self._get_related_nodes(node_id, edges_dict, depth)
        
        if related_ids:
            context += f"## 相关节点（学科内）\n\n"
            for related_id in related_ids[:10]:  # 最多10个
                if related_id in nodes_dict:
                    related = nodes_dict[related_id]
                    context += f"- **[{related_id}]** {related.get('label', '')}\n"
                    
                    # 相关节点也显示完整properties
                    related_props = related.get('properties', {})
                    if 'description' in related_props:
                        desc = related_props['description']
                        context += f"  描述: {desc[:150]}...\n"
                    
                    # 显示其他关键属性
                    for key in ['category', 'theme', 'cultivated_abilities']:
                        if key in related_props:
                            value = related_props[key]
                            if isinstance(value, list):
                                context += f"  {key}: {', '.join(str(v) for v in value)}\n"
                            else:
                                context += f"  {key}: {value}\n"
                    context += "\n"
        
        return context
    
    def _get_related_nodes(
        self,
        node_id: str,
        edges_dict: Dict[str, List[str]],
        depth: int
    ) -> List[str]:
        """获取相关节点（BFS）"""
        if depth <= 0:
            return []
        
        visited = {node_id}
        current_level = [node_id]
        related = []
        
        for _ in range(depth):
            next_level = []
            for current_id in current_level:
                neighbors = edges_dict.get(current_id, [])
                for neighbor in neighbors:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        related.append(neighbor)
                        next_level.append(neighbor)
            
            current_level = next_level
            if not current_level:
                break
        
        return related
    
    def _agent_discuss_node(
        self,
        agent: Agent,
        main_node: Dict,
        context: str,
        other_node: Dict,
        perspective: str,
        other_response: str = ""
    ) -> str:
        """让agent讨论节点"""
        prompt = f"""
# 你的知识背景

{context}

# 对方的知识节点

**[{other_node['id']}]** {other_node.get('label', '')}
{other_node.get('properties', {}).get('description', '')}

"""
        
        if other_response:
            prompt += f"""
# 对方的观点

{other_response}

"""
        
        prompt += f"""
# 任务

请从{perspective}的角度，分析：

1. 你的核心节点 [{main_node['id']}] 与对方的节点 [{other_node['id']}] 是否有内在联系？
2. 如果有联系，是什么类型的联系？（依赖、支撑、类比、应用等）
3. 结合你的学科内相关知识，说明这种联系的具体体现

要求：
- 必须基于具体的知识内容，不要空谈
- 明确引用节点ID（用方括号，如 [{main_node['id']}]）
- 如果认为没有明显联系，也要说明理由

"""
        
        return agent.client.generate(prompt, agent.system_instruction)
    
    def _is_off_topic(
        self,
        physics_response: str,
        math_response: str,
        physics_node_id: str,
        math_node_id: str
    ) -> bool:
        """检查是否偏离主题"""
        # 检查是否提到核心节点
        physics_mentioned = physics_node_id in physics_response
        math_mentioned = math_node_id in math_response
        
        if not physics_mentioned or not math_mentioned:
            return True
        
        # 检查讨论长度（太短可能是敷衍）
        if len(physics_response) < 100 or len(math_response) < 100:
            return True
        
        return False
    
    def _correct_discussion(
        self,
        physics_node: Dict,
        math_node: Dict,
        physics_response: str,
        math_response: str
    ) -> str:
        """矫正讨论"""
        prompt = f"""
正在讨论的节点对：
- 物理: [{physics_node['id']}] {physics_node.get('label', '')}
- 数学: [{math_node['id']}] {math_node.get('label', '')}

物理专家的发言：
{physics_response}

数学专家的发言：
{math_response}

问题：讨论似乎偏离了这两个具体节点。

请用1-2句话提醒专家们聚焦在这两个节点的关联上。
"""
        
        return self.meta_agent.client.generate(prompt, self.meta_agent.system_instruction)
    
    def _extract_edge(
        self,
        physics_node_id: str,
        math_node_id: str,
        physics_response: str,
        math_response: str
    ) -> Optional[Dict[str, Any]]:
        """从讨论中提取边"""
        prompt = f"""
物理专家关于 [{physics_node_id}] 的观点：
{physics_response}

数学专家关于 [{math_node_id}] 的观点：
{math_response}

请判断这两个节点之间是否存在跨学科关联。

如果存在，返回JSON格式（只返回JSON，不要其他内容）：
{{
  "source": "{physics_node_id}",
  "target": "{math_node_id}",
  "label": "关系类型（如 requires, models, analogous_to 等）",
  "properties": {{
    "description": "关系的简洁描述（1-2句话）",
    "reasoning": "发现此关联的理由",
    "confidence": 0.0到1.0之间的数值
  }}
}}

如果不存在明显关联，返回：
{{"exists": false}}
"""
        
        try:
            response = self.meta_agent.client.generate(prompt, self.meta_agent.system_instruction)
            
            # 提取JSON
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                edge_data = json.loads(json_match.group())
                
                # 检查是否标记为不存在
                if edge_data.get('exists') == False:
                    return None
                
                # 验证必需字段
                if all(k in edge_data for k in ['source', 'target', 'label', 'properties']):
                    return edge_data
        
        except Exception as e:
            print(f"提取边时出错：{e}")
        
        return None
    
    def _evaluate_edge(self, edge: Dict[str, Any]) -> tuple[bool, str]:
        """
        评估边是否应该保留
        
        Returns:
            (是否保留, 理由)
        """
        prompt = f"""
评估以下跨学科关联边：

源节点（物理）: {edge['source']}
目标节点（数学）: {edge['target']}
关系类型: {edge['label']}
描述: {edge['properties']['description']}
理由: {edge['properties']['reasoning']}
置信度: {edge['properties']['confidence']}

请评估这条边是否应该保留。判断标准：

1. 关联是否合理且有意义
2. 描述是否清晰
3. 置信度是否足够（建议≥0.6）
4. 是否是真实的跨学科知识关联

返回JSON格式：
{{
  "valid": true/false,
  "reason": "保留或拒绝的理由（1句话）"
}}
"""
        
        try:
            response = self.evaluator.client.generate(prompt, self.evaluator.system_instruction)
            
            # 提取JSON
            json_match = re.search(r'\{[\s\S]*?\}', response)
            if json_match:
                result = json.loads(json_match.group())
                return result.get('valid', False), result.get('reason', '')
        
        except Exception as e:
            print(f"评估时出错：{e}")
        
        # 默认拒绝
        return False, "评估失败"
    
    def _write_edge_to_file(self, edge: Dict[str, Any]):
        """通过function call写入边到JSON文件"""
        add_edge_to_json(str(self.output_file), edge)
        print(f"✓ 边已写入文件: {self.output_file}\n")
    
    def batch_discuss(
        self,
        node_pairs: List[tuple[str, str]],
        context_depth: int = 1
    ) -> List[Dict[str, Any]]:
        """
        批量讨论多对节点
        
        Args:
            node_pairs: 节点对列表 [(physics_id, math_id), ...]
            context_depth: 上下文深度
            
        Returns:
            生成并保留的边列表
        """
        print(f"\n{'='*70}")
        print(f"批量讨论 {len(node_pairs)} 对节点")
        print(f"{'='*70}\n")
        
        valid_edges = []
        
        for i, (physics_id, math_id) in enumerate(node_pairs, 1):
            print(f"\n进度: {i}/{len(node_pairs)}")
            
            edge = self.discuss_node_pair(physics_id, math_id, context_depth)
            
            if edge:
                valid_edges.append(edge)
        
        print(f"\n{'='*70}")
        print(f"完成！生成并保留了 {len(valid_edges)}/{len(node_pairs)} 条边")
        print(f"{'='*70}\n")
        
        return valid_edges


# Function Call 接口

def write_edge_json(file_path: str, data: Dict[str, Any]) -> None:
    """
    写入边的JSON文件
    
    Args:
        file_path: 文件路径
        data: 数据
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_edge_to_json(file_path: str, edge: Dict[str, Any]) -> None:
    """
    向JSON文件添加一条边
    
    Args:
        file_path: 文件路径
        edge: 边数据
    """
    # 读取现有数据
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 添加边
    data['edges'].append(edge)
    data['metadata']['total_edges'] = len(data['edges'])
    data['metadata']['last_updated'] = datetime.now().isoformat()
    
    # 写回
    write_edge_json(file_path, data)


if __name__ == "__main__":
    print("Node Pair Chatroom module loaded")

