#!/bin/bash

# 道易智言 - 运行脚本

# 打印彩色文本
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}===== 道易智言 - 启动程序 =====${NC}"

# 检查是否有虚拟环境
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}创建虚拟环境...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}创建虚拟环境失败${NC}"
        exit 1
    fi
fi

# 激活虚拟环境
echo -e "${YELLOW}激活虚拟环境...${NC}"
source venv/bin/activate

# 安装依赖
echo -e "${YELLOW}安装依赖...${NC}"
pip install -r backend/requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}安装依赖失败${NC}"
    exit 1
fi

# 检查.env文件
if [ ! -f "backend/.env" ]; then
    echo -e "${RED}警告: 未找到 backend/.env 文件${NC}"
    echo -e "${YELLOW}请创建 backend/.env 文件并设置 OPENROUTER_API_KEY${NC}"
    echo -e "${YELLOW}示例: OPENROUTER_API_KEY=your_api_key_here${NC}"
    
    # 如果有.env.example，复制一份
    if [ -f "backend/.env.example" ]; then
        echo -e "${YELLOW}从.env.example创建.env...${NC}"
        cp backend/.env.example backend/.env
        echo -e "${YELLOW}请编辑 backend/.env 并设置正确的API密钥${NC}"
    fi
fi

# 在开发模式下启动服务器
echo -e "${GREEN}启动服务器...${NC}"
cd backend
echo -e "${YELLOW}服务器将自动选择可用端口 (5000, 5050, 8080, 8000, 3000)${NC}"
echo -e "${YELLOW}请查看日志获取实际运行地址${NC}"
echo -e "${YELLOW}按 Ctrl+C 停止服务器${NC}"
python server.py

# 打印退出信息
echo -e "${GREEN}服务器已停止${NC}" 