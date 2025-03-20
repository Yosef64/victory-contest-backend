import cloudinary
import cloudinary.uploader
import os
CLOUD_NAME = os.getenv("CLOUD_NAME")
CLOUD_KEY = os.getenv("CLOUD_KEY")
CLOUD_SECRET = os.getenv("CLOUD_SECRET")

cloudinary.config(
    cloud_name=CLOUD_NAME,  
    api_key=CLOUD_KEY, 
    api_secret=CLOUD_SECRET, 
)

class Image:

    @staticmethod
    def upload_image(file,upload_options):
        print(upload_options,CLOUD_KEY)
        upload_response = cloudinary.uploader.upload(file=file, **upload_options)
        return upload_response
    @staticmethod
    def delete_image(public_id):
        delete_response = cloudinary.uploader.destroy(public_id)
        return delete_response
