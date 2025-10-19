"""
测试：展示完整properties是否正确传递给agent
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

# 创建聊天室
chatroom = NodePairChatroom(
    physics_agent=PhysicsAgent(),
    math_agent=MathAgent(),
    physics_graph=physics_graph,
    math_graph=math_graph,
    output_file=Path("output/test_properties/edges.json")
)

# 先查看一个节点的完整properties
print("="*70)
print("查看节点的完整properties信息")
print("="*70)
print()

physics_node_id = "displacement_velocity_acceleration"
math_node_id = "function_definition_and_elements"

physics_node = chatroom.physics_nodes[physics_node_id]
math_node = chatroom.math_nodes[math_node_id]

print("物理节点完整信息：")
print(json.dumps(physics_node, indent=2, ensure_ascii=False))
print()

print("数学节点完整信息：")
print(json.dumps(math_node, indent=2, ensure_ascii=False))
print()

# 查看构建的上下文
print("="*70)
print("查看agent会收到的上下文")
print("="*70)
print()

physics_context = chatroom._build_node_context(
    physics_node_id,
    chatroom.physics_nodes,
    chatroom.physics_edges,
    depth=1
)

print("物理agent的上下文：")
print(physics_context)
print()

math_context = chatroom._build_node_context(
    math_node_id,
    chatroom.math_nodes,
    chatroom.math_edges,
    depth=1
)

print("数学agent的上下文：")
print(math_context)
print()

# 进行一次实际讨论
print("="*70)
print("进行实际讨论")
print("="*70)
print()

edge = chatroom.discuss_node_pair(
    physics_node_id=physics_node_id,
    math_node_id=math_node_id,
    context_depth=1
)

if edge:
    print("\n✓ 成功生成边")
    print(json.dumps(edge, indent=2, ensure_ascii=False))
else:
    print("\n✗ 未生成边")

