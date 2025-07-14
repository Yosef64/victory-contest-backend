import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file
load_dotenv() 

# Retrieve values from environment variables
CLOUD_NAME = os.getenv("CLOUD_NAME")
CLOUD_KEY = os.getenv("CLOUD_KEY")
CLOUD_SECRET = os.getenv("CLOUD_SECRET")

# Ensure these variables are set (optional, but good for debugging)
if not CLOUD_NAME or not CLOUD_KEY or not CLOUD_SECRET:
    raise ValueError("Cloudinary credentials are not set in environment variables.")

cloudinary.config(
    cloud_name=CLOUD_NAME,  
    api_key=CLOUD_KEY, 
    api_secret=CLOUD_SECRET, 
    secure=True,
)

class Image:
    @staticmethod
    def upload_image(file, upload_options):
        print(upload_options, CLOUD_KEY) # CLOUD_KEY will now come from .env
        try:
            if hasattr(file, "read") or hasattr(file, "file"):
                file_bytes = file.file.read() if hasattr(file, "file") else file.read()
                upload_response = cloudinary.uploader.upload(file=file_bytes, public_id=upload_options["public_id"])
            else:
                upload_response = cloudinary.uploader.upload(file=file, public_id=upload_options["public_id"])
            return upload_response
        except Exception as e:
            print(f"Error uploading to Cloudinary: {e}")
            raise e

    @staticmethod
    def delete_image(public_id):
        delete_response = cloudinary.uploader.destroy(public_id)
        return delete_response