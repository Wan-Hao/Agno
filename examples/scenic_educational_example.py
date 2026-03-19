"""
景点教育知识点关联示例

演示如何从景点中提取教学知识点
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.educational_chatroom import EducationalChatroom


def main():
    """主函数"""
    print("="*70)
    print("景点教育知识点关联系统")
    print("="*70)
    print()
    
    # 创建聊天室
    chatroom = EducationalChatroom()
    
    # 加载景点数据
    scenic_data_path = project_root / "dataset" / "senarios" / "shanghai.json"
    
    if not scenic_data_path.exists():
        print(f"✗ 景点数据文件不存在: {scenic_data_path}")
        return
    
    print(f"正在加载景点数据: {scenic_data_path}")
    chatroom.load_scenic_spots(str(scenic_data_path))
    
    spots = chatroom.scenic_agent.list_all_spots()
    print(f"✓ 已加载 {len(spots)} 个景点\n")
    
    # 显示景点列表
    print("可用景点:")
    for i, spot in enumerate(spots):
        print(f"  {i}. {spot}")
    print()
    
    # 示例1: 分析单个景点
    print("\n" + "="*70)
    print("示例1: 分析单个景点（东方明珠电视塔）")
    print("="*70 + "\n")
    
    edges = chatroom.discover_educational_edges(
        spot_index=2,  # 东方明珠电视塔
        target_stage="高中",
        target_subjects=["数学", "物理"],
        rounds=2
    )
    
    # 示例2: 分析多个景点
    print("\n\n" + "="*70)
    print("示例2: 分析前3个景点")
    print("="*70 + "\n")
    
    all_edges = chatroom.discover_all_spots(
        target_stage="高中",
        target_subjects=["数学", "物理"],
        max_spots=3
    )
    
    # 导出结果
    output_dir = project_root / "output" / "educational_edges"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "shanghai_scenic_knowledge.json"
    
    print(f"\n正在导出结果...")
    chatroom.export_results(str(output_file))
    
    # 显示统计
    stats = chatroom.get_statistics()
    print(f"\n" + "="*70)
    print("统计信息")
    print("="*70)
    print(f"总知识点数: {stats['total_edges']}")
    print(f"\n按学科分布:")
    for subject, count in stats['by_subject'].items():
        print(f"  {subject}: {count}")
    print(f"\n按景点分布:")
    for spot, count in stats['by_spot'].items():
        print(f"  {spot}: {count}")
    print(f"\n按难度分布:")
    for diff, count in stats['by_difficulty'].items():
        print(f"  {diff}: {count}")
    print(f"\n平均置信度: {stats['avg_confidence']:.2f}")
    print()
    
    # 显示示例输出
    if chatroom.edge_builder.edges:
        print("\n" + "="*70)
        print("示例输出格式 (第一个知识点)")
        print("="*70)
        first_edge = chatroom.edge_builder.edges[0]
        print(first_edge.to_json())
    
    print("\n✓ 完成！")
    print(f"详细结果已保存到: {output_file}")


if __name__ == "__main__":
    main()


