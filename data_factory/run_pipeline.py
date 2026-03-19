import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv
import sys

# 确保可以导入 core 和 processors 模块
sys.path.append(str(Path(__file__).parent.parent))

from data_factory.agents.miner import create_miner_agent
from data_factory.agents.critic import create_critic_agent
from data_factory.agents.reader import create_reader_agent
from data_factory.utils import KnowledgeBuffer
from processors.pdf_processor import PDFProcessor

# 加载环境变量
load_dotenv()

def clean_json_string(s: str) -> str:
    """清洗 LLM 返回的 JSON 字符串"""
    s = s.strip()
    if s.startswith("```json"):
        s = s[7:]
    if s.startswith("```"):
        s = s[3:]
    if s.endswith("```"):
        s = s[:-3]
    return s.strip()

def run_pipeline(input_file: str, max_pages: int = 10):
    """
    运行智能流水线：
    1. Reader: 剪枝与记忆
    2. Miner: 挖掘 -> Buffer
    3. Critic: Buffer -> Graph
    """
    file_path = Path(input_file)
    if not file_path.exists():
        print(f"错误：文件 {file_path} 不存在")
        return

    print(f"\n🏭 启动智能流水线 (Smart Pipeline)...")
    print(f"📄 输入文件: {file_path.name}")
    
    # 初始化组件
    reader = create_reader_agent()
    miner = create_miner_agent()
    critic = create_critic_agent()
    buffer = KnowledgeBuffer()
    
    # 清空旧缓冲
    buffer.clear()
    
    # 1. PDF 处理与挖掘循环 (Reader + Miner Loop)
    print(f"\n🔄 Stage 1: 智能阅读与挖掘循环 (Reader + Miner)...")
    
    context_memory = "这是一本高中数学教材。"
    
    # 模拟逐页读取（这里只读取 PDF 文本，实际可扩展为读取章节）
    if file_path.suffix.lower() == '.pdf':
        for i in range(1, max_pages + 1):
            try:
                print(f"\n--- 处理第 {i} 页 ---")
                page_text = PDFProcessor.extract_page(file_path, i)
                
                # A. Reader 判断
                reader_resp = reader.analyze(page_text, context_memory)
                try:
                    decision_data = json.loads(clean_json_string(reader_resp))
                    decision = decision_data.get("decision", "PROCESS")
                    memory_update = decision_data.get("memory_update", "")
                    reason = decision_data.get("reason", "")
                    
                    # 更新全局记忆
                    if memory_update:
                        context_memory += f"\n[Page {i}]: {memory_update}"
                        # 保持记忆长度适中，简单截断
                        if len(context_memory) > 1000:
                            context_memory = "..." + context_memory[-1000:]
                    
                    print(f"👀 Reader 决策: {decision} | 理由: {reason}")
                    
                    if decision == "SKIP":
                        continue
                        
                except json.JSONDecodeError:
                    print("⚠️ Reader 返回格式错误，默认处理本页")
                
                # B. Miner 挖掘 (如果 Reader 决定处理)
                print(f"⛏️  Miner 正在挖掘...")
                mining_resp = miner.analyze(page_text, context_memory)
                try:
                    candidates = json.loads(clean_json_string(mining_resp))
                    if candidates:
                        buffer.add_candidates(candidates)
                    else:
                        print("   (Miner 未发现新概念)")
                except json.JSONDecodeError:
                    print("❌ Miner JSON 解析失败")
                    
                # 简单限速，避免触发 API 限制
                time.sleep(1)
                
            except Exception as e:
                print(f"⚠️ 处理第 {i} 页出错: {e}")
    else:
        print("目前流水线模式主要针对 PDF 分页优化，非 PDF 文件请使用 run_factory.py")
        return

    # 2. 异步质检 (Critic Async Consumer)
    print(f"\n\n🧐 Stage 2: 批量质检与入库 (Critic Consumer)...")
    
    all_candidates = buffer.get_all_candidates()
    if not all_candidates:
        print("⚠️ 箱子是空的，没有什么可质检的。")
        return
        
    print(f"📦 箱子里共有 {len(all_candidates)} 个待审核概念。")
    
    # 为了演示，Critic 一次性处理所有（实际生产中可以分批）
    # 注意：Critic 的 prompt 需要接收列表字符串
    candidates_str = json.dumps(all_candidates, ensure_ascii=False, indent=2)
    
    print("🚀 Critic 开始审核...")
    critique_resp = critic.analyze(candidates_str)
    
    try:
        refined_nodes = json.loads(clean_json_string(critique_resp))
        print(f"✅ 最终入库节点: {len(refined_nodes)} 个")
        
        # 保存结果
        output_file = Path(f"output/pipeline_graph_{file_path.stem}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({
                "source": str(input_file),
                "nodes": refined_nodes
            }, f, ensure_ascii=False, indent=2)
        print(f"💾 图谱已保存至: {output_file}")
        
    except json.JSONDecodeError:
        print("❌ Critic JSON 解析失败")
        print(f"Raw output: {critique_resp}")

if __name__ == "__main__":
    pdf_file = "dataset/books-pdf/普通高中教科书 数学  必修 第一册.pdf"
    # 处理前 8 页，观察 Reader 是否会跳过目录页
    run_pipeline(pdf_file, max_pages=8)


