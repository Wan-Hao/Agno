# 笛卡尔积全遍历讨论指南

## 概述

实现了两种模式：

1. **全遍历模式**：遍历所有数学×物理节点对
2. **采样模式**：智能采样，快速探索

## 模式对比

### 全遍历模式

```python
for math_node in math_nodes:      # 105个节点
    for physics_node in physics_nodes:  # 169个节点
        multi_agent_chat(math_node, physics_node)
```

**总讨论次数**：105 × 169 = **17,745 对**

**特点**：
- ✅ 完全覆盖所有可能的组合
- ✅ 支持断点续传
- ✅ 自动保存进度
- ⚠️  耗时极长（预计数天）
- ⚠️  API调用成本高

### 采样模式

```python
# 随机采样100对
sampled_pairs = random.sample(all_pairs, 100)
for pair in sampled_pairs:
    multi_agent_chat(pair)
```

**总讨论次数**：可配置（建议100-500对）

**特点**：
- ✅ 快速完成
- ✅ 多种采样策略
- ✅ 灵活可控
- ⚠️  无法保证覆盖所有关联

## 使用方法

### 方法1：全遍历（需要数天）

```bash
# 开始全遍历
python examples/full_cartesian_discussion.py

# 中途可按 Ctrl+C 中断，进度会自动保存

# 继续运行
python examples/full_cartesian_discussion.py --resume
```

**预计时间**（假设每对3秒）：
- 17,745对 × 3秒 = 53,235秒 ≈ **14.8小时**

**实际可能更长**，因为：
- API延迟
- 网络波动
- 评估时间

### 方法2：采样（推荐）

```bash
python examples/sampled_cartesian_discussion.py
```

然后选择策略：

```
请选择采样策略:
1. 随机采样100对
2. 基于关键词采样
3. 基于主题筛选
4. 自定义
```

**预计时间**（100对）：
- 100对 × 3秒 = **5分钟**

## 采样策略详解

### 策略1：随机采样

```python
random_sample(math_nodes, physics_nodes, n=100)
```

- 从所有可能的组合中随机选择N对
- 适合：探索性分析
- 优点：快速、无偏
- 缺点：可能错过重要关联

### 策略2：关键词采样

```python
keywords = ["运动", "速度", "力", "函数", "导数", "极限"]
keyword_based_sample(math_nodes, physics_nodes, keywords)
```

- 只选择描述中包含关键词的节点对
- 适合：聚焦特定概念
- 优点：相关性高
- 缺点：依赖关键词质量

### 策略3：主题筛选

```python
math_themes = ["函数", "集合"]
physics_themes = ["机械运动", "相互作用"]
theme_based_sample(math_nodes, physics_nodes, math_themes, physics_themes)
```

- 先筛选主题，再生成笛卡尔积
- 适合：跨主题研究
- 优点：结构化、可控
- 缺点：需要了解图谱结构

## 进度管理

### 全遍历模式的进度保存

```json
{
  "completed_pairs": [
    ["displacement_velocity_acceleration", "function_definition_and_elements"],
    ["instantaneous_velocity", "function_zero"],
    ...
  ],
  "last_index": 150,
  "total_valid": 45,
  "total_pairs": 17745,
  "progress_percentage": 0.84
}
```

**断点续传**：
- 自动保存进度（每10对）
- Ctrl+C中断时保存
- 下次运行自动恢复

### 查看进度

```bash
# 查看进度文件
cat output/full_cartesian/progress.json

# 查看已生成的边
cat output/full_cartesian/cross_domain_edges.json | grep '"source"' | wc -l
```

## 输出格式

两种模式输出相同的JSON格式：

```json
{
  "metadata": {
    "source_graphs": {...},
    "total_edges": 45,
    "last_updated": "2025-10-19T..."
  },
  "edges": [
    {
      "source": "physics_node_id",
      "target": "math_node_id",
      "label": "relation_type",
      "properties": {
        "description": "...",
        "reasoning": "...",
        "confidence": 0.9
      }
    },
    ...
  ]
}
```

## 实战示例

### 示例1：快速探索（5分钟）

```bash
python examples/sampled_cartesian_discussion.py
# 选择 1（随机采样100对）
```

预期结果：
- 100对讨论
- 约30-50条有效边（30-50%有效率）

### 示例2：聚焦运动学（10分钟）

