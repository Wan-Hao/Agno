# 快速参考

## 三种使用模式

### 1. 单对讨论（测试）

```bash
python examples/node_pair_discussion_example.py
```

- 讨论预定义的6对节点
- 适合：测试功能
- 耗时：~1分钟

### 2. 采样讨论（推荐）

```bash
python examples/sampled_cartesian_discussion.py
```

选项：
- 随机100对 → 5分钟
- 关键词采样 → 10分钟  
- 主题筛选 → 10-30分钟

适合：**日常使用，快速获取结果**

### 3. 全遍历（研究）

```bash
# 后台运行
nohup python examples/full_cartesian_discussion.py > log.txt 2>&1 &

# 查看进度
tail -f log.txt
```

- 遍历所有17,745对节点
- 适合：完整研究
- 耗时：**1-3天**

## 输出格式

所有模式输出相同的JSON：

```json
{
  "edges": [
    {
      "source": "physics_node_id",
      "target": "math_node_id",
      "label": "requires",
      "properties": {
        "description": "...",
        "confidence": 0.9
      }
    }
  ]
}
```

## 关键数字

| 模式 | 节点对数 | 预计时间 | 预期边数 |
|------|---------|---------|---------|
| 示例 | 6 | 1分钟 | 2-3 |
| 采样100 | 100 | 5分钟 | 30-50 |
| 采样1000 | 1000 | 1小时 | 300-500 |
| 全遍历 | 17,745 | 1-3天 | 5000-8000 |

## 数学公式

```
总节点对数 = 数学节点数 × 物理节点数
           = 105 × 169
           = 17,745
```

## 代码结构

```
for math_node in math_nodes:           # 105
    for physics_node in physics_nodes:  # 169
        # 1. 构建学科内上下文
        # 2. 双向讨论
        # 3. 元协调者检查
        # 4. 评估筛选
        # 5. Function call写入JSON
```

## 文件位置

```
output/
├── node_pair_example/       # 示例输出
├── sampled_cartesian/       # 采样输出
│   ├── edges_random_100.json
│   ├── edges_keyword_based.json
│   └── edges_theme_based.json
└── full_cartesian/          # 全遍历输出
    ├── cross_domain_edges.json
    └── progress.json        # 进度文件
```

## 常用命令

```bash
# 查看已生成的边数
cat output/*/cross_domain_edges.json | grep '"source"' | wc -l

# 查看进度
cat output/full_cartesian/progress.json

# 后台运行全遍历
nohup python examples/full_cartesian_discussion.py > log.txt 2>&1 &

# 查看日志
tail -f log.txt

# 终止运行
pkill -f full_cartesian_discussion.py
```

## 选择建议

**我该用哪个？**

| 需求 | 推荐模式 | 命令 |
|------|---------|------|
| 快速测试 | 示例 | `python examples/node_pair_discussion_example.py` |
| 日常使用 | 采样 | `python examples/sampled_cartesian_discussion.py` |
| 完整研究 | 全遍历 | `nohup python examples/full_cartesian_discussion.py &` |
| 聚焦主题 | 采样（主题） | 运行采样并选择策略3 |

## 详细文档

- **节点对模式**：`NODE_PAIR_DISCUSSION_GUIDE.md`
- **笛卡尔积**：`CARTESIAN_DISCUSSION_GUIDE.md`
- **实现总结**：`FINAL_IMPLEMENTATION.md`

