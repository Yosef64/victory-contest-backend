
from datetime import datetime, timedelta


class DateService:
    @staticmethod
    def get_week_range():
        now = datetime.utcnow()  # Get current UTC time
        start_of_week = now - timedelta(days=now.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

        end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)

        return start_of_week, end_of_week
    @staticmethod
    def get_today_range():
        now = datetime.utcnow()

        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

        end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        return start_of_day, end_of_day
    @staticmethod
    def get_month_range():
        now = datetime.utcnow()

        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        next_month = start_of_month.replace(month=start_of_month.month % 12 + 1, day=1) 
        end_of_month = next_month - timedelta(seconds=1)  

        return start_of_month, end_of_month