```bash
python examples/sampled_cartesian_discussion.py
# 选择 3（基于主题）
# 数学主题: 函数
# 物理主题: 机械运动
```

预期结果：
- 约200-300对讨论
- 约100-150条有效边（较高相关性）

### 示例3：长期全遍历（数天）

```bash
# 启动全遍历
nohup python examples/full_cartesian_discussion.py > cartesian.log 2>&1 &

# 查看进度
tail -f cartesian.log

# 查看实时统计
watch -n 60 'cat output/full_cartesian/progress.json | grep progress_percentage'
```

## 性能优化

### 并行处理（高级）

如果有多个API key，可以并行处理：

```python
# 将17745对分成10批
batch_size = 1775
for i in range(10):
    start = i * batch_size
    end = (i + 1) * batch_size
    batch_pairs = all_pairs[start:end]
    
    # 使用不同的API key和输出文件
    # 在不同的进程中运行
```

### 跳过低价值对

```python
# 在discuss_node_pair之前预筛选
def should_skip(physics_node, math_node):
    """快速判断是否值得讨论"""
    # 检查节点层级
    if is_too_abstract(physics_node) or is_too_abstract(math_node):
        return True
    
    # 检查描述长度
    if len(physics_node['description']) < 50:
        return True
    
    return False
```

## 结果分析

### 统计分析

```python
import json

with open('output/full_cartesian/cross_domain_edges.json') as f:
    data = json.load(f)

edges = data['edges']

# 按关系类型统计
from collections import Counter
relation_types = Counter(e['label'] for e in edges)
print(relation_types)

# 按置信度分布
import numpy as np
confidences = [e['properties']['confidence'] for e in edges]
print(f"平均置信度: {np.mean(confidences):.2f}")
print(f"中位数: {np.median(confidences):.2f}")

# 最高置信度的边
top_edges = sorted(edges, key=lambda e: e['properties']['confidence'], reverse=True)[:10]
for edge in top_edges:
    print(f"{edge['source']} -> {edge['target']}: {edge['properties']['confidence']}")
```

### 可视化

```python
import networkx as nx
import matplotlib.pyplot as plt

# 构建图
G = nx.DiGraph()
for edge in edges:
    G.add_edge(
        edge['source'],
        edge['target'],
        label=edge['label'],
        weight=edge['properties']['confidence']
    )

# 绘制
plt.figure(figsize=(20, 20))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=50, font_size=6)
plt.savefig('cross_domain_graph.png', dpi=300)
```

## 成本估算

### API调用成本

假设使用Gemini API：

**全遍历**：
- 17,745对 × 2次调用（物理+数学） = 35,490次
- 每次约500 tokens input + 500 tokens output
- 总tokens：约35M
- 成本：根据API定价计算

**采样100对**：
- 100对 × 2次 = 200次调用
- 总tokens：约200K
- 成本：全遍历的 1/177

## 最佳实践

### 1. 从采样开始

```bash
# 先跑100对，看看效果
python examples/sampled_cartesian_discussion.py
```

### 2. 评估有效率

如果有效率<20%，说明大部分节点对没有关联，不值得全遍历。

### 3. 分批次处理

```bash
# 不要一次性全遍历，分批次进行
# 第1批：100对
# 第2批：1000对
# 第3批：全遍历
```

### 4. 设置过滤条件

```python
# 只讨论重要的节点
important_math = [n for n in math_nodes if n['properties'].get('cultivated_abilities')]
important_physics = [n for n in physics_nodes if n['properties'].get('cultivated_abilities')]

# 这样可以大幅减少节点对数
```

## 总结

### 推荐方案

**初次使用**：
```bash
python examples/sampled_cartesian_discussion.py
# 选择策略2（关键词）或策略3（主题）
```

**深度研究**：
```bash
python examples/full_cartesian_discussion.py
# 在服务器上运行，使用 nohup 后台执行
```

### 预期结果

- **采样100对**：30-50条有效边，5-10分钟
- **采样1000对**：300-500条有效边，1-2小时  
- **全遍历17745对**：5000-8000条有效边，1-3天

### 文件位置

- 全遍历：`output/full_cartesian/cross_domain_edges.json`
- 采样：`output/sampled_cartesian/edges_*.json`
- 进度：`output/full_cartesian/progress.json`

