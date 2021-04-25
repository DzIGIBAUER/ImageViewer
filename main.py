from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtGui import QIcon, QFontDatabase, QImageReader
from PyQt6 import QtCore
from ImageViewerRepo.UI import mainWindowUI
from ImageViewerRepo.CustomWidgets import imageControls, saveDialog
from pathlib import Path
import sys

imgPath = r"C:\Users\Windows 10 Pro\Pictures\Saved Pictures\Capture.JPG"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        QtCore.QDir.addSearchPath("icons", "Resources/Icons")
        QtCore.QDir.addSearchPath("fonts", "Resources/Fonts")

        QFontDatabase.addApplicationFont("fonts:roboto/Roboto-Medium.ttf")
        self.setStyleSheet("font: Roboto Medium; font-size: 12px;")

        self.ui = mainWindowUI.Ui_MainWindow()
        self.ui.setupUi(self)

        sb = self.ui.sideBar
        sb.dodajDugme(QIcon("icons:mainIcon.ico"), "EJ", sb.toggleSideBar)
        sb.dodajDugme(QIcon("icons:exit.png"), "Edit", self.toggleEditing)

        self.ui.actionOpen.triggered.connect(self.otvoriFajl)
        self.ui.actionSave.triggered.connect(self.sacuvaj)

        self.setWindowIcon(QIcon("icons:mainIcon.ico"))
        self.setWindowTitle("Image Viewer aplikacija :D :D")

        self.formati = []
        for f in QImageReader.supportedImageFormats():
            self.formati.append(f.data().decode("utf-8"))

    def otvoriFajl(self):
        formatFilter = "".join([f"*.{_format} " for _format in self.formati])
        filePaths, formati = QFileDialog.getOpenFileNames(caption="Izaberite fajlove", filter=formatFilter,
                                                          directory=r"C:\Users\Windows 10 Pro\Pictures\Saved Pictures")
        if not filePaths:
            print("Nije izabran fajl")
            return

        for filePath in filePaths:
            fp = Path(filePath)
            imgControls = imageControls.ImageControls(self, filePath)
            self.ui.tabWidget.insertTab(0, imgControls, fp.name)
            self.ui.tabWidget.setCurrentIndex(0)

    def toggleEditing(self):
        if not self.ui.tabWidget.tabBar().count():
            return

        imgControl = self.ui.tabWidget.currentWidget()
        imgControl.toogleEdit()

    def sacuvaj(self):
        if not self.ui.tabWidget.tabBar().count():
            return
        imgControl = self.ui.tabWidget.currentWidget()

        fileName, nacin = saveDialog.SaveDialog.izaberiNacinCuvanja(self, imgControl.ui.graphicsView)

        if not nacin or not fileName:
            return

        imgControl.ui.graphicsView.sacuvajFajl(fileName, nacin)


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
