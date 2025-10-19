#!/bin/bash
# 运行示例脚本

# 激活虚拟环境
source venv/bin/activate

echo "================================"
echo "科研聊天室 - 示例运行脚本"
echo "================================"
echo ""
echo "请选择要运行的示例："
echo "1. 基础示例（3个智能体）"
echo "2. 多模态示例"
echo "3. 大规模示例（6个智能体）"
echo "4. 知识图谱示例（使用dataset/数据）"
echo "5. 自定义运行"
echo ""

read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        echo "运行基础示例..."
        python examples/basic_example.py
        ;;
    2)
        echo "运行多模态示例..."
        python examples/multimodal_example.py
        ;;
    3)
        echo "运行大规模示例..."
        python examples/six_agents_example.py
        ;;
    4)
        echo "运行知识图谱示例..."
        python examples/knowledge_graph_example.py
        ;;
    5)
        echo "自定义运行..."
        read -p "讨论主题: " topic
        read -p "智能体 (用空格分隔，如: physics literature math): " agents
        read -p "讨论轮次: " rounds
        python main.py --topic "$topic" --agents $agents --rounds $rounds
        ;;
    *)
        echo "无效的选项"
        exit 1
        ;;
esac

echo ""
echo "完成！"

