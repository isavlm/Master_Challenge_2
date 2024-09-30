from typing import Optional
from app.src.exceptions import ProductRepositoryException, ProductNotFoundException

from app.src.core.models import Product
from app.src.repositories import ProductRepository

from .request import FilterProductsByStatusRequest
from .response import FilterProductsByStatusResponse


class FilterProductByStatus:

    def __init__(self, product_repository: ProductRepository) -> None:
        self.product_repository = product_repository

    def __verify_products_exist(self, products: Optional[Product], request_status: str) -> None:
        if not products:
            raise ProductNotFoundException(f"No products found with status: {request_status}")
        
    def __call__(self, request: FilterProductsByStatusRequest) -> FilterProductsByStatusResponse:
        try:
            existing_product = self.product_repository.filter_products(request.status)
            self.__verify_product_exists(
                existing_product, request_entity_status=request.product_status
            )
            response = FilterProductsByStatusResponse(**existing_product._asdict())
            return response
        except ProductRepositoryException as e:
            raise e