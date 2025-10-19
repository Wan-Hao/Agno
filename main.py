"""
科研聊天室主程序
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
import argparse


def main():
    """主程序入口"""
    parser = argparse.ArgumentParser(
        description="科研聊天室 - 基于MAS的跨学科知识关联发现系统"
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="时间的本质",
        help="讨论主题"
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=3,
        help="讨论轮次"
    )
    parser.add_argument(
        "--agents",
        type=str,
        nargs="+",
        default=["physics", "literature", "math"],
        help="参与的智能体（可选：physics, literature, math, biology, philosophy, art）"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="输出目录"
    )
    
    args = parser.parse_args()
    
    # 验证配置
    try:
        Config.validate()
    except Exception as e:
        print(f"✗ 配置错误: {e}")
        print("请在 .env 文件中设置 GEMINI_API_KEY")
        return
    
    # 创建智能体
    agent_map = {
        "physics": PhysicsAgent,
        "literature": LiteratureAgent,
        "math": MathAgent,
        "biology": BiologyAgent,
        "philosophy": PhilosophyAgent,
        "art": ArtAgent
    }
    
    agents = []
    for agent_type in args.agents:
        if agent_type in agent_map:
            agents.append(agent_map[agent_type]())
        else:
            print(f"警告：未知的智能体类型 '{agent_type}'，已跳过")
    
    if len(agents) < 2:
        print("错误：至少需要2个智能体参与讨论")
        return
    
    # 创建聊天室
    chatroom = ResearchChatroom(
        topic=args.topic,
        agents=agents
    )
    
    # 开始讨论
    print(f"\n开始讨论主题：{args.topic}")
    print(f"参与者：{', '.join([a.name for a in agents])}")
    print(f"讨论轮次：{args.rounds}\n")
    
    edges = chatroom.discuss(
        rounds=args.rounds,
        extract_edges=True,
        evaluate_edges=True
    )
    
    # 生成报告
    print("\n生成综合报告...")
    report = chatroom.generate_report()
    
    # 设置输出目录
    output_dir = Path(args.output_dir) if args.output_dir else Config.OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 导出结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 导出知识图谱
    graph_file = output_dir / f"knowledge_graph_{timestamp}.json"
    chatroom.export_knowledge_graph(graph_file)
    
    # 导出讨论记录
    log_file = output_dir / f"discussion_log_{timestamp}.json"
    chatroom.export_discussion_log(log_file)
    
    # 导出报告
    report_file = output_dir / f"report_{timestamp}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✓ 报告已保存: {report_file}")
    
    # 显示摘要
    print(f"\n{'='*60}")
    print(f"讨论完成！")
    print(f"{'='*60}")
    print(f"发现的跨领域关联数: {len(edges)}")
    print(f"输出目录: {output_dir}")
    print(f"  - 知识图谱: {graph_file.name}")
    print(f"  - 讨论记录: {log_file.name}")
    print(f"  - 综合报告: {report_file.name}")


if __name__ == "__main__":
    from datetime import datetime
    main()

