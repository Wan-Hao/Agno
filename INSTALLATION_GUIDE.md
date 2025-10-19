# 安装指南

## 方式一：使用自动安装脚本（推荐）

```bash
# 赋予执行权限
chmod +x install.sh

# 运行安装脚本
./install.sh
```

## 方式二：手动安装

### 1. 创建虚拟环境（如果还没有）

```bash
python3 -m venv venv
```

### 2. 激活虚拟环境

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3. 升级 pip

```bash
pip install --upgrade pip
```

### 4. 安装依赖

#### 核心依赖
```bash
pip install python-dotenv pydantic
```

#### Google Gemini API
```bash
pip install google-generativeai
```

#### 文档处理
```bash
pip install pypdf PyPDF2 Pillow
```

#### 网络和HTTP
```bash
pip install requests beautifulsoup4 httpx
```

#### 多媒体处理（可选）
```bash
pip install moviepy pydub
```

#### 其他工具
```bash
pip install rich
```

### 5. 或者一次性安装所有依赖

```bash
pip install -r requirements.txt
```

如果遇到网络超时，可以使用国内镜像源：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 配置 API Key

### 1. 获取 Gemini API Key

访问 [Google AI Studio](https://aistudio.google.com/app/apikey) 获取免费的 API 密钥。

### 2. 创建环境变量文件

```bash
cp .env.example .env
```

### 3. 编辑 .env 文件

```bash
# 使用任何文本编辑器打开 .env
nano .env
# 或
vim .env
# 或
code .env
```

填入你的 API Key：

```bash
GEMINI_API_KEY=你的API密钥

# 可选配置
GEMINI_MODEL=gemini-2.0-flash-exp
TEMPERATURE=0.7
MAX_TOKENS=8192
```

## 验证安装

运行测试脚本验证安装是否成功：

```bash
# 激活虚拟环境
source venv/bin/activate

# 测试配置
python config.py

# 测试核心模块导入
python -c "from core import Agent, KnowledgeEdge; print('✓ Core modules OK')"
python -c "from agents import PhysicsAgent; print('✓ Agents OK')"
python -c "from processors import TextProcessor; print('✓ Processors OK')"
```

## 常见问题

### Q1: ModuleNotFoundError: No module named 'xxx'

**解决方案**：确保已激活虚拟环境，然后重新安装依赖：
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Q2: GEMINI_API_KEY not found

**解决方案**：
1. 确保已创建 `.env` 文件
2. 确保在 `.env` 中正确设置了 `GEMINI_API_KEY`
3. 检查 `.env` 文件是否在项目根目录

### Q3: 网络连接超时

**解决方案**：使用国内镜像源
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

或阿里云镜像：
```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### Q4: moviepy 或 pydub 安装失败

**解决方案**：这些是可选依赖（用于音视频处理）。如果不需要音视频功能，可以跳过：

```bash
# 只安装核心依赖
pip install google-generativeai python-dotenv pydantic
pip install pypdf Pillow requests beautifulsoup4 httpx rich
```

### Q5: 权限错误

**解决方案**：
```bash
# 给脚本添加执行权限
chmod +x install.sh
chmod +x run_example.sh

# 或使用 bash 直接运行
bash install.sh
bash run_example.sh
```

## Python 版本要求

- **推荐**: Python 3.10 或更高版本
- **最低**: Python 3.8

检查你的 Python 版本：

```bash
python3 --version
```

如果版本过低，请升级 Python。

## 下一步

安装完成后，查看：
- [快速入门指南](QUICKSTART.md)
- [项目摘要](PROJECT_SUMMARY.md)
- [README](README.md)

## 获取帮助

如果遇到问题：
1. 检查错误日志
2. 确保所有依赖都已正确安装
3. 验证 API Key 配置
4. 查看示例代码

祝你使用愉快！🚀

