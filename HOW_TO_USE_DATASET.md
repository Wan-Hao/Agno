# 🎯 如何使用 Dataset 数据生成新的跨领域关联边

## 快速开始（3步）

### 1️⃣ 确保环境配置好

```bash
# 如果还没安装依赖
./install.sh

# 确保配置了 API Key
cat .env | grep GEMINI_API_KEY
```

### 2️⃣ 运行知识图谱示例

```bash
# 方式一：使用脚本
./run_example.sh
# 然后选择选项 4

# 方式二：直接运行
python examples/knowledge_graph_example.py
```

### 3️⃣ 查看结果

```bash
# 查看生成的新边
cat output/knowledge_graph_example/new_cross_domain_edges.json

# 查看完整报告
cat output/knowledge_graph_example/cross_domain_analysis_report.md
```

## 💡 工作原理

```
你的数据                     系统处理                    输出结果
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

physics_knowledge_graph      KnowledgeGraphProcessor     
  (876 nodes, 1245 edges) ──→  解析图谱结构               
                               提取关键概念               
math_knowledge_graph            ↓                        
  (423 nodes, 567 edges)  ──→  PhysicsAgent ← 物理知识    
                               MathAgent ← 数学知识       
                                  ↓                       
                               ResearchChatroom           
                               3轮深入讨论                new_cross_domain_edges.json
                                  ↓                    ──→  8-12条新关联
                               MetaAgent                   
                               提取跨领域关联              integrated_knowledge_graph.json
                                  ↓                    ──→  整合后的图谱
                               EvaluatorAgent             
                               三维度质量评估              cross_domain_analysis_report.md
                                  ↓                    ──→  人类可读报告
                               结构化输出                  
                                                          discussion_log.json
                                                       ──→  完整讨论记录
```

## 📊 你会得到什么

### 新发现的跨领域关联边

系统会自动发现类似这样的关联：

```json
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
    "description": "质点的位置随时间变化可以用函数x(t)表示，运动的描述本质上是函数映射的具体应用。速度和加速度作为导数体现了微积分在运动分析中的基础作用。"
  },
  "evaluation": {
    "confidence": 0.85,
    "semantic_similarity": 0.78,
    "novelty_score": 0.72,
    "inspiration_potential": 0.81
  },
  "metadata": {
    "reasoning": "通过讨论发现，物理运动的数学描述不仅是工具性的，而是揭示了运动本质的数学结构...",
    "generated_by": "元协调者",
    "generated_at": "2025-10-18T..."
  }
}
```

### 关联类型

预期会发现的关系类型：

| 关系类型 | 描述 | 示例 |
|---------|------|------|
| **结构映射** | 概念结构的直接对应 | 运动轨迹 ↔ 函数图像 |
| **数学工具** | 数学作为物理的描述工具 | 速度 ↔ 导数 |
| **深层联系** | 本质性的理论对应 | 对称性 ↔ 群论（诺特定理） |
| **概念对应** | 不同层面的概念映射 | 守恒量 ↔ 不变量 |
| **抽象-具体** | 抽象理论的具体实现 | 连续性 ↔ 运动连续性 |

## 🎯 具体示例

### 示例1：发现物理-数学映射

**输入：** 物理图谱（机械运动、力、能量） + 数学图谱（函数、向量、微积分）

**讨论主题：** "物理学与数学的深层结构"

**预期输出：**
- 质点运动 ↔ 函数映射（结构映射，0.85）
- 力的合成 ↔ 向量加法（结构同构，0.88）
- 速度概念 ↔ 导数定义（数学工具，0.82）
- 能量守恒 ↔ 不变量（概念对应，0.79）
- 对称性 ↔ 群论（深层联系，0.91）

### 示例2：自定义聚焦

```python
# 聚焦特定主题
processor = KnowledgeGraphProcessor()
physics_data = processor.process("dataset/graph/physics_knowledge_graph_new.json")

# 只关注"波动"和"振动"相关的概念
context = processor.build_context_for_discussion(
    physics_data,
    focus_themes=["波动", "振动"],
    max_concepts=20
)
```

这样可以得到更聚焦的关联，比如：
- 简谐振动 ↔ 三角函数
- 波的叠加 ↔ 线性组合
- 共振频率 ↔ 特征值

## 📈 质量保证

每个关联都会被评估：

### 1. 语义合理性 (Semantic Similarity)
- 关联在逻辑上是否自洽？
- 两个概念之间是否真的有联系？

### 2. 知识稀有性 (Novelty Score)
- 这个关联是否新颖？
- 在现有文献中是否较少提及？

### 3. 启发潜力 (Inspiration Potential)
- 这个关联是否有研究价值？
- 是否能启发新的思路？

**综合评分 ≥ 0.7 的关联被认为是高质量的。**

