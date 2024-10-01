from typing import List, Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from app.src import Product, ProductRepository, ProductRepositoryException
from .tables import ProductSchema


class SQLProductRepository(ProductRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self) -> List[Product]:
        try:
            with self.session as session:
                products = session.query(ProductSchema).all()
                if products is None:
                    return []
                product_list = [
                    Product(
                        product_id=str(product.product_id),
                        user_id=str(product.user_id),
                        name=str(product.name),
                        description=str(product.description),
                        price=Decimal(product.price),
                        location=str(product.location),
                        status=str(product.status),
                        is_available=bool(product.is_available),
                    )
                    for product in products
                ]
                return product_list
        except Exception:
            self.session.rollback()
            raise ProductRepositoryException(method="list")

    def create(self, product: Product) -> Product:
        try:
            product_to_create = ProductSchema(
                product_id=product.product_id,
                user_id=product.user_id,
                name=product.name,
                description=product.description,
                price=product.price,
                location=product.location,
                status=product.status,
                is_available=product.is_available,
            )
            with self.session as session:
                session.add(product_to_create)
                session.commit()
            return product
        except Exception:
            self.session.rollback()
            raise ProductRepositoryException(method="create")

    def get_by_id(self, product_id: str) -> Optional[Product]:
        try:
            with self.session as session:
                product = (
                    session.query(ProductSchema)
                    .filter(ProductSchema.product_id == product_id)
                    .first()
                )
                if product is None:
                    return None
                return Product(
                    product_id=str(product.product_id),
                    user_id=str(product.user_id),
                    name=str(product.name),
                    description=str(product.description),
                    price=Decimal(product.price),
                    location=str(product.location),
                    status=str(product.status),
                    is_available=bool(product.is_available),
                )
        except Exception:
            self.session.rollback()
            raise ProductRepositoryException(method="find")

#Isadora's Code starts here


    def edit(self, product: Product) -> Product:
        
        try:
            with self.session as session:
                # Get the existing product from the database
                print(product, "This is the product")
                existing_product = session.query(ProductSchema).filter(
                    ProductSchema.product_id == product.product_id
                ).first()

                if existing_product is None:
                    raise ProductRepositoryException(method="edit", message="Product not found")
                
                # Print debugging information
                print(f"Existing product before update: {existing_product}")

                # Update the product information
                existing_product.user_id = product.user_id
                existing_product.name = product.name
                existing_product.description = product.description
                existing_product.price = product.price
                existing_product.location = product.location
                existing_product.status = product.status
                existing_product.is_available = product.is_available

                # Print debugging information after update
                print(f"Product after update: {existing_product}")

                # Commit the changes to the database
                session.commit()

            print("Product updated successfully")
            return product
        except Exception as e:
            # Print the exception to debug
            print(f"Exception occurred: {e}")
            self.session.rollback()
            raise ProductRepositoryException(method="edit") from e


    def delete(self, product_id: str) -> Product:
        try:
            with self.session as session:
                session.query(ProductSchema).filter(
                    ProductSchema.product_id == product_id).delete()
                session.commit()
            return product_id
        except Exception:
            self.session.rollback()
            raise ProductRepositoryException(method="delete")
        

    def get_by_status(self, status: str) -> Optional[Product]:
        try:
            with self.session as session:
                product = (
                    session.query(ProductSchema)
                    .filter(ProductSchema.status == status)
                    .all()      #changed first to all so that it returns all products with the status
                )
                if not product:
                    print(f"No products found with status: {status}")
                    return []
                return [
                    Product(
                        product_id=str(product.product_id),
                        user_id=str(product.user_id),
                        name=str(product.name),
                        description=str(product.description),
                        price=Decimal(product.price),
                        location=str(product.location),
                        status=str(product.status),
                        is_available=bool(product.is_available),
                    )
                    for product in product
                ]
        except Exception:
            self.session.rollback()
            raise ProductRepositoryException(method="find")