from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt
from ui.login_ui import Ui_Dialog  # فایل طراحی Login
from User.user_view_model import UserViewModel
from Book.main_view import LibraryMainView


class LoginView(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # ViewModel
        self.vm = UserViewModel()

        # اتصال دکمه‌ها
        self.btn_login.clicked.connect(self.handle_login)

        # تنظیمات
        self.txt_password.setEchoMode(self.txt_password.Password)
        self.setWindowTitle("صفحه ورود")

    def handle_login(self):
        username = self.txt_username.text().strip()
        password = self.txt_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "خطا", "لطفاً نام کاربری و رمز عبور را وارد کنید.")
            return

        user, error = self.vm.authenticate(username, password)

        if error:
            QMessageBox.warning(self, "خطا", error)
            return

        # ورود موفق
        QMessageBox.information(self, "خوش آمدید", f"به کتابخانه خوش آمدید، {user.username}!")

        # باز کردن صفحه اصلی کتابخانه
        self.library_window = LibraryMainView(current_user=user)
        self.library_window.setModal(True)
        self.library_window.exec_()

        # بعد از بستن LibraryMainView، می‌توان Login را بست
        self.close()
