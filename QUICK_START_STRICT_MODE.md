# 快速开始：严格知识图谱模式

## 一分钟理解

**问题**：之前的系统输出抽象概念之间的关联，不是图谱中的实际节点

**解决**：新的严格模式确保输出的边连接的是图谱中实际存在的节点ID

### 对比

**原来** ❌
```json
{
  "source": {"domain": "Physics", "concept": "Matter-Spacetime Interaction"},
  "target": {"domain": "Sociology", "concept": "Agency-Structure"}
}
```
→ 这些不是图谱中的节点！

**现在** ✅
```json
{
  "source": "displacement_velocity_acceleration",  // 物理图谱中的实际节点ID
  "target": "function_definition_and_elements",    // 数学图谱中的实际节点ID
  "label": "requires",
  "properties": {"description": "...", "confidence": 0.9}
}
```
→ 这些都是图谱中存在的节点ID！

## 三步使用

### 1. 测试基本功能

```bash
cd /Users/vangogh/Documents/Github/Agno
source venv/bin/activate
python test_strict_mode.py
```

应该看到：
```
✓ 节点ID提取测试通过
✓ 图谱加载测试通过
✓ 边验证测试通过
✓ 输出格式测试通过
```

### 2. 运行示例

```bash
python examples/strict_knowledge_graph_example.py
```

这会：
- 加载物理和数学图谱
- 讨论5轮，基于实际节点
- 输出纯边的JSON

### 3. 查看结果

```bash
cat output/strict_knowledge_graph_example/cross_domain_edges.json
```

## 核心概念

### 1. 节点引用

智能体必须用方括号引用节点ID：

```
物理专家: "我认为 [displacement_velocity_acceleration] 依赖于数学中的 [function_definition_and_elements]"
```

### 2. 协调者检查

协调者会检查：
- ✅ 每个专家是否引用了至少2个节点ID
- ✅ 引用的节点ID是否在图谱中存在
- ⚠️ 只有当检查失败时才介入

### 3. 边验证

提取的边会被验证：
- source必须在物理图谱中
- target必须在数学图谱中
- 无效的边会被跳过

## 输出格式

```json
{
  "edges": [
    {
      "source": "physics_node_id",
      "target": "math_node_id", 
      "label": "requires",
      "properties": {
        "description": "关系描述",
        "reasoning": "发现此关联的理由",
        "confidence": 0.9
      }
    }
  ],
  "metadata": {
    "source_graphs": {...},
    "total_edges": 15,
    "generated_at": "..."
  }
}
```

## 推荐的关系类型

- `requires` - 依赖
- `mathematical_foundation_of` - 数学基础
- `models` - 建模
- `analogous_to` - 类比
- `applies_to` - 应用于

## 代码示例

```python
from core.chatroom import StrictKnowledgeGraphChatroom
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
chatroom = StrictKnowledgeGraphChatroom(
    topic="发现物理与数学的联系",
    agents=[physics_agent, math_agent],
    physics_graph=physics_graph,
    math_graph=math_graph
)

# 讨论
edges = chatroom.discuss(
    rounds=5,
    focus_themes={
        "physics": ["机械运动与物理模型"],
        "math": ["函数"]
    }
)

# 输出
print(f"发现 {len(edges)} 条跨学科边")
for edge in edges:
    print(f"{edge['source']} -> {edge['target']}")
```

## 查看可用节点

### 物理图谱节点示例

```python
with open('dataset/graph/physics_knowledge_graph_new.json') as f:
    graph = json.load(f)

for node in graph['nodes'][:5]:
    print(f"ID: {node['id']}")
    print(f"标签: {node['label']}")
    print()
```

输出：
```
ID: mechanical_motion_and_physical_models
标签: 机械运动与物理模型

ID: displacement_velocity_acceleration
标签: 位移、速度与加速度

ID: newton_second_law
标签: 牛顿第二定律
...
```

### 数学图谱节点示例

```python
with open('dataset/graph/math_knowledge_graph_new.json') as f:
    graph = json.load(f)

for node in graph['nodes'][:5]:
    print(f"ID: {node['id']}")
    print(f"标签: {node['label']}")
    print()
```

输出：
```
ID: function_definition_and_elements
标签: 函数定义与三要素

ID: function_zero
标签: 函数零点

ID: derivative_concept
标签: 导数概念
...
```

## 常见问题

### Q: 为什么需要严格模式？

A: 原来的系统输出抽象概念，无法追溯到具体知识点。严格模式确保每条边都连接实际节点，可以：
- 直接整合到现有图谱
- 进行图谱查询和分析
- 可验证和可追溯

### Q: 协调者会频繁打断吗？

A: 不会。只有当智能体引用的节点少于2个，或引用的节点不存在时才会介入。

### Q: 如果LLM不遵守规则怎么办？

A: 系统会检测并提示。但如果持续出现问题，可能需要：
- 调整prompt
- 使用更强的LLM（如GPT-4）
- 降低检查阈值

### Q: 可以用于其他领域吗？

A: 可以！只需提供任意两个领域的知识图谱，系统就能工作。

## 详细文档

- **完整指南**: `STRICT_MODE_GUIDE.md`
- **实现细节**: `IMPLEMENTATION_SUMMARY.md`
- **代码示例**: `examples/strict_knowledge_graph_example.py`

## 总结

严格模式 = 真正的知识图谱增强

- ✅ 基于实际节点ID
- ✅ 协调者克制
- ✅ 输出可验证
- ✅ 格式标准化

**开始使用**：`python examples/strict_knowledge_graph_example.py`

