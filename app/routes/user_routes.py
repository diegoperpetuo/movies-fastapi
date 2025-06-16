from fastapi import APIRouter, HTTPException
from app.schemas import UserCreate, UserLogin, UserOut
from app.database import db
from app.models import user_helper
from app.auth import hash_password, verify_password, create_access_token
from bson import ObjectId
from jose import jwt, JWTError
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    try:
        logger.info(f"Tentando registrar usuário: {user.email}")
        
        if await db.users.find_one({"email": user.email}):
            logger.warning(f"Email já registrado: {user.email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        if not user.name or len(user.name.strip()) == 0:
            logger.warning("Nome não fornecido")
            raise HTTPException(status_code=422, detail="Name is required")
        
        if not user.email or len(user.email.strip()) == 0:
            logger.warning("Email não fornecido")
            raise HTTPException(status_code=422, detail="Email is required")
        
        if not user.password or len(user.password) < 6:
            logger.warning("Senha inválida")
            raise HTTPException(status_code=422, detail="Password must be at least 6 characters")
        
        user_dict = user.dict()
        user_dict["password"] = hash_password(user.password)
        
        logger.info("Inserindo usuário no banco de dados")
        result = await db.users.insert_one(user_dict)
        logger.info(f"Usuário inserido com ID: {result.inserted_id}")
        
        new_user = await db.users.find_one({"_id": result.inserted_id})
        logger.info("Usuário registrado com sucesso")
        return user_helper(new_user)
    except Exception as e:
        logger.error(f"Erro ao registrar usuário: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

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
