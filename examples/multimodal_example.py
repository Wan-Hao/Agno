"""
多模态示例：使用不同类型的数据输入
"""
from core.chatroom import ResearchChatroom
from agents import PhysicsAgent, ArtAgent, BiologyAgent
from config import Config
from pathlib import Path


def main():
    """多模态示例"""
    # 验证配置
    try:
        Config.validate()
    except Exception as e:
        print(f"✗ 配置错误: {e}")
        print("请在 .env 文件中设置 GEMINI_API_KEY")
        return
    
    print("="*60)
    print("多模态示例：结合文本、图片、网页数据的讨论")
    print("="*60)
    
    # 创建聊天室
    chatroom = ResearchChatroom(
        topic="对称性与和谐",
        agents=[
            PhysicsAgent(),
            ArtAgent(),
            BiologyAgent()
        ]
    )
    
    # 为每个智能体加载不同类型的数据
    print("\n加载数据...")
    
    # 物理学家：加载文本数据（可以是关于对称性的物理学文献）
    # chatroom.load_data(
    #     "物理学家",
    #     "path/to/physics_paper.pdf",
    #     "pdf"
    # )
    
    # 艺术家：加载图片数据（对称的艺术作品）
    # chatroom.load_data(
    #     "艺术评论家",
    #     "path/to/symmetric_art.jpg",
    #     "image"
    # )
    
    # 生物学家：加载网页数据（关于生物对称性的网页）
    # chatroom.load_data(
    #     "生物学家",
    #     "https://en.wikipedia.org/wiki/Symmetry_in_biology",
    #     "web"
    # )
    
    print("注意：此示例需要实际的数据文件。")
    print("取消注释上面的代码并提供真实的文件路径来运行完整示例。\n")
    
    # 开始讨论
    edges = chatroom.discuss(
        rounds=2,
        extract_edges=True,
        evaluate_edges=True
    )
    
    # 导出结果
    output_dir = Config.OUTPUT_DIR / "multimodal_example"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    chatroom.export_knowledge_graph(output_dir / "knowledge_graph.json")
    chatroom.export_discussion_log(output_dir / "discussion_log.json")
    
    report = chatroom.generate_report()
    with open(output_dir / "report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✓ 示例完成！结果已保存到: {output_dir}")


if __name__ == "__main__":
    main()

