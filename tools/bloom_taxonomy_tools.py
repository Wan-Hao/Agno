"""
布鲁姆认知目标分类标注工具

包含：
1. 六个打标签工具（对应布鲁姆六个认知层级）
2. 知识点批量查看工具
"""

import json
from typing import List, Dict, Any, Optional
from pathlib import Path


# 布鲁姆认知层级定义
BLOOM_LEVELS = {
    "Remember": "记忆 - 识别和回忆相关知识",
    "Understand": "理解 - 理解材料的含义",
    "Apply": "应用 - 在新情境中使用信息",
    "Analyze": "分析 - 将信息分解为组成部分并理解关系",
    "Evaluate": "评价 - 基于标准做出判断",
    "Create": "创造 - 组合元素形成新的整体"
}


def load_knowledge_graph(file_path: str) -> Dict[str, Any]:
    """加载知识图谱JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_knowledge_graph(file_path: str, data: Dict[str, Any]) -> None:
    """保存知识图谱JSON文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def tag_knowledge_point_remember(node_id: str, file_path: str, reasoning: str = "") -> Dict[str, Any]:
    """
    给知识点打上"记忆"层级标签
    
    Args:
        node_id: 知识点ID
        file_path: JSON文件路径
        reasoning: 打标签的理由
        
    Returns:
        操作结果
    """
    return _tag_knowledge_point(node_id, file_path, "Remember", reasoning)


def tag_knowledge_point_understand(node_id: str, file_path: str, reasoning: str = "") -> Dict[str, Any]:
    """
    给知识点打上"理解"层级标签
    
    Args:
        node_id: 知识点ID
        file_path: JSON文件路径
        reasoning: 打标签的理由
        
    Returns:
        操作结果
    """
    return _tag_knowledge_point(node_id, file_path, "Understand", reasoning)


def tag_knowledge_point_apply(node_id: str, file_path: str, reasoning: str = "") -> Dict[str, Any]:
    """
    给知识点打上"应用"层级标签
    
    Args:
        node_id: 知识点ID
        file_path: JSON文件路径
        reasoning: 打标签的理由
        
    Returns:
        操作结果
    """
    return _tag_knowledge_point(node_id, file_path, "Apply", reasoning)


def tag_knowledge_point_analyze(node_id: str, file_path: str, reasoning: str = "") -> Dict[str, Any]:
    """
    给知识点打上"分析"层级标签
    
    Args:
        node_id: 知识点ID
        file_path: JSON文件路径
        reasoning: 打标签的理由
        
    Returns:
        操作结果
    """
    return _tag_knowledge_point(node_id, file_path, "Analyze", reasoning)


def tag_knowledge_point_evaluate(node_id: str, file_path: str, reasoning: str = "") -> Dict[str, Any]:
    """
    给知识点打上"评价"层级标签
    
    Args:
        node_id: 知识点ID
        file_path: JSON文件路径
        reasoning: 打标签的理由
        
    Returns:
        操作结果
    """
    return _tag_knowledge_point(node_id, file_path, "Evaluate", reasoning)


def tag_knowledge_point_create(node_id: str, file_path: str, reasoning: str = "") -> Dict[str, Any]:
    """
    给知识点打上"创造"层级标签
    
    Args:
        node_id: 知识点ID
        file_path: JSON文件路径
        reasoning: 打标签的理由
        
    Returns:
        操作结果
    """
    return _tag_knowledge_point(node_id, file_path, "Create", reasoning)


