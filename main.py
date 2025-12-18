import sys
from PyQt5.QtWidgets import QApplication
from Book.main_view import LibraryMainView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryMainView()
    window.show()
    sys.exit(app.exec_())