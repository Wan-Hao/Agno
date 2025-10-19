"""
运行小规模采样（10对节点）用于演示
"""
import sys
from pathlib import Path
import json

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.node_pair_chatroom import NodePairChatroom
from agents import PhysicsAgent, MathAgent
from config import Config

# 验证配置
Config.validate()

# 加载图谱
dataset_dir = project_root / "dataset" / "graph"

with open(dataset_dir / "physics_knowledge_graph_new.json") as f:
    physics_graph = json.load(f)
with open(dataset_dir / "math_knowledge_graph_new.json") as f:
    math_graph = json.load(f)

# 手动选择10对有意义的节点
node_pairs = [
    # 运动与函数
    ("displacement_velocity_acceleration", "function_definition_and_elements"),
    ("instantaneous_velocity", "monotonicity_and_extrema"),
    
    # 图像
    ("motion_graphs", "graphical_method"),
    ("vt_graph", "function_representation_methods"),
    
    # 向量
    ("vector_and_scalar", "set_concepts_and_representation"),
    
    # 方程
    ("uniformly_accelerated_linear_motion", "quadratic_equation_and_inequality"),
    
    # 变化
    ("acceleration_concept", "monotonicity_and_extrema"),
    
    # 时间
    ("time_and_instant", "function_definition_and_elements"),
    
    # 关系
    ("reference_frame", "set_relations_and_operations"),
    
    # 运动学
    ("kinematics_concepts", "function_theme"),
]

print("="*70)
print(f"小规模采样演示：{len(node_pairs)} 对节点")
print("="*70)
print()

# 创建聊天室
output_file = Path("output/demo_10_pairs/cross_domain_edges.json")

chatroom = NodePairChatroom(
    physics_agent=PhysicsAgent(),
    math_agent=MathAgent(),
    physics_graph=physics_graph,
    math_graph=math_graph,
    output_file=output_file
)

# 批量讨论
valid_edges = chatroom.batch_discuss(node_pairs, context_depth=1)

# 显示结果
print("\n" + "="*70)
print("结果统计")
print("="*70)
print(f"讨论对数: {len(node_pairs)}")
print(f"有效边数: {len(valid_edges)}")
print(f"有效率: {len(valid_edges)/len(node_pairs)*100:.1f}%")
print(f"输出文件: {output_file}")

