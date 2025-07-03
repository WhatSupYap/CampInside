# GitHub 저장소 및 CI/CD 설정 가이드

## 1. GitHub 저장소 생성

### 새 저장소 생성
1. GitHub에 로그인 → **New repository** 클릭
2. **Repository name**: `campinside`
3. **Description**: `AWS Lightsail에서 실행되는 FastAPI 캠핑 예약 시스템`
4. **Public** 또는 **Private** 선택
5. **Create repository** 클릭

### 로컬 저장소와 연결
```bash
# 현재 프로젝트 디렉토리에서 실행
git init
git add .
git commit -m "Initial commit: FastAPI + PostgreSQL + Lightsail setup"

# 원격 저장소 추가 (URL을 실제 저장소로 변경)
git remote add origin https://github.com/YOUR_USERNAME/campinside.git
git branch -M main
git push -u origin main
```

## 2. GitHub Secrets 설정

### Actions Secrets 추가
GitHub 저장소 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

필수 Secrets:
```
LIGHTSAIL_HOST=3.34.123.45  # Lightsail 인스턴스 고정 IP
LIGHTSAIL_USER=ubuntu       # SSH 사용자명
LIGHTSAIL_SSH_KEY=          # .pem 파일 내용 전체 복사
```

### SSH 키 내용 복사 방법

#### Windows PowerShell:
```powershell
Get-Content "C:\Users\YourName\.ssh\campinside-key.pem" | Set-Clipboard
```

#### Windows 메모장:
1. .pem 파일을 메모장으로 열기
2. 전체 선택 후 복사
3. GitHub Secret에 붙여넣기

#### 내용 예시:
```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
...전체 키 내용...
-----END RSA PRIVATE KEY-----
```

## 3. 추가 환경변수 Secrets (선택사항)

보안이 중요한 환경변수들을 Secrets로 관리:
```
DB_HOST=your-postgres-endpoint.ap-northeast-2.rds.amazonaws.com
DB_PASSWORD=your-secure-password
SECRET_KEY=your-app-secret-key
```

## 4. CI/CD 워크플로우 테스트

### 첫 배포 테스트
```bash
# 작은 변경사항 추가
echo "# CampInside API" > README.md
git add README.md
git commit -m "Add README"
git push origin main
```

### GitHub Actions 확인
1. GitHub 저장소 → **Actions** 탭
2. 워크플로우 실행 상태 확인
3. 로그 확인하여 오류 해결

## 5. 브랜치 보호 규칙 설정 (권장)

### main 브랜치 보호
GitHub 저장소 → **Settings** → **Branches** → **Add rule**

설정:
- **Branch name pattern**: `main`
- ✅ **Require a pull request before merging**
- ✅ **Require status checks to pass before merging**
- ✅ **Require branches to be up to date before merging**
- ✅ **Include administrators**

## 6. 개발 워크플로우

### 기능 개발 프로세스
```bash
# 새 기능 브랜치 생성
git checkout -b feature/user-authentication
git push -u origin feature/user-authentication

# 개발 완료 후
git add .
git commit -m "Add user authentication system"
git push origin feature/user-authentication

# GitHub에서 Pull Request 생성
# 코드 리뷰 후 main 브랜치에 merge
```

### 핫픽스 프로세스
```bash
# 긴급 수정사항
git checkout -b hotfix/critical-bug-fix
# 수정 작업
git add .
git commit -m "Fix critical security issue"
git push origin hotfix/critical-bug-fix

# PR 생성 및 빠른 merge
```

## 7. 모니터링 및 알림 설정

### Slack 알림 (선택사항)
GitHub 저장소 → **Settings** → **Webhooks** → **Add webhook**

배포 성공/실패 알림을 받을 수 있습니다.

### 이메일 알림
GitHub **Personal settings** → **Notifications**에서 설정
