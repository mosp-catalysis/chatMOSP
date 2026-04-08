#!/bin/bash

# MOSP OpenClaw Skills 安装脚本
# 版本: 1.0.0

echo "========================================"
echo "MOSP OpenClaw Skills 安装程序"
echo "========================================"

# 检查OpenClaw workspace目录
WORKSPACE_DIR="$HOME/.openclaw/workspace"
SKILLS_DIR="$WORKSPACE_DIR/skills"

if [ ! -d "$WORKSPACE_DIR" ]; then
    echo "❌ 错误: OpenClaw workspace目录不存在: $WORKSPACE_DIR"
    echo "请先安装OpenClaw并确保其正常运行"
    exit 1
fi

# 创建skills目录（如果不存在）
mkdir -p "$SKILLS_DIR"

# 复制技能文件
echo "📁 正在复制技能文件..."
cp -r skills/* "$SKILLS_DIR/"

# 检查复制结果
echo "🔍 检查安装结果..."
COUNT=$(find "$SKILLS_DIR" -name "*mosp*" -type d | wc -l)

if [ "$COUNT" -ge 5 ]; then
    echo "✅ 安装成功！共安装了 $COUNT 个MOSP技能"
    echo ""
    echo "已安装的技能:"
    echo "1. mosp-speech2text-1.0.0 - 语音识别"
    echo "2. mosp-inputhandler-1.0.0 - 命令处理"
    echo "3. mosp-inputfilemanager-1.0.0 - 文件管理"
    echo "4. mosp-msr-1.0.0 - 团簇结构生成"
    echo "5. mosp-kmc-1.0.0 - 动力学模拟"
    echo ""
    echo "📖 使用方法:"
    echo "1. 重启OpenClaw或等待技能自动加载"
    echo "2. 使用语音或文本命令控制计算流程"
    echo "3. 详细文档请查看 examples/ 目录"
    echo ""
    echo "💡 提示: 可以运行 'openclaw skills list' 查看已安装技能"
else
    echo "⚠️  警告: 可能未完全安装所有技能"
    echo "请手动检查 $SKILLS_DIR 目录"
fi

echo "========================================"