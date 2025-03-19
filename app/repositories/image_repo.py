import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="dud4t1ptn",  
    api_key="782296869627567", 
    api_secret="yQkh1vfEsaktbElrk5h1H7Ky2ug", 
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
