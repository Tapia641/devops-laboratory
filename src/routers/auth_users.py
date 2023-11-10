from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

# AUTH O2
# Usuario y pass: OAuth2PasswordBearer
# Criterios de authenticacion: OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    username: str
    name: str
    email: str
    disable: bool


class UserDB(User):
    password: str


fake_db = {
    "tapia": {
        "username": "tapia",
        "name": "Luis",
        "email": "tapia@gmail.com",
        "disable": False,
        "password": "123456"
    }, "carlitos": {
        "username": "carlitos",
        "name": "Carlos",
        "email": "carlitos@gmail.com",
        "disable": True,
        "password": "654321"
    }
}


def search_user(username: str):
    if username in fake_db.keys():
        return User(**fake_db[username])


def search_user_DB(username: str):
    if username in fake_db.keys():
        return UserDB(**fake_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no logueado",
                            headers={"WWW-Authenticate": "bearer"})
    if user.disable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo",
                            headers={"WWW-Authenticate": "bearer"})
    return user


@router.post(path="/login")
async def auth_login(form: OAuth2PasswordRequestForm = Depends()):
    user_in_db = fake_db.get(form.username)
    if not user_in_db:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    user = search_user_DB(username=form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="Password incorrecto")

    return {"acces_token": user.username, "token_type": "bearer"}


# DEPENDS para confirmar que siempre este logueado
@router.get(path="/users/me")
async def get_my_profile(user: User = Depends(current_user)):
    return user
