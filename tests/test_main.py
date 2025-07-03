import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello FastAPI!"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"

def test_db_status():
    # DB 연결이 실패할 수 있으므로 200 또는 에러 모두 허용
    response = client.get("/db-status")
    assert response.status_code == 200
    assert "db_status" in response.json()
