from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QFrame, QVBoxLayout, QLabel, QPushButton,
                             QMessageBox)
from PyQt6.QtGui import QIcon, QFontDatabase, QImageReader, QPixmap
from PyQt6 import QtCore
from UI import mainWindowUI
from CustomWidgets import imageControls, uploadDialog, renderNacinDialog
import database, uploadImage
from functools import partial
from pathlib import Path
from enum import Enum
import sys

class StackedWidgetsEnum(Enum):
    main = 0
    podesavanje = 1
    tabWidget = 2

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
        sb.dodajDugme(QIcon("icons:menu.png"), "EJ", sb.toggleSideBar)
        sb.dodajDugme(QIcon("icons:home.png"), "Edit", self.toggleMain)
        sb.dodajDugme(QIcon("icons:gear.png"), "Podesavanje", self.togglePodesavanje)
        sb.dodajDugme(QIcon("icons:pen.png"), "Edit", self.toggleEditing)

        self.ui.actionOpen.triggered.connect(self.otvoriFajl)
        self.ui.actionSave.triggered.connect(self.sacuvaj)
        self.ui.actionUpload.triggered.connect(lambda: self.upload())

        self.setWindowIcon(QIcon("icons:mainIcon.ico"))
        self.setWindowTitle("Image Viewer aplikacija :D :D")

        self.ui.pushButtonSacuvaj.clicked.connect(self.sacuvajPodesavanja)

        self.formati = []
        for f in QImageReader.supportedImageFormats():
            self.formati.append(f.data().decode("utf-8"))

        self.dbc = database.DBControls()

        clientID = self.dbc.clientID() or ""
        self.ui.lineEditClientID.poveziCheckBox(self.ui.checkBox)
        self.ui.lineEditClientID.setText(clientID)

        self.azurirajMain()
        self.ui.stackedWidget.setCurrentIndex(0)

    def otvoriFajl(self):
        formatFilter = "".join([f"*.{_format} " for _format in self.formati])
        filePaths, formati = QFileDialog.getOpenFileNames(caption="Izaberite fajlove", filter=formatFilter)
        if not filePaths:
            return

        for filePath in filePaths:
            fp = Path(filePath)
            imgControls = imageControls.ImageControls(self, filePath)
            self.ui.tabWidget.insertTab(0, imgControls, fp.name)
            self.ui.tabWidget.setCurrentIndex(0)

            closeDugme = QPushButton("X")
            closeDugme.setMaximumSize(15, 15)

            cTab = self.ui.tabWidget.tabBar()
            closeDugme.clicked.connect(partial(self.ugasiSliku, imgControls))
            cTab.setTabButton(0, cTab.ButtonPosition.RightSide, closeDugme)

            self.ui.stackedWidget.setCurrentIndex(2)

    def ugasiSliku(self, imgc):
        index = self.ui.tabWidget.indexOf(imgc)
        naslov = self.ui.tabWidget.tabText(index)
        odg = QMessageBox.question(self, "Ugasi sliku?", f"Da li zelite da ugasite {naslov}")
        if odg == QMessageBox.StandardButtons.Yes:
            self.ui.tabWidget.removeTab(index)
            if self.ui.tabWidget.count() == 0:
                self.ui.stackedWidget.setCurrentIndex(0)

    def izbrisiUploadovanuSliku(self):
        mbox = QMessageBox()
        sig = mbox.question(self, "OzbiljnOoOoO","Da li ste sigurni da želite da obrisete sliku?")
        if sig is mbox.StandardButtons.No:
            return

        dugme = self.sender()
        id_ = dugme.property("imgID")
        frame = dugme.property("frame")
        uspesno, poruka = uploadImage.delete(self.dbc.clientID(), dugme.property("hash"))
        if uspesno:
            self.dbc.izbrisiUploadovanuSliku(id_)
            frame.layout().removeWidget(frame)
        else:
            odg = mbox.question(self, "Doslo je do greske", f"Slika nije mogla biti obrisana.\nRazlog: {poruka}\n"
                                + "Da li zelite da je izbrisete iz samo iz aplikacije?")
            if odg is mbox.StandardButtons.Yes:
                self.dbc.izbrisiUploadovanuSliku(id_)
                frame.layout().removeWidget(frame)

    def toggleEditing(self):
        if not self.ui.tabWidget.tabBar().count():
            return

        imgControl = self.ui.tabWidget.currentWidget()
        imgControl.toggleEdit()

    def togglePodesavanje(self):
        if not self.ui.stackedWidget.currentIndex() == StackedWidgetsEnum.podesavanje.value:
            self.ui.stackedWidget.setCurrentIndex(StackedWidgetsEnum.podesavanje.value)
        else:
            if self.ui.tabWidget.count() != StackedWidgetsEnum.main.value:
                self.ui.stackedWidget.setCurrentIndex(StackedWidgetsEnum.tabWidget.value)

    def toggleMain(self):
        if not self.ui.stackedWidget.currentIndex() == StackedWidgetsEnum.main.value:
            self.ui.stackedWidget.setCurrentIndex(StackedWidgetsEnum.main.value)
        else:
            if self.ui.tabWidget.count() != StackedWidgetsEnum.main.value:
                self.ui.stackedWidget.setCurrentIndex(StackedWidgetsEnum.tabWidget.value)

    def azurirajMain(self):
        uploadovaneSlike = self.dbc.uploadovaneSlike()
        if not uploadovaneSlike:
            nemaLabel = QLabel("NEMATE UPLOUDOVANIH SLIKA", self.ui.frame)
            nemaLabel.setStyleSheet("font-size: 25px;")
            self.ui.frame.layout().addWidget(nemaLabel)

        for widget in self.ui.frame.children():
            if type(widget) == QFrame:
                self.ui.frame.layout().removeWidget(widget)

        for info in uploadovaneSlike:
            id_, naslov, opis, deletehash, data = info
            fr = QFrame()
            fr.setObjectName("fr")
            fr.setStyleSheet("QFrame{color: white; background-color: rgb(49, 49, 49);}#fr{border-radius: 5px;}")
            vly = QVBoxLayout()
            fr.setLayout(vly)

            pix = self.pixmapFromBytes(data)
            nl = QLabel(naslov, fr)
            nl.setTextInteractionFlags(QtCore.Qt.TextInteractionFlags.TextSelectableByMouse)
            vly.addWidget(nl)

            imgL = QLabel("", fr)
            imgL.setPixmap(pix)
            imgL.setAlignment(QtCore.Qt.Alignment.AlignCenter)
            vly.addWidget(imgL)
            dl = QLabel(f"DeleteHash {deletehash}", fr)
            dl.setTextInteractionFlags(QtCore.Qt.TextInteractionFlags.TextSelectableByMouse)

            url = f"https://imgur.com/{id_}"
            linkLabel = QLabel(f"<a href='{url}'>{url}</a>", fr)
            linkLabel.setOpenExternalLinks(True)
            vly.addWidget(linkLabel)

            vly.addWidget(dl)
            ol = QLabel(opis, fr)
            ol.setTextInteractionFlags(QtCore.Qt.TextInteractionFlags.TextSelectableByMouse)
            vly.addWidget(ol)

            izbrisiLabel = QPushButton("X", imgL)
            izbrisiLabel.setProperty("imgID", id_)
            izbrisiLabel.setProperty("hash", deletehash)
            izbrisiLabel.setProperty("frame", fr)
            izbrisiLabel.clicked.connect(self.izbrisiUploadovanuSliku)
            izbrisiLabel.setFixedSize(15, 15)
            izbrisiLabel.setParent(imgL)
            izbrisiLabel.setStyleSheet("background-color: red;")

            self.ui.frame.layout().addWidget(fr)

    def sacuvajPodesavanja(self):
        self.dbc.namestiClientID(self.ui.lineEditClientID.raw)

    def sacuvaj(self):
        if (not self.ui.tabWidget.tabBar().count() or  # ako nema otvorenih slika nemamo sta da sacuvamo
                self.ui.stackedWidget.currentIndex() != StackedWidgetsEnum.tabWidget.value):  # ako nismo u tabWidget
            return

        imgControls = self.ui.tabWidget.currentWidget()  # trenutni ImageControls widget gde je slika

        renderNacin = renderNacinDialog.RenderNacin.izaberiNacinCuvanja(self, imgControls.ui.graphicsView)
        if not renderNacin:
            return

        imgControls.ui.graphicsView.sacuvajFajl(renderNacin)

    def upload(self):
        if (not self.ui.tabWidget.tabBar().count() or  # ako nema otvorenih slika nemamo sta da sacuvamo
                self.ui.stackedWidget.currentIndex() != StackedWidgetsEnum.tabWidget.value):  # ako nismo u tabWidget
            return

        imgControls = self.ui.tabWidget.currentWidget()  # trenutni ImageControls widget gde je slika

        renderNacin = renderNacinDialog.RenderNacin.izaberiNacinCuvanja(self, imgControls.ui.graphicsView)
        if not renderNacin:
            return

        imgControls.ui.graphicsView.spremiUpload(self.zavrsiUpload)


    def zavrsiUpload(self, nacin, dimenzije):
        pix = self.ui.tabWidget.currentWidget().ui.graphicsView.renderScene(nacin, dimenzije)
        nastavi, naslov, opis = uploadDialog.UploadDialog.uploadFile(self, pix)

        if not nastavi:
            return
        id_, deletehash = uploadImage.upload(self.bytesFromPixmap(pix), self.dbc.clientID(), naslov, opis)

        if not id_ and not deletehash:
            mb = QMessageBox()
            mb.information(self, "Greška", "Došlo je do neocekivane greške")
            return

        self.dbc.dodajUploadovanuSliku(id_, naslov, opis, deletehash, self.bytesFromPixmap(pix.scaled(
            100, 100, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
                                       )
        self.azurirajMain()

    def bytesFromPixmap(self, pixmap):
        ba = QtCore.QByteArray()
        buff = QtCore.QBuffer(ba)
        buff.open(QtCore.QIODevice.OpenMode.WriteOnly)
        ok = pixmap.save(buff, "PNG")
        assert ok
        return ba.data()

    def pixmapFromBytes(self, data):
        pixmap = QPixmap()
        ok = pixmap.loadFromData(data)
        assert ok
        return pixmap

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
