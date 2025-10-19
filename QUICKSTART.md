# 快速入门指南

## 1. 安装依赖

```bash
# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

## 2. 配置 API Key

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 Gemini API Key
# GEMINI_API_KEY=你的API密钥
```

## 3. 运行示例

### 方式一：使用脚本运行（推荐）

```bash
chmod +x run_example.sh
./run_example.sh
```

### 方式二：直接运行 Python 文件

```bash
# 运行基础示例
python examples/basic_example.py

# 运行多模态示例
python examples/multimodal_example.py

# 运行大规模示例
python examples/six_agents_example.py
```

### 方式三：使用命令行参数

```bash
# 基本用法
python main.py --topic "时间的本质" --agents physics literature math --rounds 3

# 完整参数
python main.py \
  --topic "对称性与和谐" \
  --agents physics art biology \
  --rounds 3 \
  --output-dir ./my_output
```

## 4. 编程方式使用

### 基础用法

```python
from core.chatroom import ResearchChatroom
from agents import PhysicsAgent, LiteratureAgent, MathAgent

# 创建聊天室
chatroom = ResearchChatroom(
    topic="时间的本质",
    agents=[
        PhysicsAgent(),
        LiteratureAgent(),
        MathAgent()
    ]
)

# 开始讨论
edges = chatroom.discuss(rounds=3)

# 导出结果
chatroom.export_knowledge_graph("output/graph.json")
chatroom.export_discussion_log("output/log.json")

# 生成报告
report = chatroom.generate_report()
print(report)
```

### 加载多模态数据

```python
# 为不同智能体加载不同类型的数据
chatroom.load_data("物理学家", "papers/physics.pdf", "pdf")
chatroom.load_data("艺术评论家", "images/art.jpg", "image")
chatroom.load_data("生物学家", "https://example.com/article", "web")
```

## 5. 可用的智能体类型

- `physics` - 物理学家
- `literature` - 文学评论家
- `math` - 数学家
- `biology` - 生物学家
- `philosophy` - 哲学家
- `art` - 艺术评论家

## 6. 支持的数据类型

- **文本** (`.txt`, `.md`) - 纯文本文件
- **PDF** (`.pdf`) - PDF 文档
- **图片** (`.jpg`, `.png`, `.gif`, `.webp`) - 图像文件
- **音频** (`.mp3`, `.wav`, `.ogg`, `.flac`) - 音频文件
- **视频** (`.mp4`, `.avi`, `.mov`, `.mkv`) - 视频文件
- **网页** (`http://`, `https://`) - 在线网页

## 7. 输出文件

所有输出文件默认保存在 `./output/` 目录下：

- `knowledge_graph_*.json` - 知识图谱（JSON 格式）
- `discussion_log_*.json` - 完整讨论记录
- `report_*.md` - 综合分析报告（Markdown 格式）

## 8. 常见问题

### Q: 如何获取 Gemini API Key？

A: 访问 [Google AI Studio](https://aistudio.google.com/app/apikey) 获取免费的 API 密钥。

### Q: 可以添加自定义智能体吗？

A: 可以！继承 `core.agent.Agent` 类并实现 `analyze` 方法即可。

```python
from core.agent import Agent

class CustomAgent(Agent):
    def __init__(self):
        super().__init__(
            name="自定义专家",
            domain="自定义领域",
            expertise="专业描述"
        )
    
    def analyze(self, prompt: str) -> str:
        # 实现分析逻辑
        return self.client.generate(prompt, self.system_instruction)
```

### Q: 如何调整讨论参数？

A: 编辑 `config.py` 文件中的参数：

```python
# 对话配置
MAX_DISCUSSION_ROUNDS = 10
MIN_AGENTS = 2
MAX_AGENTS = 10

# 评估配置
SEMANTIC_SIMILARITY_THRESHOLD = 0.6
NOVELTY_THRESHOLD = 0.5
CONFIDENCE_THRESHOLD = 0.7
```

## 9. 下一步

- 查看 `examples/` 目录了解更多示例
- 阅读 `README.md` 了解系统架构
- 查看理论报告了解研究背景

## 10. 获取帮助

如果遇到问题，请：

1. 检查 `.env` 文件配置是否正确
2. 确认已安装所有依赖
3. 查看错误日志
4. 参考示例代码

祝你使用愉快！🚀

