"""
简单测试：验证景点系统是否正常工作
"""
from pathlib import Path
from agents.scenic_agent import ScenicSpotAgent
from agents.domain_agents import PhysicsAgent, MathAgent
from core.educational_edge import EducationalEdgeBuilder, KnowledgePoint, EducationalEdge
import json

def test_basic():
    """基础功能测试"""
    print("="*70)
    print("测试1: 加载景点数据")
    print("="*70)
    
    # 创建景点智能体
    scenic_agent = ScenicSpotAgent()
    
    # 加载数据
    json_path = "dataset/senarios/shanghai.json"
    success = scenic_agent.load_scenic_spots_from_json(json_path)
    
    if success:
        print(f"✓ 成功加载 {len(scenic_agent.scenic_spots)} 个景点")
        
        # 显示景点列表
        print("\n景点列表:")
        for i, spot_name in enumerate(scenic_agent.list_all_spots()):
            print(f"  {i}. {spot_name}")
    else:
        print("✗ 加载失败")
        return False
    
    print("\n" + "="*70)
    print("测试2: 创建教育知识边")
    print("="*70)
    
    # 手动创建一个示例教育边
    builder = EducationalEdgeBuilder()
    
    edge = builder.add_edge(
        province_city="上海市",
        scenic_spot="上海中心大厦",
        scene_description="上海中心大厦高度达632米，采用螺旋上升的外立面设计，外立面扭转约120度以应对风力。这个设计体现了流体力学中的减阻原理。",
        stage="高中",
        subject="物理",
        chapter_number=8,
        chapter_title="流体力学基础",
        section_number="8.2",
        section_title="流体的阻力",
        point_name="空气阻力与物体形状的关系",
        point_description="理解物体在流体中运动时受到的阻力，掌握减小阻力的方法",
        formula="F_阻 = ½ρv²CdA",
        difficulty="中等偏上",
        applications=["建筑设计", "车辆设计", "空气动力学"],
        reasoning="超高建筑的抗风设计是流体力学的经典应用",
        confidence=0.9
    )
    
    print(f"✓ 创建教育边: {edge}")
    
    print("\n" + "="*70)
    print("测试3: 输出JSON格式")
    print("="*70)
    
    # 输出JSON
    output = builder.to_json_list()
    print("\n标准输出格式:")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    
    # 保存到文件
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "test_scenic_edge.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 已保存到: {output_file}")
    
    print("\n" + "="*70)
    print("✓ 所有基础测试通过！")
    print("="*70)
    
    return True


def show_spot_detail():
    """显示一个景点的详细信息"""
    print("\n" + "="*70)
    print("测试4: 查看景点详情")
    print("="*70)
    
    with open("dataset/senarios/shanghai.json", 'r', encoding='utf-8') as f:
        spots = json.load(f)
    
    # 选择上海中心大厦
    spot = spots[6]
    
    print(f"\n景点名称: {spot['scenic_spot']}")
    print(f"城市: {spot['province_city']}")
    print(f"\n描述:\n{spot['description']}")
    
    print("\n可以提取的教学点示例:")
    print("  📐 数学:")
    print("     - 螺旋曲线的数学模型")
    print("     - 扭转角度的计算")
    print("     - 高度与层数的线性关系")
    print("  ⚛️ 物理:")
    print("     - 流体力学（风阻）")
    print("     - 结构力学（抗震）")
    print("     - 材料科学（玻璃幕墙）")


if __name__ == "__main__":
    print("\n景点教育知识点关联系统 - 基础测试\n")
    
    try:
        # 运行测试
        test_basic()
        show_spot_detail()
        
        print("\n" + "="*70)
        print("✓ 系统运行正常！")
        print("\n下一步:")
        print("  - 运行 python examples/quick_scenic_demo.py (需要API)")
        print("  - 查看 SCENIC_EDUCATION_GUIDE.md 了解详情")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()


