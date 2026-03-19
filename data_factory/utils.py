import json
from pathlib import Path
from typing import List, Dict, Any

class KnowledgeBuffer:
    """
    知识缓冲箱 (The Box)
    
    作用：
    1. 存储 Miner 挖掘出的原始候选概念
    2. 充当 Miner 和 Critic 之间的解耦层
    3. 支持持久化，防止程序中断丢失数据
    """
    def __init__(self, buffer_file: str = "knowledge_buffer.json"):
        self.buffer_path = Path(buffer_file)
        self._ensure_buffer_exists()

    def _ensure_buffer_exists(self):
        if not self.buffer_path.exists():
            self.save_data([])

    def load_data(self) -> List[Dict[str, Any]]:
        try:
            with open(self.buffer_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_data(self, data: List[Dict[str, Any]]):
        with open(self.buffer_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_candidates(self, candidates: List[Dict[str, Any]]):
        """Miner 往箱子里倒矿石"""
        current_data = self.load_data()
        # 简单的去重逻辑（基于名称）
        existing_names = {item.get("concept_name") for item in current_data}
        
        new_items = []
        for c in candidates:
            if c.get("concept_name") not in existing_names:
                new_items.append(c)
        
        if new_items:
            current_data.extend(new_items)
            self.save_data(current_data)
            print(f"📦 Buffer: 新入库 {len(new_items)} 个概念 (总计: {len(current_data)})")
        else:
            print("📦 Buffer: 无新概念入库 (全部重复)")

    def get_all_candidates(self) -> List[Dict[str, Any]]:
        """Critic 从箱子里拿矿石"""
        return self.load_data()

    def clear(self):
        """清空箱子"""
        self.save_data([])


