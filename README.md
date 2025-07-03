# CampInside - FastAPI Application

AWS Lightsail + PostgreSQL + FastAPI + GitHub Actions를 사용한 캠핑 예약 시스템

## 🚀 기술 스택

- **Backend**: FastAPI, Python 3.12
- **Database**: PostgreSQL 17 (AWS Lightsail)
- **Deployment**: AWS Lightsail
- **CI/CD**: GitHub Actions
- **Web Server**: Nginx + Gunicorn

## 📋 요구사항

- Python 3.12+
- PostgreSQL 17+
- AWS Lightsail 인스턴스

## 🛠️ 로컬 개발 환경 설정

### 1. 저장소 클론
```bash
git clone https://github.com/YOUR_USERNAME/campinside.git
cd campinside
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate.ps1
# Linux/Mac
source venv/bin/activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일을 편집하여 데이터베이스 정보 입력
```

### 5. 애플리케이션 실행
```bash
uvicorn main:app --reload
```

애플리케이션이 http://localhost:8000 에서 실행됩니다.

## 🌐 프로덕션 배포

### AWS Lightsail 설정

1. **Lightsail 인스턴스 생성**
   - Ubuntu 20.04 LTS 선택
   - 적절한 인스턴스 크기 선택

2. **PostgreSQL 데이터베이스 생성**
   - Lightsail 관리형 데이터베이스 생성
   - PostgreSQL 15 선택

3. **서버 초기 설정**
```bash
# 서버에 SSH 접속 후 실행
wget https://raw.githubusercontent.com/YOUR_USERNAME/campinside/main/deploy/setup.sh
chmod +x setup.sh
./setup.sh
```

### GitHub Secrets 설정

GitHub 저장소의 Settings > Secrets and variables > Actions에서 다음 secrets를 설정:

```
LIGHTSAIL_HOST=your-lightsail-ip
LIGHTSAIL_USER=ubuntu
LIGHTSAIL_SSH_KEY=your-private-key
```

### 배포

`main` 브랜치에 push하면 자동으로 배포됩니다:

```bash
git add .
git commit -m "Deploy to production"
git push origin main
```

## 📡 API 문서

애플리케이션 실행 후 다음 URL에서 API 문서 확인:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔍 모니터링

### 애플리케이션 상태 확인
```bash
# 서비스 상태
sudo systemctl status campinside

# 로그 확인
sudo journalctl -u campinside -f

# 애플리케이션 재시작
sudo systemctl restart campinside
```

### Health Check
- http://your-domain.com/health
- http://your-domain.com/db-status

## 🧪 테스트

```bash
# 테스트 실행
pytest tests/ -v

# 커버리지 포함
pytest tests/ --cov=.
```

## 🐳 Docker 사용 (선택사항)

### 로컬 개발
```bash
docker-compose up -d
```

### 프로덕션 빌드
```bash
docker build -t campinside .
docker run -p 8000:8000 campinside
```

## 📝 프로젝트 구조

```
campinside/
├── main.py                 # FastAPI 애플리케이션
├── requirements.txt        # Python 의존성
├── .env.example           # 환경 변수 예시
├── deploy/                # 배포 관련 파일
│   ├── setup.sh          # 서버 초기 설정 스크립트
│   ├── campinside.service # Systemd 서비스 파일
│   └── nginx.conf        # Nginx 설정
├── tests/                # 테스트 파일
├── .github/
│   └── workflows/
│       └── deploy.yml    # GitHub Actions CI/CD
├── Dockerfile            # Docker 설정 (선택사항)
└── docker-compose.yml    # Docker Compose (선택사항)
```

## 🔧 다음 단계

1. **데이터베이스 스키마 설계**
   - SQLAlchemy 모델 생성
   - Alembic 마이그레이션 설정

2. **인증 시스템 구현**
   - JWT 토큰 기반 인증
   - 사용자 등록/로그인

3. **캠핑장 예약 시스템**
   - 캠핑장 정보 관리
   - 예약 생성/조회/수정/삭제

4. **결제 시스템 연동**
   - 결제 게이트웨이 연동

5. **알림 시스템**
   - 이메일/SMS 알림

## 🤝 기여

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이센스

This project is licensed under the MIT License.
