from database.db_setup import SessionLocal
from .user_model import User

class UserViewModel:
    def __init__(self):
        self.db = SessionLocal()

    def authenticate(self, username: str, password: str):
        """
        بررسی نام کاربری و رمز عبور و برگرداندن شیء User
        """
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            return None, "کاربر پیدا نشد"
        if user.password != password:
            return None, "رمز عبور اشتباه است"
        return user, None
