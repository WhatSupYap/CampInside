# 🚀 AWS Lightsail CampInside 완전 배포 가이드

이 가이드는 AWS Lightsail에서 FastAPI + PostgreSQL 애플리케이션을 처음부터 끝까지 배포하는 방법을 설명합니다.

## 📋 사전 준비사항

- [ ] AWS 계정
- [ ] GitHub 계정
- [ ] Windows PC (PowerShell 사용)
- [ ] 신용카드 (AWS 결제용)

## 🆕 2025년 최신 업데이트

- ✅ **Ubuntu 22.04 LTS** (최신 LTS 버전)
- ✅ **Python 3.12** (최신 안정 버전)
- ✅ **PostgreSQL 15** (최신 버전)
- ✅ **FastAPI 최신 버전** 지원

## 🎯 1단계: AWS Lightsail 인스턴스 생성

### 1.1 AWS 콘솔 접속
1. [AWS Lightsail 콘솔](https://lightsail.aws.amazon.com/) 접속
2. **Create instance** 클릭

### 1.2 인스턴스 설정
```
✅ Instance location: Asia Pacific (Seoul)
✅ Platform: Linux/Unix
✅ OS: Ubuntu 22.04 LTS
✅ Instance plan: $10/month (2GB RAM, 1vCPU, 60GB SSD)
✅ Instance name: campinside-server
✅ Key pair: Create new → campinside-key → Download .pem file
```

### 1.3 고정 IP 할당
1. 인스턴스 생성 완료 후
2. **Networking** 탭 → **Create static IP**
3. IP 주소 기록: `예: 3.34.123.45`

## 🗄️ 2단계: PostgreSQL 데이터베이스 생성

### 2.1 데이터베이스 생성
1. Lightsail 홈 → **Databases** 탭
2. **Create database** 클릭

### 2.2 데이터베이스 설정
```
✅ Database engine: PostgreSQL 15
✅ Database plan: $15/month (1GB RAM, 20GB SSD)
✅ Database name: campinside-db
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
git commit -m "Initial commit: FastAPI + PostgreSQL setup"
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

## 🔐 4단계: SSH 연결 설정

### 4.1 SSH 키 권한 설정 (Windows)
```powershell
# PowerShell을 관리자 권한으로 실행
icacls "C:\Users\YourName\Downloads\campinside-key.pem" /inheritance:r
icacls "C:\Users\YourName\Downloads\campinside-key.pem" /grant:r "$($env:USERNAME):R"
```

### 4.2 SSH 연결 테스트
```powershell
# SSH 연결 (IP는 실제 고정 IP로 변경)
ssh -i "C:\Users\YourName\Downloads\campinside-key.pem" ubuntu@3.34.123.45
```

성공하면 Ubuntu 서버에 접속됩니다.

## ⚙️ 5단계: 서버 초기 설정

### 5.1 설정 스크립트 실행
```bash
# 서버에서 실행
# 설정 스크립트 다운로드
wget https://raw.githubusercontent.com/YOUR_USERNAME/campinside/main/deploy/setup.sh
chmod +x setup.sh

# 실행 (대화형으로 정보 입력)
./setup.sh
```

### 5.2 스크립트 실행 시 입력할 정보
```
Repository URL: https://github.com/YOUR_USERNAME/campinside.git
DB Host: [Lightsail PostgreSQL 엔드포인트]
DB User: postgres
DB Password: [설정한 비밀번호]
DB Name: postgres
```

### 5.3 설정 완료 확인
스크립트 완료 후 다음 명령어로 확인:
```bash
# 서비스 상태 확인
sudo systemctl status campinside
sudo systemctl status nginx

# 애플리케이션 테스트
curl http://localhost/health
curl http://localhost/
```

## 🌐 6단계: 애플리케이션 접속 확인

### 6.1 웹 브라우저에서 접속
```
메인 페이지: http://3.34.123.45/
Health Check: http://3.34.123.45/health
API 문서: http://3.34.123.45/docs
DB 상태: http://3.34.123.45/db-status
```

### 6.2 정상 동작 확인
- [ ] Health check 응답: `{"status": "healthy"}`
- [ ] API 문서 페이지 로드
- [ ] DB 연결 상태 확인

## 🔄 7단계: CI/CD 자동 배포 테스트

### 7.1 코드 변경 및 푸시
```powershell
# 로컬에서 간단한 변경
echo "# CampInside API v1.0" > README.md
git add README.md
git commit -m "Update README"
git push origin main
```

### 7.2 GitHub Actions 확인
1. GitHub 저장소 → **Actions** 탭
2. 워크플로우 실행 상태 확인
3. 배포 완료까지 대기 (약 2-3분)

### 7.3 배포 확인
배포 완료 후 다시 웹사이트 접속하여 변경사항 반영 확인

## 🐛 문제 해결

### SSH 연결 문제
```bash
# 권한 오류 시
chmod 400 campinside-key.pem

# 타임아웃 시 Lightsail 방화벽 확인
# AWS 콘솔 → Lightsail → 인스턴스 → Networking 탭
```

### 서비스 상태 확인
```bash
# 로그 확인
sudo journalctl -u campinside -f

# 서비스 재시작
sudo systemctl restart campinside
sudo systemctl restart nginx
```

### 데이터베이스 연결 문제
```bash
# 데이터베이스 연결 테스트
cd /opt/campinside
source venv/bin/activate
python scripts/test_db_connection.py
```

## 🎉 완료!

축하합니다! 이제 다음이 완료되었습니다:

- ✅ AWS Lightsail 서버 구성
- ✅ PostgreSQL 데이터베이스 연결
- ✅ FastAPI 애플리케이션 배포
- ✅ Nginx 리버스 프록시 설정
- ✅ GitHub Actions CI/CD 파이프라인
- ✅ 자동 배포 시스템

## 📚 다음 단계

1. **도메인 연결** 및 **SSL 인증서** 설정
2. **데이터베이스 스키마** 설계 및 마이그레이션
3. **사용자 인증** 시스템 구현
4. **캠핑장 예약** 기능 개발
5. **모니터링** 및 **로깅** 시스템 구축

## 💰 예상 비용

- Lightsail 인스턴스: $10/월
- PostgreSQL 데이터베이스: $15/월
- **총 예상 비용: $25/월**

---

문제가 발생하면 GitHub Issues에 문의하거나 로그를 확인하여 해결하세요!