def _tag_knowledge_point(node_id: str, file_path: str, level: str, reasoning: str = "") -> Dict[str, Any]:
    """
    内部函数：给知识点打标签
    
    Args:
        node_id: 知识点ID
        file_path: JSON文件路径
        level: 布鲁姆认知层级
        reasoning: 打标签的理由
        
    Returns:
        操作结果
    """
    try:
        # 加载知识图谱
        data = load_knowledge_graph(file_path)
        
        # 查找知识点
        node_found = False
        for node in data.get("nodes", []):
            if node.get("id") == node_id:
                # 添加布鲁姆层级标签
                if "properties" not in node:
                    node["properties"] = {}
                node["properties"]["bloom_level"] = level
                if reasoning:
                    node["properties"]["bloom_reasoning"] = reasoning
                node_found = True
                break
        
        if not node_found:
            return {
                "success": False,
                "message": f"未找到ID为 {node_id} 的知识点",
                "node_id": node_id
            }
        
        # 保存知识图谱
        save_knowledge_graph(file_path, data)
        
        return {
            "success": True,
            "message": f"成功为知识点 {node_id} 打上 {level} 标签",
            "node_id": node_id,
            "level": level,
            "reasoning": reasoning
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"操作失败: {str(e)}",
            "node_id": node_id
        }


def get_knowledge_points(
    subject: str,
    page: int = 1,
    page_size: int = 10,
    dataset_dir: str = "dataset/graph"
) -> Dict[str, Any]:
    """
    批量获取知识点
    
    Args:
        subject: 科目名称 (如 "math", "physics")
        page: 页码（从1开始）
        page_size: 每页数量
        dataset_dir: 数据集目录路径
        
    Returns:
        知识点列表和分页信息
    """
    try:
        # 构建文件路径
        file_name = f"{subject}_knowledge_graph_new.json"
        file_path = Path(dataset_dir) / file_name
        
        if not file_path.exists():
            return {
                "success": False,
                "message": f"未找到科目 {subject} 的知识图谱文件: {file_path}",
                "subject": subject
            }
        
        # 加载知识图谱
        data = load_knowledge_graph(str(file_path))
        nodes = data.get("nodes", [])
        
        # 计算分页
        total = len(nodes)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        # 获取当前页的知识点
        page_nodes = nodes[start_idx:end_idx]
        
        return {
            "success": True,
            "subject": subject,
            "file_path": str(file_path),
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "nodes": page_nodes
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"操作失败: {str(e)}",
            "subject": subject
        }


def get_all_knowledge_points(subject: str, dataset_dir: str = "dataset/graph") -> Dict[str, Any]:
    """
    获取所有知识点（不分页）
    
    Args:
        subject: 科目名称 (如 "math", "physics")
        dataset_dir: 数据集目录路径
        
    Returns:
        所有知识点列表
    """
    try:
        # 构建文件路径
        file_name = f"{subject}_knowledge_graph_new.json"
        file_path = Path(dataset_dir) / file_name
        
        if not file_path.exists():
            return {
                "success": False,
                "message": f"未找到科目 {subject} 的知识图谱文件: {file_path}",
                "subject": subject
            }
        
        # 加载知识图谱
        data = load_knowledge_graph(str(file_path))
        nodes = data.get("nodes", [])
        
        return {
            "success": True,
            "subject": subject,
            "file_path": str(file_path),
            "total": len(nodes),
            "nodes": nodes
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"操作失败: {str(e)}",
            "subject": subject
        }


def get_tagging_progress(subject: str, dataset_dir: str = "dataset/graph") -> Dict[str, Any]:
    """
    获取标注进度统计
    
    Args:
        subject: 科目名称
        dataset_dir: 数据集目录路径
        
    Returns:
        标注进度统计信息
    """
    try:
        result = get_all_knowledge_points(subject, dataset_dir)
        
        if not result["success"]:
            return result
        
        nodes = result["nodes"]
        total = len(nodes)
        
        # 统计各层级数量
        level_counts = {level: 0 for level in BLOOM_LEVELS.keys()}
        tagged_count = 0
        
        for node in nodes:
            bloom_level = node.get("properties", {}).get("bloom_level")
            if bloom_level:
                tagged_count += 1
                if bloom_level in level_counts:
                    level_counts[bloom_level] += 1
        
        untagged_count = total - tagged_count
        
        return {
            "success": True,
            "subject": subject,
            "total": total,
            "tagged": tagged_count,
            "untagged": untagged_count,
            "progress_percentage": round(tagged_count / total * 100, 2) if total > 0 else 0,
            "level_distribution": level_counts
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"操作失败: {str(e)}",
            "subject": subject
        }


