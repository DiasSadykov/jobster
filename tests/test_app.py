from unittest.mock import MagicMock, Mock
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_index():
    response = client.get("/")
    assert response.status_code == 200
