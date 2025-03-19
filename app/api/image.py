
from fastapi import APIRouter, HTTPException, Request,UploadFile,File,Form
from fastapi.responses import JSONResponse
from app.schemas.contest import ContestSchema, ContestUpdateSchema
from app.services.contest_service import ContestService
from app.services.telegram_service import TelegramBot
from app.repositories.image_repo import Image
router = APIRouter()

@router.post("/upload")
async def upload_image(file:UploadFile=File(...), public_id:str=Form(None)):
    
    contents = await file.read()
    upload_options = {"public_id": public_id} if public_id else {}
    try:
        upload_response = Image.upload_image(contents, upload_options )
        print(upload_options)
        return JSONResponse({"message":upload_response},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)
@router.post("/delete")
async def delete_image(request:Request):
    data = await request.json()
    public_id = data["public_id"]
    try:
        delete_response = Image.delete_image(public_id)
        return JSONResponse({"message":delete_response},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)



