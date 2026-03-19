"""
快速演示：景点知识点关联

只分析一个景点，快速看到效果
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.educational_chatroom import EducationalChatroom
import json


def main():
    print("\n" + "="*70)
    print("快速演示：景点 → 教学知识点")
    print("="*70 + "\n")
    
    # 创建聊天室
    chatroom = EducationalChatroom()
    
    # 加载数据
    scenic_data = project_root / "dataset" / "senarios" / "shanghai.json"
    chatroom.load_scenic_spots(str(scenic_data))
    
    # 选择一个有趣的景点：上海中心大厦（索引6）
    spot_index = 6
    spot_name = chatroom.scenic_agent.scenic_spots[spot_index]["scenic_spot"]
    
    print(f"分析景点: {spot_name}")
    print(f"目标: 提取高中数学和物理知识点\n")
    
    # 发现知识点
    edges = chatroom.discover_educational_edges(
        spot_index=spot_index,
        target_stage="高中",
        target_subjects=["数学", "物理"]
    )
    
    # 输出格式化的结果
    if edges:
        print("\n" + "="*70)
        print("提取的教学知识点（标准格式）")
        print("="*70 + "\n")
        
        # 转换为你期望的格式
        output = [edge.to_dict() for edge in edges]
        print(json.dumps(output, ensure_ascii=False, indent=2))
        
        # 保存
        output_file = project_root / "output" / "demo_educational_edge.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 结果已保存: {output_file}")
    else:
        print("\n未提取到知识点")


if __name__ == "__main__":
    main()


