# 节点对节点讨论模式

## 核心设计

每次对话聚焦**一对具体节点**：

```
物理节点 [displacement_velocity_acceleration] 
    + 该节点的学科内相关知识
    
    ↕ 讨论融合可能性
    
数学节点 [function_definition_and_elements]
    + 该节点的学科内相关知识
```

## 工作流程

```
1. 选择节点对
   物理: displacement_velocity_acceleration
   数学: function_definition_and_elements

2. 构建学科内上下文
   物理agent获得:
   - 核心节点: displacement_velocity_acceleration
   - 相关节点: kinematics_concepts, velocity_concepts, acceleration_concept...
   
   数学agent获得:
   - 核心节点: function_definition_and_elements
   - 相关节点: mapping_concept, domain, range, correspondence_rule...

3. 双向讨论
   物理agent: "位移、速度、加速度的定义需要函数的概念..."
   数学agent: "函数是描述两个变量间依赖关系的工具，可以用来..."
   
4. 元协调者监控
   - 检查是否偏离核心节点
   - 仅在偏离时矫正

5. 提取边
   {
     "source": "displacement_velocity_acceleration",
     "target": "function_definition_and_elements",
     "label": "requires",
     "properties": {...}
   }

6. 评估agent判断
   ✓ 关联合理，置信度0.9
   → 保留

7. Function call写入
   → 写入 cross_domain_edges.json
```

## 快速开始

### 1. 运行示例

```bash
cd /Users/vangogh/Documents/Github/Agno
source venv/bin/activate
python examples/node_pair_discussion_example.py
```

### 2. 查看结果

```bash
cat output/node_pair_example/cross_domain_edges.json
```

输出格式：

```json
{
  "metadata": {
    "source_graphs": {
      "physics": "physics_knowledge_graph_new.json",
      "math": "math_knowledge_graph_new.json"
    },
    "created_at": "2025-10-19T...",
    "total_edges": 5
  },
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
    },
    ...
  ]
}
```

## 代码示例

### 基本使用

```python
from core.node_pair_chatroom import NodePairChatroom
from agents import PhysicsAgent, MathAgent
import json

# 加载图谱
with open('dataset/graph/physics_knowledge_graph_new.json') as f:
    physics_graph = json.load(f)
with open('dataset/graph/math_knowledge_graph_new.json') as f:
    math_graph = json.load(f)

# 创建智能体
physics_agent = PhysicsAgent()
math_agent = MathAgent()

# 创建聊天室
chatroom = NodePairChatroom(
    physics_agent=physics_agent,
    math_agent=math_agent,
    physics_graph=physics_graph,
    math_graph=math_graph,
    output_file=Path("output/edges.json")
)

# 讨论一对节点
edge = chatroom.discuss_node_pair(
    physics_node_id="velocity_concepts",
    math_node_id="derivative_concept",
    context_depth=1  # 包含1层相关节点
)

if edge:
    print(f"✓ 生成边: {edge['source']} -> {edge['target']}")
else:
    print("✗ 未生成有效边")
```

### 批量讨论

```python
# 定义节点对
node_pairs = [
    ("displacement_velocity_acceleration", "function_definition_and_elements"),
    ("instantaneous_velocity", "derivative_concept"),
    ("force_concept", "vector_and_scalar"),
]

# 批量讨论
valid_edges = chatroom.batch_discuss(
    node_pairs=node_pairs,
    context_depth=1
)

print(f"生成 {len(valid_edges)} 条有效边")
```

### 自定义输出文件

```python
from pathlib import Path

chatroom = NodePairChatroom(
    physics_agent=physics_agent,
    math_agent=math_agent,
    physics_graph=physics_graph,
    math_graph=math_graph,
    output_file=Path("custom_output/my_edges.json")
)
```

## 核心机制详解

### 1. 学科内上下文构建

为每个节点构建上下文时，会包含：

- **核心节点**：讨论的焦点
- **相关节点**：通过图谱中的边连接的节点（可配置深度）

示例：

```python
context_depth=1  # 直接相关的节点（1层）
context_depth=2  # 包含2层相关节点
```

对于 `displacement_velocity_acceleration`，深度1可能包括：
- `kinematics_concepts`（父概念）
- `velocity_concepts`（组成部分）
- `acceleration_concept`（组成部分）

