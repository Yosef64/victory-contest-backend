import cloudinary
import cloudinary.uploader
import os
CLOUD_NAME="dud4t1ptn"
CLOUD_KEY="782296869627567"
CLOUD_SECRET="yQkh1vfEsaktbElrk5h1H7Ky2ug"

cloudinary.config(
    cloud_name=CLOUD_NAME,  
    api_key=CLOUD_KEY, 
    api_secret=CLOUD_SECRET, 
    secure=True,
)

class Image:

    @staticmethod
    def upload_image(file, upload_options):
        print(upload_options, CLOUD_KEY)
        try:
            # Handle UploadFile objects by reading the file bytes
            if hasattr(file, "read") or hasattr(file, "file"):
                file_bytes = file.file.read() if hasattr(file, "file") else file.read()
                upload_response = cloudinary.uploader.upload(file=file_bytes, public_id=upload_options["public_id"])
            else:
                # Handle regular file objects
                upload_response = cloudinary.uploader.upload(file=file, public_id=upload_options["public_id"])
            return upload_response
        except Exception as e:
            print(f"Error uploading to Cloudinary: {e}")
            raise e
    
    @staticmethod
    def delete_image(public_id):
        delete_response = cloudinary.uploader.destroy(public_id)
        return delete_response
