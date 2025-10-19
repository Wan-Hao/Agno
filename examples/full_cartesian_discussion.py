"""
全遍历笛卡尔积讨论

对所有数学节点和物理节点进行两两配对讨论
math节点数 × physics节点数 = 总讨论次数
"""
import sys
from pathlib import Path
import json
import time
from datetime import datetime

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.node_pair_chatroom import NodePairChatroom
from agents import PhysicsAgent, MathAgent
from config import Config


def load_progress(progress_file: Path) -> dict:
    """加载进度"""
    if progress_file.exists():
        with open(progress_file, 'r') as f:
            return json.load(f)
    return {"completed_pairs": [], "last_index": 0, "total_valid": 0}


def save_progress(progress_file: Path, progress: dict):
    """保存进度"""
    progress["last_updated"] = datetime.now().isoformat()
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=2)


def main():
    """全遍历讨论"""
    # 验证配置
    try:
        Config.validate()
    except Exception as e:
        print(f"✗ 配置错误: {e}")
        return
    
    print("="*70)
    print("全遍历笛卡尔积讨论")
    print("="*70)
    print()
    
    # 数据路径
    dataset_dir = Path(__file__).parent.parent / "dataset" / "graph"
    physics_graph_path = dataset_dir / "physics_knowledge_graph_new.json"
    math_graph_path = dataset_dir / "math_knowledge_graph_new.json"
    
    # 加载图谱
    print("📊 加载知识图谱...")
    with open(physics_graph_path, 'r', encoding='utf-8') as f:
        physics_graph = json.load(f)
    with open(math_graph_path, 'r', encoding='utf-8') as f:
        math_graph = json.load(f)
    
    math_nodes = math_graph['nodes']
    physics_nodes = physics_graph['nodes']
    
    print(f"✓ 数学节点: {len(math_nodes)}")
    print(f"✓ 物理节点: {len(physics_nodes)}")
    
    # 计算笛卡尔积
    total_pairs = len(math_nodes) * len(physics_nodes)
    print(f"✓ 总节点对数: {total_pairs}")
    print()
    
    # 生成所有节点对（笛卡尔积）
    print("🔄 生成节点对（笛卡尔积）...")
    all_pairs = []
    for math_node in math_nodes:
        for physics_node in physics_nodes:
            all_pairs.append((physics_node['id'], math_node['id']))
    
    print(f"✓ 生成 {len(all_pairs)} 对节点")
    print()
    
    # 输出和进度文件
    output_dir = Config.OUTPUT_DIR / "full_cartesian"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "cross_domain_edges.json"
    progress_file = output_dir / "progress.json"
    
    # 加载进度
    progress = load_progress(progress_file)
    completed_pairs = set(tuple(p) for p in progress.get("completed_pairs", []))
    last_index = progress.get("last_index", 0)
    total_valid = progress.get("total_valid", 0)
    
    if completed_pairs:
        print(f"📂 发现已有进度:")
        print(f"   已完成: {len(completed_pairs)} 对")
        print(f"   有效边: {total_valid} 条")
        print(f"   继续从第 {last_index + 1} 对开始...")
        print()
    
    # 创建聊天室
    print("🎯 创建聊天室...")
    physics_agent = PhysicsAgent()
    math_agent = MathAgent()
    
    chatroom = NodePairChatroom(
        physics_agent=physics_agent,
        math_agent=math_agent,
        physics_graph=physics_graph,
        math_graph=math_graph,
        output_file=output_file
    )
    
    print()
    print("="*70)
    print("开始全遍历讨论")
    print("="*70)
    print()
    
    # 统计信息
    start_time = time.time()
    valid_count = total_valid
    skipped_count = len(completed_pairs)
    
    # 遍历所有节点对
    for i, (physics_id, math_id) in enumerate(all_pairs):
        # 跳过已完成的
        if (physics_id, math_id) in completed_pairs:
            continue
        
        # 如果从中断恢复，跳过到上次的位置
        if i < last_index:
            continue
        
        # 显示进度
        progress_pct = (i + 1) / total_pairs * 100
        elapsed = time.time() - start_time
        avg_time_per_pair = elapsed / (i - skipped_count + 1) if (i - skipped_count) > 0 else 0
        eta_seconds = avg_time_per_pair * (total_pairs - i - 1)
        
        print(f"\n{'='*70}")
        print(f"进度: {i + 1}/{total_pairs} ({progress_pct:.2f}%)")
        print(f"已完成: {i - skipped_count + 1} 对 | 有效边: {valid_count} 条")
        print(f"平均耗时: {avg_time_per_pair:.2f}秒/对")
        print(f"预计剩余: {eta_seconds/60:.1f}分钟")
        print(f"{'='*70}")
        
        # 讨论节点对
        try:
            edge = chatroom.discuss_node_pair(
                physics_node_id=physics_id,
                math_node_id=math_id,
                context_depth=1
            )
            
            if edge:
                valid_count += 1
                print(f"✓ 生成有效边 ({valid_count})")
            else:
                print(f"○ 未生成边")
            
            # 记录完成
            completed_pairs.add((physics_id, math_id))
            
            # 每10对保存一次进度
            if (i + 1) % 10 == 0:
                progress = {
                    "completed_pairs": list(completed_pairs),
                    "last_index": i,
                    "total_valid": valid_count,
                    "total_pairs": total_pairs,
                    "progress_percentage": progress_pct
                }
                save_progress(progress_file, progress)
                print(f"💾 进度已保存")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  检测到中断信号，保存进度...")
            progress = {
                "completed_pairs": list(completed_pairs),
                "last_index": i,
                "total_valid": valid_count,
                "total_pairs": total_pairs,
                "progress_percentage": progress_pct
            }
            save_progress(progress_file, progress)
            print(f"✓ 进度已保存到: {progress_file}")
            print(f"✓ 下次运行将从第 {i + 1} 对继续")
            return
        
        except Exception as e:
            print(f"✗ 处理失败: {e}")
            # 继续处理下一对
            continue
    
    # 最终保存
    progress = {
        "completed_pairs": list(completed_pairs),
        "last_index": len(all_pairs) - 1,
        "total_valid": valid_count,
        "total_pairs": total_pairs,
        "progress_percentage": 100.0,
        "status": "completed"
    }
    save_progress(progress_file, progress)
    
    # 显示最终统计
    total_time = time.time() - start_time
    
    print("\n" + "="*70)
    print("🎉 全遍历完成！")
    print("="*70)
    print()
    print(f"总节点对数: {total_pairs}")
    print(f"已处理: {len(completed_pairs)}")
    print(f"生成有效边: {valid_count}")
    print(f"有效率: {valid_count/len(completed_pairs)*100:.2f}%")
    print(f"总耗时: {total_time/3600:.2f}小时")
    print()
    print(f"结果文件: {output_file}")
    print(f"进度文件: {progress_file}")
    print()


def resume_from_progress():
    """从进度文件恢复运行"""
    print("尝试从进度恢复...")
    main()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--resume":
        resume_from_progress()
    else:
        main()

