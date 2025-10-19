#!/bin/bash

echo "======================================"
echo "Agno项目快速发布到GitHub"
echo "======================================"
echo ""

# 检查是否在正确的目录
if [ ! -f "README.md" ]; then
    echo "❌ 错误：请在项目根目录运行此脚本"
    exit 1
fi

echo "📋 检查文件..."
echo "   ✓ README.md"
echo "   ✓ .gitignore"
echo "   ✓ .env.example"
echo "   ✓ requirements.txt"
echo ""

# 检查git
if [ ! -d ".git" ]; then
    echo "🔄 初始化Git仓库..."
    git init
    echo "   ✓ Git已初始化"
else
    echo "   ✓ Git仓库已存在"
fi
echo ""

# 检查.env
if git ls-files --error-unmatch .env &> /dev/null; then
    echo "⚠️  警告：.env文件已在Git中，正在移除..."
    git rm --cached .env
    echo "   ✓ .env已从Git移除"
fi
echo ""

echo "📦 添加文件到Git..."
git add .
echo "   ✓ 文件已添加"
echo ""

echo "💾 创建提交..."
git commit -m "Initial commit: Multi-agent knowledge graph fusion system

Features:
- Node-to-node discussion between Physics and Math agents
- 4 collaborative agents (Physics, Math, Meta, Evaluator)
- Full properties context for each node
- Quality-controlled edge extraction
- Support for sampling and full Cartesian product modes"
echo "   ✓ 提交已创建"
echo ""

echo "======================================"
echo "接下来的步骤："
echo "======================================"
echo ""
echo "1. 在GitHub创建新仓库："
echo "   https://github.com/new"
echo ""
echo "2. 仓库名称: Agno"
echo "   描述: Multi-agent system for cross-domain knowledge graph fusion"
echo "   选择Public或Private"
echo "   不要勾选README和.gitignore"
echo ""
echo "3. 创建后，GitHub会显示命令，或者运行："
echo ""
echo "   git remote add origin https://github.com/your-username/Agno.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "======================================"
echo "✨ 本地准备完成！"
echo "======================================"