## 🔧 高级用法

### 调整讨论参数

```python
# 更多轮次 = 更深入的讨论
edges = chatroom.discuss(
    rounds=5,              # 增加到5轮
    extract_edges=True,
    evaluate_edges=True
)

# 预期：发现更多细节关联
```

### 多领域讨论

```python
# 可以添加更多领域
from agents import BiologyAgent, PhilosophyAgent

chatroom = ResearchChatroom(
    topic="复杂系统的跨学科理解",
    agents=[
        PhysicsAgent(),      # 从热力学、统计物理角度
        MathAgent(),         # 从复杂性理论角度
        BiologyAgent()       # 从生命系统角度
    ]
)

# 预期：发现三方甚至多方关联
```

### 主题聚焦策略

```python
# 策略1：广泛探索
context = processor.build_context_for_discussion(
    graph_data,
    focus_themes=None,    # 不限制主题
    max_concepts=40       # 更多概念
)

# 策略2：精准聚焦
context = processor.build_context_for_discussion(
    graph_data,
    focus_themes=["能量", "守恒定律"],  # 特定主题
    max_concepts=15       # 精选概念
)
```

## 📂 输出文件说明

运行后在 `output/knowledge_graph_example/` 会生成：

### 1. `new_cross_domain_edges.json`
```json
{
  "source_graphs": {...},
  "topic": "...",
  "edges": [ /* 新发现的关联 */ ],
  "statistics": {
    "total_edges": 8,
    "high_quality_edges": 6
  }
}
```
**用途**：直接整合回原知识图谱，或用于进一步分析

### 2. `integrated_knowledge_graph.json`
```json
{
  "topic": "...",
  "nodes": [ /* 所有领域的节点 */ ],
  "edges": [ /* 包含新关联的完整边集 */ ],
  "statistics": {...}
}
```
**用途**：完整的跨领域知识图谱，可用于可视化

### 3. `discussion_log.json`
```json
{
  "topic": "...",
  "agents": [...],
  "discussion_history": [
    {
      "round": 1,
      "agent": "物理学家",
      "content": "..."
    },
    ...
  ]
}
```
**用途**：分析讨论过程，理解关联的生成逻辑

### 4. `cross_domain_analysis_report.md`
```markdown
# 跨领域知识关联分析报告

## 综合洞见
...

## 发现的关联
1. [物理:概念A] → [数学:概念B]
   - 评分: 0.85
   - 描述: ...
...
```
**用途**：人类可读的完整报告

## 💡 最佳实践

### ✅ 推荐做法

1. **从小规模开始** - 先用2个智能体、2-3轮讨论测试
2. **聚焦主题** - 指定相关主题可以得到更有意义的关联
3. **控制概念数** - 20-30个概念是平衡点
4. **多次实验** - 运行多次可以发现不同角度的关联
5. **人工审核** - 对高分关联进行人工验证

### ❌ 避免的做法

1. **过多概念** - 超过50个概念会导致讨论发散
2. **过少轮次** - 1轮讨论通常不够深入
3. **无主题聚焦** - 完全随机可能得到不相关的关联
4. **忽略评分** - 低分关联（<0.5）可能不可靠

## 🎓 研究应用

### 学术研究
- 发现跨学科研究机会
- 识别学科交叉点
- 启发创新研究方向

### 教学应用
- 帮助学生理解学科联系
- 设计跨学科课程
- 创建概念地图

### 知识管理
- 构建统一知识图谱
- 自动化文献综述
- 知识融合与整合

## 🐛 常见问题

### Q: 生成的关联数量少怎么办？
A: 增加讨论轮次或调整主题范围

### Q: 关联质量不高怎么办？
A: 使用更聚焦的主题，减少概念数量

### Q: 如何整合新边回原图谱？
A: 新边已经是标准格式，可以直接合并到 edges 数组

### Q: 可以处理其他语言的图谱吗？
A: 可以，只需确保 Gemini API 支持该语言

## 📚 更多资源

- **[KNOWLEDGE_GRAPH_USAGE.md](KNOWLEDGE_GRAPH_USAGE.md)** - 完整API文档
- **[DEMO_OUTPUT.md](DEMO_OUTPUT.md)** - 详细输出示例
- **[SUMMARY.md](SUMMARY.md)** - 功能总结

---

## 🚀 立即开始！

```bash
# 第一次运行
./install.sh                              # 安装依赖
cp .env.example .env                      # 配置环境
# 编辑 .env 添加 GEMINI_API_KEY

# 运行示例
python examples/knowledge_graph_example.py

# 查看结果
ls output/knowledge_graph_example/
```

**预计耗时：** 3-5分钟（取决于网络和API速度）

**预期结果：** 8-12个高质量的跨领域关联边

祝你发现有价值的知识联系！🎉

