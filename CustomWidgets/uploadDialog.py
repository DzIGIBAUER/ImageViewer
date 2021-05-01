from PyQt6.QtWidgets import QDialog, QPushButton, QGridLayout, QLabel, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt

class UploadDialog(QDialog):
    def __init__(self, parent, pixmap):
        super().__init__(parent)
        self.upload = False

        grid = QGridLayout()
        self.setLayout(grid)
        self.setMaximumSize(400, 400)

        self.naslovEdit = QLineEdit(self)
        self.naslovEdit.setPlaceholderText("Naslov")

        slikaPrikaz = QLabel(self)
        slikaPrikaz.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))

        self.opisEdit = QTextEdit(self)
        self.opisEdit.setPlaceholderText("Opis")

        uploadButton = QPushButton("Upload", self)
        uploadButton.clicked.connect(self.klik)

        grid.addWidget(self.naslovEdit, 0, 0)
        grid.addWidget(slikaPrikaz, 1, 0)
        grid.addWidget(self.opisEdit, 2, 0)
        grid.addWidget(uploadButton, 3, 1)

    def klik(self):
        self.upload = True
        self.close()

    @classmethod
    def uploadFile(cls, parent, pixmap):
        dialog = cls(parent, pixmap)

        dialog.exec()
        return dialog.upload, dialog.naslovEdit.text(), dialog.opisEdit.toPlainText()
