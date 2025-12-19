from PyQt5.QtCore import QAbstractTableModel, Qt

class BookTableModel(QAbstractTableModel):
    def __init__(self, books=None):
        super().__init__()
        self.books = books or []
        self.headers = ["کد", "عنوان کتاب", "نویسنده", "ISBN"]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            book = self.books[index.row()]
            col = index.column()
            if col == 0: return str(book.id)
            if col == 1: return book.title
            if col == 2: return book.author
            if col == 3: return book.isbn
        

        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight | Qt.AlignVCenter
            
        return None

    def rowCount(self, index=None):
        return len(self.books)

    def columnCount(self, index=None):
        return len(self.headers)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None