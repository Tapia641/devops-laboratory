from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/products", responses={404: {"message": "Not found"}}, tags=["products"])

products_list = ["Producto1", "Producto1", "Producto1", "Producto1", "Producto1"]


@router.get(path="/list", status_code=200)
async def get_products():
    return products_list


@router.get(path="/list/{id}", status_code=200)
async def get_product(id: int):
    return products_list[id]
