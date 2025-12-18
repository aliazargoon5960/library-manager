import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt 
from Book.main_view import LibraryMainView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    

    app.setLayoutDirection(Qt.RightToLeft) 
    
    window = LibraryMainView()
    window.show()
    sys.exit(app.exec_())