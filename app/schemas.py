from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    fullName: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    fullName: str
    email: EmailStr
