"""
大规模示例：六个领域专家的跨学科讨论
"""
from core.chatroom import ResearchChatroom
from agents import (
    PhysicsAgent,
    LiteratureAgent,
    MathAgent,
    BiologyAgent,
    PhilosophyAgent,
    ArtAgent
)
from config import Config
from pathlib import Path


def main():
    """大规模六方讨论示例"""
    # 验证配置
    try:
        Config.validate()
    except Exception as e:
        print(f"✗ 配置错误: {e}")
        print("请在 .env 文件中设置 GEMINI_API_KEY")
        return
    
    print("="*60)
    print("大规模示例：六个领域专家的深度跨学科对话")
    print("="*60)
    
    # 创建聊天室 - 包含所有领域的专家
    chatroom = ResearchChatroom(
        topic="秩序、混沌与涌现",
        agents=[
            PhysicsAgent(),      # 从热力学、统计物理角度
            MathAgent(),         # 从混沌理论、复杂系统角度
            BiologyAgent(),      # 从自组织、进化角度
            PhilosophyAgent(),   # 从本体论、认识论角度
            LiteratureAgent(),   # 从叙事结构、意义生成角度
            ArtAgent()          # 从形式、创造性角度
        ]
    )
    
    # 开始深度讨论
    print("\n这将是一个较长的讨论过程，请稍候...\n")
    
    edges = chatroom.discuss(
        rounds=3,  # 多轮深入讨论
        extract_edges=True,
        evaluate_edges=True
    )
    
    # 导出结果
    output_dir = Config.OUTPUT_DIR / "six_agents_example"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    chatroom.export_knowledge_graph(output_dir / "knowledge_graph.json")
    chatroom.export_discussion_log(output_dir / "discussion_log.json")
    
    report = chatroom.generate_report()
    with open(output_dir / "report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✓ 示例完成！")
    print(f"✓ 结果已保存到: {output_dir}")
    print(f"\n发现的跨领域关联：")
    for i, edge in enumerate(edges[:10], 1):  # 显示前10个
        print(f"  {i}. {edge}")
    
    if len(edges) > 10:
        print(f"  ... 还有 {len(edges) - 10} 个关联，请查看完整报告")


if __name__ == "__main__":
    main()

