# app/services/search_service.py
from app.db.firebase import db
from app.models.menu_item import MenuItem

class SearchService:
    @staticmethod
    def search_menu_items(query: str):
        # This would come from your frontend Sidentmenu.tsx
        menu_items = [
            MenuItem(id=0, title="Home", path="/dashboard"),
            MenuItem(id=1, title="Questions", path="/dashboard/questions"),
            MenuItem(id=2, title="Contests", path="/dashboard/contest"),
            MenuItem(id=3, title="Users", path="/dashboard/users"),
            MenuItem(id=6, title="Approve Admin", path="/dashboard/admins"),
            MenuItem(id=4, title="Add Contest", path="/dashboard/addcontest"),
            MenuItem(id=5, title="Add Question", path="/dashboard/addquestion"),
        ]
        return [item for item in menu_items if query.lower() in item.title.lower()]