### 2. 偏离检测

协调者检查：

```python
def _is_off_topic(physics_response, math_response, physics_id, math_id):
    # 检查1: 是否提到核心节点ID
    if physics_id not in physics_response:
        return True
    if math_id not in math_response:
        return True
    
    # 检查2: 讨论是否太短（可能是敷衍）
    if len(physics_response) < 100 or len(math_response) < 100:
        return True
    
    return False
```

只有检测到偏离时，协调者才会介入矫正。

### 3. 边的评估

评估agent会判断：

1. **关联合理性**：两个节点间的联系是否有意义
2. **描述清晰度**：关系描述是否明确
3. **置信度**：建议 ≥ 0.6
4. **真实性**：是否是真实的跨学科关联

评估不通过的边不会写入文件。

### 4. Function Call写入

通过专门的function实现写入：

```python
def add_edge_to_json(file_path: str, edge: Dict[str, Any]):
    """向JSON文件添加一条边"""
    # 读取现有数据
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # 添加边
    data['edges'].append(edge)
    data['metadata']['total_edges'] = len(data['edges'])
    data['metadata']['last_updated'] = datetime.now().isoformat()
    
    # 写回
    with open(file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

每次讨论完成并通过评估后，边会立即写入文件。

## 节点对选择策略

### 策略1：基于主题筛选

```python
# 筛选特定主题的节点
physics_nodes = [
    n for n in physics_graph['nodes']
    if '运动' in n.get('properties', {}).get('theme', '')
]

math_nodes = [
    n for n in math_graph['nodes']
    if '函数' in n.get('properties', {}).get('theme', '')
]

# 生成节点对（笛卡尔积）
node_pairs = [
    (p['id'], m['id']) 
    for p in physics_nodes 
    for m in math_nodes
]
```

### 策略2：基于关键词匹配

```python
# 找描述中包含相似概念的节点对
import re

def find_similar_pairs(physics_graph, math_graph, keywords):
    pairs = []
    
    for p_node in physics_graph['nodes']:
        p_desc = p_node.get('properties', {}).get('description', '')
        
        for m_node in math_graph['nodes']:
            m_desc = m_node.get('properties', {}).get('description', '')
            
            # 检查是否包含共同关键词
            for keyword in keywords:
                if keyword in p_desc and keyword in m_desc:
                    pairs.append((p_node['id'], m_node['id']))
                    break
    
    return pairs

keywords = ['变化', '关系', '速率', '极限', '连续']
pairs = find_similar_pairs(physics_graph, math_graph, keywords)
```

### 策略3：随机采样

```python
import random

# 随机选择N对
physics_ids = [n['id'] for n in physics_graph['nodes']]
math_ids = [n['id'] for n in math_graph['nodes']]

random_pairs = [
    (random.choice(physics_ids), random.choice(math_ids))
    for _ in range(10)
]
```

## 输出格式规范

### 边的标准格式

```json
{
  "source": "物理节点ID（必须存在于physics_graph）",
  "target": "数学节点ID（必须存在于math_graph）",
  "label": "关系类型",
  "properties": {
    "description": "简洁的关系描述（1-2句话）",
    "reasoning": "发现此关联的详细理由",
    "confidence": 0.85
  }
}
```

### 推荐的关系类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `requires` | A需要B作为基础 | 速度需要函数概念 |
| `mathematical_foundation_of` | B是A的数学基础 | 导数是加速度的数学基础 |
| `models` | A用B建模 | 运动方程用函数建模 |
| `analogous_to` | A与B类比 | 力的合成类比向量加法 |
| `applies_to` | B应用于A | 函数图像应用于运动图像 |
| `measures` | B度量A | 速度度量位移变化 |
| `generalizes` | B是A的推广 | 函数是运动规律的抽象 |

## 进阶用法

### 1. 增量式讨论

每次只讨论一对，逐步积累：

```python
# 第一批
batch1 = [("nodeA", "node1"), ("nodeB", "node2")]
chatroom.batch_discuss(batch1)

# 第二批（自动追加到同一文件）
batch2 = [("nodeC", "node3"), ("nodeD", "node4")]
chatroom.batch_discuss(batch2)
```

### 2. 调整上下文深度

```python
# 浅层上下文（只有直接相关节点）
edge1 = chatroom.discuss_node_pair("nodeA", "node1", context_depth=1)

