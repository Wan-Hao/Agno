"""
景点数据处理器
"""
from pathlib import Path
from typing import Dict, Any, List
import json


class ScenicSpotProcessor:
    """
    景点数据处理器
    
    负责处理景点JSON数据，提取关键信息
    """
    
    def __init__(self):
        self.processor_type = "scenic_spots"
    
    def process(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        处理景点JSON文件
        
        Args:
            file_path: JSON文件路径
            
        Returns:
            景点数据列表
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 验证数据格式
            if not isinstance(data, list):
                raise ValueError("景点数据应为列表格式")
            
            processed_data = []
            for item in data:
                processed_item = self._process_spot(item)
                if processed_item:
                    processed_data.append(processed_item)
            
            return processed_data
        
        except Exception as e:
            raise Exception(f"处理景点数据失败: {str(e)}")
    
    def _process_spot(self, spot_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理单个景点数据
        
        Args:
            spot_data: 原始景点数据
            
        Returns:
            处理后的景点数据
        """
        # 提取基本信息
        processed = {
            "province_city": spot_data.get("province_city", ""),
            "scenic_spot": spot_data.get("scenic_spot", ""),
            "description": spot_data.get("description", ""),
            "processed": True
        }
        
        # 提取描述的统计信息
        description = processed["description"]
        processed["word_count"] = len(description)
        processed["sentence_count"] = description.count('。') + description.count('.')
        
        # 识别关键词类别
        processed["features"] = self._extract_features(description)
        
        return processed
    
    def _extract_features(self, description: str) -> Dict[str, bool]:
        """
        从描述中提取特征标签
        
        Args:
            description: 景点描述
            
        Returns:
            特征字典
        """
        features = {
            "has_architecture": False,  # 建筑
            "has_nature": False,        # 自然景观
            "has_water": False,         # 水体
            "has_mountain": False,      # 山地
            "has_history": False,       # 历史
            "has_modern": False,        # 现代
            "has_structure": False,     # 结构
            "has_geometry": False       # 几何
        }
        
        # 建筑相关
        architecture_keywords = ["建筑", "大楼", "塔", "楼阁", "亭台", "门", "桥", "廊", "寺", "庙"]
        if any(kw in description for kw in architecture_keywords):
            features["has_architecture"] = True
        
        # 自然景观
        nature_keywords = ["山", "水", "林", "森林", "植被", "竹", "树", "花", "草"]
        if any(kw in description for kw in nature_keywords):
            features["has_nature"] = True
        
        # 水体
        water_keywords = ["江", "河", "湖", "池", "水", "泉", "海"]
        if any(kw in description for kw in water_keywords):
            features["has_water"] = True
        
        # 山地
        mountain_keywords = ["山", "峰", "岭", "坡", "高"]
        if any(kw in description for kw in mountain_keywords):
            features["has_mountain"] = True
        
        # 历史
        history_keywords = ["历史", "古", "明代", "清代", "传统", "始建于"]
        if any(kw in description for kw in history_keywords):
            features["has_history"] = True
        
        # 现代
        modern_keywords = ["现代", "摩天", "高科技", "国际", "设计"]
        if any(kw in description for kw in modern_keywords):
            features["has_modern"] = True
        
        # 结构
        structure_keywords = ["结构", "支柱", "框架", "层", "高度", "材料"]
        if any(kw in description for kw in structure_keywords):
            features["has_structure"] = True
        
        # 几何
        geometry_keywords = ["对称", "比例", "形状", "圆", "方", "螺旋", "曲线"]
        if any(kw in description for kw in geometry_keywords):
            features["has_geometry"] = True
        
        return features
    
    def filter_by_features(
        self,
        spots: List[Dict[str, Any]],
        required_features: List[str]
    ) -> List[Dict[str, Any]]:
        """
        根据特征筛选景点
        
        Args:
            spots: 景点列表
            required_features: 需要的特征列表
            
        Returns:
            筛选后的景点列表
        """
        filtered = []
        for spot in spots:
            features = spot.get("features", {})
            if all(features.get(f"has_{feat}", False) for feat in required_features):
                filtered.append(spot)
        return filtered
    
    def get_summary(self, spots: List[Dict[str, Any]]) -> str:
        """
        获取景点数据摘要
        
        Args:
            spots: 景点列表
            
        Returns:
            摘要文本
        """
        if not spots:
            return "没有景点数据"
        
        summary = f"景点数据摘要：\n"
        summary += f"- 总数量: {len(spots)}\n"
        
        # 统计城市
        cities = set(spot.get("province_city", "") for spot in spots)
        summary += f"- 城市数: {len(cities)}\n"
        summary += f"- 城市列表: {', '.join(cities)}\n\n"
        
        # 统计特征
        feature_counts = {
            "建筑": 0,
            "自然": 0,
            "水体": 0,
            "山地": 0,
            "历史": 0,
            "现代": 0
        }
        
        for spot in spots:
            features = spot.get("features", {})
            if features.get("has_architecture"):
                feature_counts["建筑"] += 1
            if features.get("has_nature"):
                feature_counts["自然"] += 1
            if features.get("has_water"):
                feature_counts["水体"] += 1
            if features.get("has_mountain"):
                feature_counts["山地"] += 1
            if features.get("has_history"):
                feature_counts["历史"] += 1
            if features.get("has_modern"):
                feature_counts["现代"] += 1
        
        summary += "特征分布：\n"
        for feature, count in feature_counts.items():
            summary += f"- {feature}: {count} 个景点\n"
        
        return summary


if __name__ == "__main__":
    # 测试处理器
    processor = ScenicSpotProcessor()
    
    test_file = Path("dataset/senarios/shanghai.json")
    if test_file.exists():
        print("测试景点处理器...")
        spots = processor.process(test_file)
        print(f"✓ 处理了 {len(spots)} 个景点")
        print(f"\n{processor.get_summary(spots)}")
    else:
        print(f"测试文件不存在: {test_file}")


