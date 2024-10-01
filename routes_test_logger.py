# from logging_config import logger  # importing logger from logging_config.py

# from fastapi.testclient import TestClient
# from main import app  # Importing FastAPI app from the root of the project.

# client = TestClient(app)

# def test_get_product_by_id():
#     logger.info("Testing GET /products/{product_id}")
#     response = client.get("/products/00001")
#     if response.status_code == 200:
#         logger.info(f"GET /products/00001 succeeded: {response.json()}")
#     else:
#         logger.error(f"GET /products/00001 failed with status code {response.status_code}")

# def test_edit_product():
#     logger.info("Testing PUT /products/{product_id}")
#     data = {
#         "product_id": "00001",
#         "user_id": "01",
#         "name": "Updated Iphone",
#         "description": "Updated description",
#         "price": 400,
#         "location": "Sunnyvale, CA",
#         "status": "Used",
#         "is_available": True
#     }
#     response = client.put("/products/00001", json=data)
#     if response.status_code == 200:
#         logger.info(f"PUT /products/00001 succeeded: {response.json()}")
#     else:
#         logger.error(f"PUT /products/00001 failed with status code {response.status_code}, details: {response.json()}")

# def test_delete_product():
#     logger.info("Testing DELETE /products/{product_id}")
#     response = client.delete("/products/00001")
#     if response.status_code == 200:
#         logger.info("DELETE /products/00001 succeeded")
#     else:
#         logger.error(f"DELETE /products/00001 failed with status code {response.status_code}")

# if __name__ == "__main__":
#     test_get_product_by_id()
#     test_edit_product()
#     test_delete_product()
