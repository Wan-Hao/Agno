"""
科研聊天室核心类
"""
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
from core.agent import Agent
from core.edge import KnowledgeEdge
from agents.meta_agent import MetaAgent
from agents.evaluator_agent import EvaluatorAgent
from processors import (
    TextProcessor,
    PDFProcessor,
    ImageProcessor,
    AudioProcessor,
    VideoProcessor,
    WebProcessor
)
import json
from datetime import datetime
from config import Config


class ResearchChatroom:
    """
    科研聊天室
    
    多智能体协同对话系统，用于跨学科知识关联发现
    """
    
    def __init__(
        self,
        topic: str,
        agents: List[Agent],
        meta_agent: Optional[MetaAgent] = None,
        evaluator: Optional[EvaluatorAgent] = None
    ):
        """
        初始化科研聊天室
        
        Args:
            topic: 讨论主题
            agents: 参与讨论的智能体列表
            meta_agent: 元协调智能体（可选）
            evaluator: 评估智能体（可选）
        """
        self.topic = topic
        self.agents = agents
        self.meta_agent = meta_agent or MetaAgent()
        self.evaluator = evaluator or EvaluatorAgent()
        
        # 讨论历史
        self.discussion_history: List[Dict[str, Any]] = []
        
        # 发现的知识边
        self.edges: List[KnowledgeEdge] = []
        
        # 处理器
        self.processors = {
            "text": TextProcessor(),
            "pdf": PDFProcessor(),
            "image": ImageProcessor(),
            "audio": AudioProcessor(),
            "video": VideoProcessor(),
            "web": WebProcessor()
        }
        
        print(f"✓ 科研聊天室已创建")
        print(f"  主题: {self.topic}")
        print(f"  参与者: {', '.join([a.name for a in self.agents])}")
    
    def load_data(
        self,
        agent_name: str,
        data_source: Union[str, Path],
        data_type: Optional[str] = None
    ) -> bool:
        """
        为指定智能体加载数据
        
        Args:
            agent_name: 智能体名称
            data_source: 数据源（文件路径或URL）
            data_type: 数据类型（text/pdf/image/audio/video/web），如果为None则自动检测
            
        Returns:
            是否加载成功
        """
        # 查找智能体
        agent = self._find_agent(agent_name)
        if not agent:
            print(f"✗ 未找到智能体: {agent_name}")
            return False
        
        # 自动检测数据类型
        if data_type is None:
            data_type = self._detect_data_type(data_source)
        
        try:
            # 处理数据
            processor = self.processors.get(data_type)
            if not processor:
                print(f"✗ 不支持的数据类型: {data_type}")
                return False
            
            if data_type == "web":
                processed_data = processor.process(str(data_source))
            else:
                processed_data = processor.process(Path(data_source))
            
            # 加载到智能体
            agent.load_knowledge(
                data=processed_data,
                data_type=data_type,
                source=str(data_source)
            )
            
            print(f"✓ 已为 {agent_name} 加载 {data_type} 数据: {data_source}")
            return True
        
        except Exception as e:
            print(f"✗ 加载数据失败: {e}")
            return False
    
    def discuss(
        self,
        rounds: int = 3,
        extract_edges: bool = True,
        evaluate_edges: bool = True
    ) -> List[KnowledgeEdge]:
        """
        开始讨论
        
        Args:
            rounds: 讨论轮次
            extract_edges: 是否提取知识边
            evaluate_edges: 是否评估知识边
            
        Returns:
            发现的知识边列表
        """
        print(f"\n{'='*60}")
        print(f"开始讨论: {self.topic}")
        print(f"{'='*60}\n")
        
        context = ""
        
        for round_num in range(1, rounds + 1):
            print(f"\n--- 第 {round_num} 轮讨论 ---\n")
            
            # 每个智能体发言
            agent_responses = {}
            for agent in self.agents:
                print(f"[{agent.name}] 正在思考...")
                response = agent.discuss(self.topic, context)
                agent_responses[agent.name] = response
                
                # 记录历史
                self.discussion_history.append({
                    "round": round_num,
                    "agent": agent.name,
                    "domain": agent.domain,
                    "content": response,
                    "timestamp": datetime.now().isoformat()
                })
                
                print(f"[{agent.name}]: {response[:200]}...\n")
            
            # 元协调者主持
            print(f"[{self.meta_agent.name}] 正在总结...")
            moderation = self.meta_agent.moderate_discussion(
                self.topic,
                agent_responses
            )
            print(f"[{self.meta_agent.name}]: {moderation[:200]}...\n")
            
            # 更新上下文
            context = f"上一轮讨论总结：\n{moderation}\n"
            
            # 记录元协调者发言
            self.discussion_history.append({
                "round": round_num,
                "agent": self.meta_agent.name,
                "domain": self.meta_agent.domain,
                "content": moderation,
                "timestamp": datetime.now().isoformat()
            })
        
        # 提取知识边
        if extract_edges:
            print(f"\n[{self.meta_agent.name}] 正在提取知识关联...")
            self.edges = self.meta_agent.extract_edges(
                self.topic,
                self.discussion_history
            )
            print(f"✓ 发现 {len(self.edges)} 个潜在的跨领域关联\n")
        
        # 评估知识边
        if evaluate_edges and self.edges:
            print(f"[{self.evaluator.name}] 正在评估关联质量...")
            for edge in self.edges:
                self.evaluator.evaluate_edge(edge)
            print(f"✓ 评估完成\n")
        
        # 显示结果
        self._display_edges()
        
        return self.edges
    
    def export_knowledge_graph(
        self,
        output_path: Union[str, Path],
        include_metadata: bool = True
    ) -> bool:
        """
        导出知识图谱（通过 Function Call 接口）
        
        Args:
            output_path: 输出文件路径
            include_metadata: 是否包含元数据
            
        Returns:
            是否导出成功
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # 使用 Function Call 写入数据
            graph_data = self._build_graph_data(include_metadata)
            
            # 调用写入函数
            write_knowledge_graph(str(output_path), graph_data)
            
            print(f"✓ 知识图谱已导出: {output_path}")
            return True
        
        except Exception as e:
            print(f"✗ 导出失败: {e}")
            return False
    
    def export_discussion_log(
        self,
        output_path: Union[str, Path]
    ) -> bool:
        """
        导出讨论记录
        
        Args:
            output_path: 输出文件路径
            
        Returns:
            是否导出成功
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            log_data = {
                "topic": self.topic,
                "agents": [
                    {
                        "name": agent.name,
                        "domain": agent.domain,
                        "expertise": agent.expertise
                    }
                    for agent in self.agents
                ],
                "discussion_history": self.discussion_history,
                "export_time": datetime.now().isoformat()
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, ensure_ascii=False, indent=2)
            
            print(f"✓ 讨论记录已导出: {output_path}")
            return True
        
        except Exception as e:
            print(f"✗ 导出失败: {e}")
            return False
    
    def generate_report(self) -> str:
        """
        生成综合报告
        
        Returns:
            报告文本
        """
        # 评估结果
        eval_results = []
        for edge in self.edges:
            eval_results.append(self.evaluator.evaluate_edge(edge, include_reasoning=True))
        
        # 生成评估报告
        eval_report = self.evaluator.generate_evaluation_report(
            self.edges,
            eval_results
        )
        
        # 生成综合洞见
        insights = self.meta_agent.synthesize_insights(
            self.topic,
            self.edges
        )
        
        # 组合报告
        report = f"# 科研聊天室综合报告\n\n"
        report += f"**主题**: {self.topic}\n\n"
        report += f"**参与者**: {', '.join([a.name for a in self.agents])}\n\n"
        report += f"**讨论轮次**: {max([h.get('round', 0) for h in self.discussion_history])}\n\n"
        report += f"**发现的关联数**: {len(self.edges)}\n\n"
        report += "---\n\n"
        report += "## 综合洞见\n\n"
        report += insights + "\n\n"
        report += "---\n\n"
        report += eval_report
        
        return report
    
    def _find_agent(self, agent_name: str) -> Optional[Agent]:
        """查找智能体"""
        for agent in self.agents:
            if agent.name == agent_name or agent.domain == agent_name:
                return agent
        return None
    
    def _detect_data_type(self, data_source: Union[str, Path]) -> str:
        """自动检测数据类型"""
        data_str = str(data_source)
        
        # 检查是否是 URL
        if data_str.startswith("http://") or data_str.startswith("https://"):
            return "web"
        
        # 检查文件扩展名
        path = Path(data_source)
        suffix = path.suffix.lower()
        
        if suffix in ['.txt', '.md']:
            return "text"
        elif suffix in ['.pdf']:
            return "pdf"
        elif suffix in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            return "image"
        elif suffix in ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a']:
            return "audio"
        elif suffix in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']:
            return "video"
        else:
            return "text"  # 默认为文本
    
    def _build_graph_data(self, include_metadata: bool = True) -> Dict[str, Any]:
        """构建知识图谱数据"""
        nodes = []
        edges_data = []
        
        # 收集所有节点
        domains = set()
        for edge in self.edges:
            domains.add(edge.source_domain)
            domains.add(edge.target_domain)
        
        # 构建节点
        for domain in domains:
            nodes.append({
                "id": domain,
                "label": domain,
                "type": "domain"
            })
        
        # 构建边
        for edge in self.edges:
            edges_data.append(edge.to_dict())
        
        graph_data = {
            "topic": self.topic,
            "nodes": nodes,
            "edges": edges_data,
            "statistics": {
                "num_edges": len(self.edges),
                "num_domains": len(domains),
                "avg_confidence": sum([e.confidence for e in self.edges]) / len(self.edges) if self.edges else 0
            }
        }
        
        if include_metadata:
            graph_data["metadata"] = {
                "generated_at": datetime.now().isoformat(),
                "agents": [a.name for a in self.agents],
                "discussion_rounds": max([h.get('round', 0) for h in self.discussion_history])
            }
        
        return graph_data
    
    def _display_edges(self):
        """显示发现的知识边"""
        if not self.edges:
            print("未发现跨领域关联")
            return
        
        print(f"\n{'='*60}")
        print(f"发现的跨领域知识关联")
        print(f"{'='*60}\n")
        
        for i, edge in enumerate(self.edges, 1):
            print(f"{i}. {edge}")
            print(f"   描述: {edge.relation_description[:100]}...")
            if edge.semantic_similarity:
                print(f"   语义相似度: {edge.semantic_similarity:.2f}")
            if edge.novelty_score:
                print(f"   新颖度: {edge.novelty_score:.2f}")
            print()


