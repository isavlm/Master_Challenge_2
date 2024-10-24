import pytest
from unittest.mock import patch, MagicMock

from app.src.exceptions import ProductRepositoryException
from app.src.use_cases.product import FilterProductByStatus, FilterProductsByStatusResponse, EditProduct, EditProductResponse
from app.src.use_cases.product.delete.request import DeleteProductRequest
from app.src.use_cases.product.delete.response import DeleteProductResponse
from app.src.use_cases.product.delete.use_case import DeleteProduct


def test_filter_products_success(mock_product_repository, fake_product_list):
    filter_by = "New"
    expected_filtered_products = fake_product_list
    mock_product_repository.filter.return_value = expected_filtered_products

    filter_product = FilterProductByStatus(product_repository=mock_product_repository)

    response = filter_product(filter_by)

    mock_product_repository.filter.assert_called_once_with(filter_by)
    assert response == FilterProductsByStatusResponse(products=expected_filtered_products)


def test_filter_products_repository_exception(mocker, mock_product_repository):
    filter_by = "Used"
    mock_product_repository.filter.side_effect = ProductRepositoryException("filtering")

    filter_product = FilterProductByStatus(product_repository=mock_product_repository)

    with pytest.raises(ProductRepositoryException) as exc_info:
        filter_product(filter_by)
    assert str(exc_info.value) == "Exception while executing filtering in Product"


def test_edit_products_success(mock_product_repository, fake_product):
    expected_product = fake_product
    mock_product_repository.edit.return_value = expected_product

    edit_product = EditProduct(product_repository=mock_product_repository)

    response = edit_product(expected_product.product_id, expected_product)

    mock_product_repository.edit.assert_called_once_with(
        expected_product.product_id, expected_product
    )
    assert response == EditProductResponse(user_id=expected_product.user_id,
                                           product_id=expected_product.product_id,
                                           name=expected_product.name,
                                           description=expected_product.description,
                                           price=expected_product.price,
                                           location=expected_product.location,
                                           status=expected_product.status,
                                           is_available=expected_product.is_available)


def test_delete_product_success(mock_product_repository, fake_product):
    expected_response = fake_product.product_id
    mock_product_repository.delete.return_value = expected_response

    delete_product = DeleteProduct(product_repository=mock_product_repository)
    request = DeleteProductRequest(product_id=expected_response)
    response = delete_product(request)

    mock_product_repository.delete.assert_called_once_with(expected_response)
    assert response == expected_response
