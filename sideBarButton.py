from PyQt6.QtWidgets import QPushButton, QSizePolicy
from PyQt6.QtGui import QPixmap, QPainter, QIcon, QColor, QPalette
from PyQt6.QtCore import Qt, QRect, QSize, QVariantAnimation

class SideBarButton(QPushButton):
    def __init__(self, *args, **kwargs):
        if type(args[0]) is QIcon:  # ako smo dobili ikonicu kao prvi argument cuvamo je
            self.ikonica = args[0]
            sargs = args[1:]  # QPushButton-u dajemo sve sem ikonice
        else:
            sargs = args

        super().__init__(*sargs, **kwargs)

        self.iconRect = QRect(0, 0, 35, 35)

        sp = self.sizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
        self.setSizePolicy(sp)

        self.setMinimumSize(self.iconRect.size())
        self.setStyleSheet(f"padding: 3px 5px 3px {self.iconRect.width()}px;")

        self.backgroundColor = None  # bice namesteno kada se widget ucita: QColor
        self.hoverColor = QColor("lightgreen")

        self.hoverAnimacija = QVariantAnimation()
        self.hoverAnimacija.valueChanged.connect(self.setBojaDugmeta)
        self.hoverAnimacija.setDuration(350)


    def setBojaDugmeta(self, color):
        self.setStyleSheet(f"{self.styleSheet()}background-color: {color.name()};")

    def getBojaDugmeta(self):
        return QColor(self.palette().color(QPalette.ColorRole.Button).name())

    def enterEvent(self, event):
        super().enterEvent(event)
        self.onHoverBegin()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.onHoverOver()

    def onHoverBegin(self):
        eValue = self.hoverColor
        if self.hoverAnimacija.state() == QVariantAnimation.State.Running:
            pValue = self.hoverAnimacija.currentValue()
            self.hoverAnimacija.stop()
        else:
            pValue = self.backgroundColor

        self.animirajPozadinu(pValue, eValue)

    def onHoverOver(self):
        eValue = self.backgroundColor
        if self.hoverAnimacija.state() == QVariantAnimation.State.Running:
            pValue = self.hoverAnimacija.currentValue()
            self.hoverAnimacija.stop()
        else:
            pValue = self.hoverColor

        self.animirajPozadinu(pValue, eValue)

    def animirajPozadinu(self, pValue, eValue):
        self.hoverAnimacija.setStartValue(pValue)
        self.hoverAnimacija.setEndValue(eValue)
        self.hoverAnimacija.start()

    def showEvent(self, _event):
        super().showEvent(_event)
        self.backgroundColor = self.getBojaDugmeta()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        sirina = event.size().width() - self.iconRect.width()
        sirinaHint = self.sizeHint().width() - self.iconRect.width()

        self.setVidljivostTexta(sirina / sirinaHint)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        self.crtajIkonicu(painter)

    def crtajIkonicu(self, p):
        if not hasattr(self, "ikonica"):
            return

        pixmap = self.ikonica.pixmap(self.iconRect.size() - QSize(4, 4))

        y = self.iconRect.height() // 2 - pixmap.height() // 2
        x = self.iconRect.width() // 2 - pixmap.width() // 2

        p.drawPixmap(x, y, pixmap)

    def setIcon(self, icon):
        self.ikonica = icon

    def setVidljivostTexta(self, opacity):
        if opacity > 1:  # ne moze da bude vece od 1 ili manje od 0
            opacity = 1
        elif opacity < 0:
            opacity = 0

        # TODO: ovde bi valjao regex, ali zasada ovako
        stariStyleSheet = self.styleSheet()
        vidljivost = f"color: rgba(0, 0, 0, {opacity});"  # ovo treba da dodamo

        idx = stariStyleSheet.find("color:")  # mozda je vec tu stara vrednost
        if idx == -1:  # -1 znaci da nije i samo dodamo pored
            self.setStyleSheet(stariStyleSheet + vidljivost)
            return

        startIdx = stariStyleSheet.find("color:")
        endIdx = stariStyleSheet.find(";", startIdx)

        # spojimo stari stylesheet za zamenjenom starom color vrednoscu i namestamo..
        self.setStyleSheet("".join((stariStyleSheet[:startIdx], vidljivost, stariStyleSheet[endIdx + 1:])))
