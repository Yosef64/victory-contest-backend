import os
import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse
from fastapi import Response
from app.repositories.amin_repo import AdminRepository
from typing import Optional
router = APIRouter()

SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
secure_cookie = os.getenv("ENV", "dev") == "production"
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@router.post("/login")
async def login_admin(request:Request):
    data = await request.json()
    password,email = data["password"],data["email"]
    try:
        res = AdminRepository.sign_in(password=password,email=email)
        if res and res.get("email"):
            # Only issue token if login is successful
            access_token = create_access_token({"sub": res["email"], "name": res["name"]})
            response = JSONResponse({"message":res}, status_code=200)
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,  # ✅ false in dev, true in prod
                samesite=None,
                max_age=60 * 60,
                path="/"
            )
            return response
        return JSONResponse({"message":res},status_code=200)
    except Exception as e:
        return JSONResponse({"message":str(e)},status_code=500)

@router.get("/logout")
async def logout_admin():
    response = JSONResponse({"message": "Logged out successfully"})
    response.delete_cookie("access_token", path="/")
    return response
@router.post("/register")
async def register_admin(request:Request):
    data = await request.json()
    data = data["data"]
    try:
        AdminRepository.register_admin(data=data)
        return JSONResponse({"message":"success"},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)
@router.put("/{email}")
async def update_admin(request:Request,email:str):
    data = await request.json()
    admin = data["data"]
    try:
        AdminRepository.update_admin(admin,email=email)
        return JSONResponse({"message":"success"},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)
@router.get("/")
async def get_admins(request:Request):
    try:
        admins = AdminRepository.get_admins()
        return JSONResponse({"admins":admins},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)

# Example protected route
@router.get("/me")
async def get_me(access_token: Optional[str] = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        print(access_token)
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        return {"user": payload}
    except jwt.ExpiredSignatureError as e:
        return JSONResponse({"message":str(e)},status_code=401)
    except jwt.InvalidTokenError as e:
        return JSONResponse({"message":str(e)},status_code=40)
    except Exception as e:
        return JSONResponse({"message":"Internal server error"},status_code=500)