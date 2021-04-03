from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6 import QtCore
from ImageViewerRepo.UI import mainWindowUI
import sys

imgPath = r"C:\Users\Windows 10 Pro\Pictures\Saved Pictures\Capture.JPG"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        QtCore.QDir.addSearchPath("icons", "Resources/icons")

        self.trenutniPixmap = None
        self.zoomStep = 20
        self.trenutniZoom = 0

        self.ui = mainWindowUI.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.imageLabel.wheelEvent = self.namestiZoom

        self.setWindowIcon(QIcon("icons:mainIcon.ico"))
        self.setWindowTitle("Image Viewer aplikacija :D :D")

        self.namestiSliku(imgPath)

    def namestiZoom(self, event):

        if event.angleDelta().y() > 0:
            self.trenutniZoom += self.zoomStep
        else:
            self.trenutniZoom -= self.zoomStep

        size = self.trenutniPixmap.size() + QtCore.QSize(self.trenutniZoom, self.trenutniZoom)

        novaSlika = self.trenutniPixmap.scaled(size.width(), size.height(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.imageLabel.setPixmap(novaSlika)

    def namestiSliku(self, slika):
        self.trenutniPixmap = QPixmap(slika)
        self.ui.imageLabel.setPixmap(self.trenutniPixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())
