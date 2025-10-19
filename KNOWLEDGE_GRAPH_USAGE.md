# 使用知识图谱数据生成新边

## 概述

本系统现在支持从已有的知识图谱数据中提取知识，让智能体基于这些知识进行讨论，从而发现新的跨领域知识关联。

## 🎯 使用场景

你有两个知识图谱：
- `dataset/graph/physics_knowledge_graph_new.json` (3992行，物理学知识)
- `dataset/graph/math_knowledge_graph_new.json` (1650行，数学知识)

通过科研聊天室系统，让物理学家和数学家智能体基于这些知识讨论，发现它们之间的深层联系。

## 📦 新增组件

### 1. 知识图谱处理器 (`processors/knowledge_graph_processor.py`)

功能：
- ✅ 加载和解析知识图谱JSON文件
- ✅ 提取节点和边信息
- ✅ 构建知识摘要
- ✅ 根据主题筛选概念
- ✅ 为讨论构建上下文

主要方法：
```python
from processors import KnowledgeGraphProcessor

processor = KnowledgeGraphProcessor()

# 加载知识图谱
graph_data = processor.process("dataset/graph/physics_knowledge_graph_new.json")

# 构建讨论上下文
context = processor.build_context_for_discussion(
    graph_data,
    focus_themes=["机械运动与物理模型", "能量"],
    max_concepts=30
)
```

### 2. 知识图谱示例程序 (`examples/knowledge_graph_example.py`)

完整的工作流程：
1. 加载物理和数学知识图谱
2. 为每个智能体构建专门的知识上下文
3. 创建跨学科讨论
4. 提取新发现的关联边
5. 评估边的质量
6. 导出结果

## 🚀 快速使用

### 方式一：使用运行脚本

```bash
./run_example.sh
# 选择选项 4 - 知识图谱示例
```

### 方式二：直接运行

```bash
python examples/knowledge_graph_example.py
```

### 方式三：编程方式

```python
from core.chatroom import ResearchChatroom
from agents import PhysicsAgent, MathAgent
from processors import KnowledgeGraphProcessor
from pathlib import Path

# 1. 加载知识图谱
processor = KnowledgeGraphProcessor()
physics_data = processor.process("dataset/graph/physics_knowledge_graph_new.json")
math_data = processor.process("dataset/graph/math_knowledge_graph_new.json")

# 2. 创建智能体
physics_agent = PhysicsAgent()
math_agent = MathAgent()

# 3. 为智能体加载知识
physics_context = processor.build_context_for_discussion(
    physics_data,
    focus_themes=["机械运动与物理模型", "相互作用", "能量"],
    max_concepts=25
)
physics_agent.load_knowledge(
    data=physics_context,
    data_type="knowledge_graph",
    source="physics_knowledge_graph"
)

math_context = processor.build_context_for_discussion(
    math_data,
    focus_themes=["集合", "函数", "几何"],
    max_concepts=25
)
math_agent.load_knowledge(
    data=math_context,
    data_type="knowledge_graph",
    source="math_knowledge_graph"
)

# 4. 创建聊天室并讨论
chatroom = ResearchChatroom(
    topic="物理学与数学的深层结构关联",
    agents=[physics_agent, math_agent]
)

# 5. 开始讨论并提取新边
new_edges = chatroom.discuss(
    rounds=3,
    extract_edges=True,
    evaluate_edges=True
)

# 6. 导出结果
chatroom.export_knowledge_graph("output/new_integrated_graph.json")
print(f"发现 {len(new_edges)} 个新的跨领域关联！")
```

## 📊 输出结果

运行后会在 `output/knowledge_graph_example/` 目录下生成：

### 1. `new_cross_domain_edges.json`
新发现的跨领域知识关联：
```json
{
  "source_graphs": {
    "physics": "dataset/graph/physics_knowledge_graph_new.json",
    "math": "dataset/graph/math_knowledge_graph_new.json"
  },
  "topic": "物理学与数学的深层结构：从运动、空间到抽象",
  "edges": [
    {
      "source": {
        "domain": "物理学",
        "concept": "质点运动"
      },
      "target": {
        "domain": "数学",
        "concept": "函数映射"
      },
      "relation": {
        "type": "结构映射",
        "description": "质点的运动轨迹可以用函数来描述..."
      },
      "evaluation": {
        "confidence": 0.85,
        "semantic_similarity": 0.78,
        "novelty_score": 0.72
      }
    }
    // ... 更多边
  ],
  "statistics": {
    "total_edges": 12,
    "high_quality_edges": 8
  }
}
```

### 2. `integrated_knowledge_graph.json`
整合后的完整知识图谱，包含原始数据和新发现的关联

### 3. `discussion_log.json`
完整的讨论历史记录

### 4. `cross_domain_analysis_report.md`
综合分析报告：
- 讨论摘要
- 发现的关联列表
- 质量评估
- 洞见分析

## 🎯 工作原理

