from pydantic import BaseModel, EmailStr, constr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: constr(min_length=6)

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    text: constr(max_length=1024)

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
