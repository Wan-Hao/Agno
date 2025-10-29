"""
简单版本的布鲁姆认知层级标注脚本

直接使用OpenAI客户端和工具函数进行标注
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Any

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置API配置
os.environ['OPENAI_API_KEY'] = 'sk-bcGMOlL9AB7vbhACtYRYObdxtrPvcN1jPegFMKdzYfNvaAxM'
os.environ['OPENAI_BASE_URL'] = 'https://new.nexai.it.com/v1'

from core.openai_client import OpenAIClient
from tools.bloom_taxonomy_tools import (
    get_all_knowledge_points,
    tag_knowledge_point_remember,
    tag_knowledge_point_understand,
    tag_knowledge_point_apply,
    tag_knowledge_point_analyze,
    tag_knowledge_point_evaluate,
    tag_knowledge_point_create,
    get_tagging_progress
)


# 布鲁姆认知层级描述
BLOOM_LEVEL_DESCRIPTIONS = """
布鲁姆认知目标分类（由低到高）：

1. **记忆（Remember）** - 识别和回忆相关知识
   关键词：记住、列举、识别、回忆、定义
   例如：记住集合的定义，识别数学符号

2. **理解（Understand）** - 理解材料的含义，能够解释和说明
   关键词：解释、描述、说明、概括、分类
   例如：理解函数的概念，解释集合之间的关系

3. **应用（Apply）** - 在新情境中使用信息和规则
   关键词：应用、使用、计算、求解、实施
   例如：应用基本不等式求最值，使用二分法求解方程

4. **分析（Analyze）** - 将信息分解为组成部分，理解结构和关系
   关键词：分析、区分、比较、推导、归因
   例如：分析函数的单调性，比较不同集合运算的关系

5. **评价（Evaluate）** - 基于标准和准则做出判断
   关键词：评价、判断、批判、论证、辩护
   例如：评价不同解题方法的优劣，判断证明的正确性

6. **创造（Create）** - 组合元素形成新的整体或结构
   关键词：创造、设计、构建、规划、生成
   例如：构建新的数学模型，设计解题策略
"""


def classify_knowledge_point(client: OpenAIClient, node: Dict[str, Any]) -> tuple[str, str]:
    """
    使用AI分类单个知识点
    
    Returns:
        (level, reasoning) 元组
    """
    node_id = node.get("id", "")
    label = node.get("label", "")
    properties = node.get("properties", {})
    description = properties.get("description", "")
    category = properties.get("category", "")
    theme = properties.get("theme", "")
    abilities = properties.get("cultivated_abilities", [])
    
    prompt = f"""
请根据布鲁姆认知目标分类理论，对以下知识点进行分类：

{BLOOM_LEVEL_DESCRIPTIONS}

知识点信息：
- ID: {node_id}
- 名称: {label}
- 描述: {description}
- 类别: {category}
- 主题: {theme}
- 培养能力: {', '.join(abilities) if abilities else '无'}

请分析该知识点的核心学习目标，判断它最符合哪个布鲁姆认知层级。

