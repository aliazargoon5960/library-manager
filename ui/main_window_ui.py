# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(743, 600)

        # گروه اضافه کردن کتاب
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(50, 10, 661, 111))
        self.groupBox.setObjectName("groupBox")

        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")

        self.txt_isbn = QtWidgets.QLineEdit(self.groupBox)
        self.txt_isbn.setObjectName("txt_isbn")
        self.gridLayout.addWidget(self.txt_isbn, 0, 0, 1, 1)

        self.txt_author = QtWidgets.QLineEdit(self.groupBox)
        self.txt_author.setObjectName("txt_author")
        self.gridLayout.addWidget(self.txt_author, 0, 2, 1, 1)

        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)

        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 3, 1, 1)

        self.txt_title = QtWidgets.QLineEdit(self.groupBox)
        self.txt_title.setObjectName("txt_title")
        self.gridLayout.addWidget(self.txt_title, 0, 4, 1, 1)

        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 5, 1, 1)

        self.lbl_author_error = QtWidgets.QLabel(self.groupBox)
        self.lbl_author_error.setText("")
        self.lbl_author_error.setObjectName("lbl_author_error")
        self.gridLayout.addWidget(self.lbl_author_error, 1, 2, 1, 1)

        self.lbl_title_error = QtWidgets.QLabel(self.groupBox)
        self.lbl_title_error.setText("")
        self.lbl_title_error.setObjectName("lbl_title_error")
        self.gridLayout.addWidget(self.lbl_title_error, 1, 4, 1, 1)

        self.lbl_isbn_error = QtWidgets.QLabel(self.groupBox)
        self.lbl_isbn_error.setText("")
        self.lbl_isbn_error.setObjectName("lbl_isbn_error")
        self.gridLayout.addWidget(self.lbl_isbn_error, 1, 0, 1, 1)

        self.btn_add = QtWidgets.QPushButton(self.groupBox)
        self.btn_add.setObjectName("btn_add")
        self.gridLayout.addWidget(self.btn_add, 2, 1, 1, 3)

        # جدول کتاب‌ها و دکمه‌ها
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 160, 681, 401))
        self.layoutWidget.setObjectName("layoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.table_books = QtWidgets.QTableView(self.layoutWidget)
        self.table_books.setObjectName("table_books")
        self.verticalLayout.addWidget(self.table_books)

        self.btn_delete = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_delete.setObjectName("btn_delete")
        self.verticalLayout.addWidget(self.btn_delete)

        # دکمه جدید برای کتاب‌های قرضی
        self.btn_borrowed_books = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_borrowed_books.setObjectName("btn_borrowed_books")
        self.verticalLayout.addWidget(self.btn_borrowed_books)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "کتابخانه"))

        self.groupBox.setTitle(_translate("Dialog", "اضافه کردن کتاب"))
        self.label_3.setText(_translate("Dialog", "Isbn"))
        self.label_2.setText(_translate("Dialog", "نویسنده :"))
        self.label.setText(_translate("Dialog", "عنوان کتاب :"))
        self.btn_add.setText(_translate("Dialog", "اضافه به کتابخانه"))
        self.btn_delete.setText(_translate("Dialog", "حذف کتاب انتخاب شده"))
        self.btn_borrowed_books.setText(_translate("Dialog", "کتاب‌های قرضی"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
