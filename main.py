from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget
from PyQt6.QtGui import QPixmap, QIcon, QFontDatabase, QImageReader
from PyQt6 import QtCore
from ImageViewerRepo.UI import mainWindowUI, imageControlsUI
from pathlib import Path
import sys

imgPath = r"C:\Users\Windows 10 Pro\Pictures\Saved Pictures\Capture.JPG"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        QtCore.QDir.addSearchPath("icons", "Resources/icons")
        QtCore.QDir.addSearchPath("fonts", "Resources/fonts")

        QFontDatabase.addApplicationFont("fonts:roboto/Roboto-Medium.ttf")
        self.setStyleSheet("font: Roboto Medium; font-size: 12px;")

        self.ui = mainWindowUI.Ui_MainWindow()
        self.ui.setupUi(self)

        expandCall = self.ui.sideBar.toggleSideBar
        self.ui.sideBar.dodajDugme(QIcon("icons:home.png"), "Nesto", expandCall)
        self.ui.sideBar.dodajDugme(QIcon("icons:mainicon.ico"), "IDEEEEEO", expandCall)
        self.ui.sideBar.dodajDugme(QIcon("icons:exit.png"), "Napusti", expandCall)

        # self.ui.tabWidget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, QPushButton("a"))

        self.ui.actionOpen.triggered.connect(self.otvoriFajl)

        self.setWindowIcon(QIcon("icons:mainIcon.ico"))
        self.setWindowTitle("Image Viewer aplikacija :D :D")

        self.formati = []
        for f in QImageReader.supportedImageFormats():
            self.formati.append(f.data().decode("utf-8"))

    def otvoriFajl(self):
        formatFilter = "".join([f"*.{_format} " for _format in self.formati])
        filePaths, formati = QFileDialog.getOpenFileNames(caption="Izaberite fajlove", filter=formatFilter)
        if not filePaths:
            print("Nije izabran fajl")
            return

        for filePath in filePaths:
            fp = Path(filePath)
            imageControls = QWidget()

            imgCUi = imageControlsUI.Ui_imageControls()
            imgCUi.setupUi(imageControls)
            imgCUi.label.setPixmap(QPixmap(filePath))

            self.ui.tabWidget.insertTab(0, imageControls, fp.name)

# stae ovo bee
class Slika(QPixmap):
    def __init__(self, slika=None):
        super().__init__(slika)

        self.trenutniZoom = 0
        self.zoomKorak = 20

    def namestiZoom(self, scrollSmer):
        # ili uvelicivamo ili smanjujemo sliku
        if scrollSmer == "up":
            noviZoom = self.trenutniZoom + self.zoomKorak
        else:
            noviZoom = self.trenutniZoom - self.zoomKorak

        size = self.size() + QtCore.QSize(noviZoom, noviZoom)

        self.trenutniZoom = noviZoom

        return self.scaled(size.width(), size.height(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
    # transformMode = Qt.SmoothTransformation



if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook


    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())
