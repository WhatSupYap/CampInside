#!/bin/bash

# AWS Lightsail Ubuntu 서버 초기 설정 스크립트
# 이 스크립트를 서버에서 한 번 실행하여 초기 환경을 구성합니다.

set -e

# 색상 출력을 위한 변수
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== CampInside 서버 초기 설정 시작 ===${NC}"

# 사용자 입력 받기
echo -e "${YELLOW}GitHub 저장소 URL을 입력하세요 (예: https://github.com/username/campinside.git):${NC}"
read -p "Repository URL: " REPO_URL

echo -e "${YELLOW}PostgreSQL 연결 정보를 입력하세요:${NC}"
read -p "DB Host (Lightsail endpoint): " DB_HOST
read -p "DB User (보통 postgres): " DB_USER
read -s -p "DB Password: " DB_PASSWORD
echo
read -p "DB Name (보통 campinside): " DB_NAME

# 1. 시스템 업데이트
echo -e "${GREEN}1. 시스템 업데이트 중...${NC}"
sudo apt update && sudo apt upgrade -y

# 2. 필수 패키지 설치
echo -e "${GREEN}2. 필수 패키지 설치 중...${NC}"
sudo apt install -y software-properties-common
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev python3-pip nginx git curl htop tree build-essential

# Python 3.12를 기본 python3로 설정
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
sudo update-alternatives --set python3 /usr/bin/python3.12

# pip 업그레이드
python3 -m pip install --upgrade pip

# 3. 애플리케이션 디렉토리 생성
echo -e "${GREEN}3. 애플리케이션 디렉토리 설정 중...${NC}"
sudo mkdir -p /opt/campinside
sudo chown ubuntu:ubuntu /opt/campinside

# 4. Git 저장소 클론
echo -e "${GREEN}4. Git 저장소 클론 중...${NC}"
cd /opt
if [ -d "/opt/campinside/.git" ]; then
    echo "기존 저장소 업데이트 중..."
    cd /opt/campinside
    git pull origin main
else
    sudo rm -rf /opt/campinside
    sudo git clone "$REPO_URL" campinside
    sudo chown -R ubuntu:ubuntu /opt/campinside
fi

# 5. Python 가상환경 설정
echo -e "${GREEN}5. Python 가상환경 설정 중...${NC}"
cd /opt/campinside
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 6. 환경 변수 파일 생성
echo -e "${GREEN}6. 환경 변수 파일 생성 중...${NC}"
cat > .env << EOF
DB_HOST=$DB_HOST
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_NAME=$DB_NAME
DB_PORT=5432
APP_ENV=production
DEBUG=False
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
EOF

echo -e "${YELLOW}환경 변수 파일이 생성되었습니다.${NC}"

# 7. Systemd 서비스 설정
echo -e "${GREEN}7. Systemd 서비스 설정 중...${NC}"
# 환경 변수를 포함한 서비스 파일 생성
cat > /tmp/campinside.service << EOF
[Unit]
Description=CampInside FastAPI Application
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/opt/campinside
ExecStart=/opt/campinside/venv/bin/gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Environment="DB_HOST=$DB_HOST"
Environment="DB_USER=$DB_USER"
Environment="DB_PASSWORD=$DB_PASSWORD"
Environment="DB_NAME=$DB_NAME"
Environment="DB_PORT=5432"
Environment="APP_ENV=production"
Environment="DEBUG=False"
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

sudo mv /tmp/campinside.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable campinside

# 8. Nginx 설정
echo -e "${GREEN}8. Nginx 설정 중...${NC}"
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)
cat > /tmp/campinside_nginx << EOF
server {
    listen 80;
    server_name $PUBLIC_IP _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
    }

    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        access_log off;
    }
}
EOF

sudo mv /tmp/campinside_nginx /etc/nginx/sites-available/campinside
sudo ln -sf /etc/nginx/sites-available/campinside /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl enable nginx

# 9. 방화벽 설정
echo -e "${GREEN}9. 방화벽 설정 중...${NC}"
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

# 10. 서비스 시작
echo -e "${GREEN}10. 서비스 시작 중...${NC}"
sudo systemctl start campinside
sudo systemctl start nginx

# 11. 상태 확인
echo -e "${GREEN}11. 서비스 상태 확인...${NC}"
sleep 3
sudo systemctl status campinside --no-pager
sudo systemctl status nginx --no-pager

# 12. 연결 테스트
echo -e "${GREEN}12. 연결 테스트 중...${NC}"
sleep 2
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Health check 성공!${NC}"
else
    echo -e "${RED}❌ Health check 실패. 로그를 확인하세요.${NC}"
    echo "로그 확인: sudo journalctl -u campinside -f"
fi

echo -e "${GREEN}=== 설정 완료 ===${NC}"
echo -e "${YELLOW}애플리케이션 URL: http://$PUBLIC_IP${NC}"
echo -e "${YELLOW}Health Check: http://$PUBLIC_IP/health${NC}"
echo -e "${YELLOW}API 문서: http://$PUBLIC_IP/docs${NC}"
echo ""
echo -e "${YELLOW}유용한 명령어:${NC}"
echo "로그 확인: sudo journalctl -u campinside -f"
echo "서비스 재시작: sudo systemctl restart campinside"
echo "Nginx 재시작: sudo systemctl restart nginx"
echo "상태 확인: sudo systemctl status campinside"