请按以下JSON格式回复（只输出JSON，不要其他内容）：
{{
  "level": "Remember/Understand/Apply/Analyze/Evaluate/Create",
  "reasoning": "简短的判断理由（不超过50字）"
}}
"""
    
    system_instruction = "你是一位教育评估专家，精通布鲁姆认知目标分类理论。请客观、准确地对知识点进行分类。"
    
    try:
        response = client.generate(prompt, system_instruction)
        # 尝试解析JSON
        # 移除可能的markdown代码块标记
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        
        result = json.loads(response)
        level = result.get("level", "Understand")
        reasoning = result.get("reasoning", "")
        
        # 验证level是否合法
        valid_levels = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
        if level not in valid_levels:
            # 尝试修正
            for valid_level in valid_levels:
                if valid_level.lower() in level.lower():
                    level = valid_level
                    break
            else:
                level = "Understand"  # 默认值
        
        return level, reasoning
        
    except Exception as e:
        print(f"  ⚠️  解析失败: {e}, 使用默认值")
        # 返回默认值
        return "Understand", "自动分类失败，使用默认层级"


def tag_knowledge_point(node_id: str, level: str, reasoning: str, file_path: str) -> bool:
    """
    给知识点打标签
    
    Returns:
        是否成功
    """
    tag_functions = {
        "Remember": tag_knowledge_point_remember,
        "Understand": tag_knowledge_point_understand,
        "Apply": tag_knowledge_point_apply,
        "Analyze": tag_knowledge_point_analyze,
        "Evaluate": tag_knowledge_point_evaluate,
        "Create": tag_knowledge_point_create
    }
    
    tag_func = tag_functions.get(level)
    if not tag_func:
        print(f"  ❌ 未知的层级: {level}")
        return False
    
    try:
        result = tag_func(node_id, file_path, reasoning)
        return result.get("success", False)
    except Exception as e:
        print(f"  ❌ 标注失败: {e}")
        return False


def process_subject(subject: str, client: OpenAIClient):
    """处理单个科目的标注"""
    
    print(f"\n{'='*80}")
    print(f"开始处理 {subject.upper()} 知识图谱")
    print(f"{'='*80}\n")
    
    # 获取所有知识点
    result = get_all_knowledge_points(subject)
    
    if not result["success"]:
        print(f"❌ 获取知识点失败: {result.get('message', '未知错误')}")
        return
    
    nodes = result["nodes"]
    file_path = result["file_path"]
    total = len(nodes)
    
    print(f"📊 找到 {total} 个知识点")
    print(f"📁 文件路径: {file_path}\n")
    
    # 逐个处理知识点
    success_count = 0
    fail_count = 0
    
    for i, node in enumerate(nodes, 1):
        node_id = node.get("id", "")
        label = node.get("label", "")
        
        print(f"[{i}/{total}] 处理: {label} ({node_id})")
        
        # 分类
        level, reasoning = classify_knowledge_point(client, node)
        print(f"  → 层级: {level}")
        print(f"  → 理由: {reasoning}")
        
        # 打标签
        if tag_knowledge_point(node_id, level, reasoning, file_path):
            print(f"  ✅ 标注成功")
            success_count += 1
        else:
            print(f"  ❌ 标注失败")
            fail_count += 1
        
        print()
    
    # 显示统计
    print(f"\n{'='*80}")
    print(f"{subject.upper()} 知识图谱标注完成")
    print(f"{'='*80}")
    print(f"✅ 成功: {success_count}")
    print(f"❌ 失败: {fail_count}")
    print(f"📈 成功率: {success_count/total*100:.1f}%")
    
    # 获取最终统计
    progress = get_tagging_progress(subject)
    if progress.get("success"):
        print(f"\n最终统计:")
        print(f"  总知识点数: {progress['total']}")
        print(f"  已标注: {progress['tagged']}")
        print(f"  完成度: {progress['progress_percentage']}%")
        print(f"\n  布鲁姆认知层级分布:")
        for level, count in progress['level_distribution'].items():
            if count > 0:
                print(f"    {level}: {count}")


def main():
    """主函数"""
    
    print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                     布鲁姆认知层级批量标注任务                                  ║
║                                                                                ║
║  将对以下数据集进行标注：                                                       ║
║  1. math_knowledge_graph_new.json (数学知识图谱)                              ║
║  2. physics_knowledge_graph_new.json (物理知识图谱)                           ║
║                                                                                ║
║  使用模型: gemini-2.5-pro                                                      ║
╚════════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # 创建OpenAI客户端
    client = OpenAIClient(
        model_name="gemini-2.5-pro",
        temperature=0.3  # 使用较低的温度以获得更一致的结果
    )
    
    # 处理两个科目
    subjects = ["math", "physics"]
    
    for subject in subjects:
        try:
            process_subject(subject, client)
        except Exception as e:
            print(f"\n❌ 处理 {subject} 时发生错误: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"\n{'='*80}")
    print("🎉 所有标注任务完成！")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()

