# Press Shift+F10 to execute it or replace it with your code.
from fastapi import APIRouter, HTTPException

# BaseModel: Modelar un objeto
from pydantic import BaseModel


# Entity user
class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    age: int
    email: str
    salary: str


users_fake_db = [
    User(id=1, first_name="Calros", last_name="Hernandez", age=27, email="carlos@gmail.com", salary="90000"),
    User(id=2, first_name="Mario", last_name="Garcia", age=27, email="mario@gmail.com", salary="77888"),
    User(id=3, first_name="Joshua", last_name="Jimenez", age=27, email="joshua@gmail.com", salary="80000")
]

router = APIRouter(prefix="/api/v1/users")



# Start the server: uvicorn users:app --reload
@router.get("/list/{id}")
async def user(id: int):
    users = filter(lambda user: user.id == id, users_fake_db)
    print(users)
    try:
        return list(users)[0]
    except:
        return {'error': 'No se ha encontrado el usuario'}
    # return User(id=4, first_name="Calros", last_name="Hernandez", age=27, email="carlos@gmail.com", salary="90000")


@router.get("/query")
async def user(id: int):
    users = filter(lambda user: user.id == id, users_fake_db)
    print(users)
    try:
        return list(users)[0]
    except:
        return {'error': 'No se ha encontrado el usuario'}


@router.post(path="/add/", status_code=201, response_model=User)
async def add_user(user: User):
    # try:
    if user not in users_fake_db:
        users_fake_db.append(user)
        return user
    else:
        raise HTTPException(status_code=204, detail="Usuario existente")
    # except:
    #     return {"error": "No se pudo agregar el usuario"}


@router.put("/modify/")
async def modify_user(user: User):
    try:
        # if user in users_fake_db:
        for index, saved_user in enumerate(users_fake_db):
            # print(saved_user.id, user.id)
            if saved_user.id == user.id:
                users_fake_db[index] = user
                return {"message": "El usuario fue modificado con exito"}
            # else:
            #     return {"error": "Usuario no existente"}
    except:
        return {"error": "No se pudo agregar el usuario"}


@router.delete("/delete/{id}")
async def delete_user(id: int):
    try:
        # if user in users_fake_db:
        for index, saved_user in enumerate(users_fake_db):
            # print(saved_user.id, user.id)
            if saved_user.id == id:
                del users_fake_db[index]
                # users_fake_db.remove(id)
                return {"message": "El usuario fue eliminado con exito"}
            # else:
            #     return {"error": "Usuario no existente"}
    except:
        return {"error": "No se pudo eliminar el usuario"}


# Status code
"""
100 information
200 successful
300 redirection
400 Client error
500 Server error
"""
