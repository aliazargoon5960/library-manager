import sys
from PyQt5.QtWidgets import QApplication
from User.login_view import LoginView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = LoginView()
    dlg.show()
    sys.exit(app.exec_())
