import unittest
from unittest.mock import MagicMock
from app.src.use_cases.product.delete.delete import DeleteProduct
from app.src.use_cases.product.delete.request import DeleteProductRequest
from app.src.core.models import Product
from app.src.exceptions import ProductNotFoundException

class TestDeleteProduct(unittest.TestCase):
    def test_delete_existing_product(self):
        # Arrange
        product_repository = MagicMock()
        product_repository.get_by_id.return_value = Product(id="123")
        delete_product = DeleteProduct(product_repository)
        request = DeleteProductRequest(product_id="123")

        # Act
        response = delete_product(request)

        # Assert
        product_repository.delete.assert_called_once_with("123")
        self.assertTrue(response.success)
        self.assertEqual(response.message, "Product deleted successfully")

    def test_delete_non_existent_product(self):
        # Arrange
        product_repository = MagicMock()
        product_repository.get_by_id.return_value = None
        delete_product = DeleteProduct(product_repository)
        request = DeleteProductRequest(product_id="123")

        # Act & Assert
        with self.assertRaises(ProductNotFoundException):
            delete_product(request)

if __name__ == '__main__':
    unittest.main()