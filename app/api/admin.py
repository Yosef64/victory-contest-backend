from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse
from app.repositories.amin_repo import AdminRepository
router = APIRouter()

@router.post("/login")
async def login_admin(request:Request):
    data = await request.json()
    password,email = data["password"],data["email"]
    try:
        res = AdminRepository.sign_in(password=password,email=email)
        return JSONResponse({"message":res},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)

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