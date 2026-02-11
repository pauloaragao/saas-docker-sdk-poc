"""
Example test file
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestRoot:
    """Root endpoint tests"""
    
    def test_root(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "API is running"


class TestHealth:
    """Health check tests"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
