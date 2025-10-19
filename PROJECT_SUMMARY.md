# 项目摘要

## 科研聊天室 - 基于MAS的跨学科知识关联发现系统

### 项目概述

这是一个完整的多智能体系统（Multi-Agent System, MAS），用于发现不同学科领域之间的潜在知识关联。系统通过让多个具有不同学科背景的AI智能体围绕共同主题进行讨论，从对话中提取和评估跨学科的知识关联。

### 核心特性

✅ **多智能体协同** - 支持多个领域专家智能体同时参与讨论
✅ **多模态数据输入** - 支持文本、PDF、图片、音视频、网页等多种数据类型
✅ **自动关联提取** - 使用元协调智能体自动识别跨领域知识关联
✅ **智能评估系统** - 从语义合理性、知识稀有性、启发潜力三个维度评估关联质量
✅ **结构化输出** - 通过Function Call接口确保输出格式一致性
✅ **完整的Pipeline** - 从数据输入到结果导出的完整工作流

### 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    数据输入层                            │
│  (文本、PDF、图片、音频、视频、网页)                    │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                  对话协同层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ 物理Agent│  │ 文学Agent│  │ 数学Agent│  ...         │
│  └──────────┘  └──────────┘  └──────────┘              │
│         ↓              ↓              ↓                  │
│              ┌─────────────────┐                         │
│              │  元协调Agent     │                         │
│              └─────────────────┘                         │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│               边评估与输出层                             │
│  ┌─────────────┐    ┌──────────────────────┐            │
│  │ 评估Agent   │ →  │  知识图谱 (JSON)      │            │
│  └─────────────┘    │  讨论记录 (JSON)      │            │
│                     │  综合报告 (Markdown)  │            │
│                     └──────────────────────┘            │
└─────────────────────────────────────────────────────────┘
```

### 技术栈

- **AI模型**: Google Gemini 2.0 Flash
- **开发语言**: Python 3.13
- **核心库**: 
  - `google-generativeai` - Gemini API
  - `pydantic` - 数据验证
  - `pypdf` - PDF处理
  - `Pillow` - 图像处理
  - `beautifulsoup4` - 网页解析

### 目录结构

```
Agno/
├── config.py                 # 配置管理
├── main.py                   # 主程序入口
├── core/                     # 核心模块
│   ├── agent.py             # Agent基类
│   ├── chatroom.py          # 聊天室核心
│   ├── edge.py              # 知识边定义
│   └── gemini_client.py     # Gemini API封装
├── agents/                   # 智能体实现
│   ├── domain_agents.py     # 领域专家Agent
│   ├── meta_agent.py        # 元协调Agent
│   └── evaluator_agent.py   # 评估Agent
├── processors/               # 数据处理器
│   ├── text_processor.py
│   ├── pdf_processor.py
│   ├── image_processor.py
│   ├── audio_processor.py
│   ├── video_processor.py
│   └── web_processor.py
├── examples/                 # 示例代码
│   ├── basic_example.py
│   ├── multimodal_example.py
│   └── six_agents_example.py
└── output/                   # 输出目录
```

### 已实现的智能体

1. **PhysicsAgent** (物理学家) - 从物理学角度分析时空、能量、熵等概念
2. **LiteratureAgent** (文学评论家) - 从文学角度分析叙事、隐喻、意义等
3. **MathAgent** (数学家) - 从数学角度分析结构、模式、对称性等
4. **BiologyAgent** (生物学家) - 从生物学角度分析进化、适应、自组织等
5. **PhilosophyAgent** (哲学家) - 从哲学角度分析本质、真理、存在等
6. **ArtAgent** (艺术评论家) - 从艺术角度分析形式、美学、表现等

### 核心类说明

#### Agent (智能体基类)
```python
class Agent:
    def analyze(prompt: str) -> str        # 分析内容
    def discuss(topic: str, context: str) -> str  # 参与讨论
    def load_knowledge(data, type, source)  # 加载知识
```

#### ResearchChatroom (聊天室)
```python
class ResearchChatroom:
    def load_data(agent_name, source, type)  # 加载数据
    def discuss(rounds=3) -> List[Edge]      # 开始讨论
    def export_knowledge_graph(path)         # 导出图谱
    def generate_report() -> str             # 生成报告
```

#### KnowledgeEdge (知识边)
```python
class KnowledgeEdge:
    source_domain: str           # 源领域
    source_concept: str          # 源概念
    target_domain: str           # 目标领域
    target_concept: str          # 目标概念
    relation_type: str           # 关系类型
    confidence: float            # 置信度
    semantic_similarity: float   # 语义相似度
    novelty_score: float         # 新颖度
```

### 使用场景

1. **跨学科研究辅助** - 帮助研究者发现不同领域之间的联系
2. **知识图谱构建** - 自动构建跨领域知识图谱
3. **创新灵感激发** - 通过跨领域类比激发创新思路
4. **教育应用** - 帮助学生理解跨学科概念的联系
5. **文献综述** - 辅助进行跨学科文献分析

### 评估维度

系统从三个维度评估知识关联的质量：

1. **语义合理性** (Semantic Similarity)
   - 关联在逻辑和语义层面是否自洽
   - 概念之间是否存在明确的对应关系

2. **知识稀有性** (Novelty Score)
   - 关联是否具有新颖性
   - 在现有文献中是否较少被提及

3. **启发潜力** (Inspiration Potential)
   - 关联是否能够启发新的研究方向
   - 是否具有理论或应用价值

### 输出格式

#### 知识图谱 (JSON)
```json
{
  "topic": "时间的本质",
  "nodes": [...],
  "edges": [
    {
      "source": {"domain": "物理学", "concept": "熵增原理"},
      "target": {"domain": "文学", "concept": "时间流逝的不可逆性"},
      "relation": {
        "type": "隐喻映射",
        "description": "..."
      },
      "evaluation": {
        "confidence": 0.85,
        "semantic_similarity": 0.78,
        "novelty_score": 0.72
      }
    }
  ]
}
```

#### 综合报告 (Markdown)
- 总体统计
- 综合洞见
- 详细评估
- 每个关联的分析

### 配置选项

在 `config.py` 中可以调整：

- API密钥和模型选择
- 讨论轮次和参与者数量
- 评估阈值
- 输出目录

### 扩展性

系统设计考虑了良好的扩展性：

✅ **添加新的智能体** - 继承Agent类即可
✅ **添加新的数据处理器** - 实现Processor接口
✅ **自定义评估标准** - 扩展EvaluatorAgent
✅ **集成外部知识库** - 通过load_knowledge接口

### 研究价值

这个系统实现了理论报告中提出的核心概念：

1. ✅ 多模态数据驱动的MAS
2. ✅ 自主协作的跨学科对话机制
3. ✅ 知识边的自动提取与评估
4. ✅ 结构化的Function Call输出
5. ✅ 完整的Pipeline实现

### 性能考虑

- 使用Gemini Flash模型，响应速度快
- 批量处理评估，提高效率
- 模块化设计，便于并行处理
- 缓存机制可进一步优化（待实现）

### 下一步优化方向

1. 添加对话缓存机制
2. 实现并行评估
3. 集成外部知识库（如Wikipedia、学术数据库）
4. 添加可视化界面
5. 实现增量式知识图谱更新
6. 添加人工反馈机制

### 许可证

MIT License

---

**开发完成日期**: 2025-10-18
**版本**: 1.0.0

