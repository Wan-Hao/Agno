"""
布鲁姆认知目标分类评估Agent

负责：
1. 阅读和理解知识点
2. 根据布鲁姆认知层级对知识点进行分类
3. 调用工具给知识点打标签
"""

from agno.agent import Agent
from agno.tools.python import PythonFunction
from tools.bloom_taxonomy_tools import (
    tag_knowledge_point_remember,
    tag_knowledge_point_understand,
    tag_knowledge_point_apply,
    tag_knowledge_point_analyze,
    tag_knowledge_point_evaluate,
    tag_knowledge_point_create,
    get_knowledge_points,
    get_all_knowledge_points,
    get_tagging_progress,
    BLOOM_LEVELS
)


def create_bloom_taxonomy_agent(model: str = "gpt-4o") -> Agent:
    """
    创建布鲁姆认知层级评估Agent
    
    Args:
        model: 使用的模型名称
        
    Returns:
        配置好的Agent实例
    """
    
    # 构建详细的系统提示词
    system_prompt = f"""你是一位教育评估专家，精通布鲁姆认知目标分类理论。

布鲁姆认知层级（由低到高）：
1. **记忆（Remember）**: 识别和回忆相关知识
   - 关键词：记住、列举、识别、回忆、定义
   - 例如：记住集合的定义，识别数学符号
   
2. **理解（Understand）**: 理解材料的含义，能够解释和说明
   - 关键词：解释、描述、说明、概括、分类
   - 例如：理解函数的概念，解释集合之间的关系
   
3. **应用（Apply）**: 在新情境中使用信息和规则
   - 关键词：应用、使用、计算、求解、实施
   - 例如：应用基本不等式求最值，使用二分法求解方程
   
4. **分析（Analyze）**: 将信息分解为组成部分，理解结构和关系
   - 关键词：分析、区分、比较、推导、归因
   - 例如：分析函数的单调性，比较不同集合运算的关系
   
5. **评价（Evaluate）**: 基于标准和准则做出判断
   - 关键词：评价、判断、批判、论证、辩护
   - 例如：评价不同解题方法的优劣，判断证明的正确性
   
6. **创造（Create）**: 组合元素形成新的整体或结构
   - 关键词：创造、设计、构建、规划、生成
   - 例如：构建新的数学模型，设计解题策略

你的任务：
1. 仔细阅读每个知识点的描述、标签和能力培养目标
2. 根据知识点的内容判断其所属的布鲁姆认知层级
3. 使用相应的工具为知识点打上标签
4. 提供清晰的理由说明为什么归类到该层级

判断标准：
- 考虑知识点的核心学习目标
- 注意知识点中的关键动词
- 基础概念和定义通常是"记忆"或"理解"层级
- 需要推导、证明的通常是"分析"层级
- 实际应用和建模通常是"应用"层级
- 设计和构建新方法通常是"创造"层级

注意事项：
- 每个知识点只能归类到一个主要层级
- 选择最能体现该知识点核心要求的层级
- 基础性的预备知识通常在较低层级
- 复杂的综合性知识通常在较高层级
"""
    
    # 创建Agent并注册工具
    agent = Agent(
        name="Bloom Taxonomy Evaluator",
        model=model,
        instructions=system_prompt,
        tools=[
            PythonFunction(function=get_knowledge_points),
            PythonFunction(function=get_all_knowledge_points),
            PythonFunction(function=get_tagging_progress),
            PythonFunction(function=tag_knowledge_point_remember),
            PythonFunction(function=tag_knowledge_point_understand),
            PythonFunction(function=tag_knowledge_point_apply),
            PythonFunction(function=tag_knowledge_point_analyze),
            PythonFunction(function=tag_knowledge_point_evaluate),
            PythonFunction(function=tag_knowledge_point_create),
        ],
        show_tool_calls=True,
        markdown=True,
    )
    
    return agent


def create_knowledge_reviewer_agent(model: str = "gpt-4o") -> Agent:
    """
    创建知识点预览Agent，用于第一阶段的知识点整体理解
    
    Args:
        model: 使用的模型名称
        
    Returns:
        配置好的Agent实例
    """
    
    system_prompt = """你是一位教育领域的知识图谱分析专家。

你的任务是：
1. 使用工具批量获取并阅读所有知识点
2. 分析知识点的整体结构和层次
3. 识别知识点的难度分布
4. 理解不同知识点之间的关联关系
5. 为后续的布鲁姆认知层级标注提供整体认知基础

分析要点：
- 注意知识点的学科主题和类别
- 识别基础性概念和高级应用
- 理解预备知识与主题知识的关系
- 观察能力培养目标（数学抽象、逻辑推理、数学建模等）

请提供一个简洁的总结报告，包括：
- 知识点总数
- 主要主题分布
- 难度层次的初步判断
- 关键的基础性知识点
"""
    
    agent = Agent(
        name="Knowledge Reviewer",
        model=model,
        instructions=system_prompt,
        tools=[
            PythonFunction(function=get_knowledge_points),
            PythonFunction(function=get_all_knowledge_points),
            PythonFunction(function=get_tagging_progress),
        ],
        show_tool_calls=True,
        markdown=True,
    )
    
    return agent

