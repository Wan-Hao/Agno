"""
布鲁姆认知层级标注工作流

工作流程：
1. 第一阶段：知识点整体预览和理解（Knowledge Reviewer Agent）
2. 第二阶段：逐个知识点进行布鲁姆认知层级标注（Bloom Taxonomy Evaluator Agent）
3. 第三阶段：生成标注报告
"""

from agno.workflow import Workflow, Step, StepOutput
from agents.bloom_taxonomy_agent import (
    create_bloom_taxonomy_agent,
    create_knowledge_reviewer_agent
)
from tools.bloom_taxonomy_tools import get_tagging_progress, get_all_knowledge_points
from typing import Dict, Any


def create_bloom_taxonomy_workflow(subject: str = "math", model: str = "gpt-4o") -> Workflow:
    """
    创建布鲁姆认知层级标注工作流
    
    Args:
        subject: 科目名称（如 "math", "physics"）
        model: 使用的模型名称
        
    Returns:
        配置好的Workflow实例
    """
    
    # 创建两个Agent
    reviewer_agent = create_knowledge_reviewer_agent(model=model)
    evaluator_agent = create_bloom_taxonomy_agent(model=model)
    
    # 定义第一阶段：知识点预览
    def stage_1_review_knowledge(step_input):
        """第一阶段：阅读所有知识点，建立整体认知"""
        prompt = f"""
请完成以下任务：

1. 使用 get_all_knowledge_points 工具获取 {subject} 科目的所有知识点
2. 仔细阅读每个知识点的：
   - id 和 label（知识点名称）
   - description（知识点描述）
   - category（所属类别）
   - theme（主题）
   - cultivated_abilities（培养的能力）
   - course_nature（课程性质：必修/选修）

3. 分析并总结：
   - 总共有多少个知识点
   - 主要包含哪些主题和类别
   - 知识点的难度层次（基础概念、应用、分析等）
   - 识别出最基础的预备知识
   - 识别出最高级的应用/创造类知识

4. 为后续的布鲁姆认知层级标注提供整体建议：
   - 哪些类型的知识点通常属于较低层级（记忆、理解）
   - 哪些类型的知识点通常属于较高层级（分析、评价、创造）

请使用工具获取数据并提供详细的分析报告。
"""
        return StepOutput(content=prompt)
    
    # 定义第二阶段：标注知识点
    def stage_2_tag_knowledge_points(step_input):
        """第二阶段：对所有知识点进行布鲁姆认知层级标注"""
        prompt = f"""
基于上一阶段的整体认知，现在请对 {subject} 科目的所有知识点进行布鲁姆认知层级标注。

任务流程：
1. 使用 get_all_knowledge_points 工具获取所有知识点
2. 对每个知识点：
   a. 仔细分析其描述、能力培养目标和在知识体系中的位置
   b. 判断其所属的布鲁姆认知层级：
      - Remember（记忆）：基础定义和概念的识别
      - Understand（理解）：能够解释和说明的概念
      - Apply（应用）：能够在新情境中使用的知识和方法
      - Analyze（分析）：需要分解、比较、推导的知识
      - Evaluate（评价）：需要做出判断和论证的知识
      - Create（创造）：需要构建新模型、设计新方法的知识
   c. 调用对应的标注工具（tag_knowledge_point_XXX）
   d. 在 reasoning 参数中提供简短的判断理由

3. 建议的标注策略：
   - 对于"XXX的概念"、"XXX的定义"类知识点，通常是 Remember 或 Understand
   - 对于"XXX的性质"、"XXX的关系"类知识点，通常是 Understand 或 Analyze
   - 对于"XXX的求解"、"XXX的应用"类知识点，通常是 Apply
   - 对于需要推导、证明的知识点，通常是 Analyze
   - 对于建模、设计、构建类知识点，通常是 Create

请逐个为所有知识点打上合适的布鲁姆认知层级标签。

重要提示：
- 请确保为**每一个**知识点都打上标签
- 使用正确的文件路径（通过 get_all_knowledge_points 返回的 file_path）
- 提供清晰的理由
- 可以分批处理，但要确保不遗漏任何知识点
"""
        return StepOutput(content=prompt)
    
    # 定义第三阶段：生成报告
    def stage_3_generate_report(step_input):
        """第三阶段：生成标注完成报告"""
        prompt = f"""
标注工作已完成，现在请生成最终报告。

任务：
1. 使用 get_tagging_progress 工具获取标注进度和统计信息
2. 生成一份完整的报告，包括：
   - 总知识点数
   - 已标注数量和未标注数量
   - 各个布鲁姆认知层级的分布：
     * Remember（记忆）
     * Understand（理解）
     * Apply（应用）
     * Analyze（分析）
     * Evaluate（评价）
     * Create（创造）
   - 分析该学科知识点的认知层级特点
   - 提供改进建议（如果有未标注的知识点）

请生成一份清晰、专业的标注报告。
"""
        return StepOutput(content=prompt)
    
    # 构建工作流
    workflow = Workflow(
        name="Bloom Taxonomy Tagging Workflow",
        steps=[
            Step(name="Stage 1: Review Knowledge", executor=stage_1_review_knowledge),
            Step(name="Stage 1: Agent Review", executor=reviewer_agent),
            Step(name="Stage 2: Prepare Tagging", executor=stage_2_tag_knowledge_points),
            Step(name="Stage 2: Agent Tag", executor=evaluator_agent),
            Step(name="Stage 3: Prepare Report", executor=stage_3_generate_report),
            Step(name="Stage 3: Generate Report", executor=evaluator_agent),
        ]
    )
    
    return workflow


def run_bloom_taxonomy_pipeline(subject: str = "math", model: str = "gpt-4o") -> Dict[str, Any]:
    """
    运行布鲁姆认知层级标注Pipeline
    
    Args:
        subject: 科目名称
        model: 使用的模型名称
        
    Returns:
        执行结果
    """
    print(f"\n{'='*80}")
    print(f"开始运行布鲁姆认知层级标注Pipeline")
    print(f"科目: {subject}")
    print(f"模型: {model}")
    print(f"{'='*80}\n")
    
    # 创建工作流
    workflow = create_bloom_taxonomy_workflow(subject=subject, model=model)
    
    # 运行工作流
    initial_input = f"开始为 {subject} 科目的知识点进行布鲁姆认知层级标注"
    
    # 运行工作流
    workflow.print_response(initial_input, markdown=True)
    
    # 获取最终统计
    print(f"\n{'='*80}")
    print("获取最终统计信息...")
    print(f"{'='*80}\n")
    
    progress = get_tagging_progress(subject=subject)
    
    if progress["success"]:
        print(f"\n✅ 标注完成统计:")
        print(f"   - 总知识点数: {progress['total']}")
        print(f"   - 已标注: {progress['tagged']}")
        print(f"   - 未标注: {progress['untagged']}")
        print(f"   - 完成度: {progress['progress_percentage']}%")
        print(f"\n   布鲁姆认知层级分布:")
        for level, count in progress['level_distribution'].items():
            print(f"     - {level}: {count}")
    else:
        print(f"\n❌ 获取统计信息失败: {progress['message']}")
    
    return progress


