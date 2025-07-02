# main.py
from fastapi import FastAPI
import os
import uvicorn
from dotenv import load_dotenv
import mysql.connector # 또는 psycopg2 for PostgreSQL

load_dotenv() # .env 파일 로드

app = FastAPI()

# DB 연결 정보 (환경 변수에서 가져오기)
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT", 3306) # MySQL 기본 포트

@app.get("/")
async def read_root():
    return {"message": "Hello FastAPI!"}

@app.get("/db-status")
async def get_db_status():
    try:
        # MySQL 연결 시도
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        if conn.is_connected():
            conn.close()
            return {"db_status": "connected successfully"}
        else:
            return {"db_status": "connection failed"}
    except Exception as e:
        return {"db_status": f"connection error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)