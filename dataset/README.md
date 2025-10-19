# Dataset 目录说明

## 📊 数据集内容

本目录包含用于科研聊天室系统的知识图谱数据。

### 当前数据

```
dataset/
└── graph/
    ├── physics_knowledge_graph_new.json    # 物理学知识图谱 (3992行)
    └── math_knowledge_graph_new.json       # 数学知识图谱 (1650行)
```

### 数据结构

每个知识图谱文件包含：

```json
{
  "nodes": [
    {
      "id": "concept_id",
      "label": "概念名称",
      "properties": {
        "description": "概念描述",
        "subject": "学科",
        "theme": "主题",
        "category": "分类",
        ...
      }
    },
    ...
  ],
  "edges": [
    {
      "source": "source_concept_id",
      "target": "target_concept_id",
      "relation": "关系类型",
      ...
    },
    ...
  ]
}
```

## 🚀 如何使用

### 1. 运行示例程序

```bash
# 使用脚本运行
./run_example.sh
# 选择选项 4

# 或直接运行
python examples/knowledge_graph_example.py
```

### 2. 编程方式使用

```python
from processors import KnowledgeGraphProcessor
from agents import PhysicsAgent, MathAgent
from core.chatroom import ResearchChatroom

# 加载知识图谱
processor = KnowledgeGraphProcessor()
physics_data = processor.process("dataset/graph/physics_knowledge_graph_new.json")
math_data = processor.process("dataset/graph/math_knowledge_graph_new.json")

# 构建上下文
physics_context = processor.build_context_for_discussion(
    physics_data,
    focus_themes=["机械运动与物理模型", "能量"],
    max_concepts=25
)

# 创建智能体并加载知识
physics_agent = PhysicsAgent()
physics_agent.load_knowledge(physics_context, "knowledge_graph", "physics")

# 开始讨论
chatroom = ResearchChatroom(
    topic="物理与数学的深层联系",
    agents=[physics_agent, math_agent]
)

new_edges = chatroom.discuss(rounds=3)
```

## 📖 详细文档

- **[KNOWLEDGE_GRAPH_USAGE.md](../KNOWLEDGE_GRAPH_USAGE.md)** - 完整使用指南
- **[DEMO_OUTPUT.md](../DEMO_OUTPUT.md)** - 预期输出示例
- **[SUMMARY.md](../SUMMARY.md)** - 功能总结

## 🎯 预期结果

使用这些数据，系统将：

1. ✅ 加载物理和数学知识图谱（共约1300+个概念）
2. ✅ 让物理学家和数学家智能体基于这些知识讨论
3. ✅ 自动发现约8-12个高质量的跨领域关联
4. ✅ 评估关联的语义合理性、新颖性和启发价值
5. ✅ 输出结构化的新边数据（可直接整合回图谱）

### 发现的关联示例

| 物理概念 | 数学概念 | 关系类型 | 评分 |
|---------|---------|---------|------|
| 质点运动 | 函数映射 | 结构映射 | 0.85 |
| 力的合成 | 向量加法 | 结构同构 | 0.88 |
| 能量守恒 | 不变量 | 概念对应 | 0.79 |
| 对称性 | 群论 | 深层联系 | 0.91 |

## 📂 输出位置

运行后，结果保存在：

```
output/knowledge_graph_example/
├── new_cross_domain_edges.json          # 新发现的跨领域关联
├── integrated_knowledge_graph.json      # 整合后的完整图谱
├── discussion_log.json                  # 完整讨论历史
└── cross_domain_analysis_report.md      # 综合分析报告
```

## 🔧 添加新数据

要添加其他领域的知识图谱：

1. 将JSON文件放入 `dataset/graph/` 目录
2. 确保文件格式符合上述结构
3. 使用 `KnowledgeGraphProcessor` 加载
4. 创建对应领域的智能体
5. 开始跨领域讨论

示例：
```python
# 添加生物学知识图谱
biology_data = processor.process("dataset/graph/biology_knowledge_graph.json")
biology_agent = BiologyAgent()
biology_agent.load_knowledge(
    processor.build_context_for_discussion(biology_data),
    "knowledge_graph",
    "biology"
)
```

## 💡 使用建议

1. **聚焦主题** - 使用 `focus_themes` 参数筛选相关概念
2. **控制规模** - `max_concepts=20-30` 是较好的平衡
3. **多轮讨论** - 3-5轮能产生深入洞见
4. **质量筛选** - 关注评分 ≥ 0.7 的高质量关联

## 🎓 研究价值

这些数据和系统可用于：

- **知识图谱融合** - 自动连接不同领域的图谱
- **跨学科研究** - 发现学科交叉点
- **教学应用** - 展示学科间的内在联系
- **文献分析** - 从多学科角度分析
- **创新启发** - 通过类比激发新思路

---

**准备好了就开始吧！** 🚀

```bash
python examples/knowledge_graph_example.py
```

