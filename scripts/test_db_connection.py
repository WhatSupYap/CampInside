#!/usr/bin/env python3
"""
PostgreSQL 연결 테스트 스크립트
서버에서 데이터베이스 연결을 테스트합니다.
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv

def test_database_connection():
    """데이터베이스 연결 테스트"""
    
    # 환경 변수 로드
    load_dotenv()
    
    # 연결 정보
    db_config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'port': os.getenv('DB_PORT', 5432)
    }
    
    print("🔍 데이터베이스 연결 테스트 시작...")
    print(f"Host: {db_config['host']}")
    print(f"Database: {db_config['database']}")
    print(f"User: {db_config['user']}")
    print(f"Port: {db_config['port']}")
    print("-" * 50)
    
    try:
        # 데이터베이스 연결
        print("📡 연결 시도 중...")
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # PostgreSQL 버전 확인
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ 연결 성공!")
        print(f"PostgreSQL 버전: {version}")
        
        # 데이터베이스 정보 확인
        cursor.execute("SELECT current_database(), current_user, inet_server_addr(), inet_server_port();")
        db_info = cursor.fetchone()
        print(f"현재 데이터베이스: {db_info[0]}")
        print(f"현재 사용자: {db_info[1]}")
        print(f"서버 주소: {db_info[2]}")
        print(f"서버 포트: {db_info[3]}")
        
        # 테이블 목록 확인
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"\n📋 기존 테이블 ({len(tables)}개):")
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("\n📋 테이블 없음 (새 데이터베이스)")
        
        # 간단한 테스트 테이블 생성/삭제
        print(f"\n🧪 테스트 쿼리 실행...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS connection_test (
                id SERIAL PRIMARY KEY,
                test_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                message TEXT
            );
        """)
        
        cursor.execute("""
            INSERT INTO connection_test (message) 
            VALUES ('Connection test successful');
        """)
        
        cursor.execute("SELECT COUNT(*) FROM connection_test;")
        count = cursor.fetchone()[0]
        print(f"✅ 테스트 레코드 수: {count}")
        
        # 테스트 테이블 삭제
        cursor.execute("DROP TABLE connection_test;")
        print("🧹 테스트 테이블 정리 완료")
        
        # 연결 종료
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\n🎉 모든 테스트 통과!")
        return True
        
    except psycopg2.Error as e:
        print(f"❌ PostgreSQL 오류: {e}")
        return False
    except Exception as e:
        print(f"❌ 연결 오류: {e}")
        return False

def check_environment():
    """환경 변수 확인"""
    print("🔧 환경 변수 확인...")
    
    required_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # 비밀번호는 마스킹
            if 'PASSWORD' in var:
                print(f"  {var}: {'*' * len(value)}")
            else:
                print(f"  {var}: {value}")
        else:
            missing_vars.append(var)
            print(f"  {var}: ❌ 없음")
    
    if missing_vars:
        print(f"\n❌ 누락된 환경 변수: {', '.join(missing_vars)}")
        print("💡 .env 파일을 확인하거나 환경 변수를 설정하세요.")
        return False
    
    print("✅ 모든 환경 변수 확인됨")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("🐘 CampInside PostgreSQL 연결 테스트")
    print("=" * 60)
    
    # 환경 변수 확인
    if not check_environment():
        sys.exit(1)
    
    print()
    
    # 데이터베이스 연결 테스트
    if test_database_connection():
        print("\n🚀 데이터베이스 연결 준비 완료!")
        sys.exit(0)
    else:
        print("\n💥 데이터베이스 연결 실패")
        print("\n🔧 문제 해결 방법:")
        print("1. Lightsail 데이터베이스가 실행 중인지 확인")
        print("2. 네트워크 연결 확인")
        print("3. 데이터베이스 자격 증명 확인")
        print("4. 방화벽 설정 확인")
        sys.exit(1)
