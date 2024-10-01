from fastapi import APIRouter, Depends, HTTPException

from app.src.use_cases import (
    ListProducts,
    ListProductResponse,
    FindProductById,
    FindProductByIdResponse,
    FindProductByIdRequest,
    CreateProduct,
    CreateProductResponse,
    CreateProductRequest,
    DeleteProductResponse,
    DeleteProductRequest,
    DeleteProduct,
    EditProduct,
    EditProductResponse,
    EditProductRequest,
    FilterProductByStatus,
    FilterProductsByStatusResponse,
    FilterProductsByStatusRequest
)
from ..dtos import (
    ProductBase,
    ListProductResponseDto,
    CreateProductRequestDto,
    CreateProductResponseDto,
    FindProductByIdResponseDto,
    EditProductResponseDto,
    EditProductRequestDto,
)
from factories.use_cases import (
    list_product_use_case,
    find_product_by_id_use_case,
    create_product_use_case,
    delete_product_use_case,
    edit_product_use_case,
    filter_product_use_case,
)

product_router = APIRouter(prefix="/products")


@product_router.get("/", response_model=ListProductResponseDto)
async def get_products(
    use_case: ListProducts = Depends(list_product_use_case),
) -> ListProductResponse:
    response_list = use_case()
    response = [
        {**product._asdict(), "status": str(product.status.value)}
        for product in response_list.products
    ]
    response_dto: ListProductResponseDto = ListProductResponseDto(
        products=[ProductBase(**product) for product in response]
    )
    return response_dto


@product_router.get("/{product_id}", response_model=FindProductByIdResponseDto)
async def get_product_by_id(
    product_id: str, use_case: FindProductById = Depends(find_product_by_id_use_case)
) -> FindProductByIdResponse:
    response = use_case(FindProductByIdRequest(product_id=product_id))
    response_dto: FindProductByIdResponseDto = FindProductByIdResponseDto(
        **response._asdict()
    )
    return response_dto


@product_router.post("/", response_model=CreateProductResponseDto | str)
async def create_product(
    request: CreateProductRequestDto,
    use_case: CreateProduct = Depends(create_product_use_case),
) -> CreateProductResponse:
    if request.status not in ["New", "Used", "For parts"]:
        return "Not a valid status value (New, Used, For parts)"
    response = use_case(
        CreateProductRequest(
            product_id=request.product_id,
            user_id=request.user_id,
            name=request.name,
            description=request.description,
            price=request.price,
            location=request.location,
            status=request.status,
            is_available=request.is_available,
        )
    )
    response_dto: CreateProductResponseDto = CreateProductResponseDto(
        **response._asdict()
    )
    return response_dto


# Isadora's code starts here.

#ROUTE TO DELETE
@product_router.delete("/{product_id}", response_model=DeleteProductResponse)
async def delete_product(
    product_id: str, use_case: DeleteProduct = Depends(delete_product_use_case)
) -> DeleteProductResponse:
    response = use_case(DeleteProductRequest(product_id=product_id))
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="Product not found")


#Route to EDIT
@product_router.put("/{product_id}", response_model=EditProductResponseDto)
async def edit_product(
    product_id: str, 
    request: EditProductRequestDto,
    use_case: EditProduct = Depends(edit_product_use_case),    
) -> EditProductResponseDto:
    # Convert the DTO to the request model expected by the use case
    edit_request = EditProductRequest(
        product_id=request.product_id,
        user_id=request.user_id,
        name=request.name,
        description=request.description,
        price=request.price,
        location=request.location,
        status=request.status,
        is_available=request.is_available,
    )
    
    # Call the use case
    response = use_case(product_id, edit_request)
    
    if response:
        # Convert the response to EditProductResponseDto
        return EditProductResponseDto(
            product_id=response.product_id,
            user_id=response.user_id,
            name=response.name,
            description=response.description,
            price=response.price,
            location=response.location,
            status=response.status,
            is_available=response.is_available
        )
    else:
        raise HTTPException(status_code=404, detail="Product not found")


# Adding a logger to check my code. 