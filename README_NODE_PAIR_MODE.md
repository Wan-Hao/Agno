# 节点对节点讨论模式 - 快速上手

## 这是什么？

一个让AI智能体基于**具体知识节点**进行跨学科讨论的系统。

### 核心特点

```
物理节点: [displacement_velocity_acceleration]
    + 学科内相关知识
    
    ↕ 精确讨论
    
数学节点: [function_definition_and_elements]
    + 学科内相关知识
    
    ↓
    
生成边: displacement_velocity_acceleration --[requires]--> function_definition_and_elements
    
    ↓
    
评估 → 保留/拒绝
    
    ↓
    
Function Call 写入 JSON
```

## 一分钟使用

```bash
cd /Users/vangogh/Documents/Github/Agno
source venv/bin/activate
python examples/node_pair_discussion_example.py
```

查看结果：

```bash
cat output/node_pair_example/cross_domain_edges.json
```

## 输出示例

```json
{
  "edges": [
    {
      "source": "displacement_velocity_acceleration",
      "target": "function_definition_and_elements",
      "label": "requires",
      "properties": {
        "description": "位移、速度和加速度的定义依赖函数概念",
        "reasoning": "速度是位移对时间的函数，加速度是速度对时间的函数",
        "confidence": 0.92
      }
    }
  ],
  "metadata": {
    "total_edges": 1,
    "last_updated": "2025-10-19T..."
  }
}
```

## 工作流程

### 1. 创建聊天室

```python
from core.node_pair_chatroom import NodePairChatroom
from agents import PhysicsAgent, MathAgent
import json

# 加载图谱
with open('dataset/graph/physics_knowledge_graph_new.json') as f:
    physics_graph = json.load(f)
with open('dataset/graph/math_knowledge_graph_new.json') as f:
    math_graph = json.load(f)

# 创建聊天室
chatroom = NodePairChatroom(
    physics_agent=PhysicsAgent(),
    math_agent=MathAgent(),
    physics_graph=physics_graph,
    math_graph=math_graph,
    output_file=Path("output/edges.json")
)
```

### 2. 讨论节点对

```python
# 讨论一对节点
edge = chatroom.discuss_node_pair(
    physics_node_id="velocity_concepts",
    math_node_id="derivative_concept",
    context_depth=1
)

# 或批量讨论
node_pairs = [
    ("velocity_concepts", "derivative_concept"),
    ("force_concept", "vector_and_scalar"),
]
valid_edges = chatroom.batch_discuss(node_pairs)
```

### 3. 自动筛选和保存

系统会自动：
1. ✅ 检查讨论是否偏离（元协调者）
2. ✅ 评估边的质量（评估agent）
3. ✅ 通过function call写入JSON
4. ✅ 只保留有效的边

## 核心机制

### 学科内上下文

每个agent讨论时会携带：

```
核心节点: displacement_velocity_acceleration
相关节点:
  - kinematics_concepts
  - velocity_concepts
  - acceleration_concept
  - ...
```

这确保讨论基于**实际的知识结构**，而不是空谈。

### 偏离检测

协调者只在以下情况介入：
- 未提到核心节点ID
- 讨论过短（<100字符）

其他情况**保持静默**，让专家自由讨论。

### 质量评估

评估agent检查：
- 关联是否合理
- 描述是否清晰
- 置信度是否足够（≥0.6）

**不合格的边会被拒绝**，不写入文件。

### Function Call写入

```python
def add_edge_to_json(file_path: str, edge: Dict[str, Any]):
    """向JSON文件添加一条边"""
    # 读取 → 添加 → 写回
    ...
```

每条通过评估的边**立即写入**，增量构建知识图谱。

## 与其他模式的区别

### 原模式：主题式讨论

```python
chatroom.discuss(
    rounds=5,
    focus_themes={"physics": ["运动"], "math": ["函数"]}
)
```

输出：
```json
{
  "source": {"domain": "Physics", "concept": "Motion"},
  "target": {"domain": "Math", "concept": "Function"}
}
```

❌ 问题：
- 不是图谱中的实际节点
- 讨论宽泛，不聚焦
- 难以验证和集成

### 节点对模式

```python
chatroom.discuss_node_pair(
    physics_node_id="displacement_velocity_acceleration",
    math_node_id="function_definition_and_elements"
)
```

输出：
```json
{
  "source": "displacement_velocity_acceleration",
  "target": "function_definition_and_elements",
  "label": "requires",
  "properties": {...}
}
```

✅ 优势：
- 实际节点ID，可直接集成
- 讨论精确，聚焦具体知识点
- 携带学科上下文，不孤立
- 自动评估和筛选

## 配置选项

### 上下文深度

```python
context_depth=1  # 推荐：包含1层相关节点
context_depth=2  # 更丰富的上下文（token消耗更大）
```

### 节点对选择

```python
# 手动指定
node_pairs = [
    ("nodeA", "node1"),
    ("nodeB", "node2"),
]

# 或基于主题筛选
physics_nodes = [n for n in physics_graph['nodes'] if '运动' in n['label']]
math_nodes = [n for n in math_graph['nodes'] if '函数' in n['label']]
node_pairs = [(p['id'], m['id']) for p in physics_nodes for m in math_nodes]
```

## 完整文档

- **快速指南**：本文件
- **详细指南**：`NODE_PAIR_DISCUSSION_GUIDE.md`
- **代码示例**：`examples/node_pair_discussion_example.py`

## 为什么使用这个模式？

### 之前的问题

1. **不基于实际节点**：输出抽象概念，无法追溯
2. **讨论宽泛**：多个主题混在一起，不聚焦
3. **质量不可控**：没有筛选机制

### 现在的解决

1. ✅ **实际节点ID**：source和target都在图谱中
2. ✅ **精确聚焦**：每次讨论一对具体节点
3. ✅ **质量保证**：评估agent筛选
4. ✅ **增量构建**：通过function call逐步积累
5. ✅ **可追溯**：每条边有清晰的来源和理由

## 开始使用

```bash
# 1. 激活环境
source venv/bin/activate

# 2. 运行示例
python examples/node_pair_discussion_example.py

# 3. 查看结果
cat output/node_pair_example/cross_domain_edges.json
```

## 需要帮助？

查看详细文档：
```bash
cat NODE_PAIR_DISCUSSION_GUIDE.md
```

