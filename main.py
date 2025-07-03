# main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
import uvicorn
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv() # .env 파일 로드

app = FastAPI(
    title="CampInside API", 
    version="2.0.0",
    description="PostgreSQL 17 + Python 3.12 기반 캠핑 예약 시스템 테스트"
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

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CampInside - Hello World!</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                text-align: center;
                background: white;
                padding: 3rem;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                max-width: 500px;
                margin: 20px;
            }
            h1 {
                color: #2c3e50;
                font-size: 3rem;
                margin-bottom: 1rem;
                font-weight: 700;
            }
            p {
                color: #7f8c8d;
                font-size: 1.2rem;
                margin-bottom: 2rem;
                line-height: 1.6;
            }
            .badge {
                display: inline-block;
                background: #3498db;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 25px;
                font-size: 0.9rem;
                margin: 0.5rem;
                font-weight: 500;
            }
            .links {
                margin-top: 2rem;
            }
            .links a {
                display: inline-block;
                background: #2ecc71;
                color: white;
                text-decoration: none;
                padding: 0.8rem 1.5rem;
                border-radius: 10px;
                margin: 0.5rem;
                transition: background 0.3s;
                font-weight: 500;
            }
            .links a:hover {
                background: #27ae60;
            }
            .emoji {
                font-size: 4rem;
                margin-bottom: 1rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="emoji">🏕️</div>
            <h1>Hello World!</h1>
            <p>CampInside API에 오신 것을 환영합니다!<br>
            FastAPI + PostgreSQL + AWS Lightsail로 구축된<br>
            캠핑 예약 시스템입니다.</p>
            
            <div class="badges">
                <span class="badge">FastAPI 2.0.0</span>
                <span class="badge">PostgreSQL 17</span>
                <span class="badge">Python 3.12</span>
                <span class="badge">AWS Lightsail</span>
            </div>
            
            <div class="links">
                <a href="/docs" target="_blank">📚 API 문서</a>
                <a href="/health" target="_blank">💚 헬스체크</a>
                <a href="/db-status" target="_blank">🗄️ DB 상태</a>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

@app.get("/api", description="JSON API 응답")
async def api_root():
    return {"message": "Hello FastAPI!", "status": "success", "version": "2.0.0"}

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