# PostgreSQL 17.5 최적화 가이드

## 🚀 PostgreSQL 17.5 장점

PostgreSQL 17.5는 2025년 최신 버전으로 다음과 같은 개선사항이 있습니다:

### 🔥 주요 성능 개선
- **JSON 처리 성능 30% 향상**
- **병렬 쿼리 성능 개선**
- **인덱스 성능 최적화**
- **메모리 사용량 최적화**

### 🛡️ 보안 강화
- **향상된 SSL/TLS 지원**
- **새로운 인증 방법**
- **로그 보안 강화**

### 🆕 새로운 기능
- **개선된 JSON/JSONB 지원**
- **더 나은 파티셔닝**
- **향상된 리플리케이션**

## ⚙️ FastAPI + PostgreSQL 17.5 최적화 설정

### 1. 연결 설정 최적화

```python
# main.py - PostgreSQL 17 최적화 설정
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()

# 연결 풀 설정 (PostgreSQL 17 최적화)
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT', 5432),
    'sslmode': 'require',  # PostgreSQL 17 보안 강화
    'application_name': 'campinside_api',
    'connect_timeout': 10,
    'command_timeout': 30,
}

# 연결 풀 생성 (성능 최적화)
connection_pool = psycopg2.pool.ThreadedConnectionPool(
    1, 20,  # 최소 1개, 최대 20개 연결
    **DB_CONFIG
)

def get_db_connection():
    """데이터베이스 연결 가져오기"""
    return connection_pool.getconn()

def release_db_connection(conn):
    """데이터베이스 연결 반환"""
    connection_pool.putconn(conn)

@app.get("/db-status-advanced")
async def get_db_status_advanced():
    """PostgreSQL 17 고급 상태 확인"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # PostgreSQL 17 전용 정보 조회
        cursor.execute("""
            SELECT 
                version() as pg_version,
                current_setting('server_version_num') as version_num,
                current_setting('shared_preload_libraries') as shared_libs,
                current_setting('max_connections') as max_conn,
                current_setting('shared_buffers') as shared_buffers,
                pg_size_pretty(pg_database_size(current_database())) as db_size
        """)
        
        db_info = cursor.fetchone()
        
        # 연결 통계
        cursor.execute("""
            SELECT 
                count(*) as active_connections,
                count(*) FILTER (WHERE state = 'active') as active_queries
            FROM pg_stat_activity 
            WHERE datname = current_database()
        """)
        
        conn_stats = cursor.fetchone()
        
        cursor.close()
        release_db_connection(conn)
        
        return {
            "status": "connected",
            "postgresql_version": db_info['pg_version'],
            "version_number": db_info['version_num'],
            "database_size": db_info['db_size'],
            "max_connections": db_info['max_conn'],
            "shared_buffers": db_info['shared_buffers'],
            "active_connections": conn_stats['active_connections'],
            "active_queries": conn_stats['active_queries'],
            "connection_pool_info": {
                "pool_size": connection_pool.maxconn,
                "available": connection_pool.maxconn - len(connection_pool._used)
            }
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

### 2. SQLAlchemy + PostgreSQL 17 설정

```python
# database.py - SQLAlchemy 설정
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os

# PostgreSQL 17 최적화 연결 문자열
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?sslmode=require&application_name=campinside_sqlalchemy"

# PostgreSQL 17 최적화 엔진 설정
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False,  # 운영환경에서는 False
    # PostgreSQL 17 특화 설정
    connect_args={
        "sslmode": "require",
        "connect_timeout": 10,
        "command_timeout": 30,
        "application_name": "campinside_sqlalchemy"
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 메타데이터 설정 (PostgreSQL 17 스키마 지원)
metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)

def get_db():
    """데이터베이스 세션 생성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 3. 데이터베이스 성능 모니터링

```python
# monitoring.py - PostgreSQL 17 모니터링
@app.get("/db-performance")
async def get_db_performance():
    """PostgreSQL 17 성능 모니터링"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # 느린 쿼리 확인
        cursor.execute("""
            SELECT 
                query,
                calls,
                total_exec_time,
                mean_exec_time,
                max_exec_time
            FROM pg_stat_statements 
            ORDER BY mean_exec_time DESC 
            LIMIT 5
        """)
        slow_queries = cursor.fetchall()
        
        # 테이블 크기 확인
        cursor.execute("""
            SELECT 
                schemaname,
                tablename,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
        """)
        table_sizes = cursor.fetchall()
        
        # 인덱스 사용률
        cursor.execute("""
            SELECT 
                schemaname,
                tablename,
                idx_tup_read,
                seq_tup_read,
                CASE 
                    WHEN seq_tup_read + idx_tup_read = 0 THEN 0
                    ELSE (idx_tup_read::float / (seq_tup_read + idx_tup_read) * 100)::int
                END as index_usage_percent
            FROM pg_stat_user_tables
            ORDER BY seq_tup_read DESC
        """)
        index_usage = cursor.fetchall()
        
        cursor.close()
        release_db_connection(conn)
        
        return {
            "slow_queries": slow_queries,
            "table_sizes": table_sizes,
            "index_usage": index_usage
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

## 🔧 PostgreSQL 17.5 서버 설정 최적화

### 서버 설정 조정 (선택사항)

```bash
# PostgreSQL 17 설정 최적화 (Lightsail에서는 제한적)
# 이 설정들은 참고용이며, Lightsail 관리형 DB에서는 일부만 가능

# 연결 관련
max_connections = 100
shared_buffers = 256MB  # RAM의 25% 정도

# 성능 관련  
effective_cache_size = 1GB  # RAM의 75% 정도
random_page_cost = 1.1  # SSD 환경
seq_page_cost = 1.0

# WAL 설정
wal_buffers = 16MB
checkpoint_completion_target = 0.9

# 통계 수집
track_activities = on
track_counts = on
track_io_timing = on
track_functions = all
```

## 🧪 PostgreSQL 17.5 테스트

```python
# test_postgresql17.py - PostgreSQL 17 전용 테스트
import pytest
import psycopg2
from psycopg2.extras import RealDictCursor

def test_postgresql17_features():
    """PostgreSQL 17 기능 테스트"""
    
    # JSON 성능 테스트
    cursor.execute("""
        SELECT '{"name": "CampInside", "version": "2025.7"}'::jsonb ? 'name' as has_name
    """)
    result = cursor.fetchone()
    assert result['has_name'] == True
    
    # 새로운 SQL 기능 테스트
    cursor.execute("""
        SELECT 
            CURRENT_TIMESTAMP as now,
            version() as pg_version
    """)
    result = cursor.fetchone()
    assert "PostgreSQL 17" in result['pg_version']

def test_connection_performance():
    """연결 성능 테스트"""
    import time
    
    start_time = time.time()
    conn = get_db_connection()
    connect_time = time.time() - start_time
    
    assert connect_time < 1.0  # 1초 이내 연결
    release_db_connection(conn)
```

## ✅ PostgreSQL 17.5 사용 시 장점

1. **🚀 성능**: 이전 버전 대비 20-30% 성능 향상
2. **🛡️ 보안**: 최신 보안 패치 및 기능
3. **🔧 안정성**: 버그 수정 및 안정성 개선
4. **📊 모니터링**: 향상된 통계 및 모니터링 기능
5. **🌟 호환성**: FastAPI, SQLAlchemy 완벽 호환

**결론: PostgreSQL 17.5는 2025년 현재 최고의 선택입니다!** ✨
