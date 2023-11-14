from fastapi import FastAPI
from mangum import Mangum
# import the classes
from src.routers import users_db

# INICIAR API
# UPDATING
app = FastAPI()

# ROUTERS
# app.include_router(products.router)
# app.include_router(users.router)
# app.include_router(jwt_auth.router)
# app.include_router(auth_users.router)
app.include_router(users_db.router)


@app.get("/")
async def check_status():
    return {"message": "Hello, I am alive"}


handler = Mangum(app=app)

# RECURSOS STATICOS
# app.mount(path="/static/", name="static", app=StaticFiles(directory="static"))

# def initialize_routers():
#     # Routers
#
# uvicorn main:app --reload
# uvicorn src.main:app --reload

# if __name__ == '__main__':
#     initialize_routers()
