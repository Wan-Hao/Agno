# Agno - 跨学科知识图谱融合系统

基于多智能体协作的知识图谱跨学科关联发现系统。通过让物理学家和数学家Agent进行节点对节点的讨论，自动发现并提取跨学科知识边。

## ✨ 核心特性

- 🎯 **节点对节点讨论**：每次讨论聚焦一对具体节点，精确可验证
- 🤖 **多Agent协作**：4个专业Agent分工协作（物理学家、数学家、元协调者、评估专家）
- 📊 **完整上下文**：携带节点完整properties和学科内相关知识
- ✅ **质量保证**：评估Agent筛选，只保留高质量边
- 💾 **增量构建**：通过Function Call实时写入JSON

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/your-username/Agno.git
cd Agno

# 安装依赖
pip install -r requirements.txt

# 配置API Key
cp .env.example .env
# 编辑.env文件，填入你的GEMINI_API_KEY或OPENAI_API_KEY
```

### 运行小示例 (推荐首次使用)

**耗时**: ~2-3分钟  
**讨论**: 10对节点  
**预期输出**: 3-5条边

```bash
python run_small_sample.py
```

查看结果：
```bash
cat output/demo_10_pairs/cross_domain_edges.json
```

### 运行完整示例

**耗时**: ~5分钟  
**讨论**: 6对预定义节点  

```bash
python examples/node_pair_discussion_example.py
```

查看结果：
```bash
cat output/node_pair_example/cross_domain_edges.json
```

## 📊 使用方式

### 方式1: 小规模采样 (5-30分钟)

```bash
python examples/sampled_cartesian_discussion.py
```

然后选择采样策略：
- `1` - 随机采样100对 (约5分钟)
- `2` - 基于关键词采样 (约10分钟)
- `3` - 基于主题筛选 (约10-30分钟)
- `4` - 自定义数量

### 方式2: 全遍历 (1-3天)

遍历所有数学×物理节点对 (105 × 169 = 17,745对)

```bash
# 后台运行
nohup python examples/full_cartesian_discussion.py > cartesian.log 2>&1 &

# 查看进度
tail -f cartesian.log

# 或查看进度百分比
cat output/full_cartesian/progress.json
```

**特性**：
- ✅ 支持断点续传 (Ctrl+C中断后可继续)
- ✅ 自动保存进度 (每10对保存一次)
- ✅ 预计输出5,000-8,000条高质量边

## 📁 输出格式

所有模式输出相同的JSON格式：

```json
{
  "metadata": {
    "source_graphs": {
      "physics": "physics_knowledge_graph_new.json",
      "math": "math_knowledge_graph_new.json"
    },
    "total_edges": 5,
    "last_updated": "2025-10-19T..."
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
    }
  ]
}
```

## 🏗️ 系统架构

### 4个协作Agent

| Agent | 角色 | 职责 |
|-------|------|------|
| **PhysicsAgent** | 物理学家 | 从物理角度分析节点关联 |
| **MathAgent** | 数学家 | 从数学角度回应和分析 |
| **MetaAgent** | 元协调者 | 检查偏离、提取边 |
| **EvaluatorAgent** | 评估专家 | 评估边的质量，决定保留 |

### 工作流程

```
1. 构建上下文 (节点完整properties + 学科内相关知识)
   ↓
2. PhysicsAgent 分析
   ↓
3. MathAgent 回应
   ↓
4. MetaAgent 检查是否偏离 (仅在偏离时介入)
   ↓
5. MetaAgent 提取边
   ↓
6. EvaluatorAgent 评估 (决定保留或拒绝)
   ↓
