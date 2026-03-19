"""
景点智能体
"""
from core.agent import Agent
from typing import Optional, List, Dict, Any
from core.openai_client import OpenAIClient
import json


class ScenicSpotAgent(Agent):
    """
    景点智能体
    
    负责：
    1. 从JSON中提取景点描述
    2. 分析景点的特征和知识点
    3. 引导物理和数学专家发现景点与学科的关联
    """
    
    def __init__(
        self,
        name: str = "景点导览专家",
        api_client: Optional[OpenAIClient] = None
    ):
        super().__init__(
            name=name,
            domain="旅游景点与文化",
            expertise=(
                "景点历史文化、建筑特色、自然景观、"
                "人文价值、游客体验、空间设计"
            ),
            api_client=api_client
        )
        
        # 存储景点数据
        self.scenic_spots: List[Dict[str, Any]] = []
        self.current_spot: Optional[Dict[str, Any]] = None
    
    def _default_system_instruction(self) -> str:
        return (
            f"你是一位资深的景点导览专家，名字是{self.name}。"
            f"你精通{self.expertise}。"
            f"你正在参与一个特殊的跨学科对话，目标是将旅游景点与学科知识（物理学、数学等）建立联系。\n\n"
            f"**你的职责**：\n"
            f"1. 深入分析景点的各个方面（建筑、自然、历史、空间、视觉等）\n"
            f"2. 识别景点中可能蕴含的科学原理或数学结构\n"
            f"3. 向物理学家和数学家提出引导性问题\n"
            f"4. 帮助专家们发现景点特征与学科知识的关联\n\n"
            f"**分析视角**：\n"
            f"- 建筑结构：对称性、稳定性、材料力学、几何形态\n"
            f"- 自然景观：地质地貌、水文特征、光影变化、生态系统\n"
            f"- 空间布局：比例关系、黄金分割、路径设计、视觉透视\n"
            f"- 历史演变：时间序列、发展规律、因果关系\n"
            f"- 视觉体验：光学现象、色彩理论、对比效果\n\n"
            f"请用生动、具体的语言描述景点，并巧妙地引导专家们从科学角度思考。"
        )
    
    def load_scenic_spots_from_json(self, json_path: str) -> bool:
        """
        从JSON文件加载景点数据
        
        Args:
            json_path: JSON文件路径
            
        Returns:
            是否加载成功
        """
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                self.scenic_spots = json.load(f)
            
            # 加载到知识库
            self.load_knowledge(
                data=self.scenic_spots,
                data_type="scenic_spots",
                source=json_path
            )
            
            print(f"✓ 已为 {self.name} 加载 {len(self.scenic_spots)} 个景点")
            return True
        
        except Exception as e:
            print(f"✗ 加载景点数据失败: {e}")
            return False
    
    def set_current_spot(self, spot_name: str) -> bool:
        """
        设置当前讨论的景点
        
        Args:
            spot_name: 景点名称
            
        Returns:
            是否设置成功
        """
        for spot in self.scenic_spots:
            if spot.get("scenic_spot") == spot_name:
                self.current_spot = spot
                print(f"✓ 当前景点: {spot_name}")
                return True
        
        print(f"✗ 未找到景点: {spot_name}")
        return False
    
    def get_spot_by_index(self, index: int) -> Optional[Dict[str, Any]]:
        """
        按索引获取景点
        
        Args:
            index: 景点索引（从0开始）
            
        Returns:
            景点数据
        """
        if 0 <= index < len(self.scenic_spots):
            self.current_spot = self.scenic_spots[index]
            return self.current_spot
        return None
    
    def list_all_spots(self) -> List[str]:
        """获取所有景点名称列表"""
        return [spot.get("scenic_spot", "") for spot in self.scenic_spots]
    
    def analyze(self, prompt: str) -> str:
        """从景点角度分析"""
        full_prompt = (
            f"作为景点导览专家，请分析以下内容：\n\n"
            f"{prompt}\n\n"
            f"请从景点特征、空间设计、自然现象等角度提供见解。"
        )
        return self.client.generate(full_prompt, self.system_instruction)
    
    def introduce_spot(
        self,
        spot: Optional[Dict[str, Any]] = None,
        focus_aspects: Optional[List[str]] = None
    ) -> str:
        """
        介绍景点（面向物理和数学专家）
        
        Args:
            spot: 景点数据（如果为None则使用current_spot）
            focus_aspects: 重点关注的方面列表
            
        Returns:
            景点介绍文本
        """
        if spot is None:
            spot = self.current_spot
        
        if not spot:
            return "当前没有选定的景点。"
        
        spot_name = spot.get("scenic_spot", "未知景点")
        city = spot.get("province_city", "")
        description = spot.get("description", "")
        
        prompt = f"""
请对以下景点进行专业介绍，特别要引导物理学家和数学家思考其中蕴含的科学原理：

**景点名称**：{spot_name}
**所在地**：{city}
**描述**：
{description}

请完成以下任务：

1. **景点特征提取**：总结该景点的核心特征（建筑、自然、空间、材料等）

2. **潜在科学点识别**：指出可能涉及的科学领域，例如：
   - 结构力学（建筑支撑、跨度、材料）
   - 几何学（形状、对称性、比例）
   - 光学（反射、折射、视觉效果）
   - 流体力学（水流、风力）
   - 热力学（温度、能量）
   - 其他相关领域

3. **引导性问题**：向物理学家和数学家各提出2-3个问题，引导他们思考景点与学科的关联

请用生动且专业的语言，让专家们对景点产生兴趣并启发他们的思考。
"""
        
        if focus_aspects:
            prompt += f"\n\n特别关注以下方面：{', '.join(focus_aspects)}"
        
        return self.client.generate(prompt, self.system_instruction)
    
    def extract_knowledge_points(self, spot: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        提取景点中的潜在知识点
        
        Args:
            spot: 景点数据
            
        Returns:
            知识点列表
        """
        if spot is None:
            spot = self.current_spot
        
        if not spot:
            return []
        
        description = spot.get("description", "")
        
        prompt = f"""
分析以下景点描述，提取其中可能与物理学或数学相关的知识点：

{description}

请列出所有潜在的知识点（每行一个），格式为：
- 知识点名称：简短说明

例如：
- 建筑力学：建筑的支撑结构和稳定性
- 几何对称：建筑外观的对称性设计
"""
        
        response = self.client.generate(prompt, self.system_instruction)
        
        # 简单解析（实际应用中可以更复杂）
        knowledge_points = []
        for line in response.split('\n'):
            line = line.strip()
            if line.startswith('-') or line.startswith('•'):
                knowledge_points.append(line.lstrip('-•').strip())
        
        return knowledge_points
    
    def facilitate_discussion(
        self,
        physics_response: str,
        math_response: str
    ) -> str:
        """
        促进讨论（在物理和数学专家发言后）
        
        Args:
            physics_response: 物理专家的发言
            math_response: 数学专家的发言
            
        Returns:
            促进性评论和新的引导
        """
        if not self.current_spot:
            return "当前没有讨论的景点。"
        
        spot_name = self.current_spot.get("scenic_spot", "")
        
        prompt = f"""
你刚刚介绍了景点「{spot_name}」，现在两位专家已经发表了观点：

**物理学家的观点**：
{physics_response}

**数学家的观点**：
{math_response}

作为景点专家，请：
1. 总结两位专家提出的关联点
2. 指出他们的观点如何与景点实际特征相呼应
3. 补充他们可能忽略的景点细节
4. 提出新的引导性问题，促进更深入的讨论

请简洁但富有洞察力地回应（不超过300字）。
"""
        
        return self.client.generate(prompt, self.system_instruction)


if __name__ == "__main__":
    # 测试景点智能体
    agent = ScenicSpotAgent()
    print(f"✓ {agent.name} initialized")
    print(f"  Domain: {agent.domain}")
    print(f"  Expertise: {agent.expertise}")
    
    # 测试加载景点数据
    test_json_path = "dataset/senarios/shanghai.json"
    if agent.load_scenic_spots_from_json(test_json_path):
        print(f"\n景点列表:")
        for i, spot in enumerate(agent.list_all_spots()):
            print(f"  {i+1}. {spot}")


