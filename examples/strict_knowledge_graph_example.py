"""
严格基于知识图谱节点的跨学科讨论示例

特点：
1. 讨论严格围绕图谱中的具体节点ID展开
2. 协调者更克制，只在偏离时介入
3. 输出纯边的JSON（节点ID到节点ID）
"""
from core.chatroom import StrictKnowledgeGraphChatroom
from agents import PhysicsAgent, MathAgent
from processors import KnowledgeGraphProcessor
from config import Config
from pathlib import Path
import json


def main():
    """严格的知识图谱驱动对话"""
    # 验证配置
    try:
        Config.validate()
    except Exception as e:
        print(f"✗ 配置错误: {e}")
        print("请在 .env 文件中设置 GEMINI_API_KEY")
        return
    
    print("="*70)
    print("严格知识图谱模式：基于节点ID的跨学科关联发现")
    print("="*70)
    print()
    
    # 数据路径
    dataset_dir = Path(__file__).parent.parent / "dataset" / "graph"
    physics_graph_path = dataset_dir / "physics_knowledge_graph_new.json"
    math_graph_path = dataset_dir / "math_knowledge_graph_new.json"
    
    # 检查文件
    if not physics_graph_path.exists() or not math_graph_path.exists():
        print("✗ 知识图谱文件不存在")
        return
    
    print("📊 加载知识图谱数据...\n")
    
    # 加载图谱
    with open(physics_graph_path, 'r', encoding='utf-8') as f:
        physics_graph = json.load(f)
    with open(math_graph_path, 'r', encoding='utf-8') as f:
        math_graph = json.load(f)
    
    print(f"✓ 物理图谱: {len(physics_graph['nodes'])} 节点, {len(physics_graph['edges'])} 边")
    print(f"✓ 数学图谱: {len(math_graph['nodes'])} 节点, {len(math_graph['edges'])} 边")
    print()
    
    # 创建智能体
    physics_agent = PhysicsAgent()
    math_agent = MathAgent()
    
    # 创建严格知识图谱聊天室
    chatroom = StrictKnowledgeGraphChatroom(
        topic="发现物理学与数学知识点之间的内在联系",
        agents=[physics_agent, math_agent],
        physics_graph=physics_graph,
        math_graph=math_graph
    )
    
    # 开始讨论
    print("🎯 开始基于节点的跨学科讨论...\n")
    print("讨论规则：")
    print("  1. 每位专家必须引用具体的节点ID")
    print("  2. 协调者仅在讨论偏离时提示")
    print("  3. 输出边必须连接实际的节点ID")
    print()
    
    edges = chatroom.discuss(
        rounds=5,  # 5轮讨论
        focus_themes={
            "physics": ["机械运动与物理模型", "相互作用"],
            "math": ["函数", "集合"]
        }
    )
    
    # 输出纯边的JSON
    output_dir = Config.OUTPUT_DIR / "strict_knowledge_graph_example"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*70)
    print("💾 保存纯边JSON...")
    print("="*70 + "\n")
    
    # 导出纯边JSON
    edges_file = output_dir / "cross_domain_edges.json"
    edges_json = {
        "edges": [
            {
                "source": edge["source"],  # 节点ID
                "target": edge["target"],  # 节点ID
                "label": edge["label"],
                "properties": edge["properties"]
            }
            for edge in edges
        ],
        "metadata": {
            "source_graphs": {
                "physics": str(physics_graph_path),
                "math": str(math_graph_path)
            },
            "total_edges": len(edges),
            "generated_at": chatroom.get_timestamp()
        }
    }
    
    with open(edges_file, 'w', encoding='utf-8') as f:
        json.dump(edges_json, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 纯边JSON已保存: {edges_file}")
    print(f"  总边数: {len(edges)}")
    print()
    
    # 显示示例边
    if edges:
        print("🌟 发现的跨学科边示例：\n")
        for i, edge in enumerate(edges[:5], 1):
            print(f"{i}. {edge['source']} --[{edge['label']}]--> {edge['target']}")
            print(f"   {edge['properties']['description'][:100]}...")
            print()
    
    # 导出讨论日志
    chatroom.export_discussion_log(output_dir / "discussion_log.json")
    
    print("="*70)
    print("✨ 完成！")
    print("="*70)
    print()
    print(f"结果保存在: {output_dir}")
    print()


if __name__ == "__main__":
    main()

