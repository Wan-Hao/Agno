# 系统架构说明

## 核心代码文件

### 1. 核心模块 (`core/`)

#### `core/node_pair_chatroom.py` ⭐ 主要实现
```python
class NodePairChatroom:
    """节点对节点聊天室 - 核心类"""
    
    # 主要方法：
    - __init__()              # 初始化，加载图谱，构建索引
    - discuss_node_pair()     # 讨论单对节点（核心流程）
    - batch_discuss()         # 批量讨论多对节点
    - _build_node_context()   # 构建学科内上下文
    - _agent_discuss_node()   # agent讨论节点
    - _is_off_topic()         # 检查是否偏离
    - _correct_discussion()   # 矫正讨论
    - _extract_edge()         # 提取边
    - _evaluate_edge()        # 评估边
    - _write_edge_to_file()   # 写入JSON

# Function Call接口
- write_edge_json()         # 写入JSON文件
- add_edge_to_json()        # 追加边到JSON
```

**核心职责**：
- 管理节点对讨论的完整流程
- 协调各个agent的交互
- 构建包含完整properties的上下文
- 验证和保存结果

#### `core/agent.py`
```python
class Agent:
    """基础Agent类"""
    
    - __init__()
    - discuss()              # 讨论方法
    - load_knowledge()       # 加载知识
    - client                 # API客户端
```

#### `core/edge.py`
```python
class KnowledgeEdge:
    """知识边数据模型"""
    
    - source_domain
    - source_concept
    - target_domain
    - target_concept
    - relation_type
    - confidence
    - to_dict()
```

#### `core/gemini_client.py` / `core/openai_client.py`
```python
class GeminiClient / OpenAIClient:
    """API客户端"""
    
    - generate()             # 生成响应
```

### 2. 智能体模块 (`agents/`)

#### `agents/domain_agents.py`
```python
class PhysicsAgent(Agent):
    """物理学家Agent"""
    
    domain = "物理学"
    expertise = "经典力学、运动学、动力学..."

class MathAgent(Agent):
    """数学家Agent"""
    
    domain = "数学"
    expertise = "函数、微积分、代数..."
```

#### `agents/meta_agent.py`
```python
class MetaAgent(Agent):
    """元协调者Agent"""
    
    - moderate_discussion()   # 主持讨论
    - extract_edges()         # 提取边
    - synthesize_insights()   # 综合洞见
```

#### `agents/evaluator_agent.py`
```python
class EvaluatorAgent(Agent):
    """评估Agent"""
    
    - evaluate_edge()         # 评估边的质量
    - generate_evaluation_report()
```

### 3. 示例脚本 (`examples/`)

#### `examples/node_pair_discussion_example.py`
- 单对节点讨论示例
- 预定义6对节点

#### `examples/sampled_cartesian_discussion.py`
- 采样模式：随机/关键词/主题
- 100-500对节点

#### `examples/full_cartesian_discussion.py`
- 全遍历模式：17,745对节点
- 支持断点续传

#### `run_small_sample.py`
- 快速演示：10对节点

## 完整流程图

