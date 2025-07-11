from app.db.firebase import db
ADMIN_REF = db.collection("admin")

class AdminRepository:
    @staticmethod
    def sign_in(email,password):
        admin = ADMIN_REF.document(email).get()
        
        if not admin.exists:
            return None 

        admin_data = admin.to_dict() or {}
        hashed_password = admin_data["password"] 
        isApproved = admin_data["isApproved"]         
        if password != hashed_password or not isApproved:
            return {"isApproved":isApproved,"auth":password == hashed_password}  
        
        return {"email":admin_data["email"],"name":admin_data["name"]}
    @staticmethod
    def register_admin(data):
        ADMIN_REF.document(data["email"]).set({**data,"isApproved":False})
        return True
    @staticmethod
    def update_admin(data,email):
        ADMIN_REF.document(email).update(data)
        return 
    @staticmethod
    def get_admins():
        admins = [admin.to_dict() for admin in ADMIN_REF.stream()]
        return admins