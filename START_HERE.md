# 🚀 从这里开始

欢迎使用**科研聊天室** - 基于多智能体系统（MAS）的跨学科知识关联发现系统！

## ⚡ 快速开始（3步）

### 1️⃣ 安装依赖

```bash
./install.sh
```

### 2️⃣ 配置 API Key

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 Gemini API Key
# 获取免费 API Key: https://aistudio.google.com/app/apikey
```

### 3️⃣ 运行示例

```bash
./run_example.sh
```

## 📚 文档导航

根据你的需求，选择对应的文档：

### 🆕 新手用户
1. **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** - 详细的安装步骤
2. **[QUICKSTART.md](QUICKSTART.md)** - 5分钟快速入门
3. **[examples/](examples/)** - 三个示例程序

### 👨‍💻 开发者
1. **[README.md](README.md)** - 项目概述和架构
2. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - 技术细节和扩展
3. **源代码注释** - 每个模块都有详细的文档字符串

### 🎓 研究者
1. **理论报告（聊天记录）** - 研究背景和动机
2. **[DELIVERY_REPORT.md](DELIVERY_REPORT.md)** - 完整的实现报告
3. **输出示例（运行后生成）** - 实际的知识图谱结果

## 💡 快速命令

### 运行基础示例
```bash
python examples/basic_example.py
```

### 自定义运行
```bash
python main.py \
  --topic "对称性与和谐" \
  --agents physics art biology \
  --rounds 3
```

### 查看可用智能体
```python
python -c "from agents import *; print('物理学家、文学家、数学家、生物学家、哲学家、艺术家')"
```

## 🎯 系统功能

✅ **6种领域专家智能体** - 物理、文学、数学、生物、哲学、艺术  
✅ **6种数据类型支持** - 文本、PDF、图片、音频、视频、网页  
✅ **自动关联发现** - AI驱动的跨学科知识挖掘  
✅ **智能评估系统** - 三维度质量评估  
✅ **结构化输出** - JSON知识图谱 + Markdown报告  

## 📁 项目结构

```
Agno/
├── 📖 START_HERE.md          ← 你在这里
├── 📖 README.md               ← 项目介绍
├── 📖 QUICKSTART.md           ← 快速入门
├── 📖 INSTALLATION_GUIDE.md   ← 安装指南
├── 🔧 install.sh              ← 安装脚本
├── ▶️  run_example.sh          ← 运行脚本
├── 🐍 main.py                 ← 主程序
├── 🧠 core/                   ← 核心模块
├── 🤖 agents/                 ← 智能体
├── 📊 processors/             ← 数据处理器
├── 📝 examples/               ← 示例代码
└── 📂 output/                 ← 输出目录（自动创建）
```

## 🔑 获取 API Key

1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 登录你的 Google 账号
3. 点击 "Create API Key"
4. 复制 API Key
5. 粘贴到 `.env` 文件中

**注意**: Gemini API 提供免费额度，足够日常使用！

## 🎬 使用示例

### Python 代码方式

```python
from core.chatroom import ResearchChatroom
from agents import PhysicsAgent, LiteratureAgent, MathAgent

# 创建聊天室
chatroom = ResearchChatroom(
    topic="时间的本质与流逝",
    agents=[
        PhysicsAgent(),
        LiteratureAgent(),
        MathAgent()
    ]
)

# 开始讨论
edges = chatroom.discuss(rounds=3)

# 导出结果
chatroom.export_knowledge_graph("output/my_graph.json")
print(chatroom.generate_report())
```

### 命令行方式

```bash
python main.py \
  --topic "时间的本质" \
  --agents physics literature math \
  --rounds 3 \
  --output-dir ./my_output
```

## 🆘 遇到问题？

### 常见问题速查

| 问题 | 解决方案 |
|------|---------|
| 找不到模块 | 运行 `./install.sh` |
| API Key 错误 | 检查 `.env` 文件 |
| 网络超时 | 使用国内镜像源安装 |
| 权限错误 | 运行 `chmod +x *.sh` |

### 详细帮助
查看 **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** 的"常见问题"章节

## 🌟 下一步

完成快速开始后，你可以：

1. 📖 阅读 [QUICKSTART.md](QUICKSTART.md) 了解更多用法
2. 🔧 尝试修改 `examples/` 中的示例代码
3. 🎨 创建自定义的智能体（继承 `Agent` 类）
4. 📊 加载你自己的数据（支持多种格式）
5. 🚀 开始你的跨学科研究！

## 📞 技术支持

- **文档**: 查看项目中的各个 `.md` 文件
- **示例**: 运行 `examples/` 目录下的示例代码
- **源码**: 每个模块都有详细的注释

## 🎉 准备好了吗？

```bash
# 让我们开始吧！
./install.sh
cp .env.example .env
# 编辑 .env 添加你的 API Key
./run_example.sh
```

祝你使用愉快！🚀

---

**需要更多帮助？** 查看 [QUICKSTART.md](QUICKSTART.md) 或 [README.md](README.md)

