from fastapi import FastAPI

# import the classes
from src.routers import users_db

# INICIAR API
app = FastAPI()

# ROUTERS
# app.include_router(products.router)
# app.include_router(users.router)
# app.include_router(jwt_auth.router)
# app.include_router(auth_users.router)
app.include_router(users_db.router)

# RECURSOS STATICOS
# app.mount(path="/static/", name="static", app=StaticFiles(directory="static"))

# def initialize_routers():
#     # Routers
#
#
# uvicorn main:app --reload
# uvicorn src.main:app --reload

# if __name__ == '__main__':
#     initialize_routers()
