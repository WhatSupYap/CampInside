# AWS Lightsail SSH 연결 가이드

## Windows에서 SSH 연결

### 1. SSH 키 파일 준비
다운로드받은 `.pem` 파일을 적절한 위치에 저장하세요.
예: `C:\Users\YourName\.ssh\campinside-key.pem`

### 2. PowerShell에서 연결

#### 키 파일 권한 설정 (Windows)
```powershell
# PowerShell을 관리자 권한으로 실행
icacls "C:\Users\YourName\.ssh\campinside-key.pem" /inheritance:r
icacls "C:\Users\YourName\.ssh\campinside-key.pem" /grant:r "$($env:USERNAME):R"
```

#### SSH 연결
```powershell
# PowerShell에서 연결
ssh -i "C:\Users\YourName\.ssh\campinside-key.pem" ubuntu@YOUR_LIGHTSAIL_IP

# 예시
ssh -i "C:\Users\YourName\.ssh\campinside-key.pem" ubuntu@3.34.123.45
```

### 3. WSL(Ubuntu)에서 연결

#### 키 파일 복사 및 권한 설정
```bash
# WSL에서 키 파일 복사
cp /mnt/c/Users/YourName/.ssh/campinside-key.pem ~/.ssh/
chmod 400 ~/.ssh/campinside-key.pem

# SSH 연결
ssh -i ~/.ssh/campinside-key.pem ubuntu@YOUR_LIGHTSAIL_IP
```

### 4. VS Code SSH 확장 사용

1. **Remote - SSH** 확장 설치
2. `Ctrl+Shift+P` → "Remote-SSH: Connect to Host" 선택
3. SSH 설정 추가:
```
Host campinside
    HostName YOUR_LIGHTSAIL_IP
    User ubuntu
    IdentityFile C:\Users\YourName\.ssh\campinside-key.pem
```

## 첫 연결 후 할 일

### 1. 서버 기본 설정
```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Python 3.12 설치 (Ubuntu 22.04 기본 패키지)
sudo apt install -y python3.12 python3.12-venv python3.12-dev python3-pip

# Python 3.12를 기본 python3로 설정
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

# 타임존 설정
sudo timedatectl set-timezone Asia/Seoul

# 한국어 로케일 설정 (선택사항)
sudo locale-gen ko_KR.UTF-8
```

### 2. Git 설정
```bash
# Git 사용자 정보 설정
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# GitHub SSH 키 생성 (선택사항)
ssh-keygen -t ed25519 -C "your.email@example.com"
cat ~/.ssh/id_ed25519.pub  # 이 내용을 GitHub에 등록
```

### 3. 프로젝트 설정 스크립트 실행

#### 방법 1: GitHub에서 프로젝트를 올린 경우
```bash
# GitHub 프로젝트 클론 (본인의 GitHub username으로 변경)
git clone https://github.com/YOUR_USERNAME/campinside.git
cd campinside

# 설정 스크립트 실행
chmod +x deploy/setup.sh
./deploy/setup.sh
```

#### 방법 2: 로컬에서 파일 업로드
```bash
# SCP로 프로젝트 파일 업로드 (로컬 PowerShell에서 실행)
scp -i "키파일.pem" -r ./campinside ubuntu@서버IP:~/

# 서버에서 스크립트 실행
cd ~/campinside
chmod +x deploy/setup.sh
./deploy/setup.sh
```

#### 방법 3: 직접 설정 (스크립트 없이)
```bash
# Docker 설치
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
sudo systemctl enable docker
sudo systemctl start docker

# PostgreSQL 설정 등 필요한 설정들을 수동으로 진행
```

## 트러블슈팅

### SSH 연결 거부 오류
```bash
# 연결이 거부되는 경우, Lightsail 방화벽 확인
# AWS Lightsail 콘솔 → 인스턴스 → 네트워킹 탭에서 SSH(22) 포트 확인
```

### 권한 오류
```bash
# .pem 파일 권한이 너무 개방적인 경우
chmod 400 your-key.pem
```

### 타임아웃 오류
```bash
# 인스턴스가 실행 중인지 확인
# Lightsail 콘솔에서 인스턴스 상태 확인
```
