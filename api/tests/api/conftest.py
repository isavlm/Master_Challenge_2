import pytest
from fastapi.testclient import TestClient

from api.src.create_app import create_app
from unittest.mock import MagicMock


@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def api_client(app) -> TestClient:
    client = TestClient(app)
    return client

@pytest.fixture
def mock_session_manager():
    mock_session_manager = MagicMock()
    mock_session_manager.get_session.return_value = MagicMock()
    return mock_session_manager

@pytest.fixture
def mock_product_repository():
    return MagicMock()