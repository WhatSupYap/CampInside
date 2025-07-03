# Ubuntu 22.04 LTS + Python 3.12 설정 가이드

## 🐧 Ubuntu 22.04 LTS 특화 설정

### Python 3.12 설치 및 설정

Ubuntu 22.04 LTS에서는 Python 3.12가 기본 저장소에 있습니다.

```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Python 3.12 및 관련 패키지 설치
sudo apt install -y python3.12 python3.12-venv python3.12-dev python3-pip

# Python 3.12를 기본 python3로 설정
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

# pip 업그레이드
python3 -m pip install --upgrade pip

# 버전 확인
python3 --version  # Python 3.12.x
pip --version
```

### 추가 개발 도구 설치

```bash
# 컴파일러 및 개발 도구
sudo apt install -y build-essential gcc g++ make

# PostgreSQL 클라이언트 라이브러리 (psycopg2 컴파일용)
sudo apt install -y libpq-dev

# SSL/TLS 라이브러리
sudo apt install -y libssl-dev libffi-dev

# 압축 라이브러리
sudo apt install -y zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev

# Git 최신 버전
sudo apt install -y git-all

# 모니터링 도구
sudo apt install -y htop iotop nethogs tree curl wget
```

### systemd 서비스 최적화 (Ubuntu 22.04용)

```bash
# systemd 서비스 파일 업데이트
sudo tee /etc/systemd/system/campinside.service > /dev/null <<EOF
[Unit]
Description=CampInside FastAPI Application
After=network-online.target
Wants=network-online.target

[Service]
Type=exec
User=ubuntu
Group=ubuntu
WorkingDirectory=/opt/campinside
ExecStart=/opt/campinside/venv/bin/gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --access-logfile /var/log/campinside/access.log --error-logfile /var/log/campinside/error.log
Environment="DB_HOST=your-postgres-endpoint"
Environment="DB_USER=postgres"
Environment="DB_PASSWORD=your-password"
Environment="DB_NAME=campinside"
Environment="DB_PORT=5432"
Environment="APP_ENV=production"
Environment="DEBUG=False"
Environment="PYTHONPATH=/opt/campinside"
Restart=always
RestartSec=3
StartLimitBurst=3
StartLimitInterval=60

# 보안 설정
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/campinside /var/log/campinside

[Install]
WantedBy=multi-user.target
EOF

# 로그 디렉토리 생성
sudo mkdir -p /var/log/campinside
sudo chown ubuntu:ubuntu /var/log/campinside

# 서비스 활성화
sudo systemctl daemon-reload
sudo systemctl enable campinside
```

### Nginx 최적화 설정 (Ubuntu 22.04용)

```bash
# Nginx 최신 버전 설치
sudo apt update
sudo apt install -y nginx

# 최적화된 설정
sudo tee /etc/nginx/sites-available/campinside > /dev/null <<EOF
server {
    listen 80;
    listen [::]:80;
    server_name _ default_server;

    # 보안 헤더
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    # 로그 설정
    access_log /var/log/nginx/campinside_access.log;
    error_log /var/log/nginx/campinside_error.log;

    # 메인 애플리케이션
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
        
        # 타임아웃 설정
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check (로그 제외)
    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        access_log off;
    }

    # 정적 파일 (나중에 사용)
    location /static/ {
        alias /opt/campinside/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # 파일 업로드 크기 제한
    client_max_body_size 10M;
}
EOF

# 설정 활성화
sudo ln -sf /etc/nginx/sites-available/campinside /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl restart nginx
```

### 방화벽 설정 (UFW)

```bash
# UFW 기본 설정
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 필요한 포트 허용
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS

# 방화벽 활성화
sudo ufw --force enable

# 상태 확인
sudo ufw status verbose
```

### 시스템 모니터링 설정

```bash
# 시스템 리소스 모니터링 도구 설치
sudo apt install -y htop iotop nethogs

# 로그 회전 설정
sudo tee /etc/logrotate.d/campinside > /dev/null <<EOF
/var/log/campinside/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 0644 ubuntu ubuntu
    postrotate
        systemctl reload campinside
    endscript
}
EOF
```

### 성능 최적화

```bash
# 스왑 파일 생성 (메모리 부족 방지)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 부팅 시 자동 마운트
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 스왑 설정 최적화
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf

# 설정 적용
sudo sysctl -p
```

### 자동 업데이트 설정

```bash
# 보안 업데이트 자동 설치
sudo apt install -y unattended-upgrades

# 설정 편집
sudo dpkg-reconfigure -plow unattended-upgrades

# 자동 업데이트 확인
sudo systemctl status unattended-upgrades
```

## 🔍 트러블슈팅

### Python 3.12 관련 문제

```bash
# 패키지 의존성 문제 해결
sudo apt install -y python3.12-distutils

# pip 재설치
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.12 get-pip.py

# 가상환경 재생성
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### systemd 서비스 디버깅

```bash
# 서비스 상태 확인
sudo systemctl status campinside -l --no-pager

# 로그 확인
sudo journalctl -u campinside -f

# 설정 파일 검증
sudo systemd-analyze verify /etc/systemd/system/campinside.service
```

이제 Ubuntu 22.04 LTS와 Python 3.12에 최적화된 환경이 준비되었습니다!
