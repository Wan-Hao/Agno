#!/bin/bash
# 安装脚本

echo "================================"
echo "科研聊天室 - 依赖安装脚本"
echo "================================"
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 升级 pip
echo "升级 pip..."
pip install --upgrade pip

# 安装依赖（分批安装，避免网络超时）
echo ""
echo "安装核心依赖..."
pip install python-dotenv pydantic

echo ""
echo "安装 Google Gemini API..."
pip install google-generativeai

echo ""
echo "安装文档处理库..."
pip install pypdf PyPDF2 Pillow

echo ""
echo "安装网络库..."
pip install requests beautifulsoup4 httpx

echo ""
echo "安装多媒体处理库..."
pip install moviepy pydub

echo ""
echo "安装其他依赖..."
pip install rich

echo ""
echo "================================"
echo "✓ 依赖安装完成！"
echo "================================"
echo ""
echo "下一步："
echo "1. 复制 .env.example 到 .env"
echo "2. 在 .env 中设置你的 GEMINI_API_KEY"
echo "3. 运行 ./run_example.sh 查看示例"
echo ""

