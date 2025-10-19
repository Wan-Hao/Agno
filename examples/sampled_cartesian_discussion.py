"""
采样笛卡尔积讨论

不是讨论所有节点对，而是：
1. 随机采样N对
2. 基于关键词匹配采样
3. 基于主题筛选采样
"""
import sys
from pathlib import Path
import json
import random

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.node_pair_chatroom import NodePairChatroom
from agents import PhysicsAgent, MathAgent
from config import Config


def random_sample(math_nodes, physics_nodes, n=100):
    """随机采样N对"""
    print(f"🎲 随机采样 {n} 对节点...")
    
    all_pairs = [
        (p['id'], m['id'])
        for m in math_nodes
        for p in physics_nodes
    ]
    
    sampled = random.sample(all_pairs, min(n, len(all_pairs)))
    print(f"✓ 采样完成: {len(sampled)} 对")
    return sampled


def keyword_based_sample(math_nodes, physics_nodes, keywords, max_pairs=200):
    """基于关键词匹配采样"""
    print(f"🔍 基于关键词采样: {keywords}")
    
    pairs = []
    
    for math_node in math_nodes:
        math_desc = math_node.get('properties', {}).get('description', '')
        math_label = math_node.get('label', '')
        
        for physics_node in physics_nodes:
            physics_desc = physics_node.get('properties', {}).get('description', '')
            physics_label = physics_node.get('label', '')
            
            # 检查是否包含关键词
            has_keyword = False
            for keyword in keywords:
                if (keyword in math_desc or keyword in math_label) and \
                   (keyword in physics_desc or keyword in physics_label):
                    has_keyword = True
                    break
            
            if has_keyword:
                pairs.append((physics_node['id'], math_node['id']))
                
                if len(pairs) >= max_pairs:
                    break
        
        if len(pairs) >= max_pairs:
            break
    
    print(f"✓ 找到 {len(pairs)} 对包含关键词的节点")
    return pairs


def theme_based_sample(math_nodes, physics_nodes, math_themes, physics_themes):
    """基于主题筛选采样"""
    print(f"📚 基于主题采样")
    print(f"   数学主题: {math_themes}")
    print(f"   物理主题: {physics_themes}")
    
    # 筛选数学节点
    filtered_math = []
    for node in math_nodes:
        props = node.get('properties', {})
        theme = props.get('theme', '')
        category = props.get('category', '')
        
        if any(t in theme or t in category for t in math_themes):
            filtered_math.append(node)
    
    # 筛选物理节点
    filtered_physics = []
    for node in physics_nodes:
        props = node.get('properties', {})
        theme = props.get('theme', '')
        category = props.get('category', '')
        
        if any(t in theme or t in category for t in physics_themes):
            filtered_physics.append(node)
    
    print(f"✓ 筛选后: {len(filtered_math)} 个数学节点, {len(filtered_physics)} 个物理节点")
    
    # 生成笛卡尔积
    pairs = [
        (p['id'], m['id'])
        for m in filtered_math
        for p in filtered_physics
    ]
    
    print(f"✓ 生成 {len(pairs)} 对节点")
    return pairs


def main():
    """主函数"""
    # 验证配置
    try:
        Config.validate()
    except Exception as e:
        print(f"✗ 配置错误: {e}")
        return
    
    print("="*70)
    print("采样笛卡尔积讨论")
    print("="*70)
    print()
    
    # 加载图谱
    dataset_dir = Path(__file__).parent.parent / "dataset" / "graph"
    
    with open(dataset_dir / "physics_knowledge_graph_new.json", 'r') as f:
        physics_graph = json.load(f)
    with open(dataset_dir / "math_knowledge_graph_new.json", 'r') as f:
        math_graph = json.load(f)
    
    math_nodes = math_graph['nodes']
    physics_nodes = physics_graph['nodes']
    
    print(f"📊 图谱信息")
    print(f"   数学节点: {len(math_nodes)}")
    print(f"   物理节点: {len(physics_nodes)}")
    print(f"   全量笛卡尔积: {len(math_nodes) * len(physics_nodes)} 对")
    print()
    
    # 选择采样策略
    print("请选择采样策略:")
    print("1. 随机采样100对")
    print("2. 基于关键词采样")
    print("3. 基于主题筛选")
    print("4. 自定义")
    print()
    
    choice = input("请输入选项 (1-4，默认1): ").strip() or "1"
    
    node_pairs = []
    output_suffix = ""
    
    if choice == "1":
        node_pairs = random_sample(math_nodes, physics_nodes, n=100)
        output_suffix = "random_100"
    
    elif choice == "2":
        keywords = ["运动", "速度", "加速度", "力", "能量", "函数", "导数", "极限", "变化", "关系"]
        node_pairs = keyword_based_sample(math_nodes, physics_nodes, keywords, max_pairs=200)
        output_suffix = "keyword_based"
    
    elif choice == "3":
        math_themes = ["函数", "集合"]
        physics_themes = ["机械运动与物理模型", "相互作用"]
        node_pairs = theme_based_sample(math_nodes, physics_nodes, math_themes, physics_themes)
        output_suffix = "theme_based"
    
    elif choice == "4":
        n = int(input("随机采样数量: "))
        node_pairs = random_sample(math_nodes, physics_nodes, n=n)
        output_suffix = f"custom_{n}"
    
    if not node_pairs:
        print("✗ 未生成节点对")
        return
    
    print()
    print("="*70)
    print(f"开始讨论 {len(node_pairs)} 对节点")
    print("="*70)
    print()
    
    # 创建聊天室
    output_file = Config.OUTPUT_DIR / "sampled_cartesian" / f"edges_{output_suffix}.json"
    
    physics_agent = PhysicsAgent()
    math_agent = MathAgent()
    
    chatroom = NodePairChatroom(
        physics_agent=physics_agent,
        math_agent=math_agent,
        physics_graph=physics_graph,
        math_graph=math_graph,
        output_file=output_file
    )
    
    # 批量讨论
    valid_edges = chatroom.batch_discuss(
        node_pairs=node_pairs,
        context_depth=1
    )
    
    # 显示结果
    print("\n" + "="*70)
    print("📊 讨论结果")
    print("="*70)
    print()
    print(f"讨论节点对数: {len(node_pairs)}")
    print(f"生成有效边: {len(valid_edges)}")
    print(f"有效率: {len(valid_edges)/len(node_pairs)*100:.1f}%")
    print()
    print(f"结果文件: {output_file}")
    print()


if __name__ == "__main__":
    main()

