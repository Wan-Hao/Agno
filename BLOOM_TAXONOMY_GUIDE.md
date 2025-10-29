# 布鲁姆认知层级标注Pipeline使用指南

## 📋 概述

本Pipeline使用AI Agent自动对知识图谱中的知识点进行布鲁姆认知目标分类（Bloom's Taxonomy）标注。

## 🎯 布鲁姆认知层级

布鲁姆认知目标分类将学习目标分为六个层级（由低到高）：

1. **记忆（Remember）** 
   - 识别和回忆相关知识
   - 关键词：记住、列举、识别、回忆、定义
   - 示例：记住集合的定义，识别数学符号

2. **理解（Understand）**
   - 理解材料的含义，能够解释和说明
   - 关键词：解释、描述、说明、概括、分类
   - 示例：理解函数的概念，解释集合之间的关系

3. **应用（Apply）**
   - 在新情境中使用信息和规则
   - 关键词：应用、使用、计算、求解、实施
   - 示例：应用基本不等式求最值，使用二分法求解方程

4. **分析（Analyze）**
   - 将信息分解为组成部分，理解结构和关系
   - 关键词：分析、区分、比较、推导、归因
   - 示例：分析函数的单调性，比较不同集合运算的关系

5. **评价（Evaluate）**
   - 基于标准和准则做出判断
   - 关键词：评价、判断、批判、论证、辩护
   - 示例：评价不同解题方法的优劣，判断证明的正确性

6. **创造（Create）**
   - 组合元素形成新的整体或结构
   - 关键词：创造、设计、构建、规划、生成
   - 示例：构建新的数学模型，设计解题策略

## 🏗️ 架构设计

### 1. 工具层（Tools）

位置：`tools/bloom_taxonomy_tools.py`

包含以下工具函数：

#### 标注工具（6个）
- `tag_knowledge_point_remember()` - 标记为"记忆"层级
- `tag_knowledge_point_understand()` - 标记为"理解"层级
- `tag_knowledge_point_apply()` - 标记为"应用"层级
- `tag_knowledge_point_analyze()` - 标记为"分析"层级
- `tag_knowledge_point_evaluate()` - 标记为"评价"层级
- `tag_knowledge_point_create()` - 标记为"创造"层级

#### 查询工具
- `get_knowledge_points()` - 分页获取知识点
- `get_all_knowledge_points()` - 获取所有知识点
- `get_tagging_progress()` - 获取标注进度统计

### 2. Agent层

位置：`agents/bloom_taxonomy_agent.py`

#### Knowledge Reviewer Agent
- **作用**：第一阶段预览和理解所有知识点
- **能力**：批量阅读、分析知识结构、识别难度层次
- **输出**：整体认知报告

#### Bloom Taxonomy Evaluator Agent
- **作用**：第二阶段对知识点进行布鲁姆认知层级标注
- **能力**：理解布鲁姆分类理论、调用标注工具、提供理由
- **输出**：标注结果和统计报告

### 3. 工作流层（Workflow）

位置：`workflows/bloom_taxonomy_workflow.py`

使用Agno框架构建的三阶段工作流：

```
Stage 1: 知识点整体预览
  ├─ Prepare Review Prompt
  └─ Knowledge Reviewer Agent 执行

Stage 2: 批量标注
  ├─ Prepare Tagging Prompt  
  └─ Bloom Taxonomy Evaluator Agent 执行

Stage 3: 生成报告
  ├─ Prepare Report Prompt
  └─ Generate Final Report
```

## 🚀 快速开始

### 1. 环境准备

确保已安装依赖：

```bash
# 安装Agno框架
pip install agno

# 或使用项目的requirements.txt
pip install -r requirements.txt
```

配置API密钥（在 `config.py` 或环境变量中）：

```bash
export OPENAI_API_KEY="your-api-key"
```

### 2. 运行示例

```bash
python examples/bloom_taxonomy_example.py
```

交互式选择：
- 科目名称（如：math, physics）
- 使用的模型（推荐：gpt-4o）

### 3. 程序化调用

```python
from workflows.bloom_taxonomy_workflow import run_bloom_taxonomy_pipeline

# 运行Pipeline
result = run_bloom_taxonomy_pipeline(
    subject="math",      # 科目
    model="gpt-4o"       # 模型
)

# 查看结果
print(f"已标注: {result['tagged']}/{result['total']}")
print(f"完成度: {result['progress_percentage']}%")
```

### 4. 单独使用工具

