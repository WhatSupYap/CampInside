# 🎯 AWS Lightsail 상세 설정 가이드 (2025년 7월 기준)

## 📱 1단계: AWS 계정 준비 및 Lightsail 접속

### 1.1 AWS 계정 로그인
1. [AWS 콘솔](https://aws.amazon.com/ko/) 접속
2. **AWS 계정으로 로그인** 클릭
3. 계정이 없다면 **새 AWS 계정 생성**

### 1.2 Lightsail 서비스 접속
1. AWS 관리 콘솔에서 **"Lightsail"** 검색
2. **Amazon Lightsail** 클릭
3. 또는 직접 [lightsail.aws.amazon.com](https://lightsail.aws.amazon.com/) 접속

---

## 🖥️ 2단계: Lightsail 인스턴스 생성

### 2.1 인스턴스 생성 시작
```
👆 "Create instance" 버튼 클릭
```

### 2.2 인스턴스 위치 선택
```
📍 Instance location: Asia Pacific (Seoul) - ap-northeast-2
   ✅ 이유: 한국에서 가장 가까운 AWS 리전 (낮은 지연시간)
```

### 2.3 플랫폼 및 운영체제 선택
```
🐧 Platform: Linux/Unix 선택
📀 Blueprint: OS Only 탭 선택
💿 Operating System: Ubuntu 22.04 LTS 선택
   ✅ 2025년 7월 현재 Lightsail에서 지원하는 최신 Ubuntu LTS
```

### 2.4 인스턴스 플랜 선택 (2025년 7월 기준)
```
💲 인스턴스 플랜 옵션:

🔹 $5/월: 512MB RAM, 1vCPU, 20GB SSD 
   ❌ 개발용으로도 부족 (비추천)

🔹 $10/월: 1GB RAM, 1vCPU, 40GB SSD
   ⚠️ 최소 사양 (소규모 개발용)

✅ $12/월: 2GB RAM, 1vCPU, 60GB SSD ⭐ 권장
   ✅ FastAPI + PostgreSQL 운영에 적합
   ✅ 여유로운 메모리와 저장공간

🔹 $20/월: 4GB RAM, 2vCPU, 80GB SSD
   💰 성능이 중요한 상용 서비스용
```

### 2.5 인스턴스 식별 정보 설정
```
🏷️ Instance name: campinside-server-2025
📝 Resource tags (선택사항):
   - Key: Project, Value: CampInside
   - Key: Environment, Value: Production
   - Key: Owner, Value: YourName
```

### 2.6 SSH 키 페어 설정 ⚠️ 중요!
```
🔐 SSH Key pair:
   ✅ "Create new" 선택
   📝 Key pair name: campinside-key-2025
   💾 "Download" 클릭하여 .pem 파일 저장
   📂 안전한 위치에 저장: C:\Users\YourName\.ssh\
```

### 2.7 인스턴스 생성 완료
```
🚀 "Create instance" 클릭
⏱️ 생성 시간: 약 1-2분
✅ 상태가 "Running"이 될 때까지 대기
```

---

## 🌐 3단계: 고정 IP 설정

### 3.1 고정 IP가 필요한 이유
```
❌ 동적 IP: 인스턴스 재시작 시 IP 변경
✅ 고정 IP: 항상 같은 IP 주소 유지
💡 도메인 연결 시 필수
```

### 3.2 고정 IP 생성
```
1. 생성된 인스턴스 클릭
2. "Networking" 탭 클릭
3. "Create static IP" 클릭
4. Static IP name: campinside-static-ip
5. "Create" 클릭
```

### 3.3 IP 주소 기록
```
📝 고정 IP 주소 예시: 3.34.123.45
   ✅ 이 IP를 GitHub Secrets에 등록 예정
   ✅ 도메인 DNS 설정에도 사용
```

---

## 🗄️ 4단계: PostgreSQL 데이터베이스 생성

### 4.1 데이터베이스 생성 시작
```
1. Lightsail 홈페이지로 돌아가기
2. "Databases" 탭 클릭
3. "Create database" 클릭
```

### 4.2 데이터베이스 엔진 선택
```
🐘 Database engine: PostgreSQL
📊 Version: 17.x (최신 버전 - 17.5 포함) ⭐ 2025년 최신
   ✅ FastAPI와 완벽 호환
   ✅ 최신 성능 개선 및 보안 강화
   ✅ JSON 처리 성능 대폭 향상
   ✅ 쿼리 성능 최적화
```

### 4.3 데이터베이스 플랜 선택 (2025년 7월 기준)
```
💲 데이터베이스 플랜 옵션:

🔹 $15/월: 1GB RAM, 20GB SSD, burst성능
   ✅ 개발 및 소규모 운영용 (권장)

🔹 $30/월: 2GB RAM, 32GB SSD, 일정 성능
   💰 중간 규모 서비스용

🔹 $60/월: 4GB RAM, 64GB SSD, 고성능
   🚀 대용량 데이터 처리용
```

### 4.4 데이터베이스 식별 정보
```
🏷️ Database name: campinside-db-2025
📍 Availability zone: ap-northeast-2a (자동 선택)
```

### 4.5 마스터 사용자 설정 ⚠️ 중요!
```
👤 Master username: postgres (기본값 사용)
🔒 Master password: 
   ✅ 최소 8자리
   ✅ 대소문자, 숫자, 특수문자 포함
   📝 예시: CampInside2025!@#
   💾 안전한 곳에 기록 필수!
```

### 4.6 데이터베이스 생성 완료
```
🚀 "Create database" 클릭
⏱️ 생성 시간: 약 5-10분
✅ 상태가 "Available"이 될 때까지 대기
```

---

## 📝 5단계: 연결 정보 정리

### 5.1 인스턴스 연결 정보
```
🖥️ 서버 정보:
   📍 고정 IP: 3.34.123.45 (실제 IP로 변경)
   👤 사용자명: ubuntu
   🔐 SSH 키: campinside-key-2025.pem
   🌍 지역: 서울 (ap-northeast-2)
```

### 5.2 데이터베이스 연결 정보
```
🐘 PostgreSQL 정보:
   📍 엔드포인트: xxxxx.ap-northeast-2.rds.amazonaws.com
   👤 사용자명: postgres
   🔒 비밀번호: CampInside2025!@#
   🗄️ 기본 DB: postgres
   🔌 포트: 5432
```

### 5.3 연결 정보 확인 방법
```
데이터베이스 생성 완료 후:
1. Databases 탭에서 생성한 DB 클릭
2. "Connect" 탭에서 엔드포인트 확인
3. 📋 복사 버튼으로 엔드포인트 복사
```

---

## 🔍 6단계: 설정 확인

### 6.1 인스턴스 상태 확인
```
✅ 확인 사항:
   - 인스턴스 상태: Running
   - 고정 IP: 할당됨
   - SSH 키: 다운로드 완료
   - 방화벽: HTTP(80), HTTPS(443), SSH(22) 허용
```

### 6.2 데이터베이스 상태 확인
```
✅ 확인 사항:
   - 데이터베이스 상태: Available
   - 엔드포인트: 생성됨
   - 마스터 계정: 설정됨
   - 백업: 자동 활성화
```

---

## 💰 7단계: 비용 계산 (2025년 7월 기준)

### 7.1 월간 예상 비용
```
🖥️ Lightsail 인스턴스 (2GB): $12/월
🗄️ PostgreSQL 데이터베이스 (1GB): $15/월
🌐 데이터 전송 (첫 1TB 무료): $0/월
🔒 고정 IP (인스턴스 실행 중): $0/월

💰 총 월간 비용: $27/월
📅 연간 비용: $324/년
```

### 7.2 비용 최적화 팁
```
💡 비용 절약 방법:
   - 개발 시에만 인스턴스 실행
   - 스냅샷으로 데이터 백업 후 임시 삭제
   - 모니터링으로 불필요한 리소스 확인
```

---

## ⚠️ 8단계: 보안 및 주의사항

### 8.1 중요한 보안 설정
```
🔐 SSH 키 관리:
   ✅ .pem 파일을 안전한 위치에 보관
   ✅ 권한 설정: 600 (소유자만 읽기)
   ❌ 절대 GitHub에 업로드 금지

🔒 데이터베이스 보안:
   ✅ 강력한 비밀번호 사용
   ✅ 정기적인 비밀번호 변경
   ✅ 백업 설정 확인
```

### 8.2 백업 설정 확인
```
💾 자동 백업 (기본 활성화):
   - 인스턴스: 7일간 스냅샷 보관
   - 데이터베이스: 7일간 자동 백업
   - 수동 스냅샷도 생성 가능
```

---

## 🎯 다음 단계 미리보기

```
✅ AWS Lightsail 설정 완료
⬇️ 다음: SSH 연결 및 서버 초기 설정
⬇️ 그 다음: GitHub 저장소 연결
⬇️ 마지막: 애플리케이션 배포 자동화
```

---

## 🆘 문제 해결 (FAQ)

### Q1: Ubuntu 22.04가 보이지 않아요
```
A: Lightsail 콘솔에서 "OS Only" 탭을 선택했는지 확인하세요.
   "Apps + OS" 탭이 아닌 "OS Only" 탭에서 선택해야 합니다.
```

### Q2: 인스턴스 생성이 실패해요
```
A: 다음을 확인하세요:
   - 신용카드 정보가 올바른지
   - 계정 한도에 문제가 없는지
   - 다른 리전(서울 대신 오레곤)에서 시도
```

### Q3: 데이터베이스 연결이 안 돼요
```
A: 데이터베이스 생성 완료까지 5-10분 소요됩니다.
   상태가 "Available"이 될 때까지 기다려주세요.
```

이제 AWS Lightsail 설정이 완료되었습니다! 다음 단계로 SSH 연결을 진행하시겠어요? 🚀
