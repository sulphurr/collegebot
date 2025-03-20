# tests/test_api_endpoints.py
from fastapi.testclient import TestClient
from your_app.app import app
from your_app.db import get_db_connection
from unittest.mock import patch, Mock

@pytest.fixture
def client():
    """Create FastAPI test client"""
    return TestClient(app)

@pytest.fixture
def mock_db_connection():
    """Mock database connection"""
    with patch('your_app.db.get_db_connection') as mock_conn:
        yield mock_conn

def test_query_endpoint(client, mock_db_connection):
    """Test main query endpoint"""
    response = client.get("/query", params={"query": "room S101"})
    assert response.status_code == 200
    
    # Test error handling
    response_error = client.get("/query", params={"query": ""})
    assert response_error.status_code == 400

def test_small_talk_handling(client, mock_db_connection):
    """Test small talk categorization"""
    response = client.get("/query", params={"query": "hello how are you"})
    assert response.status_code == 200
    assert "I'm here to help!" in response.text

@patch('your_app.app.categorize_query')
def test_category_routing(mock_categorize, client, mock_db_connection):
    """Test query routing based on category"""
    mock_categorize.return_value = "small_talk"
    response = client.get("/query", params={"query": "hello"})
    assert response.status_code == 200
    
    mock_categorize.assert_called_once_with("hello")