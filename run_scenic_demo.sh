#!/bin/bash

# 景点教育知识点提取演示脚本

echo "========================================"
echo "  景点教育知识点关联系统"
echo "========================================"
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "✗ 虚拟环境不存在，请先运行 install.sh"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

# 检查API密钥
if [ ! -f ".env" ]; then
    echo "✗ .env 文件不存在"
    echo "请创建 .env 文件并配置 API 密钥"
    exit 1
fi

echo "请选择运行模式:"
echo "  1) 快速演示 (单个景点)"
echo "  2) 完整示例 (多个景点)"
echo ""
read -p "请输入选择 (1 或 2): " choice

case $choice in
    1)
        echo ""
        echo "运行快速演示..."
        python examples/quick_scenic_demo.py
        ;;
    2)
        echo ""
        echo "运行完整示例..."
        python examples/scenic_educational_example.py
        ;;
    *)
        echo "✗ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "✓ 完成！查看 output/ 目录获取结果"