```
开始
  ↓
[1] 加载知识图谱
  ├─ physics_knowledge_graph_new.json (169节点)
  └─ math_knowledge_graph_new.json (105节点)
  ↓
[2] 创建NodePairChatroom
  ├─ 初始化PhysicsAgent
  ├─ 初始化MathAgent
  ├─ 初始化MetaAgent (元协调者)
  ├─ 初始化EvaluatorAgent (评估者)
  └─ 构建节点索引和邻接表
  ↓
[3] 生成节点对
  ├─ 方式1: 手动指定
  ├─ 方式2: 随机采样
  ├─ 方式3: 关键词匹配
  ├─ 方式4: 主题筛选
  └─ 方式5: 全遍历 (math × physics)
  ↓
[4] 对每一对节点执行 discuss_node_pair()
  ↓
  ├─ [4.1] 验证节点存在
  │     ├─ physics_node_id in physics_nodes?
  │     └─ math_node_id in math_nodes?
  │
  ├─ [4.2] 构建学科内上下文 (_build_node_context)
  │     ├─ PhysicsAgent获得:
  │     │   ├─ 核心物理节点的完整properties
  │     │   │   ├─ description
  │     │   │   ├─ stage
  │     │   │   ├─ subject
  │     │   │   ├─ category
  │     │   │   ├─ theme
  │     │   │   └─ cultivated_abilities
  │     │   └─ 相关物理节点(1-2层)
  │     │
  │     └─ MathAgent获得:
  │         ├─ 核心数学节点的完整properties
  │         │   ├─ description
  │         │   ├─ course_nature
  │         │   ├─ subject
  │         │   ├─ category
  │         │   ├─ theme
  │         │   └─ cultivated_abilities
  │         └─ 相关数学节点(1-2层)
  │
  ├─ [4.3] PhysicsAgent讨论 (_agent_discuss_node)
  │     ├─ 输入: physics上下文 + math节点信息
  │     ├─ Prompt: "从物理角度分析关联"
  │     └─ 输出: physics_response
  │
  ├─ [4.4] MathAgent讨论
  │     ├─ 输入: math上下文 + physics节点信息 + physics_response
  │     ├─ Prompt: "从数学角度回应"
  │     └─ 输出: math_response
  │
  ├─ [4.5] MetaAgent检查偏离 (_is_off_topic)
  │     ├─ 检查1: physics_node_id在physics_response中?
  │     ├─ 检查2: math_node_id在math_response中?
  │     ├─ 检查3: 讨论长度 >= 100字符?
  │     │
  │     ├─ 如果偏离:
  │     │   ├─ MetaAgent.correct_discussion()
  │     │   └─ return None (跳过此节点对)
  │     │
  │     └─ 如果聚焦:
  │         └─ 继续
  │
  ├─ [4.6] MetaAgent提取边 (_extract_edge)
  │     ├─ 输入: physics_response + math_response
  │     ├─ Prompt: "提取跨学科关联，返回JSON"
  │     └─ 输出: edge = {
  │           "source": "physics_node_id",
  │           "target": "math_node_id",
  │           "label": "relation_type",
  │           "properties": {
  │             "description": "...",
  │             "reasoning": "...",
  │             "confidence": 0.9
  │           }
  │         }
  │
  ├─ [4.7] EvaluatorAgent评估边 (_evaluate_edge)
  │     ├─ 输入: edge
  │     ├─ Prompt: "评估边的质量"
  │     ├─ 评估标准:
  │     │   ├─ 关联是否合理?
  │     │   ├─ 描述是否清晰?
  │     │   ├─ 置信度 >= 0.6?
  │     │   └─ 是否是真实的跨学科关联?
  │     │
  │     ├─ 如果通过:
  │     │   └─ 继续到4.8
  │     │
  │     └─ 如果拒绝:
  │         └─ return None (不保存)
  │
  └─ [4.8] Function Call写入JSON (add_edge_to_json)
        ├─ 读取现有文件
        ├─ 追加edge到edges数组
        ├─ 更新metadata
        └─ 写回文件
  ↓
[5] 循环处理所有节点对
  ↓
[6] 完成
  └─ 输出: cross_domain_edges.json
```

## Agent角色详解

### 1. PhysicsAgent (物理学家)
```python
role = "领域专家"
职责 = {
    "核心": "从物理学视角分析节点",
    "输入": "物理节点 + 学科内上下文 + 对方节点",
    "输出": "物理学角度的关联分析",
    "专长": [
        "经典力学",
        "运动学",
        "动力学",
        "电磁学",
        "热学"
    ]
}
```

**调用时机**: 每对节点的第一轮讨论

**Prompt示例**:
```
你的知识背景:
[displacement_velocity_acceleration] 位移、速度与加速度
  - description: ...
  - category: 机械运动与物理模型
  - cultivated_abilities: 物理观念, 科学思维

对方的知识节点:
[function_definition_and_elements] 函数定义与三要素
  - description: ...

任务: 从物理学角度分析这两个节点的关联
```

### 2. MathAgent (数学家)
```python
role = "领域专家"
职责 = {
    "核心": "从数学视角分析节点",
    "输入": "数学节点 + 学科内上下文 + 对方节点 + 对方观点",
    "输出": "数学角度的关联分析和回应",
    "专长": [
        "函数",
        "微积分",
        "代数",
        "几何",
        "集合论"
    ]
}
```

**调用时机**: 每对节点的第二轮讨论

**Prompt示例**:
```
你的知识背景:
[function_definition_and_elements] 函数定义与三要素
  - description: ...
  - category: 函数概念与性质
  - cultivated_abilities: 数学抽象, 逻辑推理

对方的知识节点:
[displacement_velocity_acceleration] 位移、速度与加速度

对方的观点:
[PhysicsAgent的完整回答]

任务: 从数学角度回应并分析关联
```

### 3. MetaAgent (元协调者)
```python
role = "协调和提取"
职责 = {
    "监控": "检查讨论是否偏离核心节点",
    "矫正": "在偏离时引导回到正轨",
    "提取": "从讨论中提取结构化的边",
    "条件": "只在必要时介入，平时保持静默"
}
```

**调用时机**: 
- 偏离检查: 每对节点讨论后
- 矫正: 仅当检测到偏离
- 提取: 每对节点讨论完成后

**Prompt示例 (提取边)**:
```
物理专家关于 [displacement_velocity_acceleration] 的观点:
[physics_response]

数学专家关于 [function_definition_and_elements] 的观点:
[math_response]

请判断是否存在跨学科关联，返回JSON:
{
  "source": "physics_node_id",
  "target": "math_node_id",
  "label": "relation_type",
  "properties": {...}
}
```

### 4. EvaluatorAgent (评估专家)
```python
role = "质量控制"
职责 = {
    "评估": "判断边的质量和合理性",
    "筛选": "决定是否保留边",
    "标准": [
        "关联合理性",
        "描述清晰度",
        "置信度 >= 0.6",
        "真实的跨学科关联"
    ]
}
```

