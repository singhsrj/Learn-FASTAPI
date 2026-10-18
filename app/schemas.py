# Here we define the type of data we want to accept from the request body
# so we define the data structures here we will be working with , those are called schemas , like we have them in a database

# Fastapi handles data validation , which means that if the user input anything other than specified data type , then it will raise a error by itself
from pydantic import BaseModel
from fastapi_users import schemas
import uuid
class PostCreate(BaseModel):
    title: str
    content: str

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass
