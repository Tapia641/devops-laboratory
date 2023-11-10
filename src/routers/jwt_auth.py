from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

# AUTH O2
# Usuario y pass: OAuth2PasswordBearer
# Criterios de authenticacion: OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta

# JWT
from jose import jwt, JWTError
from passlib.context import CryptContext

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1

# $ openssl rand -hex 32
SECRET = "a5fdbb3c8c6f613d17bffa286bb61efc595e0d8ec620ab57f36ce730c7732d4d"

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


# Authenticacion JWT
# pip install  "python-jose[cryptography]"
# pip install  passlib[bcrypt]

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
        "password": "$2a$12$nOQ8u8LeFnCHXD..zLiziuVV7Lron9B62yZYvEEvJZpvS4d6nt6y2"
    }, "carlitos": {
        "username": "carlitos",
        "name": "Carlos",
        "email": "carlitos@gmail.com",
        "disable": True,
        "password": "$2a$12$rPgMoy/MwBaacfx.YNGTBeKqaPMGT3ylnLnxoEKDIevdtKJR6ouF."
    }
}


def search_user(username: str):
    if username in fake_db.keys():
        return User(**fake_db[username])


def search_user_db(username: str):
    if username in fake_db.keys():
        return UserDB(**fake_db[username])


@router.post(path="/login")
async def auth_login(form: OAuth2PasswordRequestForm = Depends()):
    user_in_db = fake_db.get(form.username)
    if not user_in_db:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    user = search_user_db(username=form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="Password incorrecto")

    access_token_expiration = timedelta(minutes=ACCESS_TOKEN_DURATION)
    expire = datetime.utcnow() + access_token_expiration

    access_token = {"sub": user.username, "exp": expire}

    return {"acces_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


async def auth_user(token: str = Depends(oauth2)):
    try:
        username = jwt.decode(token, SECRET, ALGORITHM).get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales no validas",
                                headers={"WWW-Authenticate": "bearer"})
        else:
            return search_user(username)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales no validas",
                            headers={"WWW-Authenticate": "bearer"})


async def current_user(user: User = Depends(auth_user)):
    if user.disable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo",
                            headers={"WWW-Authenticate": "bearer"})
    return user


# DEPENDS para confirmar que siempre este logueado
@router.get(path="/users/me")
async def get_my_profile(user: User = Depends(current_user)):
    return user
