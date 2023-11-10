from fastapi import APIRouter, HTTPException, status

from src.db.models.user import User
from src.db.schemas.user import user_schema, users_schema_list
# DB
from src.db.client import db_client

# Object ID
from bson import ObjectId


# ROUTER /API/V1/USERS
router = APIRouter(prefix="/api/v1/users", tags=["users"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})


# ADD USERS
@router.post(path="/", status_code=status.HTTP_200_OK, response_model=User)
async def add_users(user: User):
    if type(search_user_by_field("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user exists.")

    # Estructura de la BD
    db = db_client.test.employees

    # MONGO ACEPTA JSON
    user_dict = dict(user)

    # PARA HACER EL ID AUTOMATICO
    del user_dict["id"]

    # INSERTAMOS
    id = db.insert_one(user_dict).inserted_id

    # BUSCAMOS
    new_user = user_schema(db.find_one({"_id": id}))

    # CONVERTIMOS NUEVAMENTE A LA CLASE
    return User(**new_user)


def search_user_by_field(field: str, key):
    try:
        db = db_client.test.employees
        user_found = user_schema(db.find_one({field: key}))
        return User(**user_found)
    except:
        return {"error": "No se ha encontrado el usuario"}


@router.get(path="/", response_model=list[User], status_code=status.HTTP_200_OK)
async def get_users():
    db = db_client.test.employees
    users = users_schema_list(db.find())
    return users


@router.get(path="/{id}")
async def get_user(id: str):
    return search_user_by_field("_id", ObjectId(id))


@router.put("/")
async def update_user(user: User):
    user_dict = dict(user)
    del user_dict["id"]
    try:
        db = db_client.test.employees
        user_updated = db.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "User updated"}
    return search_user_by_field("_id", ObjectId(user.id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    db = db_client.test.employees
    user_found = db.find_one_and_delete({"_id": ObjectId(id)})
    if not user_found:
        return {"error": "No se pudo eliminar el usuario"}


# Status code
"""
100 information
200 successful
300 redirection
400 Client error
500 Server error
"""
