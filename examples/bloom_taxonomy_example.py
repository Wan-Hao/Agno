"""
布鲁姆认知层级标注示例

演示如何使用布鲁姆认知层级标注Pipeline对知识点进行自动标注
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from workflows.bloom_taxonomy_workflow import run_bloom_taxonomy_pipeline
from tools.bloom_taxonomy_tools import get_tagging_progress


def main():
    """主函数"""
    
    print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                     布鲁姆认知层级标注Pipeline示例                              ║
║                                                                                ║
║  本示例演示如何使用AI Agent自动对知识图谱中的知识点进行布鲁姆认知层级标注      ║
╚════════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # 选择科目
    subject = input("请输入科目名称 (默认: math): ").strip() or "math"
    
    # 选择模型
    print("\n可用模型:")
    print("  1. gpt-4o (推荐，准确度高)")
    print("  2. gpt-4o-mini (快速，成本低)")
    print("  3. gpt-4-turbo")
    
    model_choice = input("\n请选择模型 (默认: 1): ").strip() or "1"
    
    model_map = {
        "1": "gpt-4o",
        "2": "gpt-4o-mini",
        "3": "gpt-4-turbo"
    }
    
    model = model_map.get(model_choice, "gpt-4o")
    
    # 显示当前状态
    print(f"\n📊 检查当前标注状态...")
    progress = get_tagging_progress(subject=subject)
    
    if progress["success"]:
        print(f"\n当前状态:")
        print(f"  - 总知识点数: {progress['total']}")
        print(f"  - 已标注: {progress['tagged']}")
        print(f"  - 未标注: {progress['untagged']}")
        print(f"  - 完成度: {progress['progress_percentage']}%")
        
        if progress['tagged'] > 0:
            print(f"\n  当前布鲁姆认知层级分布:")
            for level, count in progress['level_distribution'].items():
                if count > 0:
                    print(f"    - {level}: {count}")
    
    # 确认是否继续
    print(f"\n⚠️  即将使用 {model} 模型对 {subject} 科目的知识点进行标注")
    print("   这可能需要几分钟时间，并会消耗API调用配额")
    
    confirm = input("\n是否继续？(y/N): ").strip().lower()
    
    if confirm != 'y':
        print("\n❌ 已取消操作")
        return
    
    # 运行Pipeline
    print("\n" + "="*80)
    print("🚀 开始运行布鲁姆认知层级标注Pipeline...")
    print("="*80 + "\n")
    
    try:
        result = run_bloom_taxonomy_pipeline(subject=subject, model=model)
        
        print("\n" + "="*80)
        print("✅ Pipeline执行完成！")
        print("="*80)
        
    except Exception as e:
        print("\n" + "="*80)
        print(f"❌ Pipeline执行失败: {str(e)}")
        print("="*80)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


