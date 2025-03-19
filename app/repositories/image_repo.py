import cloudinary
import cloudinary.uploader
CLOUD_NAME = "dud4t1ptn"
CLOUD_KEY = "782296869627567"
CLOUD_SECRET = "yQkh1vfEsaktbElrk5h1H7Ky2ug"
cloudinary.config(
    cloud_name=CLOUD_NAME,  
    api_key=CLOUD_KEY, 
    api_secret=CLOUD_SECRET, 
)

class Image:

    @staticmethod
    def upload_image(file,upload_options):
        upload_response = cloudinary.uploader.upload(file=file, **upload_options)
        return upload_response
    @staticmethod
    def delete_image(public_id):
        delete_response = cloudinary.uploader.destroy(public_id)
        return delete_response
