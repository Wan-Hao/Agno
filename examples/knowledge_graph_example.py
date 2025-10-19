"""
知识图谱示例：使用已有的物理和数学知识图谱数据进行跨学科讨论
"""
from core.chatroom import ResearchChatroom
from agents import PhysicsAgent, MathAgent
from processors import KnowledgeGraphProcessor
from config import Config
from pathlib import Path
import json


def main():
    """知识图谱数据驱动的跨学科讨论"""
    # 验证配置
    try:
        Config.validate()
    except Exception as e:
        print(f"✗ 配置错误: {e}")
        print("请在 .env 文件中设置 GEMINI_API_KEY")
        return
    
    print("="*70)
    print("知识图谱驱动示例：物理学与数学的跨学科知识关联发现")
    print("="*70)
    print()
    
    # 数据路径
    dataset_dir = Path(__file__).parent.parent / "dataset" / "graph"
    physics_graph_path = dataset_dir / "physics_knowledge_graph_new.json"
    math_graph_path = dataset_dir / "math_knowledge_graph_new.json"
    
    # 检查数据文件
    if not physics_graph_path.exists():
        print(f"✗ 物理知识图谱文件不存在: {physics_graph_path}")
        return
    if not math_graph_path.exists():
        print(f"✗ 数学知识图谱文件不存在: {math_graph_path}")
        return
    
    print("📊 加载知识图谱数据...\n")
    
    # 创建处理器
    kg_processor = KnowledgeGraphProcessor()
    
    # 加载物理知识图谱
    print("→ 加载物理知识图谱...")
    physics_data = kg_processor.process(physics_graph_path)
    print(f"  ✓ 物理知识图谱: {physics_data['metadata']['num_nodes']} 个节点, "
          f"{physics_data['metadata']['num_edges']} 条边")
    
    # 加载数学知识图谱
    print("→ 加载数学知识图谱...")
    math_data = kg_processor.process(math_graph_path)
    print(f"  ✓ 数学知识图谱: {math_data['metadata']['num_nodes']} 个节点, "
          f"{math_data['metadata']['num_edges']} 条边")
    print()
    
    # 创建智能体
    physics_agent = PhysicsAgent()
    math_agent = MathAgent()
    
    # 为智能体加载知识
    print("📚 为智能体加载知识...\n")
    
    # 为物理智能体构建上下文（聚焦某些主题）
    physics_context = kg_processor.build_context_for_discussion(
        physics_data,
        focus_themes=["机械运动与物理模型", "相互作用", "能量", "动量"],
        max_concepts=25
    )
    physics_agent.load_knowledge(
        data=physics_context,
        data_type="knowledge_graph",
        source=str(physics_graph_path)
    )
    print(f"  ✓ 已为 {physics_agent.name} 加载物理知识")
    
    # 为数学智能体构建上下文
    math_context = kg_processor.build_context_for_discussion(
        math_data,
        focus_themes=["集合", "函数", "几何", "向量"],
        max_concepts=25
    )
    math_agent.load_knowledge(
        data=math_context,
        data_type="knowledge_graph",
        source=str(math_graph_path)
    )
    print(f"  ✓ 已为 {math_agent.name} 加载数学知识")
    print()
    
    # 创建聊天室
    chatroom = ResearchChatroom(
        topic="物理学与数学的深层结构：从运动、空间到抽象",
        agents=[physics_agent, math_agent]
    )
    
    # 开始讨论
    print("🎯 开始跨学科讨论...\n")
    print("讨论将围绕以下问题展开：")
    print("  1. 物理中的运动、力、能量概念与数学中的函数、向量、变换有何对应？")
    print("  2. 物理模型的建立如何依赖数学抽象？")
    print("  3. 有哪些深层的结构相似性或概念映射？")
    print()
    
    edges = chatroom.discuss(
        rounds=3,  # 进行3轮深入讨论
        extract_edges=True,
        evaluate_edges=True
    )
    
    # 输出结果
    output_dir = Config.OUTPUT_DIR / "knowledge_graph_example"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*70)
    print("💾 保存结果...")
    print("="*70 + "\n")
    
    # 导出新发现的知识边
    new_edges_file = output_dir / "new_cross_domain_edges.json"
    edges_data = {
        "source_graphs": {
            "physics": str(physics_graph_path),
            "math": str(math_graph_path)
        },
        "topic": chatroom.topic,
        "edges": [edge.to_dict() for edge in edges],
        "statistics": {
            "total_edges": len(edges),
            "high_quality_edges": len([e for e in edges if e.get_overall_score() >= 0.7])
        }
    }
    
    with open(new_edges_file, 'w', encoding='utf-8') as f:
        json.dump(edges_data, f, ensure_ascii=False, indent=2)
    print(f"✓ 新发现的跨领域关联已保存: {new_edges_file}")
    
    # 导出完整知识图谱
    chatroom.export_knowledge_graph(output_dir / "integrated_knowledge_graph.json")
    
    # 导出讨论记录
    chatroom.export_discussion_log(output_dir / "discussion_log.json")
    
    # 生成综合报告
    report = chatroom.generate_report()
    report_file = output_dir / "cross_domain_analysis_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✓ 综合分析报告已保存: {report_file}")
    print()
    
    # 显示统计信息
    print("="*70)
    print("📊 发现的跨领域知识关联统计")
    print("="*70)
    print()
    print(f"总关联数: {len(edges)}")
    
    if edges:
        high_quality = [e for e in edges if e.get_overall_score() >= 0.7]
        medium_quality = [e for e in edges if 0.5 <= e.get_overall_score() < 0.7]
        
        print(f"高质量关联 (≥0.7): {len(high_quality)}")
        print(f"中等质量关联 (0.5-0.7): {len(medium_quality)}")
        print()
        
        # 显示几个高质量的关联示例
        if high_quality:
            print("🌟 高质量关联示例：")
            print()
            for i, edge in enumerate(high_quality[:5], 1):
                print(f"{i}. {edge}")
                print(f"   评分: {edge.get_overall_score():.2f}")
                print(f"   描述: {edge.relation_description[:150]}...")
                print()
        
        # 关系类型分布
        relation_types = {}
        for edge in edges:
            rel_type = edge.relation_type
            relation_types[rel_type] = relation_types.get(rel_type, 0) + 1
        
        print("📈 关系类型分布：")
        for rel_type, count in sorted(relation_types.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {rel_type}: {count}")
    else:
        print("未发现明确的跨领域关联")
    
    print()
    print("="*70)
    print("✨ 完成！")
    print("="*70)
    print()
    print(f"所有结果已保存到: {output_dir}")
    print()
    print("你可以查看：")
    print(f"  1. 新的跨领域关联: {new_edges_file.name}")
    print(f"  2. 整合后的知识图谱: integrated_knowledge_graph.json")
    print(f"  3. 完整的讨论记录: discussion_log.json")
    print(f"  4. 综合分析报告: {report_file.name}")
    print()


if __name__ == "__main__":
    main()

