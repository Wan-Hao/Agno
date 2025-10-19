"""
快速测试严格模式功能
"""
import json
from pathlib import Path

# 测试节点ID提取
def test_node_id_extraction():
    """测试从文本中提取节点ID"""
    import re
    
    test_text = """
    我认为 [velocity_acceleration] 与 [function_zero] 有关联。
    另外，[newton_second_law] 也与 [derivative_concept] 相关。
    """
    
    node_refs = re.findall(r'\[([a-z_0-9]+)\]', test_text)
    print(f"提取的节点ID: {node_refs}")
    assert len(node_refs) == 4
    print("✓ 节点ID提取测试通过")


# 测试图谱加载
def test_graph_loading():
    """测试知识图谱加载"""
    dataset_dir = Path(__file__).parent / "dataset" / "graph"
    physics_path = dataset_dir / "physics_knowledge_graph_new.json"
    math_path = dataset_dir / "math_knowledge_graph_new.json"
    
    with open(physics_path, 'r', encoding='utf-8') as f:
        physics_graph = json.load(f)
    
    with open(math_path, 'r', encoding='utf-8') as f:
        math_graph = json.load(f)
    
    print(f"物理图谱: {len(physics_graph['nodes'])} 节点")
    print(f"数学图谱: {len(math_graph['nodes'])} 节点")
    
    # 测试节点索引
    physics_nodes = {n['id']: n for n in physics_graph['nodes']}
    math_nodes = {n['id']: n for n in math_graph['nodes']}
    
    # 检查一些关键节点
    assert 'mechanical_motion_and_physical_models' in physics_nodes
    assert 'function_definition_and_elements' in math_nodes
    
    print("✓ 图谱加载测试通过")


# 测试边验证
def test_edge_validation():
    """测试边的验证逻辑"""
    dataset_dir = Path(__file__).parent / "dataset" / "graph"
    physics_path = dataset_dir / "physics_knowledge_graph_new.json"
    math_path = dataset_dir / "math_knowledge_graph_new.json"
    
    with open(physics_path, 'r', encoding='utf-8') as f:
        physics_graph = json.load(f)
    
    with open(math_path, 'r', encoding='utf-8') as f:
        math_graph = json.load(f)
    
    physics_nodes = {n['id']: n for n in physics_graph['nodes']}
    math_nodes = {n['id']: n for n in math_graph['nodes']}
    
    # 测试有效边
    test_edges = [
        {
            "source": "displacement_velocity_acceleration",
            "target": "function_definition_and_elements",
            "label": "requires"
        },
        {
            "source": "invalid_node",
            "target": "function_definition_and_elements",
            "label": "requires"
        }
    ]
    
    validated = []
    for edge in test_edges:
        source_id = edge['source']
        target_id = edge['target']
        
        if source_id in physics_nodes and target_id in math_nodes:
            validated.append(edge)
            print(f"✓ 有效边: {source_id} -> {target_id}")
        else:
            print(f"✗ 无效边: {source_id} -> {target_id}")
    
    assert len(validated) == 1
    print("✓ 边验证测试通过")


# 测试输出格式
def test_output_format():
    """测试输出JSON格式"""
    edges = [
        {
            "source": "velocity",
            "target": "function_definition_and_elements",
            "label": "requires",
            "properties": {
                "description": "速度定义需要函数概念",
                "reasoning": "速度是位移关于时间的函数",
                "confidence": 0.9
            }
        }
    ]
    
    output = {
        "edges": edges,
        "metadata": {
            "total_edges": len(edges),
            "generated_at": "2025-10-19"
        }
    }
    
    # 验证格式
    assert "edges" in output
    assert "metadata" in output
    assert isinstance(output["edges"], list)
    
    edge = output["edges"][0]
    assert "source" in edge
    assert "target" in edge
    assert "label" in edge
    assert "properties" in edge
    
    print("输出格式示例:")
    print(json.dumps(output, indent=2, ensure_ascii=False))
    print("✓ 输出格式测试通过")


if __name__ == "__main__":
    print("="*60)
    print("严格模式功能测试")
    print("="*60)
    print()
    
    try:
        print("1. 测试节点ID提取...")
        test_node_id_extraction()
        print()
        
        print("2. 测试图谱加载...")
        test_graph_loading()
        print()
        
        print("3. 测试边验证...")
        test_edge_validation()
        print()
        
        print("4. 测试输出格式...")
        test_output_format()
        print()
        
        print("="*60)
        print("✨ 所有测试通过！")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()