**调用时机**: 每条边提取后

**Prompt示例**:
```
评估以下跨学科关联边:
source: displacement_velocity_acceleration
target: function_definition_and_elements
label: requires
description: ...
confidence: 0.9

返回JSON:
{
  "valid": true/false,
  "reason": "评估理由"
}
```

## 数据流

```
输入数据
  ├─ physics_knowledge_graph_new.json
  │    └─ 169个节点, 每个包含完整properties
  │
  └─ math_knowledge_graph_new.json
       └─ 105个节点, 每个包含完整properties

    ↓

处理流程
  ├─ 节点对1: [physics_A] ↔ [math_X]
  │    ├─ PhysicsAgent分析
  │    ├─ MathAgent分析
  │    ├─ MetaAgent提取
  │    └─ EvaluatorAgent评估 → 边1 (如果通过)
  │
  ├─ 节点对2: [physics_B] ↔ [math_Y]
  │    └─ ... → 边2 (如果通过)
  │
  └─ ...

    ↓

输出数据
  └─ cross_domain_edges.json
       └─ {
            "edges": [边1, 边2, ...],
            "metadata": {...}
          }
```

## 关键设计决策

### 1. 为什么用节点对而不是主题讨论?
```
❌ 主题讨论:
   - "讨论运动与函数的关系"
   - 太宽泛，难以聚焦
   - 输出的边不精确

✅ 节点对讨论:
   - "[displacement_velocity_acceleration] ↔ [function_definition_and_elements]"
   - 精确聚焦具体知识点
   - 输出的边可验证、可追溯
```

### 2. 为什么需要学科内上下文?
```
❌ 孤立节点:
   "函数定义与三要素"
   - agent不知道这个概念在数学体系中的位置

✅ 携带上下文:
   "函数定义与三要素"
   + 相关: mapping_concept, function_three_elements, domain, range...
   - agent了解这个概念的前置、后续和相关知识
```

### 3. 为什么需要4个不同的Agent?
```
PhysicsAgent:  领域专业知识
MathAgent:     领域专业知识
MetaAgent:     跨学科视角 + 提取能力
EvaluatorAgent: 客观评判标准

单个Agent无法同时具备:
- 深度领域知识
- 跨学科视角
- 客观评估能力
```

### 4. 为什么需要评估筛选?
```
不筛选的结果:
- 17,745对 × 30% = 5,323条边
- 包含大量低质量、不相关的边

筛选后的结果:
- 17,745对 → ~3,000-4,000条高质量边
- 每条都有明确的理由和足够的置信度
```

## 配置选项

### 1. 上下文深度
```python
context_depth = 1  # 包含1层相关节点 (推荐)
context_depth = 2  # 包含2层相关节点 (更丰富，但token消耗大)
```

### 2. 采样策略
```python
# 随机
random.sample(all_pairs, 100)

# 关键词
keyword_based_sample(keywords=["运动", "函数", "变化"])

# 主题
theme_based_sample(
    math_themes=["函数"],
    physics_themes=["机械运动"]
)
```

### 3. 评估阈值
```python
# 在EvaluatorAgent的prompt中调整
confidence >= 0.6  # 当前标准
confidence >= 0.8  # 更严格
```

## 性能特点

| 指标 | 数值 |
|------|------|
| 每对讨论时间 | 3-5秒 |
| API调用次数/对 | 4次 (Physics + Math + Meta + Evaluator) |
| Token消耗/对 | ~2000 tokens |
| 有效边比例 | 30-50% |
| 全遍历预计时间 | 14-48小时 |

## 扩展性

### 支持新的学科
```python
# 只需添加新的Agent
class BiologyAgent(Agent):
    domain = "生物学"
    expertise = "细胞、遗传、生态..."

# 创建新的聊天室
chatroom = NodePairChatroom(
    physics_agent=BiologyAgent(),
    math_agent=ChemistryAgent(),
    physics_graph=biology_graph,
    math_graph=chemistry_graph
)
```

### 自定义评估标准
```python
class StrictEvaluatorAgent(EvaluatorAgent):
    """更严格的评估"""
    def evaluate_edge(self, edge):
        # 自定义评估逻辑
        if edge['properties']['confidence'] < 0.8:
            return False, "置信度太低"
        ...
```

## 总结

**核心文件**:
- `core/node_pair_chatroom.py` - 主要逻辑
- `agents/domain_agents.py` - PhysicsAgent, MathAgent
- `agents/meta_agent.py` - 协调和提取
- `agents/evaluator_agent.py` - 质量控制

**使用的Agent** (4个):
1. PhysicsAgent - 物理领域专家
2. MathAgent - 数学领域专家
3. MetaAgent - 元协调者
4. EvaluatorAgent - 评估专家

**核心流程**:
```
加载图谱 → 生成节点对 → 对每对:
  [Physics分析] → [Math回应] → [Meta检查] → [Meta提取] → [Evaluator筛选] → [写入JSON]
```

**输出**: 纯边的JSON，source和target都是实际节点ID

