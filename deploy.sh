#!/bin/bash

# 一键部署脚本
# 用法: ./deploy.sh [server_ip] [ssh_user]

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 默认参数
SERVER_IP=${1:-"your_server_ip"}
SSH_USER=${2:-"root"}
PROJECT_NAME="ChewyNotification"
REMOTE_DIR="/opt/chewy-notification"

echo -e "${GREEN}🚀 开始部署 Chewy Notification...${NC}"

# 1. 检查参数
if [ "$SERVER_IP" = "your_server_ip" ]; then
    echo -e "${RED}❌ 请提供服务器 IP 地址${NC}"
    echo "用法: ./deploy.sh <server_ip> [ssh_user]"
    exit 1
fi

echo -e "${YELLOW}📋 部署信息:${NC}"
echo "  服务器: $SERVER_IP"
echo "  用户: $SSH_USER"
echo "  远程目录: $REMOTE_DIR"
echo ""

# 2. 打包项目
echo -e "${GREEN}📦 打包项目文件...${NC}"
tar -czf /tmp/${PROJECT_NAME}.tar.gz \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='*.sqlite3' \
    --exclude='venv' \
    --exclude='.venv' \
    --exclude='node_modules' \
    --exclude='.DS_Store' \
    .

# 3. 上传到服务器
echo -e "${GREEN}📤 上传到服务器...${NC}"
scp /tmp/${PROJECT_NAME}.tar.gz ${SSH_USER}@${SERVER_IP}:/tmp/

# 4. 在服务器上执行部署
echo -e "${GREEN}🔧 远程部署...${NC}"
ssh ${SSH_USER}@${SERVER_IP} << 'ENDSSH'
set -e

# 创建目录
mkdir -p /opt/chewy-notification
cd /opt/chewy-notification

# 解压
echo "解压项目文件..."
tar -xzf /tmp/ChewyNotification.tar.gz -C /opt/chewy-notification
rm /tmp/ChewyNotification.tar.gz

# 创建数据和日志目录
mkdir -p data logs

# 停止旧容器
echo "停止旧容器..."
docker-compose down || true

# 构建并启动
echo "构建 Docker 镜像..."
docker-compose build

echo "启动容器..."
docker-compose up -d

# 等待服务启动
echo "等待服务启动..."
sleep 5

# 检查容器状态
docker-compose ps

echo "✅ 部署完成！"
ENDSSH

# 5. 清理本地临时文件
rm /tmp/${PROJECT_NAME}.tar.gz

# 6. 测试服务
echo -e "${GREEN}🧪 测试服务...${NC}"
sleep 2
curl -f http://${SERVER_IP}:8002/admin/ > /dev/null 2>&1 && \
    echo -e "${GREEN}✅ 服务运行正常！${NC}" || \
    echo -e "${RED}❌ 服务可能未正常启动，请检查日志${NC}"

echo ""
echo -e "${GREEN}🎉 部署完成！${NC}"
echo -e "${YELLOW}访问地址:${NC}"
echo "  API: http://${SERVER_IP}:8002/api/notifications/"
echo "  Admin: http://${SERVER_IP}:8002/admin/"
echo ""
echo -e "${YELLOW}查看日志:${NC}"
echo "  ssh ${SSH_USER}@${SERVER_IP} 'cd ${REMOTE_DIR} && docker-compose logs -f'"
echo ""
echo -e "${YELLOW}下一步:${NC}"
echo "  1. 配置 Nginx 反向代理（运行 ./setup-nginx.sh）"
echo "  2. 在 Admin 后台添加通知渠道和目标"
