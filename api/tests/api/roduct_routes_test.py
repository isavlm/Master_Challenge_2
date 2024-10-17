#following example from @Santiago220991 

from decimal import Decimal
from faker import Faker
from unittest.mock import MagicMock

from factories.use_cases.product import 
{delete_product_use_case, 
list_product_use_case, filter_product_use_case,
edit_product_use_case_product_use_case}
from app.src.core.models._product import Product, ProductStatuses


fake = Faker()

def test_get_products_endpoint_success(app, client, mock_session_manager):
    mock_response = MagicMock()
    products = [Product(
        product_id=fake.uuid4(),
        user_id=fake.uuid4(),
        name=fake.word(),
        description=fake.sentence(),
        price=Decimal(fake.pyint(min_value=0, max_value=9999, step=1)),
        location=fake.address(),
        status=fake.random_element(elements=(
            ProductStatuses.NEW, ProductStatuses.USED, ProductStatuses.FOR_PARTS)),
        is_available=fake.boolean()
        )]

    mock_response.products = products
    mock_use_case = MagicMock(return_value=mock_response)

    app.dependency_overrides[list_product_use_case] = mock_use_case lambda: mock_use_case #I still don't understand this line/Lambda

    """Python lambdas are little, anonymous functions, subject to a more restrictive but more concise syntax than regular Python functions."""
    

    
