"""
运行布鲁姆认知层级标注

对math和physics两个知识图谱进行自动标注
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置API配置
os.environ['OPENAI_API_KEY'] = 'sk-bcGMOlL9AB7vbhACtYRYObdxtrPvcN1jPegFMKdzYfNvaAxM'
os.environ['OPENAI_BASE_URL'] = 'https://new.nexai.it.com/v1'

from workflows.bloom_taxonomy_workflow import run_bloom_taxonomy_pipeline


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
    
    subjects = ["math", "physics"]
    model = "gemini-2.5-pro"
    
    for subject in subjects:
        print(f"\n{'='*80}")
        print(f"开始标注 {subject.upper()} 知识图谱")
        print(f"{'='*80}\n")
        
        try:
            result = run_bloom_taxonomy_pipeline(subject=subject, model=model)
            
            print(f"\n✅ {subject.upper()} 知识图谱标注完成！")
            if result.get("success"):
                print(f"   总知识点数: {result.get('total', 'N/A')}")
                print(f"   已标注: {result.get('tagged', 'N/A')}")
                print(f"   完成度: {result.get('progress_percentage', 'N/A')}%")
                
        except Exception as e:
            print(f"\n❌ {subject.upper()} 知识图谱标注失败: {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"\n{'='*80}")
    print("所有标注任务完成！")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()


