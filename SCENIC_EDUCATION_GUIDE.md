# 景点教育知识点关联系统使用指南

## 📚 概述

这个系统可以从旅游景点中自动提取教学知识点，将真实的景点场景与学科知识（数学、物理等）建立关联，生成可用于教学的素材。

## 🎯 核心功能

### 1. 景点智能体 (`ScenicSpotAgent`)
- 从JSON文件加载景点数据
- 分析景点的教学潜力
- 引导学科专家发现知识点

### 2. 教育知识边 (`EducationalEdge`)
- 标准化的输出格式
- 包含完整的知识点信息（章节、公式、难度等）
- 符合教学大纲要求

### 3. 教育聊天室 (`EducationalChatroom`)
- 三方协作：景点专家 + 物理专家 + 数学专家
- 自动提取教学知识点
- 导出标准化JSON格式

## 📋 输出格式

```json
{
  "province_city": "上海市",
  "scenic_spot": "上海中心大厦",
  "name": "上海中心大厦采用螺旋上升的外立面设计，外立面扭转约120度。这个扭转设计不仅美观，更重要的是为了应对高空风力。随着高度增加，建筑受到的风压呈非线性增长，扭转设计可以有效减少风阻。这体现了流体力学中的伯努利原理和压力分布理论。",
  "stage": "高中",
  "subject": "物理",
  "knowledge_point": {
    "chapter_number": 8,
    "chapter_title": "流体力学基础",
    "section_number": "8.2",
    "section_title": "流体的阻力",
    "point_name": "空气阻力与物体形状的关系",
    "description": "理解物体在流体中运动时受到的阻力，掌握减小阻力的方法",
    "formula": "F_阻 = ½ρv²CdA",
    "difficulty": "中等偏上",
    "applications": ["建筑设计", "车辆设计", "空气动力学"]
  },
  "reasoning": "超高建筑的抗风设计是流体力学的经典应用，学生可以直观理解理论在实际中的价值",
  "confidence": 0.9
}
```

## 🚀 快速开始

### 方法1: 快速演示（推荐新手）

```bash
# 分析单个景点，快速看到效果
python examples/quick_scenic_demo.py
```

这会分析上海中心大厦，提取高中数学和物理知识点。

### 方法2: 完整示例

```bash
# 分析多个景点，生成完整数据集
python examples/scenic_educational_example.py
```

### 方法3: 自定义代码

```python
from core.educational_chatroom import EducationalChatroom

# 创建聊天室
chatroom = EducationalChatroom()

# 加载景点数据
chatroom.load_scenic_spots("dataset/senarios/shanghai.json")

# 分析单个景点
edges = chatroom.discover_educational_edges(
    spot_index=2,           # 景点索引
    target_stage="高中",    # 目标学段
    target_subjects=["数学", "物理"]  # 目标学科
)

# 导出结果
chatroom.export_results("output/educational_edges.json")
```

## 📊 数据流程

```
景点JSON
    ↓
景点专家分析教学潜力
    ↓
物理/数学专家提取具体知识点
    ↓
生成教育知识边
    ↓
导出标准JSON格式
```

## 🎓 支持的学段和学科

### 学段
- 小学
- 初中
- **高中**（默认）
- 大学

### 学科
- **数学**（几何、代数、统计等）
- **物理**（力学、光学、热学、流体等）
- 化学（规划中）
- 生物（规划中）

## 📝 景点数据格式

输入的景点JSON格式：

```json
[
  {
    "province_city": "上海市",
    "scenic_spot": "东方明珠电视塔",
    "description": "东方明珠电视塔位于上海浦东新区陆家嘴核心地带，是上海乃至中国极具标志性的高塔之一。塔高约468米..."
  }
]
```

## 🔧 高级配置

### 自定义学科Agent

```python
from agents.domain_agents import PhysicsAgent, MathAgent
from core.educational_chatroom import EducationalChatroom

# 创建自定义配置的Agent
physics_agent = PhysicsAgent(name="高中物理教师")
math_agent = MathAgent(name="高中数学教师")

# 创建聊天室
chatroom = EducationalChatroom(
    physics_agent=physics_agent,
    math_agent=math_agent
)
```

### 批量处理多个景点

```python
# 分析所有景点
all_edges = chatroom.discover_all_spots(
    target_stage="高中",
    target_subjects=["数学", "物理"],
    max_spots=10  # 最多处理10个景点
)

# 按学科筛选
math_edges = chatroom.edge_builder.filter_by_subject("数学")
physics_edges = chatroom.edge_builder.filter_by_subject("物理")
```

### 查看统计信息

```python
stats = chatroom.get_statistics()
print(f"总知识点数: {stats['total_edges']}")
print(f"按学科: {stats['by_subject']}")
print(f"按难度: {stats['by_difficulty']}")
```

## 📦 输出文件

运行后会在 `output/` 目录生成：

- `educational_edges/shanghai_scenic_knowledge.json` - 所有知识点
- `demo_educational_edge.json` - 快速演示结果

## 💡 应用场景

1. **教学设计**：为老师提供真实场景的教学素材
2. **研学旅行**：设计基于景点的学习任务
3. **教材编写**：丰富教材中的实际案例
4. **在线教育**：制作景点知识点视频课程
5. **博物馆教育**：设计互动式学习体验

## 🎯 知识点质量标准

系统提取的知识点符合以下标准：

1. ✅ **准确性**：知识点符合教学大纲
2. ✅ **关联性**：与景点特征有明确对应
3. ✅ **适用性**：适合目标学段的学生
4. ✅ **可操作性**：可以基于景点实际讲解
5. ✅ **完整性**：包含章节、公式、应用等完整信息

## 🔍 示例知识点

### 数学示例：豫园 → 几何对称

```json
{
  "scenic_spot": "豫园",
  "name": "豫园的亭台楼阁、假山池塘、曲径回廊展现了中国古典园林的对称美学。主要建筑沿中轴线对称分布，左右两侧的亭台、廊桥、假山形成镜像关系。这种轴对称设计不仅美观，还体现了中国传统文化中的平衡理念。",
  "subject": "数学",
  "knowledge_point": {
    "point_name": "轴对称与中心对称",
    "chapter_title": "图形的对称",
    "formula": "对称点关于对称轴距离相等"
  }
}
```

### 物理示例：外滩 → 光的反射

```json
{
  "scenic_spot": "外滩",
  "name": "夜晚的外滩，黄浦江水面如镜，对岸浦东的高楼灯光在江面形成清晰的倒影。这是光的反射现象，江面相当于一个平面镜，入射光线与反射光线的夹角满足反射定律。",
  "subject": "物理",
  "knowledge_point": {
    "point_name": "光的反射定律",
    "chapter_title": "光现象",
    "formula": "入射角 = 反射角"
  }
}
```

## 🛠️ 故障排查

### 问题1：没有提取到知识点

**可能原因**：
- 景点描述不够详细
- 目标学段设置不合适

**解决方法**：
- 补充景点描述中的技术细节
- 调整 `target_stage` 参数

### 问题2：知识点质量不高

**可能原因**：
- Agent的system_instruction不够具体

**解决方法**：
- 自定义Agent的指令
- 增加讨论轮次 `rounds=3`

## 📚 相关文档

- `README.md` - 项目总览
- `QUICK_START_STRICT_MODE.md` - 严格模式指南
- `HOW_TO_USE_DATASET.md` - 数据集使用

## 🤝 贡献

欢迎贡献更多景点数据和知识点提取策略！

## 📄 许可

与主项目相同的许可协议。


