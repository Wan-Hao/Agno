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

# 选择1对有意义的节点用于多轮对话测试
node_pairs = [
    # 运动与函数 - 这是一个很好的跨学科关联例子
    ("displacement_velocity_acceleration", "function_definition_and_elements"),
]

print("="*70)
print(f"多轮对话测试：{len(node_pairs)} 对节点")
print(f"测试节点对: [位移、速度与加速度] ↔ [函数定义与三要素]")
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

