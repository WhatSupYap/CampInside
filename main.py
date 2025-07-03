# main.py
from fastapi import FastAPI
import os
import uvicorn
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv() # .env 파일 로드

app = FastAPI(
    title="CampInside API", 
    version="2.0.0",
    description="PostgreSQL 17 + Python 3.12 기반 캠핑 예약 시스템"
)

# DB 연결 정보 (PostgreSQL 17 환경변수)
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT", 5432) # PostgreSQL 기본 포트

# PostgreSQL 17 연결 설정
DB_CONFIG = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_NAME,
    'port': DB_PORT,
    'sslmode': 'require',  # PostgreSQL 17 보안 강화
    'application_name': 'campinside_api',
    'connect_timeout': 10,
}

@app.get("/")
async def read_root():
    return {"message": "Hello FastAPI!"}

@app.get("/db-status")
async def get_db_status():
    try:
        # PostgreSQL 17 연결 시도
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # PostgreSQL 17 버전 및 상태 확인
        cursor.execute("""
            SELECT 
                version() as pg_version,
                current_setting('server_version_num') as version_num,
                current_database() as database_name,
                current_user as current_user,
                pg_size_pretty(pg_database_size(current_database())) as db_size
        """)
        db_info = cursor.fetchone()
        
        # 연결 통계
        cursor.execute("""
            SELECT count(*) as active_connections
            FROM pg_stat_activity 
            WHERE datname = current_database()
        """)
        conn_info = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return {
            "db_status": "connected successfully",
            "postgresql_version": db_info['pg_version'],
            "version_number": db_info['version_num'],
            "database": db_info['database_name'],
            "user": db_info['current_user'],
            "database_size": db_info['db_size'],
            "active_connections": conn_info['active_connections'],
            "features": ["PostgreSQL 17", "SSL enabled", "JSON optimization"]
        }
    except Exception as e:
        return {"db_status": f"connection error: {str(e)}"}

@app.get("/db-performance")
async def get_db_performance():
    """PostgreSQL 17 성능 정보"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # 기본 성능 통계
        cursor.execute("""
            SELECT 
                current_setting('shared_buffers') as shared_buffers,
                current_setting('effective_cache_size') as effective_cache_size,
                current_setting('max_connections') as max_connections,
                current_setting('wal_buffers') as wal_buffers
        """)
        perf_info = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return {
            "status": "success",
            "postgresql_config": dict(perf_info),
            "optimization": "PostgreSQL 17 optimized for FastAPI"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트 - CI/CD에서 사용"""
    try:
        # 기본 응답
        health_status = {
            "status": "healthy",
            "service": "CampInside API",
            "version": "2.0.0"
        }
        
        # DB 연결 확인 (간단한 버전)
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        
        health_status["database"] = "connected"
        return health_status
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "CampInside API",
            "version": "2.0.0",
            "database": "disconnected",
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)