```python
from tools.bloom_taxonomy_tools import (
    get_all_knowledge_points,
    tag_knowledge_point_understand,
    get_tagging_progress
)

# 获取所有知识点
result = get_all_knowledge_points(subject="math")
nodes = result["nodes"]

# 手动标注某个知识点
tag_knowledge_point_understand(
    node_id="set_definition",
    file_path="dataset/graph/math_knowledge_graph_new.json",
    reasoning="集合的含义需要理解和解释，属于理解层级"
)

# 查看进度
progress = get_tagging_progress(subject="math")
print(progress)
```

## 📊 输出格式

标注后的知识点会在 `properties` 中增加以下字段：

```json
{
  "id": "set_definition",
  "label": "集合的含义",
  "properties": {
    "description": "...",
    "bloom_level": "Understand",
    "bloom_reasoning": "集合的含义需要理解和解释，属于理解层级"
  }
}
```

## 🔧 自定义配置

### 修改模型

在创建workflow时指定：

```python
workflow = create_bloom_taxonomy_workflow(
    subject="math",
    model="gpt-4o-mini"  # 使用更快的模型
)
```

### 批处理策略

对于大量知识点，Agent会自动采用批处理策略，可以在agent的instructions中调整。

### 标注标准

可以在 `agents/bloom_taxonomy_agent.py` 中修改 `system_prompt` 来调整标注标准和策略。

## 📈 查看标注进度

使用进度查询工具：

```python
from tools.bloom_taxonomy_tools import get_tagging_progress

progress = get_tagging_progress(subject="math")

print(f"总数: {progress['total']}")
print(f"已标注: {progress['tagged']}")
print(f"未标注: {progress['untagged']}")
print(f"完成度: {progress['progress_percentage']}%")

# 各层级分布
for level, count in progress['level_distribution'].items():
    print(f"{level}: {count}")
```

## 🎨 工作流特点

1. **两阶段理解**
   - 第一阶段：整体预览，建立全局认知
   - 第二阶段：基于全局认知进行精确标注

2. **智能推理**
   - Agent理解布鲁姆分类理论
   - 根据知识点的描述、能力目标等综合判断
   - 提供标注理由，可追溯

3. **批量处理**
   - 自动处理所有知识点
   - 无需人工干预
   - 支持大规模知识图谱

4. **进度跟踪**
   - 实时查看标注进度
   - 统计各层级分布
   - 生成最终报告

## 🔍 示例：标注策略

Agent会根据以下策略进行标注：

| 知识点类型 | 典型布鲁姆层级 | 示例 |
|----------|--------------|------|
| XXX的概念/定义 | Remember/Understand | 集合的含义、函数定义 |
| XXX的性质/关系 | Understand/Analyze | 函数单调性、集合包含关系 |
| XXX的求解/应用 | Apply | 二分法求解、不等式求解 |
| XXX的推导/证明 | Analyze | 方程根与图像交点 |
| XXX的建模/设计 | Create | 指数增长模型、分段函数应用 |
| XXX的评价/判断 | Evaluate | 逆否等价性、解法优劣 |

## 📝 注意事项

1. **API成本**：使用GPT-4o等模型会产生API调用费用，大规模标注前请评估成本

2. **标注质量**：建议使用GPT-4o以获得最佳标注质量，GPT-4o-mini速度快但准确度略低

3. **数据备份**：标注会直接修改JSON文件，建议先备份原始文件

4. **重复标注**：重复运行会覆盖已有标签，如需保留请先备份

5. **错误处理**：如果某些知识点标注失败，可以查看日志并手动标注

## 🤝 扩展开发

### 添加新的认知层级

如需使用其他分类体系，可以：

1. 在 `tools/bloom_taxonomy_tools.py` 中添加新的标注函数
2. 在 `agents/bloom_taxonomy_agent.py` 中更新系统提示词
3. 注册新工具到Agent

### 支持新的科目

只需确保 `dataset/graph/` 目录下有对应的JSON文件：

```
dataset/graph/
  ├── math_knowledge_graph_new.json
  ├── physics_knowledge_graph_new.json
  └── your_subject_knowledge_graph_new.json
```

## 📚 相关文档

- [Agno框架文档](https://docs.agno.com/)
- [Bloom's Taxonomy理论](https://en.wikipedia.org/wiki/Bloom%27s_taxonomy)
- [知识图谱使用指南](./KNOWLEDGE_GRAPH_USAGE.md)

## 🐛 问题排查

### 问题1：找不到模块

```
ModuleNotFoundError: No module named 'agno'
```

**解决**：安装Agno框架
```bash
pip install agno
```

### 问题2：API密钥错误

```
OpenAI API key not found
```

**解决**：配置API密钥
```bash
export OPENAI_API_KEY="your-key"
```

### 问题3：文件路径错误

```
未找到科目 xxx 的知识图谱文件
```

**解决**：检查 `dataset/graph/` 目录下是否有对应文件

---

## 📧 联系方式

如有问题或建议，请提交Issue或Pull Request。


