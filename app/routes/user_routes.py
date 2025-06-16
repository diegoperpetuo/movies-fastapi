from fastapi import APIRouter, HTTPException
from app.schemas import UserCreate, UserLogin, UserOut
from app.database import db
from app.models import user_helper
from app.auth import hash_password, verify_password, create_access_token
from bson import ObjectId
from jose import jwt, JWTError
import os

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    if await db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    result = await db.users.insert_one(user_dict)
    new_user = await db.users.find_one({"_id": result.inserted_id})
    return user_helper(new_user)

@router.post("/login")
async def login(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"user_id": str(db_user["_id"])})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def get_me(token: str):
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=[os.getenv("JWT_ALGORITHM")])
        user_id = payload.get("user_id")
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        return user_helper(user)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
