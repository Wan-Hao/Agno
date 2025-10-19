# 系统总览

## 📁 核心代码文件

```
Agno/
├── core/
│   ├── node_pair_chatroom.py    ⭐ 核心实现 (550行)
│   ├── agent.py                  基础Agent类
│   ├── edge.py                   边数据模型
│   └── gemini_client.py          API客户端
│
├── agents/
│   ├── domain_agents.py          PhysicsAgent, MathAgent
│   ├── meta_agent.py             MetaAgent (协调+提取)
│   └── evaluator_agent.py        EvaluatorAgent (评估)
│
├── examples/
│   ├── node_pair_discussion_example.py      示例(6对)
│   ├── sampled_cartesian_discussion.py      采样模式
│   └── full_cartesian_discussion.py         全遍历模式
│
├── dataset/graph/
│   ├── physics_knowledge_graph_new.json     169节点
│   └── math_knowledge_graph_new.json        105节点
│
└── output/
    └── */cross_domain_edges.json            输出结果
```

## 🤖 使用的Agent (4个)

| Agent | 角色 | 调用时机 | 职责 |
|-------|------|----------|------|
| **PhysicsAgent** | 物理学家 | 第1轮 | 从物理角度分析节点关联 |
| **MathAgent** | 数学家 | 第2轮 | 从数学角度回应和分析 |
| **MetaAgent** | 元协调者 | 讨论后 | 检查偏离、提取边 |
| **EvaluatorAgent** | 评估专家 | 提取边后 | 评估边的质量，决定保留 |

## 🔄 完整流程 (单对节点)

```
输入: physics_node_id, math_node_id
  ↓
┌─────────────────────────────────────────────┐
│ Step 1: 构建上下文                            │
├─────────────────────────────────────────────┤
│ • 读取physics_node的完整properties           │
│ • 找到相关物理节点(通过图谱边)                 │
│ • 读取math_node的完整properties              │
│ • 找到相关数学节点                            │
└─────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────┐
│ Step 2: PhysicsAgent 分析                   │
├─────────────────────────────────────────────┤
│ 输入:                                        │
│   - physics_node + 学科内上下文              │
│   - math_node信息                           │
│ 输出:                                        │
│   - physics_response (关联分析)             │
└─────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────┐
│ Step 3: MathAgent 回应                      │
├─────────────────────────────────────────────┤
│ 输入:                                        │
│   - math_node + 学科内上下文                │
│   - physics_node信息                        │
│   - physics_response                        │
│ 输出:                                        │
│   - math_response (回应+分析)               │
└─────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────┐
│ Step 4: MetaAgent 检查偏离                  │
├─────────────────────────────────────────────┤
│ 检查:                                        │
│   ✓ physics_node_id 在 physics_response?   │
│   ✓ math_node_id 在 math_response?         │
│   ✓ 讨论长度 >= 100字符?                    │
│                                             │
│ 如果偏离 → 矫正 → 跳过                       │
│ 如果聚焦 → 继续                              │
└─────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────┐
│ Step 5: MetaAgent 提取边                    │
├─────────────────────────────────────────────┤
│ 输入:                                        │
│   - physics_response + math_response        │
│ 输出:                                        │
│   {                                         │
│     "source": "physics_node_id",           │
│     "target": "math_node_id",              │
│     "label": "requires",                   │
│     "properties": {                        │
│       "description": "...",                │
│       "reasoning": "...",                  │
│       "confidence": 0.9                    │
│     }                                       │
│   }                                         │
└─────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────┐
│ Step 6: EvaluatorAgent 评估                │
├─────────────────────────────────────────────┤
│ 评估标准:                                    │
│   ✓ 关联合理?                               │
│   ✓ 描述清晰?                               │
│   ✓ confidence >= 0.6?                     │
│   ✓ 真实的跨学科关联?                        │
│                                             │
│ 通过 → 继续                                 │
│ 拒绝 → 跳过                                 │
└─────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────┐
│ Step 7: Function Call 写入JSON              │
├─────────────────────────────────────────────┤
│ add_edge_to_json(file_path, edge)          │
│   ├─ 读取现有文件                            │
│   ├─ 追加edge到edges数组                    │
│   ├─ 更新metadata                           │
│   └─ 写回文件                                │
└─────────────────────────────────────────────┘
  ↓
输出: 边已保存到 cross_domain_edges.json
```

## 📊 数据示例