# 深层上下文（包含2层相关节点）
edge2 = chatroom.discuss_node_pair("nodeB", "node2", context_depth=2)
```

深度越大，上下文越丰富，但token消耗也越大。

### 3. 过滤和后处理

```python
import json

# 读取生成的边
with open("output/edges.json") as f:
    data = json.load(f)

# 按置信度过滤
high_conf = [
    e for e in data['edges']
    if e['properties']['confidence'] >= 0.8
]

print(f"高置信度边: {len(high_conf)}")

# 按关系类型分组
from collections import defaultdict
by_type = defaultdict(list)
for edge in data['edges']:
    by_type[edge['label']].append(edge)

for rel_type, edges in by_type.items():
    print(f"{rel_type}: {len(edges)} 条边")
```

### 4. 可视化边

```python
import networkx as nx
import matplotlib.pyplot as plt

# 构建图
G = nx.DiGraph()

for edge in data['edges']:
    G.add_edge(
        edge['source'],
        edge['target'],
        label=edge['label'],
        weight=edge['properties']['confidence']
    )

# 绘制
nx.draw(G, with_labels=True, node_color='lightblue')
plt.savefig('cross_domain_graph.png')
```

## 与之前模式的对比

### 之前：主题式讨论

```python
chatroom.discuss(
    rounds=5,
    focus_themes={"physics": ["运动"], "math": ["函数"]}
)
```

- ❌ 讨论宽泛，不聚焦
- ❌ 输出的边可能不精确
- ❌ 难以控制讨论质量

### 现在：节点对讨论

```python
chatroom.discuss_node_pair(
    physics_node_id="displacement_velocity_acceleration",
    math_node_id="function_definition_and_elements"
)
```

- ✅ 每次聚焦一对具体节点
- ✅ 输出的边精确、可验证
- ✅ 可控制的质量（评估agent筛选）

## 最佳实践

### 1. 选择有意义的节点对

优先选择：
- ✅ 概念层级相似的节点
- ✅ 描述中有共同关键词的节点
- ✅ 在各自学科中重要的节点

避免：
- ❌ 过于宽泛的高层节点（如"物理学"）
- ❌ 过于具体的叶节点（如"某个例题"）

### 2. 合理设置上下文深度

```python
context_depth=1  # 推荐：快速且相关
context_depth=2  # 适用于复杂关联
context_depth=3  # 可能引入噪声
```

### 3. 批量处理时的进度保存

```python
node_pairs = [...]  # 100对节点

# 分批处理，避免一次性失败
batch_size = 10
for i in range(0, len(node_pairs), batch_size):
    batch = node_pairs[i:i+batch_size]
    chatroom.batch_discuss(batch)
    print(f"完成批次 {i//batch_size + 1}")
```

### 4. 监控评估结果

```python
# 统计通过率
total_pairs = len(node_pairs)
valid_edges = chatroom.batch_discuss(node_pairs)
pass_rate = len(valid_edges) / total_pairs

print(f"通过率: {pass_rate:.1%}")

# 如果通过率过低（<30%），考虑调整节点对选择策略
```

## 故障排除

### 问题1：边的评估总是不通过

**原因**：节点对选择不当，或评估标准过严

**解决**：
1. 检查节点对是否有实际关联
2. 查看评估agent的拒绝理由
3. 如需要，调整评估prompt的标准

### 问题2：讨论频繁偏离

**原因**：节点描述不清晰，或上下文噪声过多

**解决**：
1. 降低context_depth（从2降到1）
2. 检查节点的description字段质量
3. 优化agent的system instruction

### 问题3：写入文件失败

**原因**：文件权限或路径问题

**解决**：
```python
# 确保输出目录存在
output_file = Path("output/edges.json")
output_file.parent.mkdir(parents=True, exist_ok=True)
```

## 总结

节点对讨论模式提供了：

✅ **精确聚焦**：每次讨论一对具体节点  
✅ **学科上下文**：携带相关知识，不孤立讨论  
✅ **质量保证**：评估agent筛选，只保留有意义的边  
✅ **增量构建**：通过function call逐步积累边  
✅ **可追溯**：每条边都有清晰的来源和理由

这是真正意义上的**知识图谱增强与融合**。

