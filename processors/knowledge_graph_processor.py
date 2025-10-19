"""
知识图谱数据处理器
"""
from pathlib import Path
from typing import Dict, Any, List
import json


class KnowledgeGraphProcessor:
    """知识图谱数据处理器"""
    
    @staticmethod
    def process(file_path: Path) -> Dict[str, Any]:
        """
        处理知识图谱文件
        
        Args:
            file_path: 知识图谱JSON文件路径
            
        Returns:
            处理后的数据字典
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Knowledge graph file not found: {file_path}")
        
        # 读取知识图谱
        with open(file_path, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)
        
        # 提取节点和边
        nodes = graph_data.get("nodes", [])
        edges = graph_data.get("edges", [])
        
        # 构建摘要信息
        summary = KnowledgeGraphProcessor._build_summary(nodes, edges)
        
        # 提取关键概念
        key_concepts = KnowledgeGraphProcessor._extract_key_concepts(nodes, limit=50)
        
        return {
            "type": "knowledge_graph",
            "source": str(file_path),
            "content": summary,
            "nodes": nodes,
            "edges": edges,
            "key_concepts": key_concepts,
            "metadata": {
                "num_nodes": len(nodes),
                "num_edges": len(edges),
                "file_name": file_path.name,
                "file_size": file_path.stat().st_size
            }
        }
    
    @staticmethod
    def _build_summary(nodes: List[Dict], edges: List[Dict]) -> str:
        """
        构建知识图谱摘要
        
        Args:
            nodes: 节点列表
            edges: 边列表
            
        Returns:
            摘要文本
        """
        summary = f"知识图谱包含 {len(nodes)} 个概念节点和 {len(edges)} 个关系边。\n\n"
        
        # 提取主题分类
        themes = set()
        categories = set()
        for node in nodes:
            props = node.get("properties", {})
            if "theme" in props:
                themes.add(props["theme"])
            if "category" in props:
                categories.add(props["category"])
        
        if themes:
            summary += f"主要主题：{', '.join(list(themes)[:10])}\n"
        if categories:
            summary += f"主要分类：{', '.join(list(categories)[:10])}\n"
        
        # 列举一些核心概念
        summary += "\n核心概念示例：\n"
        for i, node in enumerate(nodes[:20], 1):
            label = node.get("label", "未知")
            desc = node.get("properties", {}).get("description", "")
            desc_short = desc[:100] + "..." if len(desc) > 100 else desc
            summary += f"{i}. {label}: {desc_short}\n"
        
        if len(nodes) > 20:
            summary += f"... 还有 {len(nodes) - 20} 个概念\n"
        
        return summary
    
    @staticmethod
    def _extract_key_concepts(nodes: List[Dict], limit: int = 50) -> List[Dict[str, str]]:
        """
        提取关键概念
        
        Args:
            nodes: 节点列表
            limit: 提取数量限制
            
        Returns:
            关键概念列表
        """
        key_concepts = []
        
        for node in nodes[:limit]:
            concept = {
                "id": node.get("id", ""),
                "label": node.get("label", ""),
                "description": node.get("properties", {}).get("description", "")
            }
            key_concepts.append(concept)
        
        return key_concepts
    
    @staticmethod
    def get_concepts_by_theme(
        graph_data: Dict[str, Any],
        theme: str
    ) -> List[Dict[str, str]]:
        """
        根据主题筛选概念
        
        Args:
            graph_data: 知识图谱数据
            theme: 主题名称
            
        Returns:
            符合主题的概念列表
        """
        nodes = graph_data.get("nodes", [])
        concepts = []
        
        for node in nodes:
            props = node.get("properties", {})
            if props.get("theme") == theme or props.get("category") == theme:
                concepts.append({
                    "id": node.get("id", ""),
                    "label": node.get("label", ""),
                    "description": props.get("description", "")
                })
        
        return concepts
    
    @staticmethod
    def build_context_for_discussion(
        graph_data: Dict[str, Any],
        focus_themes: List[str] = None,
        max_concepts: int = 30
    ) -> str:
        """
        为讨论构建上下文
        
        Args:
            graph_data: 知识图谱数据
            focus_themes: 关注的主题列表
            max_concepts: 最大概念数量
            
        Returns:
            讨论上下文文本
        """
        nodes = graph_data.get("nodes", [])
        
        # 如果指定了主题，优先选择相关概念
        if focus_themes:
            selected_nodes = []
            for node in nodes:
                props = node.get("properties", {})
                theme = props.get("theme", "")
                category = props.get("category", "")
                if theme in focus_themes or category in focus_themes:
                    selected_nodes.append(node)
            
            # 如果找到的不够，补充其他节点
            if len(selected_nodes) < max_concepts:
                for node in nodes:
                    if node not in selected_nodes:
                        selected_nodes.append(node)
                        if len(selected_nodes) >= max_concepts:
                            break
        else:
            selected_nodes = nodes[:max_concepts]
        
        # 构建上下文
        context = "以下是知识图谱中的关键概念：\n\n"
        for i, node in enumerate(selected_nodes, 1):
            label = node.get("label", "未知")
            desc = node.get("properties", {}).get("description", "")
            context += f"{i}. **{label}**\n"
            context += f"   {desc}\n\n"
        
        return context


if __name__ == "__main__":
    # 测试知识图谱处理器
    print("Knowledge Graph Processor module loaded successfully")

