# 严格知识图谱模式使用指南

## 概述

**严格知识图谱模式**是一种改进的跨学科讨论方式，它确保：

1. **讨论严格基于知识图谱节点** - 每个论点都必须锚定在图谱中的实际节点ID上
2. **协调者更克制** - 只在讨论真正偏离节点时才介入
3. **输出纯边的JSON** - 边的两端必须是实际存在的节点ID

## 与原版本的区别

### 原版本问题

```json
{
  "source": {
    "domain": "Physics (General Relativity)",
    "concept": "Matter-Spacetime Interaction"
  },
  "target": {
    "domain": "Sociology",
    "concept": "Agency-Structure Feedback Loop"
  }
}
```

- ❌ 源和目标是抽象概念，不是图谱中的节点
- ❌ 讨论空泛，缺乏具体锚点
- ❌ 协调者频繁介入

### 严格模式

```json
{
  "source": "velocity_acceleration",
  "target": "function_zero",
  "label": "mathematical_foundation_of",
  "properties": {
    "description": "速度和加速度的计算依赖于函数的零点概念",
    "reasoning": "运动方程求解需要找到函数的零点",
    "confidence": 0.9
  }
}
```

- ✅ source和target是图谱中的实际节点ID
- ✅ 讨论围绕具体知识点展开
- ✅ 协调者仅在必要时介入

## 使用方法

### 1. 基本使用

```python
from core.chatroom import StrictKnowledgeGraphChatroom
from agents import PhysicsAgent, MathAgent
import json

# 加载知识图谱
with open('physics_knowledge_graph.json', 'r') as f:
    physics_graph = json.load(f)

with open('math_knowledge_graph.json', 'r') as f:
    math_graph = json.load(f)

# 创建智能体
physics_agent = PhysicsAgent()
math_agent = MathAgent()

# 创建聊天室
chatroom = StrictKnowledgeGraphChatroom(
    topic="发现物理与数学的内在联系",
    agents=[physics_agent, math_agent],
    physics_graph=physics_graph,
    math_graph=math_graph
)

# 开始讨论
edges = chatroom.discuss(
    rounds=5,
    focus_themes={
        "physics": ["机械运动与物理模型"],
        "math": ["函数", "集合"]
    }
)

# 输出边
print(f"发现 {len(edges)} 条跨学科边")
```

### 2. 运行示例

```bash
cd /Users/vangogh/Documents/Github/Agno
source venv/bin/activate
python examples/strict_knowledge_graph_example.py
```

## 工作原理

### 1. 节点上下文构建

系统为每个智能体提供可用节点列表：

```
## 物理知识节点

- **[velocity_acceleration]** 速度与加速度
  描述物体运动的基本物理量...

- **[newton_second_law]** 牛顿第二定律
  力与加速度的关系...

## 数学知识节点

- **[function_zero]** 函数零点
  使函数值为零的自变量...

- **[derivative_concept]** 导数概念
  函数变化率的数学表示...
```

### 2. 强制节点引用

智能体在讨论时必须使用方括号引用节点ID：

```
物理专家: 
"我认为 [velocity_acceleration] 与数学中的 [derivative_concept] 有密切联系，
因为瞬时速度的定义本质上就是位移对时间的导数..."
```

### 3. 协调者检查机制

协调者会检查：
- 是否引用了足够数量的节点ID（每个专家至少2个）
- 引用的节点ID是否在图谱中存在
- 只有当检查失败时才介入

### 4. 边提取与验证

从讨论中提取边时：
1. 识别讨论中引用的所有节点ID
2. 提取节点间的关联关系
3. 验证source和target都在图谱中
4. 只保留有效的边

## 输出格式

### 边的JSON格式

```json
{
  "edges": [
    {
      "source": "velocity_acceleration",
      "target": "derivative_concept",
      "label": "requires",
      "properties": {
        "description": "速度和加速度的定义需要导数概念",
        "reasoning": "瞬时速度是位移对时间的导数",
        "confidence": 0.95
      }
    },
    {
      "source": "newton_second_law",
      "target": "function_definition_and_elements",
      "label": "mathematical_model",
      "properties": {
        "description": "牛顿第二定律用函数关系描述力和加速度",
        "reasoning": "F=ma是一个函数关系",
        "confidence": 0.85
      }
    }
  ],
  "metadata": {
    "source_graphs": {
      "physics": "path/to/physics_graph.json",
      "math": "path/to/math_graph.json"
    },
    "total_edges": 2,
    "generated_at": "2025-10-19T..."
  }
}
```

### 标准边类型（label）

推荐使用的关系类型：

- `mathematical_foundation_of` - 数学基础
- `models` - 建模关系
- `requires` - 需要/依赖
- `analogous_to` - 类比关系
- `generalizes` - 泛化关系
- `applies_to` - 应用于
- `measures` - 度量关系

## 最佳实践

### 1. 选择合适的主题范围

```python
focus_themes={
    "physics": ["机械运动与物理模型", "相互作用"],  # 不要太宽泛
    "math": ["函数"]  # 不要太窄
}
```

### 2. 适当的讨论轮次

- 3-5轮：快速探索
- 5-8轮：深入讨论
- 8+轮：全面分析（可能产生重复）

### 3. 后处理边数据

```python
# 按置信度筛选
high_quality_edges = [
    e for e in edges 
    if e['properties']['confidence'] >= 0.8
]

# 按关系类型分组
from collections import defaultdict
edges_by_type = defaultdict(list)
for edge in edges:
    edges_by_type[edge['label']].append(edge)
```

## 故障排除

### 问题：智能体不引用节点ID

**原因**：节点描述不够清晰或prompt不够强调

**解决**：
1. 检查节点的description字段是否完整
2. 增加对节点引用的强调
3. 减少一次提供的节点数量（<30个）

### 问题：协调者频繁介入

**原因**：节点ID检测规则太严格

**解决**：
调整 `_check_if_off_topic` 中的阈值：
```python
if len(physics_node_refs) < 1 or len(math_node_refs) < 1:  # 从2改为1
    return True
```

### 问题：提取的边为空

**原因**：节点ID提取失败或格式不匹配

**解决**：
1. 检查正则表达式是否匹配节点ID格式
2. 在讨论日志中确认agent确实引用了节点
3. 调整边提取的prompt

## 进阶使用

### 自定义节点筛选

```python
def custom_filter(node):
    # 只选择包含"运动"的物理节点
    return "运动" in node.get('label', '')

physics_custom = [n for n in physics_graph['nodes'] if custom_filter(n)]
```

### 导出为Neo4j格式

```python
def to_neo4j(edges, physics_nodes, math_nodes):
    cypher = []
    
    # 创建节点
    for node_id, node in physics_nodes.items():
        cypher.append(
            f"CREATE (:{node['label'].replace(' ', '_')} "
            f"{{id: '{node_id}', label: '{node['label']}', domain: 'Physics'}})"
        )
    
    # 创建关系
    for edge in edges:
        cypher.append(
            f"MATCH (a {{id: '{edge['source']}'}}), "
            f"(b {{id: '{edge['target']}'}}) "
            f"CREATE (a)-[:{edge['label'].upper()}]->(b)"
        )
    
    return "\n".join(cypher)
```

## 总结

严格知识图谱模式确保了：

✅ **高质量的关联** - 基于实际知识点，不是空谈  
✅ **可验证的输出** - 每条边都可以追溯到具体节点  
✅ **高效的讨论** - 协调者不过度介入  
✅ **标准化格式** - 纯边的JSON，易于集成和分析

这是**真正意义上的知识图谱增强**，而不是概念层面的类比讨论。

