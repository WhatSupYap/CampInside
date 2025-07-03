# 🚀 AWS Lightsail CampInside 2025 최신 배포 가이드

**Ubuntu 22.04 LTS + Python 3.12 + PostgreSQL 15**

이 가이드는 2025년 최신 환경에서 AWS Lightsail에 FastAPI 애플리케이션을 배포하는 방법을 설명합니다.

## 🆕 2025년 업데이트 사항

- ✅ **Ubuntu 22.04 LTS** (Lightsail 최신 지원 버전)
- ✅ **Python 3.12** (최신 안정 버전)
- ✅ **PostgreSQL 15** (AWS Lightsail 최신 지원)
- ✅ **개선된 보안 설정**
- ✅ **성능 최적화**

## 📋 사전 준비사항

- [ ] AWS 계정
- [ ] GitHub 계정  
- [ ] Windows PC (PowerShell 사용)
- [ ] 신용카드 (AWS 결제용)

## 🎯 1단계: AWS Lightsail 인스턴스 생성

### 1.1 AWS 콘솔 접속
1. [AWS Lightsail 콘솔](https://lightsail.aws.amazon.com/) 접속
2. **Create instance** 클릭

### 1.2 인스턴스 설정 (2025년 권장사양)
```
✅ Instance location: Asia Pacific (Seoul) 
✅ Platform: Linux/Unix
✅ OS: Ubuntu 22.04 LTS ⭐ 최신 버전
✅ Instance plan: $12/month (2GB RAM, 1vCPU, 60GB SSD) ⭐ 2025년 권장
✅ Instance name: campinside-server-2025
✅ Key pair: Create new → campinside-key-2025 → Download .pem file
```

### 1.3 고정 IP 할당
1. 인스턴스 생성 완료 후
2. **Networking** 탭 → **Create static IP**
3. IP 주소 기록: `예: 3.34.123.45`

## 🗄️ 2단계: PostgreSQL 데이터베이스 생성

### 2.1 데이터베이스 생성
1. Lightsail 홈 → **Databases** 탭
2. **Create database** 클릭

### 2.2 데이터베이스 설정 (2025년 권장사양)
```
✅ Database engine: PostgreSQL 17 ⭐ 최신 버전 (17.5 사용 가능)
✅ Database plan: $18/month (1GB RAM, 32GB SSD) ⭐ 2025년 요금
✅ Database name: campinside-db-2025
✅ Master username: postgres
✅ Master password: [강력한 비밀번호 생성 및 기록]
```

### 2.3 연결 정보 기록
```
DB_HOST: [데이터베이스 엔드포인트]
DB_USER: postgres  
DB_PASSWORD: [설정한 비밀번호]
DB_NAME: postgres (기본값)
DB_PORT: 5432
```

## 💻 3단계: GitHub 저장소 설정

### 3.1 GitHub 저장소 생성
1. GitHub → **New repository**
2. Repository name: `campinside`
3. **Public** 선택
4. **Create repository**

### 3.2 로컬 코드 푸시
```powershell
# PowerShell에서 프로젝트 디렉토리로 이동
cd "C:\OneDrive\Beomsup_kim@outlook.kr\OneDrive\Study-Dev\campinside"

# Git 초기화 및 푸시
git init
git add .
git commit -m "Initial commit: Ubuntu 22.04 + Python 3.12 setup"
git remote add origin https://github.com/YOUR_USERNAME/campinside.git
git branch -M main
git push -u origin main
```

### 3.3 GitHub Secrets 설정
GitHub 저장소 → **Settings** → **Secrets and variables** → **Actions**

**New repository secret** 클릭하여 다음 3개 추가:

```
Name: LIGHTSAIL_HOST
Secret: 3.34.123.45  # 실제 고정 IP

Name: LIGHTSAIL_USER
Secret: ubuntu

Name: LIGHTSAIL_SSH_KEY  
Secret: [.pem 파일 전체 내용 복사]
```

## 🔐 4단계: SSH 연결 설정 (Windows 11/PowerShell)

### 4.1 SSH 키 권한 설정
```powershell
# PowerShell을 관리자 권한으로 실행
$keyPath = "C:\Users\$env:USERNAME\Downloads\campinside-key-2025.pem"
icacls $keyPath /inheritance:r
icacls $keyPath /grant:r "$($env:USERNAME):R"
```

### 4.2 SSH 연결 테스트
```powershell
# SSH 연결 (IP는 실제 고정 IP로 변경)
ssh -i "C:\Users\$env:USERNAME\Downloads\campinside-key-2025.pem" ubuntu@3.34.123.45
```

## ⚙️ 5단계: 서버 초기 설정 (Ubuntu 22.04 + Python 3.12)

### 5.1 기본 환경 설정
```bash
# Ubuntu 22.04 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Python 3.12 및 필수 도구 설치
sudo apt install -y python3.12 python3.12-venv python3.12-dev python3-pip
sudo apt install -y build-essential libpq-dev nginx git curl

# Python 3.12를 기본으로 설정
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

# 버전 확인
python3 --version  # Python 3.12.x 확인
```

### 5.2 자동 설정 스크립트 실행
```bash
# 설정 스크립트 다운로드 및 실행
wget https://raw.githubusercontent.com/YOUR_USERNAME/campinside/main/deploy/setup.sh
chmod +x setup.sh
./setup.sh
```

### 5.3 스크립트 실행 시 입력할 정보
```
Repository URL: https://github.com/YOUR_USERNAME/campinside.git
DB Host: [Lightsail PostgreSQL 엔드포인트]
DB User: postgres
DB Password: [설정한 비밀번호]
DB Name: postgres
```

## 🌐 6단계: 애플리케이션 접속 확인

### 6.1 웹 브라우저에서 접속
```
메인 페이지: http://3.34.123.45/
Health Check: http://3.34.123.45/health
API 문서: http://3.34.123.45/docs
DB 상태: http://3.34.123.45/db-status
```

### 6.2 성능 및 상태 확인
```bash
# 시스템 리소스 확인
htop

# 서비스 상태 확인
sudo systemctl status campinside
sudo systemctl status nginx

# 로그 확인
sudo journalctl -u campinside -f
```

## 🔄 7단계: CI/CD 자동 배포 테스트

### 7.1 코드 변경 및 푸시
```powershell
# 로컬에서 변경
echo "# CampInside API v2.0 - Ubuntu 22.04 + Python 3.12" > README.md
git add README.md
git commit -m "Update for Ubuntu 22.04 + Python 3.12"
git push origin main
```

### 7.2 GitHub Actions 확인
1. GitHub 저장소 → **Actions** 탭
2. 워크플로우 실행 상태 확인
3. Python 3.12 환경에서 테스트 통과 확인

## 🛡️ 보안 및 최적화 (2025년 베스트 프랙티스)

### 보안 강화
```bash
# 방화벽 설정
sudo ufw enable
sudo ufw allow 22,80,443/tcp

# 자동 보안 업데이트
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 성능 최적화
```bash
# 스왑 파일 생성 (2GB)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

## 💰 2025년 예상 비용

- Lightsail 인스턴스 (2GB): **$12/월**
- PostgreSQL 데이터베이스 (1GB): **$18/월**
- 데이터 전송: **$1-2/월**
- **총 예상 비용: $31-32/월**

## 🎉 완료!

축하합니다! 2025년 최신 환경으로 완전히 업그레이드된 배포가 완료되었습니다:

- ✅ Ubuntu 22.04 LTS (최신 LTS)
- ✅ Python 3.12 (최신 안정 버전)
- ✅ PostgreSQL 15 (최신 DB)
- ✅ 보안 강화 및 성능 최적화
- ✅ 자동 CI/CD 파이프라인

## 📚 추가 리소스

- [Ubuntu 22.04 특화 설정 가이드](./UBUNTU_22_04_SETUP.md)
- [SSH 연결 가이드](./SSH_CONNECTION_GUIDE.md)  
- [GitHub 설정 가이드](./GITHUB_SETUP_GUIDE.md)

---

🚀 **이제 최신 환경에서 안전하고 빠른 애플리케이션을 운영할 수 있습니다!**