# Function Call 接口
def write_knowledge_graph(file_path: str, graph_data: Dict[str, Any]) -> None:
    """
    写入知识图谱数据（Function Call 接口）
    
    这是一个标准化的写入接口，确保数据格式的一致性
    
    Args:
        file_path: 输出文件路径
        graph_data: 图谱数据
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)


def add_edge_to_graph(
    file_path: str,
    edge_data: Dict[str, Any]
) -> None:
    """
    向已有图谱添加边（Function Call 接口）
    
    Args:
        file_path: 图谱文件路径
        edge_data: 边数据
    """
    # 读取现有数据
    with open(file_path, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)
    
    # 添加边
    graph_data["edges"].append(edge_data)
    graph_data["statistics"]["num_edges"] = len(graph_data["edges"])
    
    # 写回
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)


class StrictKnowledgeGraphChatroom:
    """
    严格的知识图谱驱动聊天室
    
    特点：
    1. 讨论必须基于图谱中实际存在的节点ID
    2. 协调者更克制，只在真正偏离时介入
    3. 输出纯边的JSON（节点ID之间的连接）
    """
    
    def __init__(
        self,
        topic: str,
        agents: List[Agent],
        physics_graph: Dict[str, Any],
        math_graph: Dict[str, Any],
        meta_agent: Optional[MetaAgent] = None
    ):
        """
        初始化严格知识图谱聊天室
        
        Args:
            topic: 讨论主题
            agents: 智能体列表（应包含物理和数学专家）
            physics_graph: 物理知识图谱
            math_graph: 数学知识图谱
            meta_agent: 元协调者（可选）
        """
        self.topic = topic
        self.agents = agents
        self.meta_agent = meta_agent or MetaAgent()
        
        # 知识图谱
        self.physics_graph = physics_graph
        self.math_graph = math_graph
        
        # 构建节点索引
        self.physics_nodes = {n['id']: n for n in physics_graph.get('nodes', [])}
        self.math_nodes = {n['id']: n for n in math_graph.get('nodes', [])}
        
        # 讨论历史
        self.discussion_history: List[Dict[str, Any]] = []
        
        # 发现的边
        self.discovered_edges: List[Dict[str, Any]] = []
        
        print(f"✓ 严格知识图谱聊天室已创建")
        print(f"  主题: {self.topic}")
        print(f"  物理节点: {len(self.physics_nodes)}")
        print(f"  数学节点: {len(self.math_nodes)}")
    
    def discuss(
        self,
        rounds: int = 5,
        focus_themes: Dict[str, List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        开始基于节点的讨论
        
        Args:
            rounds: 讨论轮次
            focus_themes: 关注的主题 {"physics": [...], "math": [...]}
            
        Returns:
            发现的边列表
        """
        print(f"\n{'='*60}")
        print(f"开始基于节点的讨论: {self.topic}")
        print(f"{'='*60}\n")
        
        # 筛选节点
        physics_focus_nodes = self._filter_nodes_by_themes(
            self.physics_nodes,
            focus_themes.get("physics", []) if focus_themes else []
        )
        math_focus_nodes = self._filter_nodes_by_themes(
            self.math_nodes,
            focus_themes.get("math", []) if focus_themes else []
        )
        
        print(f"关注范围：")
        print(f"  物理节点: {len(physics_focus_nodes)}")
        print(f"  数学节点: {len(math_focus_nodes)}")
        print()
        
        # 为智能体提供节点列表
        context = self._build_node_context(physics_focus_nodes, math_focus_nodes)
        
        for round_num in range(1, rounds + 1):
            print(f"\n--- 第 {round_num} 轮讨论 ---\n")
            
            # 物理专家
            physics_agent = self._find_agent_by_domain("物理")
            if physics_agent:
                print(f"[{physics_agent.name}] 正在分析物理节点...")
                physics_response = self._agent_discuss_nodes(
                    physics_agent,
                    physics_focus_nodes,
                    context,
                    "请从物理学角度，选择3-5个你认为可能与数学概念有联系的物理节点（请引用节点ID），并说明你认为它们可能关联到哪些数学概念。"
                )
                self._record_discussion(round_num, physics_agent, physics_response)
                print(f"[{physics_agent.name}]: {physics_response[:300]}...\n")
            
            # 数学专家
            math_agent = self._find_agent_by_domain("数学")
            if math_agent:
                print(f"[{math_agent.name}] 正在分析数学节点...")
                math_response = self._agent_discuss_nodes(
                    math_agent,
                    math_focus_nodes,
                    context + "\n\n物理专家的观点：\n" + physics_response,
                    "请从数学角度，选择3-5个你认为可能与物理概念有联系的数学节点（请引用节点ID），并回应物理专家的观点。"
                )
                self._record_discussion(round_num, math_agent, math_response)
                print(f"[{math_agent.name}]: {math_response[:300]}...\n")
            
            # 协调者检查是否偏离
            should_moderate = self._check_if_off_topic(physics_response, math_response)
            
            if should_moderate:
                print(f"[{self.meta_agent.name}] 检测到讨论偏离，进行引导...")
                moderation = self._moderate_and_guide(
                    round_num,
                    physics_response,
                    math_response,
                    physics_focus_nodes,
                    math_focus_nodes
                )
                print(f"[{self.meta_agent.name}]: {moderation[:200]}...\n")
                context += f"\n\n协调者提示：{moderation}\n"
            else:
                print(f"[{self.meta_agent.name}] 讨论进展良好，继续...\n")
            
            # 更新上下文
            context = self._update_context(physics_response, math_response)
        
        # 提取边
        print(f"\n[{self.meta_agent.name}] 正在提取节点间的关联边...")
        self.discovered_edges = self._extract_edges_from_discussion()
        print(f"✓ 发现 {len(self.discovered_edges)} 条跨学科边\n")
        
        return self.discovered_edges
    
    def _filter_nodes_by_themes(
        self,
        nodes_dict: Dict[str, Dict],
        themes: List[str]
    ) -> List[Dict[str, Any]]:
        """根据主题筛选节点"""
        if not themes:
            return list(nodes_dict.values())[:30]  # 默认返回前30个
        
        filtered = []
        for node in nodes_dict.values():
            props = node.get('properties', {})
            node_theme = props.get('theme', '')
            node_category = props.get('category', '')
            
            if any(theme in node_theme or theme in node_category for theme in themes):
                filtered.append(node)
        
        return filtered[:50]  # 最多50个节点
    
    def _build_node_context(
        self,
        physics_nodes: List[Dict],
        math_nodes: List[Dict]
    ) -> str:
        """构建节点上下文"""
        context = "# 可用的知识节点\n\n"
        context += "## 物理知识节点\n\n"
        
        for node in physics_nodes[:20]:
            node_id = node['id']
            label = node.get('label', '')
            desc = node.get('properties', {}).get('description', '')
            context += f"- **[{node_id}]** {label}\n"
            context += f"  {desc[:150]}...\n\n"
        
        context += "\n## 数学知识节点\n\n"
        
        for node in math_nodes[:20]:
            node_id = node['id']
            label = node.get('label', '')
            desc = node.get('properties', {}).get('description', '')
            context += f"- **[{node_id}]** {label}\n"
            context += f"  {desc[:150]}...\n\n"
        
        return context
    
    def _agent_discuss_nodes(
        self,
        agent: Agent,
        available_nodes: List[Dict],
        context: str,
        specific_instruction: str
    ) -> str:
        """让智能体基于节点进行讨论"""
        prompt = f"""
{context}

任务：{specific_instruction}

重要规则：
1. 必须引用具体的节点ID（用方括号包裹，如[node_id]）
2. 每个观点都要锚定在具体节点上
3. 不要空谈抽象概念，要基于图谱中的实际知识点

请基于以上节点，提出你的观点。
"""
        return agent.client.generate(prompt, agent.system_instruction)
    
    def _check_if_off_topic(
        self,
        physics_response: str,
        math_response: str
    ) -> bool:
        """检查讨论是否偏离节点"""
        # 检查是否引用了节点ID
        import re
        
        physics_node_refs = re.findall(r'\[([a-z_0-9]+)\]', physics_response)
        math_node_refs = re.findall(r'\[([a-z_0-9]+)\]', math_response)
        
        # 如果引用的节点ID少于2个，认为偏离
        if len(physics_node_refs) < 2 or len(math_node_refs) < 2:
            return True
        
        # 检查引用的节点是否存在
        valid_physics = sum(1 for nid in physics_node_refs if nid in self.physics_nodes)
        valid_math = sum(1 for nid in math_node_refs if nid in self.math_nodes)
        
        if valid_physics < 2 or valid_math < 2:
            return True
        
        return False
    
    def _moderate_and_guide(
        self,
        round_num: int,
        physics_response: str,
        math_response: str,
        physics_nodes: List[Dict],
        math_nodes: List[Dict]
    ) -> str:
        """协调者引导讨论回到节点"""
        prompt = f"""
讨论轮次: {round_num}

物理专家的发言：
{physics_response}

数学专家的发言：
{math_response}

问题：讨论似乎偏离了具体的知识节点，或引用的节点ID不足。

请提醒专家们：
1. 必须引用具体的节点ID
2. 基于图谱中的实际知识点讨论
3. 指出一些可能被忽略但重要的节点

请简短地（不超过3句话）引导讨论回到正轨。
"""
        return self.meta_agent.client.generate(prompt, self.meta_agent.system_instruction)
    
    def _update_context(
        self,
        physics_response: str,
        math_response: str
    ) -> str:
        """更新上下文"""
        return f"""
上一轮讨论摘要：

物理视角：
{physics_response[:500]}

数学视角：
{math_response[:500]}

请在此基础上继续深入探讨节点间的联系。
"""
    
    def _extract_edges_from_discussion(self) -> List[Dict[str, Any]]:
        """从讨论中提取边"""
        # 构建讨论历史文本
        discussion_text = ""
        for turn in self.discussion_history:
            discussion_text += f"\n[{turn['agent']}]: {turn['content']}\n"
        
        # 请求元协调者提取边
        prompt = f"""
以下是物理和数学专家的讨论记录：

{discussion_text}

请提取所有明确的跨学科知识关联。对于每条边，提供：

1. source: 源节点ID（必须是物理图谱中的实际节点ID）
2. target: 目标节点ID（必须是数学图谱中的实际节点ID）
3. label: 关系类型（如 "mathematical_foundation_of", "models", "analogous_to" 等）
4. properties:
   - description: 关系描述
   - reasoning: 发现此关联的理由
   - confidence: 0-1之间的置信度

返回JSON数组格式：
[
  {{
    "source": "physics_node_id",
    "target": "math_node_id",
    "label": "relation_type",
    "properties": {{
      "description": "...",
      "reasoning": "...",
      "confidence": 0.85
    }}
  }},
  ...
]

重要：source和target必须是讨论中实际引用的节点ID！
"""
        
        try:
            response = self.meta_agent.client.generate(prompt, self.meta_agent.system_instruction)
            
            # 提取JSON
            import re
            json_match = re.search(r'\[[\s\S]*\]', response)
            if json_match:
                edges_data = json.loads(json_match.group())
                
                # 验证节点ID
                validated_edges = []
                for edge in edges_data:
                    source_id = edge.get('source', '')
                    target_id = edge.get('target', '')
                    
                    # 检查节点是否存在
                    if source_id in self.physics_nodes and target_id in self.math_nodes:
                        validated_edges.append(edge)
                    elif source_id in self.math_nodes and target_id in self.physics_nodes:
                        # 交换方向
                        validated_edges.append({
                            'source': target_id,
                            'target': source_id,
                            'label': edge.get('label', ''),
                            'properties': edge.get('properties', {})
                        })
                    else:
                        print(f"警告：跳过无效边 {source_id} -> {target_id}")
                
                return validated_edges
            
        except Exception as e:
            print(f"提取边时出错：{e}")
        
        return []
    
    def _find_agent_by_domain(self, domain_keyword: str) -> Optional[Agent]:
        """根据领域关键词查找智能体"""
        for agent in self.agents:
            if domain_keyword in agent.domain or domain_keyword in agent.name:
                return agent
        return None
    
    def _record_discussion(
        self,
        round_num: int,
        agent: Agent,
        content: str
    ):
        """记录讨论"""
        self.discussion_history.append({
            "round": round_num,
            "agent": agent.name,
            "domain": agent.domain,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def export_discussion_log(self, output_path: Path) -> bool:
        """导出讨论日志"""
        try:
            log_data = {
                "topic": self.topic,
                "discussion_history": self.discussion_history,
                "export_time": datetime.now().isoformat()
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, ensure_ascii=False, indent=2)
            
            print(f"✓ 讨论日志已导出: {output_path}")
            return True
        except Exception as e:
            print(f"✗ 导出失败: {e}")
            return False
    
    def get_timestamp(self) -> str:
        """获取时间戳"""
        return datetime.now().isoformat()


if __name__ == "__main__":
    print("Research Chatroom module loaded successfully")