### 数据流程

```
知识图谱JSON文件
       ↓
KnowledgeGraphProcessor
  - 解析节点和边
  - 提取关键概念
  - 构建上下文
       ↓
智能体知识加载
  - PhysicsAgent ← 物理知识
  - MathAgent ← 数学知识
       ↓
ResearchChatroom讨论
  - 多轮对话
  - 主题聚焦
  - 概念碰撞
       ↓
MetaAgent提取关联
  - 识别跨领域联系
  - 生成知识边
       ↓
EvaluatorAgent评估
  - 语义合理性
  - 知识稀有性
  - 启发潜力
       ↓
输出新的知识边
  - JSON格式
  - 结构化数据
  - 可视化报告
```

### 关键特性

1. **智能上下文构建**
   - 根据主题自动筛选相关概念
   - 控制输入的概念数量，避免过载
   - 保留概念的完整描述

2. **多轮深入讨论**
   - 第一轮：各自表达领域视角
   - 第二轮：寻找概念对应
   - 第三轮：提炼深层联系

3. **自动关联提取**
   - MetaAgent监控讨论
   - 识别概念映射
   - 生成结构化的边数据

4. **三维度评估**
   - 语义合理性：逻辑自洽性
   - 知识稀有性：新颖程度
   - 启发潜力：研究价值

## 📈 预期结果示例

基于你的数据，系统可能发现的跨领域关联：

### 物理 → 数学

| 物理概念 | 数学概念 | 关系类型 | 描述 |
|---------|---------|---------|------|
| 质点运动 | 函数映射 | 结构映射 | 位置随时间变化可用函数表示 |
| 力的合成 | 向量加法 | 数学建模 | 力的合成遵循向量加法规则 |
| 能量守恒 | 不变量 | 概念对应 | 守恒量对应数学中的不变量 |
| 参考系变换 | 坐标变换 | 数学工具 | 物理参考系变换是坐标变换 |
| 周期运动 | 周期函数 | 函数描述 | 周期运动用周期函数建模 |

### 数学 → 物理

| 数学概念 | 物理概念 | 关系类型 | 描述 |
|---------|---------|---------|------|
| 连续性 | 运动连续性 | 抽象-具体 | 数学连续性在物理中体现为运动的连续 |
| 微分 | 瞬时速率 | 工具应用 | 微分用于计算瞬时速度 |
| 积分 | 累积效应 | 工具应用 | 积分计算位移、功等累积量 |
| 对称性 | 守恒定律 | 深层对应 | 数学对称性对应物理守恒定律（诺特定理） |
| 线性空间 | 力学系统 | 结构同构 | 力学系统状态空间是线性空间 |

## 🔧 高级用法

### 自定义主题聚焦

```python
# 聚焦特定主题
physics_context = processor.build_context_for_discussion(
    physics_data,
    focus_themes=["波动", "振动", "能量"],  # 自定义主题
    max_concepts=20
)
```

### 调整讨论策略

```python
chatroom = ResearchChatroom(
    topic="波动现象的数学本质",
    agents=[physics_agent, math_agent]
)

# 更多轮次，更深入讨论
edges = chatroom.discuss(rounds=5)
```

### 批量处理多个图谱

```python
# 可以扩展到更多领域
from agents import BiologyAgent, PhilosophyAgent

# 加载更多知识图谱并进行三方或多方讨论
chatroom = ResearchChatroom(
    topic="复杂系统的跨学科理解",
    agents=[physics_agent, math_agent, biology_agent]
)
```

## 💡 使用建议

1. **聚焦主题**：指定相关的主题，让讨论更聚焦
2. **控制概念数量**：20-30个概念是较好的平衡点
3. **多轮讨论**：3-5轮可以得到较深入的洞见
4. **质量筛选**：关注评分≥0.7的高质量关联

## 🎓 研究价值

这个系统可以用于：

1. **知识图谱融合**：自动发现不同领域知识图谱之间的连接
2. **跨学科研究**：辅助研究者发现学科交叉点
3. **教学应用**：帮助学生理解不同学科的内在联系
4. **文献分析**：从多学科文献中提取隐含关联
5. **创新启发**：通过类比激发新的研究思路

## 📝 注意事项

1. **API配置**：确保在`.env`中设置了`GEMINI_API_KEY`
2. **数据路径**：确保知识图谱文件存在于`dataset/graph/`目录
3. **输出目录**：结果会自动保存到`output/knowledge_graph_example/`
4. **讨论时间**：3轮讨论大约需要3-5分钟（取决于网络和API速度）

## 🚀 下一步

运行示例后，你可以：

1. 查看生成的新边数据
2. 分析哪些关联最有价值
3. 将新边整合回原始知识图谱
4. 使用可视化工具展示关联网络
5. 基于发现的关联进行深入研究

---

**准备好了吗？运行命令开始吧！**

```bash
python examples/knowledge_graph_example.py
```

