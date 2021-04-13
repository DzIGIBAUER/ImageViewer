from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6 import QtCore
from ImageViewerRepo.UI import mainWindowUI
from ImageViewerRepo.sideBarButton import SideBarButton
import sys

imgPath = r"C:\Users\Windows 10 Pro\Pictures\Saved Pictures\Capture.JPG"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        QtCore.QDir.addSearchPath("icons", "Resources/icons")

        # move promenljive
        self.mousePocetnaPozicija = QtCore.QPointF()
        self.imgPocetnaPozicija = QtCore.QPointF()

        self.slika = Slika(imgPath)

        self.ui = mainWindowUI.Ui_MainWindow()
        self.ui.setupUi(self)

        expandCall = self.ui.sideBar.toggleSideBar
        self.ui.sideBar.dodajDugme(QIcon("icons:home.png"), "Nesto", expandCall)


        # ne valja sranje, SRANJEE
        self.ui.imageLabel.wheelEvent = self.zoomEvent
        self.ui.imageLabel.mousePressEvent = self.moveStart
        self.ui.imageLabel.mouseMoveEvent = self.moveUpdate
        self.ui.imageLabel.mouseReleaseEvent = self.moveEnd

        self.setWindowIcon(QIcon("icons:mainIcon.ico"))
        self.setWindowTitle("Image Viewer aplikacija :D :D")

        self.prikaziSliku(self.slika)


    def zoomEvent(self, event):
        # angle > 0 je up, angle < 0 je down
        angle = event.angleDelta().y()
        scrollSmer = "up" if angle > 0 else "down"
        novaSlika = self.slika.namestiZoom(scrollSmer)

        self.ui.imageLabel.resize(novaSlika.size() + QtCore.QSize(10, 10))
        print(f"Velicina nove slike je {novaSlika.size()}\n{self.ui.imageLabel.size()}")

        self.prikaziSliku(novaSlika)

    def prikaziSliku(self, slikaPixmap):
        self.trenutniPixmap = QPixmap(slikaPixmap)
        self.ui.imageLabel.setPixmap(self.trenutniPixmap)

    def moveStart(self, event):
        self.mousePocetnaPozicija = event.globalPosition()
        self.imgPocetnaPozicija = QtCore.QPointF(self.ui.imageLabel.pos())

    def moveUpdate(self, event):
        globalPos = event.globalPosition()
        razlika = globalPos - self.mousePocetnaPozicija
        novaPos = self.imgPocetnaPozicija + razlika
        self.ui.imageLabel.move(novaPos.toPoint())


    def moveEnd(self, _event):
        self.mousePocetnaPozicija = QtCore.QPoint()

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