7. Function Call 写入JSON
```

## 📂 项目结构

```
Agno/
├── core/                           # 核心模块
│   ├── node_pair_chatroom.py      # 主要实现 ⭐
│   ├── agent.py                   # 基础Agent类
│   ├── edge.py                    # 边数据模型
│   └── gemini_client.py           # API客户端
│
├── agents/                         # 智能体
│   ├── domain_agents.py           # PhysicsAgent, MathAgent
│   ├── meta_agent.py              # 元协调者
│   └── evaluator_agent.py         # 评估专家
│
├── examples/                       # 示例脚本
│   ├── node_pair_discussion_example.py      # 完整示例
│   ├── sampled_cartesian_discussion.py      # 采样模式
│   └── full_cartesian_discussion.py         # 全遍历模式
│
├── dataset/graph/                  # 知识图谱数据
│   ├── physics_knowledge_graph_new.json     # 169个物理节点
│   └── math_knowledge_graph_new.json        # 105个数学节点
│
├── output/                         # 输出目录
│   ├── demo_10_pairs/             # 小示例输出
│   ├── node_pair_example/         # 完整示例输出
│   ├── sampled_cartesian/         # 采样输出
│   └── full_cartesian/            # 全遍历输出
│
├── run_small_sample.py            # 快速测试脚本 ⭐
├── requirements.txt               # 依赖列表
├── .env.example                   # 环境变量模板
└── README.md                      # 本文件
```

## 💡 核心设计

### 为什么用节点对讨论？

```
❌ 主题式讨论: "讨论运动与函数的关系"
   - 太宽泛，难以聚焦
   - 输出的边不精确

✅ 节点对讨论: "[displacement_velocity_acceleration] ↔ [function_definition_and_elements]"
   - 精确聚焦具体知识点
   - 输出的边可验证、可追溯
```

### 为什么需要4个Agent？

```
单Agent方案 ❌
  └─ 无法同时具备：领域专业知识 + 跨学科视角 + 客观评估

多Agent方案 ✅
  ├─ PhysicsAgent:  深度物理知识
  ├─ MathAgent:     深度数学知识
  ├─ MetaAgent:     跨学科提取能力
  └─ EvaluatorAgent: 客观评估标准
```

### 为什么需要完整properties？

每个节点的properties包含：
- `description`: 详细描述
- `category`: 所属类别
- `theme`: 主题
- `cultivated_abilities`: 培养的能力
- `stage/course_nature`: 课程性质

→ Agent拥有更多上下文，做出更准确的判断

## 📈 性能数据

| 指标 | 数值 |
|------|------|
| 总节点对数 | 105 × 169 = 17,745 |
| 每对讨论时间 | 3-5秒 |
| API调用/对 | 4次 (Physics + Math + Meta + Evaluator) |
| 有效边比例 | 30-50% |
| 全遍历预计时间 | 14-48小时 |
| 预期输出边数 | 5,000-8,000条 |

## 🔧 配置选项

### 上下文深度

```python
context_depth = 1  # 包含1层相关节点 (推荐)
context_depth = 2  # 包含2层相关节点 (更丰富，但token消耗大)
```

### 采样策略

```python
# 1. 随机采样
random_sample(math_nodes, physics_nodes, n=100)

# 2. 关键词匹配
keyword_based_sample(keywords=["运动", "函数", "变化"])

# 3. 主题筛选
theme_based_sample(
    math_themes=["函数"],
    physics_themes=["机械运动"]
)
```

## 📚 文档

- **快速参考**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **系统架构**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **系统总览**: [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)
- **节点对模式**: [NODE_PAIR_DISCUSSION_GUIDE.md](NODE_PAIR_DISCUSSION_GUIDE.md)
- **笛卡尔积讨论**: [CARTESIAN_DISCUSSION_GUIDE.md](CARTESIAN_DISCUSSION_GUIDE.md)

## 🎯 使用场景

### 1. 教育研究
- 发现跨学科教学联系
- 构建学科融合课程
- 分析知识点依赖关系

### 2. 知识图谱增强
- 自动发现跨领域边
- 丰富知识图谱连接
- 验证和补充专家标注

### 3. AI辅助研究
- 探索学科交叉点
- 发现隐藏的概念联系
- 生成研究假设

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- 基于物理和数学高中知识图谱数据
- 使用Gemini/OpenAI API进行多智能体协作

## 📞 联系方式

- GitHub Issues: [提交问题](https://github.com/your-username/Agno/issues)
- Email: your-email@example.com

---

**⭐ 如果这个项目对您有帮助，请给个Star！**
