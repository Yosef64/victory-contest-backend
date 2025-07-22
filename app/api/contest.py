import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, Request, UploadFile, Form, File
from fastapi.responses import JSONResponse
from app.schemas.contest import ContestSchema, ContestUpdateSchema
from app.services.contest_service import ContestService
from app.services.telegram_service import TelegramBot

router = APIRouter()

def convert_to_24hour_format(time_str: str) -> str:
    """Convert time string to 24-hour format if needed"""
    try:
        # Try parsing as 12-hour format first (e.g., "03:30 PM")
        time_obj = datetime.strptime(time_str, "%I:%M %p")
        return time_obj.strftime("%H:%M")
    except ValueError:
        try:
            # Try parsing as 24-hour format (e.g., "15:30")
            datetime.strptime(time_str, "%H:%M")
            return time_str
        except ValueError:
            # Re-raise the error with a more specific message if neither format matches
            raise ValueError(f"Invalid time format: '{time_str}'. Expected 'HH:MM AM/PM' or 'HH:MM'.")

@router.get("/")
async def get_all_contests():
    try:
        contests = ContestService.get_all_contests()
        return JSONResponse({"contests": contests})
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)

@router.get("/{contest_id}")
async def get_contest_by_id(request: Request, contest_id: str):
    try:
        contest = ContestService.get_contest_by_id(contest_id)
        return JSONResponse({"contest": contest}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)

@router.post("/add")
async def add_contest(request: Request):
    data = await request.json()
    contest = data["contest"]
    try:
        contest_id = ContestService.add_contest(contest)
        return JSONResponse({"message": "success", "id": contest_id}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)

@router.put("/reschedule/{contest_id}")
async def reschedule_contest(request: Request, contest_id: str):
    # This endpoint seems to be a duplicate of PATCH for time updates.
    # It's better to use a single, more generic PATCH endpoint for updates.
    # The PATCH endpoint below is more robust.
    data = await request.json()
    try:
        # Convert time formats if needed
        if 'start_time' in data:
            data['start_time'] = convert_to_24hour_format(data['start_time'])
        if 'end_time' in data:
            data['end_time'] = convert_to_24hour_format(data['end_time'])

        ContestService.update_contest(contest_id, data)
        return JSONResponse({"message": "success"}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)

@router.patch("/{contest_id}")
async def update_contest(request: Request, contest_id: str):
    raw_data = await request.json()
    print(f"Received raw data for update for contest {contest_id}: {raw_data}") # Debugging line
    
    update_data = {}
    try:
        if 'start_time' in raw_data and raw_data['start_time'] is not None:
            if not isinstance(raw_data['start_time'], str) or not raw_data['start_time'].strip():
                raise HTTPException(status_code=400, detail="Invalid start_time format: must be a non-empty string.")
            try:
                update_data['start_time'] = convert_to_24hour_format(raw_data['start_time'])
            except ValueError as ve:
                raise HTTPException(status_code=400, detail=f"Failed to convert start_time: {ve}")

        if 'end_time' in raw_data and raw_data['end_time'] is not None:
            if not isinstance(raw_data['end_time'], str) or not raw_data['end_time'].strip():
                raise HTTPException(status_code=400, detail="Invalid end_time format: must be a non-empty string.")
            try:
                update_data['end_time'] = convert_to_24hour_format(raw_data['end_time'])
            except ValueError as ve:
                raise HTTPException(status_code=400, detail=f"Failed to convert end_time: {ve}")
        
        # Add other fields if they can be updated via this endpoint
        if 'title' in raw_data and raw_data['title'] is not None:
            update_data['title'] = raw_data['title']
        if 'description' in raw_data and raw_data['description'] is not None:
            update_data['description'] = raw_data['description']
        # ... and so on for any other fields you want to allow updating

        if not update_data:
            return JSONResponse({"message": "No valid fields provided for update."}, status_code=400)

        print(f"Data after time conversion and validation for contest {contest_id}: {update_data}") # Debugging line
        ContestService.update_contest(contest_id, update_data)
        return JSONResponse({"message": "success"}, status_code=200)
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"An unexpected error occurred during contest update for {contest_id}: {e}")
        return JSONResponse({"message": f"An internal server error occurred: {str(e)}"}, status_code=500)

@router.delete("/delete/{contest_id}")
async def delete_contest(contest_id: str):
    try:
        ContestService.delete_contest(contest_id)
        return JSONResponse({"message": "success"}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)

@router.post("/announce")
async def announce_contest(
    file: UploadFile = File(None), # Make file optional
    contest: str = Form(...),
    message: str = Form(...)
):
    contents = None
    if file:
        contents = await file.read()
    try:
        contest_data = json.loads(contest)
        # Add more specific error handling here for TelegramBot
        try:
            # Assuming TelegramBot.send_message_to_all can handle None for contents if file is optional
            TelegramBot.send_message_to_all(contest_data, message, contents)
            return JSONResponse({"message": "success"}, status_code=200)
        except Exception as telegram_e:
            # Log the specific error from TelegramBot to help diagnose
            print(f"Error sending Telegram message: {telegram_e}")
            return JSONResponse({"message": f"Failed to send Telegram announcement: {str(telegram_e)}"}, status_code=500)
    except json.JSONDecodeError as json_e:
        print(f"Error decoding contest JSON: {json_e}")
        return JSONResponse({"message": f"Invalid contest data format: {str(json_e)}"}, status_code=400)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return JSONResponse({"message": str(e)}, status_code=500)

@router.post("/register")
async def register_contest(request: Request):
    data = await request.json()
    contest_id, student_id = data["contest_id"], data["tele_id"]
    try:
        ContestService.register_user_for_Contest(contest_id, student_id)
        return JSONResponse({"message":"success"},status_code=200)
    except Exception as e:
        return JSONResponse({"message":str(e)},status_code=500)
@router.get("/participants/{contest_id}")
async def get_participants(contest_id: str):
    try:
        participants = ContestService.get_number_of_participants(contest_id)
        return JSONResponse({"participants": participants}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)

@router.get("/active/{contest_id}")
async def get_active_contestants(request: Request, contest_id: str):
    try:
        active_contestants = ContestService.get_active_contestants(contest_id)
        return JSONResponse({"active_contestants": active_contestants}, status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)



@router.get("/is_registered/{contest_id}/{student_id}")
async def is_user_registered(contest_id: str, student_id: str):
    try:
        registered = ContestService.is_user_registered(contest_id, student_id)
        return JSONResponse({"registered": registered}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)

@router.get("/is_active/{contest_id}/{student_id}")
async def is_user_active(contest_id: str, student_id: str):
    try:
        active = ContestService.activate_user(contest_id, student_id)
        return JSONResponse({"active": active}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)


