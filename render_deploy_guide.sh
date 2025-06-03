#!/bin/bash
# 道易智言项目 - Render部署准备脚本

echo "===== 道易智言 - Render部署准备脚本 ====="
echo "此脚本将帮助您准备项目以便在Render上部署"

# 确保所有必要文件已添加到Git
echo "1. 确保所有必要文件已添加到Git..."
git add .
git commit -m "准备Render部署" || echo "没有新的更改需要提交"

# 推送到GitHub
echo "2. 推送最新代码到GitHub..."
git push -u origin main || { echo "推送失败，请检查GitHub连接"; exit 1; }

# 验证环境文件
if [ ! -f backend/.env.example ]; then
    echo "3. 创建环境变量示例文件..."
    cat > backend/.env.example << EOF
# 道易智言环境变量示例
# 复制此文件为.env并填写您的API密钥

# OpenRouter API密钥 (必需)
OPENROUTER_API_KEY=your_api_key_here

# 服务器设置
DEBUG=False
HOST=0.0.0.0
PORT=10000
EOF
    echo "已创建环境变量示例文件: backend/.env.example"
    git add backend/.env.example
    git commit -m "添加环境变量示例文件"
    git push
else
    echo "3. 环境变量示例文件已存在 ✓"
fi

# 验证requirements.txt
echo "4. 验证requirements.txt..."
if [ ! -f requirements.txt ]; then
    echo "ERROR: 根目录中缺少requirements.txt文件！"
    exit 1
fi

# 验证Procfile
echo "5. 验证Procfile..."
if [ ! -f Procfile ]; then
    echo "ERROR: 根目录中缺少Procfile文件！"
    exit 1
fi

# 打开Render部署页面
echo "===== 准备工作完成! ====="
echo "现在请在浏览器中打开Render部署页面..."
open https://dashboard.render.com/new/web-service

echo ""
echo "请在Render页面上按照以下步骤操作:"
echo "1. 选择'Build and deploy from a Git repository'"
echo "2. 连接您的GitHub账号并授权访问"
echo "3. 找到并选择'jajabong/daoyizhiyan'仓库"
echo "4. 配置以下选项:"
echo "   - 名称: daoyizhiyan"
echo "   - 区域: 选择适合您用户的区域"
echo "   - 分支: main"
echo "   - 运行时环境: Python 3"
echo "   - 构建命令: pip install -r requirements.txt"
echo "   - 启动命令: cd backend && gunicorn server:app"
echo "   - 实例类型: Free"
echo "5. 展开Advanced选项，添加以下环境变量:"
echo "   - OPENROUTER_API_KEY: 您的OpenRouter API密钥"
echo "   - DEBUG: False"
echo "   - PORT: 10000"
echo "6. 点击'Create Web Service'按钮开始部署"
echo ""
echo "部署完成后，Render将为您提供一个访问URL"
echo "===== 祝您部署成功! =====" 