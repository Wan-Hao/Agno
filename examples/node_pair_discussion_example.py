"""
节点对节点讨论示例

演示如何让两个agent围绕具体的节点对进行讨论
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.node_pair_chatroom import NodePairChatroom
from agents import PhysicsAgent, MathAgent
from config import Config
import json


def main():
    """节点对节点的讨论"""
    # 验证配置
    try:
        Config.validate()
    except Exception as e:
        print(f"✗ 配置错误: {e}")
        print("请在 .env 文件中设置 GEMINI_API_KEY")
        return
    
    print("="*70)
    print("节点对节点讨论：精确的跨学科关联发现")
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
    
    print("📊 加载知识图谱...\n")
    
    # 加载图谱
    with open(physics_graph_path, 'r', encoding='utf-8') as f:
        physics_graph = json.load(f)
    with open(math_graph_path, 'r', encoding='utf-8') as f:
        math_graph = json.load(f)
    
    print(f"✓ 物理图谱: {len(physics_graph['nodes'])} 节点")
    print(f"✓ 数学图谱: {len(math_graph['nodes'])} 节点")
    print()
    
    # 创建智能体
    physics_agent = PhysicsAgent()
    math_agent = MathAgent()
    
    # 创建聊天室
    output_file = Config.OUTPUT_DIR / "node_pair_example" / "cross_domain_edges.json"
    
    chatroom = NodePairChatroom(
        physics_agent=physics_agent,
        math_agent=math_agent,
        physics_graph=physics_graph,
        math_graph=math_graph,
        output_file=output_file
    )
    
    print("\n🎯 开始节点对讨论...\n")
    
    # 定义要讨论的节点对
    node_pairs = [
        # 运动与函数
        ("displacement_velocity_acceleration", "function_definition_and_elements"),
        ("instantaneous_velocity", "derivative_concept"),
        
        # 力与向量
        ("force_concept", "vector_and_scalar"),
        ("force_composition_and_resolution", "vector_operations"),
        
        # 方程与函数零点
        ("motion_equations", "function_zero"),
        
        # 图像与函数图像
        ("motion_graphs", "graphical_method"),
    ]
    
    print("计划讨论的节点对：")
    for i, (p_id, m_id) in enumerate(node_pairs, 1):
        print(f"{i}. [{p_id}] ↔ [{m_id}]")
    print()
    
    # 批量讨论
    valid_edges = chatroom.batch_discuss(
        node_pairs=node_pairs,
        context_depth=1  # 包含直接相关的节点
    )
    
    # 显示结果
    print("\n" + "="*70)
    print("📊 讨论结果")
    print("="*70)
    print()
    
    print(f"讨论节点对数: {len(node_pairs)}")
    print(f"生成并保留的边: {len(valid_edges)}")
    print(f"保留率: {len(valid_edges)/len(node_pairs)*100:.1f}%")
    print()
    
    if valid_edges:
        print("✓ 保留的边：\n")
        for i, edge in enumerate(valid_edges, 1):
            print(f"{i}. {edge['source']} --[{edge['label']}]--> {edge['target']}")
            print(f"   {edge['properties']['description']}")
            print(f"   置信度: {edge['properties']['confidence']}")
            print()
    
    print(f"结果已保存到: {output_file}")
    print()
    
    # 读取最终文件
    with open(output_file, 'r', encoding='utf-8') as f:
        final_data = json.load(f)
    
    print("="*70)
    print("📄 最终JSON文件内容")
    print("="*70)
    print()
    print(f"总边数: {final_data['metadata']['total_edges']}")
    print(f"创建时间: {final_data['metadata']['created_at']}")
    print()
    
    print("="*70)
    print("✨ 完成！")
    print("="*70)


def demonstrate_single_pair():
    """演示单对节点的讨论"""
    print("="*70)
    print("单对节点讨论演示")
    print("="*70)
    print()
    
    # 简化：只讨论一对
    dataset_dir = Path(__file__).parent.parent / "dataset" / "graph"
    
    with open(dataset_dir / "physics_knowledge_graph_new.json", 'r') as f:
        physics_graph = json.load(f)
    with open(dataset_dir / "math_knowledge_graph_new.json", 'r') as f:
        math_graph = json.load(f)
    
    physics_agent = PhysicsAgent()
    math_agent = MathAgent()
    
    chatroom = NodePairChatroom(
        physics_agent=physics_agent,
        math_agent=math_agent,
        physics_graph=physics_graph,
        math_graph=math_graph,
        output_file=Path("output/demo_single_pair.json")
    )
    
    # 讨论一对节点
    edge = chatroom.discuss_node_pair(
        physics_node_id="displacement_velocity_acceleration",
        math_node_id="function_definition_and_elements",
        context_depth=1
    )
    
    if edge:
        print("\n✓ 成功生成边：")
        print(json.dumps(edge, indent=2, ensure_ascii=False))
    else:
        print("\n✗ 此节点对未生成有效的边")


if __name__ == "__main__":
    # 运行完整示例
    main()
    
    # 或者运行单对演示
    # demonstrate_single_pair()

