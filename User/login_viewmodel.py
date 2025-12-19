from database.db_setup import SessionLocal
from .user_model import User


class LoginViewModel:
    def login(self, username, password):
        session = SessionLocal()

        user = session.query(User).filter(
            User.username == username,
            User.password == password
        ).first()

        session.close()

        if not user:
            return False, "اطلاعات ورود نادرست است", None

        return True, "ورود موفق", user
