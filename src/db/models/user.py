from pydantic import BaseModel


class User(BaseModel):
    id: str = None
    username: str
    name: str
    last_name: str
    email: str
    department: str
    salary: int
