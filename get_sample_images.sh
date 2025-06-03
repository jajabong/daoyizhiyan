#!/bin/bash

# 道易智言 - 样例图片下载脚本

# 打印彩色文本
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}===== 道易智言 - 下载样例背景图片 =====${NC}"

# 创建图片目录
IMAGES_DIR="frontend/assets/images"
mkdir -p "$IMAGES_DIR"

# 下载样例山水画背景
echo -e "${YELLOW}正在下载样例背景图片...${NC}"

# 使用curl下载图片
# 这里使用的是一个公共领域的中国山水画图片
curl -o "$IMAGES_DIR/landscape-bg.jpg" -L "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Huang_Gongwang._Dwelling_in_the_Fuchun_Mountains._1350._National_Palace_Museum%2C_Taipei.jpg/1280px-Huang_Gongwang._Dwelling_in_the_Fuchun_Mountains._1350._National_Palace_Museum%2C_Taipei.jpg"

# 检查下载是否成功
if [ $? -eq 0 ]; then
    echo -e "${GREEN}背景图片下载成功！${NC}"
    echo -e "${YELLOW}图片保存在: ${IMAGES_DIR}/landscape-bg.jpg${NC}"
    echo -e "${YELLOW}这是一幅公共领域的中国古代山水画《富春山居图》的局部，由黄公望创作于约1350年。${NC}"
else
    echo -e "${RED}图片下载失败。${NC}"
    echo -e "${YELLOW}请手动添加一个名为landscape-bg.jpg的图片到${IMAGES_DIR}目录。${NC}"
fi

echo -e "${GREEN}完成${NC}" 