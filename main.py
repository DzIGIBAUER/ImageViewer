from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6 import QtCore
from ImageViewerRepo.UI import mainWindowUI
import sys

img_path = r"C:\Users\Windows 10 Pro\Pictures\Saved Pictures\Capture.JPG"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        QtCore.QDir.addSearchPath('icons', 'Resources/icons')

        self.setupUi()

    def setupUi(self):
        self.setWindowIcon(QIcon("icons:mainIcon.ico"))

        ui = mainWindowUI.Ui_MainWindow()
        ui.setupUi(self)

        # mora nakon setupUi
        self.setWindowTitle("Image Viewer aplikacija :D :D")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())
