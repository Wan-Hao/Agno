# 🚀 景点教育系统 - 快速参考

## 一分钟了解

**这是什么？**
一个AI系统，能从旅游景点中自动提取教学知识点，生成结构化的教育素材。

**输入** → **输出**
```
景点描述 (JSON)  →  教学知识点 (JSON)
```

## 🎯 核心概念

### 三个Agent协作
```
景点专家 → 分析教学潜力
   ↓
物理专家 → 提取物理知识点
   ↓
数学专家 → 提取数学知识点
   ↓
结构化输出 → 标准JSON格式
```

## 📁 关键文件（3个）

| 文件 | 职责 | 行数 |
|------|------|------|
| `agents/scenic_agent.py` | 景点智能体 | ~220 |
| `core/educational_edge.py` | 数据结构 | ~230 |
| `core/educational_chatroom.py` | 协调系统 | ~370 |

## 💻 使用（3步）

### 方法1：快速演示
```bash
python examples/quick_scenic_demo.py
```

### 方法2：代码调用
```python
from core.educational_chatroom import EducationalChatroom

chatroom = EducationalChatroom()
chatroom.load_scenic_spots("dataset/senarios/shanghai.json")

edges = chatroom.discover_educational_edges(
    spot_index=6,           # 上海中心大厦
    target_stage="高中",
    target_subjects=["数学", "物理"]
)

chatroom.export_results("output/result.json")
```

### 方法3：批量处理
```python
all_edges = chatroom.discover_all_spots(
    target_stage="高中",
    max_spots=10
)
```

## 📊 输出格式

```json
{
  "province_city": "上海市",
  "scenic_spot": "上海中心大厦",
  "name": "螺旋上升约120度的外形...",
  "stage": "高中",
  "subject": "数学",
  "knowledge_point": {
    "chapter_number": 4,
    "chapter_title": "解析几何",
    "point_name": "空间曲线的参数方程",
    "formula": "P(h) = (x(h), y(h), z(h))",
    "difficulty": "中等偏上",
    "applications": ["机器人轨迹", "3D动画"]
  },
  "reasoning": "该场景将抽象的参数方程具象化..."
}
```

## 🎓 支持的学科和学段

**学段**：小学 | 初中 | **高中** | 大学

**学科**：**数学** | **物理** | 化学 | 生物

## 📈 真实输出质量

从`output/demo_educational_edge.json`可以看到：

✅ **场景描述详细**：100-200字，具体到某个特征  
✅ **知识点精准**：符合课标，有明确章节  
✅ **公式完整**：包含变量说明  
✅ **应用丰富**：3个实际案例  
✅ **教学推理清晰**：说明为什么适合教学

## 🔧 自定义参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `spot_index` | 景点索引 | `0-9` |
| `target_stage` | 学段 | `"高中"` |
| `target_subjects` | 学科列表 | `["数学", "物理"]` |
| `rounds` | 讨论轮次 | `2-3` |
| `max_spots` | 批量处理数量 | `10` |

## 📚 完整文档

- **详细介绍**：`SCENIC_SYSTEM_OVERVIEW.md`
- **使用指南**：`SCENIC_EDUCATION_GUIDE.md`
- **示例代码**：`examples/quick_scenic_demo.py`

## 💡 典型应用

1. **研学旅行**：设计基于景点的学习任务
2. **教材编写**：丰富教材中的实际案例
3. **在线教育**：制作景点知识点视频课程
4. **博物馆教育**：设计互动式学习体验

## 🎯 系统优势

- ✅ **自动化**：AI自动提取，无需人工编写
- ✅ **标准化**：符合教学大纲，格式统一
- ✅ **高质量**：场景详细，推理清晰
- ✅ **可扩展**：易于添加新学科、新景点

## 📞 快速帮助

```bash
# 测试系统
python test_scenic_system.py

# 运行演示
python examples/quick_scenic_demo.py

# 查看输出
cat output/demo_educational_edge.json | python -m json.tool
```

---

**核心价值**：让学生在真实场景中理解抽象知识！🎓