### 输入 (节点)
```json
{
  "id": "displacement_velocity_acceleration",
  "label": "位移、速度与加速度",
  "properties": {
    "description": "理解位移、速度、加速度概念...",
    "stage": "Compulsory",
    "subject": "Physics",
    "category": "机械运动与物理模型",
    "theme": "机械运动与物理模型",
    "cultivated_abilities": ["物理观念", "科学思维"]
  }
}
```

### 输出 (边)
```json
{
  "source": "displacement_velocity_acceleration",
  "target": "function_definition_and_elements",
  "label": "requires",
  "properties": {
    "description": "位移、速度和加速度的定义依赖函数概念",
    "reasoning": "速度是位移对时间的函数...",
    "confidence": 0.92
  }
}
```

## 💡 关键设计

### 1. 为何用4个Agent?

```
单Agent方案 ❌
  └─ 无法同时具备: 领域专业知识 + 跨学科视角 + 客观评估

多Agent方案 ✅
  ├─ PhysicsAgent:  深度物理知识
  ├─ MathAgent:     深度数学知识
  ├─ MetaAgent:     跨学科提取能力
  └─ EvaluatorAgent: 客观评估标准
```

### 2. 为何需要完整properties?

```
只有description ❌
  └─ "理解位移、速度、加速度概念..."

完整properties ✅
  ├─ description:          详细描述
  ├─ category:             机械运动与物理模型
  ├─ theme:                机械运动与物理模型
  ├─ cultivated_abilities: 物理观念, 科学思维
  └─ stage/course_nature:  Compulsory

→ Agent拥有更多上下文，做出更准确的判断
```

### 3. 为何需要学科内相关节点?

```
孤立节点 ❌
  [displacement_velocity_acceleration]
  └─ Agent不知道这个概念在物理体系中的位置

携带上下文 ✅
  [displacement_velocity_acceleration]
  ├─ 相关: kinematics_concepts (父概念)
  ├─ 相关: velocity_concepts (组成部分)
  ├─ 相关: acceleration_concept (组成部分)
  └─ 相关: uniformly_accelerated_linear_motion (应用)

→ Agent了解前置、后续和相关知识
```

## 🚀 使用方式

### 方式1: 快速测试 (10对, 2分钟)
```bash
python run_small_sample.py
```

### 方式2: 采样讨论 (100-500对, 5-30分钟)
```bash
python examples/sampled_cartesian_discussion.py
# 选择策略: 随机/关键词/主题
```

### 方式3: 全遍历 (17,745对, 1-3天)
```bash
nohup python examples/full_cartesian_discussion.py > log.txt 2>&1 &
```

## 📈 性能数据

| 项目 | 数值 |
|------|------|
| 总节点对数 | 105 × 169 = 17,745 |
| 每对耗时 | 3-5秒 |
| API调用/对 | 4次 |
| 有效边比例 | 30-50% |
| 预期输出边数 | 5,000-8,000条 |

## 📝 核心代码位置

### 主要流程实现
```python
# core/node_pair_chatroom.py

def discuss_node_pair(self, physics_node_id, math_node_id):
    """单对节点讨论的完整流程"""
    # 1. 构建上下文
    physics_context = self._build_node_context(...)  # Line 145-157
    
    # 2. Physics分析
    physics_response = self._agent_discuss_node(...)  # Line 161-168
    
    # 3. Math回应
    math_response = self._agent_discuss_node(...)  # Line 172-180
    
    # 4. 检查偏离
    if self._is_off_topic(...):  # Line 183-196
        return None
    
    # 5. 提取边
    edge = self._extract_edge(...)  # Line 199-208
    
    # 6. 评估
    is_valid, reason = self._evaluate_edge(edge)  # Line 212
    
    # 7. 写入
    if is_valid:
        self._write_edge_to_file(edge)  # Line 218
```

### Agent定义
```python
# agents/domain_agents.py (Line 10-50)
class PhysicsAgent(Agent):
    domain = "物理学"

class MathAgent(Agent):
    domain = "数学"
```

### 评估逻辑
```python
# core/node_pair_chatroom.py (Line 399-437)
def _evaluate_edge(self, edge):
    """评估边的质量"""
    # 调用EvaluatorAgent的LLM
    # 返回 (is_valid, reason)
```

## 🎯 总结

**一句话描述**: 
4个Agent协作，对物理和数学图谱的节点进行两两配对讨论，提取跨学科边，经过评估后通过function call写入JSON。

**核心创新**:
1. ✅ 节点对讨论（精确、可验证）
2. ✅ 完整properties上下文（信息丰富）
3. ✅ 多Agent协作（专业+协调+评估）
4. ✅ Function call写入（标准化、增量）
