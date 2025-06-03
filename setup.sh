#!/bin/bash

# 道易智言 - 安装配置脚本

# 打印彩色文本
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== 道易智言 - 安装配置 =====${NC}"

# 检查python是否安装
echo -e "${YELLOW}检查Python版本...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}未找到Python3。请安装Python 3.8或更高版本后再运行此脚本。${NC}"
    exit 1
fi

python_version=$(python3 --version | cut -d" " -f2)
echo -e "${GREEN}检测到Python版本: ${python_version}${NC}"

# 创建项目目录结构
echo -e "${YELLOW}创建项目目录结构...${NC}"
mkdir -p frontend/css frontend/js frontend/assets/images
mkdir -p backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}创建Python虚拟环境...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}创建虚拟环境失败。请检查Python版本和venv模块安装状态。${NC}"
        exit 1
    fi
    echo -e "${GREEN}虚拟环境创建成功${NC}"
else
    echo -e "${GREEN}虚拟环境已存在${NC}"
fi

# 激活虚拟环境
echo -e "${YELLOW}激活虚拟环境...${NC}"
source venv/bin/activate

# 安装依赖
echo -e "${YELLOW}安装Python依赖...${NC}"
pip install -r backend/requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}安装依赖失败${NC}"
    exit 1
fi
echo -e "${GREEN}依赖安装完成${NC}"

# 创建和配置.env文件
echo -e "${YELLOW}配置环境变量...${NC}"
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}创建.env文件...${NC}"
    cat > backend/.env << EOF
# 道易智言环境配置

# OpenRouter API配置
OPENROUTER_API_KEY=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

# 应用设置
DEBUG=True
HOST=0.0.0.0
PORT=5000
EOF
    echo -e "${GREEN}.env文件创建成功${NC}"
else
    echo -e "${GREEN}.env文件已存在${NC}"
fi

# 创建.env.example文件作为示例
if [ ! -f "backend/.env.example" ]; then
    echo -e "${YELLOW}创建.env.example示例文件...${NC}"
    cat > backend/.env.example << EOF
# 道易智言环境配置

# OpenRouter API配置
OPENROUTER_API_KEY=your_openrouter_api_key_here

# 应用设置
DEBUG=True
HOST=0.0.0.0
PORT=5000
EOF
    echo -e "${GREEN}.env.example文件创建成功${NC}"
fi

# 确保运行脚本有执行权限
echo -e "${YELLOW}设置脚本执行权限...${NC}"
chmod +x run.sh
echo -e "${GREEN}脚本权限设置完成${NC}"

echo -e "${BLUE}===== 安装配置完成 =====${NC}"
echo -e "${GREEN}现在可以运行 ./run.sh 启动应用${NC}"
echo -e "${YELLOW}默认服务器地址: http://localhost:5000${NC}" 