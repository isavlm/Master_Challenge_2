#following example from @Santiago220991 

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock 
from api.src import create_app 

@pytest.fixture(scope="module")
def app():
    return create_app() 


@pytest.fixture(scope="module")
def client(app):
    return TestClient(app)  #Simulates requests to the FastApi without using the server.


@pytest.fixture(scope="module")
def mock_session_manager():
    mock_session_manager = MagicMock() #Creates a mock/fake object to simulate Session Manager - this checks the db connections or activity.

    mock_session_manager.get_session.return_value = MagicMock()
    return mock_session_manager


"""app fixture: Creates a FastAPI app instance for testing.
client fixture: Creates a test client for making simulated HTTP requests to the app.
mock_session_manager fixture: Mocks a session manager, often used to mock database interactions during testing."""

#Fixture: reusable piece of code that helps set up specific environment or state before tests are run.

