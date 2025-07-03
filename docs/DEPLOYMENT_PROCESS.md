# AWS Lightsail + PostgreSQL + FastAPI + GitHub Actions 배포 가이드

## 1단계: GitHub Repository 설정

### 1.1 GitHub에 Repository 생성
1. GitHub에서 새 repository `campinside` 생성
2. README.md, .gitignore 체크 해제 (이미 파일들이 있으므로)

### 1.2 로컬에서 GitHub에 Push
```bash
# 현재 디렉토리에서 실행
git init
git add .
git commit -m "Initial commit: FastAPI + PostgreSQL setup"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/campinside.git
git push -u origin main
```

## 2단계: AWS Lightsail 설정

### 2.1 Lightsail 인스턴스 생성
- OS: Ubuntu 22.04 LTS
- 플랜: $5/월 이상 권장
- SSH 키페어 생성 및 다운로드

### 2.2 Lightsail PostgreSQL 데이터베이스 생성
- 데이터베이스 엔진: PostgreSQL
- 플랜: $15/월 이상 권장
- 마스터 사용자명: postgres
- 초기 데이터베이스명: campinside

### 2.3 방화벽 설정
- HTTP (80)
- HTTPS (443)
- SSH (22)
- Custom TCP (8000) - FastAPI 개발용

## 3단계: GitHub Secrets 설정

Repository → Settings → Secrets and variables → Actions에서 다음 추가:

- `LIGHTSAIL_IP`: Lightsail 인스턴스 공용 IP
- `SSH_PRIVATE_KEY`: .pem 파일 내용 전체 복사
- `DB_HOST`: PostgreSQL 엔드포인트
- `DB_USER`: postgres
- `DB_PASSWORD`: 설정한 데이터베이스 비밀번호
- `DB_NAME`: campinside

## 4단계: 서버 초기 설정

SSH로 서버 접속 후:
```bash
# 프로젝트 클론
git clone https://github.com/YOUR_USERNAME/campinside.git
cd campinside

# 설정 스크립트 실행
chmod +x deploy/setup.sh
sudo ./deploy/setup.sh
```

## 5단계: GitHub Actions 트리거

main 브랜치에 코드를 push하면 자동으로 배포됩니다:
```bash
git add .
git commit -m "Deploy to production"
git push origin main
```

## 6단계: 확인

브라우저에서 다음 URL 접속:
- `http://YOUR_LIGHTSAIL_IP:8000` - FastAPI 애플리케이션
- `http://YOUR_LIGHTSAIL_IP:8000/docs` - API 문서

## 트러블슈팅

### 일반적인 문제들
1. SSH 연결 실패 → 방화벽 확인
2. PostgreSQL 연결 실패 → 엔드포인트 및 보안그룹 확인
3. 권한 오류 → setup.sh 실행 권한 확인
4. 포트 충돌 → systemctl status 명령으로 서비스 상태 확인
