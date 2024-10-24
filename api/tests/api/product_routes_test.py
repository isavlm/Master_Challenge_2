# following example from @Santiago220991 
import pytest
from decimal import Decimal
from faker import Faker
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from factories.use_cases.product import delete_product_use_case, list_product_use_case, filter_product_use_case, edit_product_use_case, get_products_use_case
from app.src.core.models._product import Product, ProductStatuses

fake = Faker()

# Test 1: Test for getting products successfully
def test_get_products_endpoint_success(api_client: TestClient, mock_session_manager: MagicMock):
    mock_response = MagicMock()
    expected_products = [{
        "product_id": str(fake.uuid4()),
        "name": fake.word(),
        "price": fake.pydecimal(left_digits=4, right_digits=2, positive=True)
    }]
    
    mock_response = expected_products
    mock_use_case = MagicMock(return_value=mock_response)

    # Overriding the product use case with mock
    api_client.app.dependency_overrides[get_products_use_case] = lambda: mock_use_case

    # Sending GET request
    response = api_client.get("/products")

    # Asserting the results
    assert response.status_code == 200
    assert mock_use_case.call_count == 1
    assert response.json() == expected_products
    mock_use_case.assert_called_once()

# Test 2: Test for filtering products
def test_filter_products_endpoint_success(api_client: TestClient, mock_session_manager: MagicMock):
    mock_response = MagicMock()
    expected_filtered_products = [{
        "product_id": str(fake.uuid4()),
        "status": "New",
        "name": fake.word()
    }]
    
    mock_response = expected_filtered_products
    mock_use_case = MagicMock(return_value=mock_response)

    api_client.app.dependency_overrides[filter_product_use_case] = lambda: mock_use_case

    filter_by = "New"
    response = api_client.get(f"/products?status={filter_by}")

    assert response.status_code == 200
    assert mock_use_case.call_count == 1
    assert response.json() == expected_filtered_products
    mock_use_case.assert_called_once_with(filter_by)

# Test 3: Test for editing a product
def test_edit_product_endpoint(api_client: TestClient, mock_session_manager: MagicMock):
    mock_response = MagicMock()
    product = {
        "product_id": str(fake.uuid4()),
        "name": fake.word(),
        "price": fake.pydecimal(left_digits=4, right_digits=2, positive=True),
        "status": "Used"
    }

    mock_use_case = MagicMock(return_value=product)
    api_client.app.dependency_overrides[edit_product_use_case] = lambda: mock_use_case

    request_body = {
        "name": product['name'],
        "price": str(product['price']),
        "status": product['status']
    }

    response = api_client.put(f"/products/{product['product_id']}", json=request_body)

    assert response.status_code == 200
    assert mock_use_case.call_count == 1
    assert response.json() == product
    mock_use_case.assert_called_once()

# Test 4: Test for deleting a product
def test_delete_product_endpoint_success(api_client: TestClient, mock_session_manager: MagicMock):
    product_id = str(fake.uuid4())
    mock_response = product_id
    mock_use_case = MagicMock(return_value=mock_response)

    api_client.app.dependency_overrides[delete_product_use_case] = lambda: mock_use_case

    response = api_client.delete(f"/products/{product_id}")

    assert response.status_code == 200
    expected_response = f"The product with id {product_id} was deleted."
    assert response.json() == expected_response
    mock_use_case.assert_called_once_with(product_id)

