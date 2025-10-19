"""
基础示例：简单的三方讨论
"""
from core.chatroom import ResearchChatroom
from agents import PhysicsAgent, LiteratureAgent, MathAgent
from config import Config
from pathlib import Path


def main():
    """基础示例"""
    # 验证配置
    try:
        Config.validate()
    except Exception as e:
        print(f"✗ 配置错误: {e}")
        print("请在 .env 文件中设置 GEMINI_API_KEY")
        return
    
    print("="*60)
    print("基础示例：物理学、文学、数学的跨学科对话")
    print("="*60)
    
    # 创建聊天室
    chatroom = ResearchChatroom(
        topic="时间的本质与流逝",
        agents=[
            PhysicsAgent(),
            LiteratureAgent(),
            MathAgent()
        ]
    )
    
    # 开始讨论
    edges = chatroom.discuss(
        rounds=2,  # 简短的讨论
        extract_edges=True,
        evaluate_edges=True
    )
    
    # 导出结果
    output_dir = Config.OUTPUT_DIR / "basic_example"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    chatroom.export_knowledge_graph(output_dir / "knowledge_graph.json")
    chatroom.export_discussion_log(output_dir / "discussion_log.json")
    
    # 生成报告
    report = chatroom.generate_report()
    with open(output_dir / "report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✓ 示例完成！结果已保存到: {output_dir}")


if __name__ == "__main__":
    main()

