import json
import os
from pathlib import Path
from dotenv import load_dotenv
import sys

# 确保可以导入 core 和 processors 模块
sys.path.append(str(Path(__file__).parent.parent))

from data_factory.agents.miner import create_miner_agent
from data_factory.agents.critic import create_critic_agent
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

def run_knowledge_factory(input_file: str, max_pages: int = 20):
    """
    运行知识工厂流水线：挖掘 -> 辩论/质检 -> 输出
    Args:
        input_file: 输入文件路径
        max_pages:如果是PDF，最大处理页数（默认20页，用于快速测试）
    """
    file_path = Path(input_file)
    if not file_path.exists():
        print(f"错误：文件 {file_path} 不存在")
        return

    print(f"\n🏭 启动知识工厂 (Agentic Knowledge Factory)...")
    print(f"📄 读取文件: {file_path.name}")
    
    raw_text = ""
    if file_path.suffix.lower() == '.pdf':
        print(f"📚 检测到 PDF 文件，正在解析前 {max_pages} 页...")
        try:
            # 提取指定页数的文本
            pages_text = []
            for i in range(1, max_pages + 1):
                try:
                    text = PDFProcessor.extract_page(file_path, i)
                    pages_text.append(text)
                except Exception as e:
                    print(f"⚠️ 读取第 {i} 页失败: {e}")
                    break
            raw_text = "\n\n".join(pages_text)
            print(f"✅ 成功提取 {len(raw_text)} 个字符")
        except Exception as e:
            print(f"❌ PDF 解析失败: {e}")
            return
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

    # 1. 挖掘阶段 (Mining Phase)
    print(f"\n⛏️  Stage 1: 知识挖掘 (Miner Agent)...")
    miner = create_miner_agent()
    mining_response_text = miner.analyze(raw_text)
    
    candidates = []
    try:
        cleaned_mining = clean_json_string(mining_response_text)
        candidates = json.loads(cleaned_mining)
        print(f"✅ 挖掘出 {len(candidates)} 个候选概念：")
        for c in candidates:
            print(f"   - [{c.get('concept_type')}] {c.get('concept_name')}")
    except json.JSONDecodeError as e:
        print(f"❌ Miner JSON 解析失败: {e}")
        print(f"原始输出: {mining_response_text}")
        return

    # 2. 质检阶段 (Critique Phase)
    print(f"\n🧐 Stage 2: 专家质检与布鲁姆增强 (Critic Agent)...")
    critic = create_critic_agent()
    
    # 为了演示稳定性，仅处理前 5 个核心概念
    print(f"⚠️ 演示模式：仅处理前 5 个候选概念 (共 {len(candidates)} 个)")
    candidates_subset = candidates[:5]
    
    # 将候选列表转换为文本供Critic阅读
    candidates_json_str = json.dumps(candidates_subset, ensure_ascii=False, indent=2)
    
    critique_response_text = critic.analyze(candidates_json_str)
    
    refined_nodes = []
    try:
        cleaned_critique = clean_json_string(critique_response_text)
        refined_nodes = json.loads(cleaned_critique)
        print(f"✅ 最终通过审核节点: {len(refined_nodes)} 个")
    except json.JSONDecodeError as e:
        print(f"❌ Critic JSON 解析失败: {e}")
        print(f"原始输出: {critique_response_text}")
        return
    
    # 3. 结果展示与保存
    output_dir = Path("output/factory_results")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"graph_{file_path.stem}.json"
    
    final_data = {
        "source_file": str(file_path),
        "nodes": refined_nodes
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
        
    print(f"\n💾 结果已保存至: {output_file}")
    
    # 打印一个示例节点看看效果
    if refined_nodes:
        print("\n✨ 示例节点展示 (包含布鲁姆层级):")
        example = refined_nodes[0]
        print(json.dumps(example, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    # 优先测试用户提供的 PDF
    pdf_file = "dataset/books-pdf/普通高中教科书 数学  必修 第一册.pdf"
    if Path(pdf_file).exists():
        run_knowledge_factory(pdf_file, max_pages=5)
    else:
        # 回退到 Markdown 测试
        test_file = "dataset/raw_data/texts/mechanical_energy.md"
        run_knowledge_factory(test_file)
