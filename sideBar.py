from PyQt6.QtWidgets import QFrame, QPushButton, QSizePolicy
from PyQt6.QtCore import QPropertyAnimation, QSize, QEasingCurve
from ImageViewerRepo.sideBarButton import SideBarButton

class SideBar(QFrame):
    def __init__(self, *args, **kwargs):
        super(SideBar, self).__init__(*args, **kwargs)
        self.expanded = False
        self.dugmad = []
        self.shrinkedWidth = 0
        self.animacija = QPropertyAnimation(self, b"maximumWidth")

    def toggleSideBar(self):
        if self.expanded:
            pValue = self.maximumWidth()
            eValue = self.shrinkedWidth
            self.expanded = False
        else:
            pValue = self.maximumWidth()
            eValue = 100
            self.expanded = True

        self.animacija.setStartValue(pValue)
        self.animacija.setEndValue(eValue)
        self.animacija.start()

    def dodajDugme(self, icon, text, callback):
        dugme = SideBarButton(icon, text)
        self.layout().insertWidget(len(self.children()) - 1, dugme)
        self.dugmad.append(dugme)
        dugme.clicked.connect(callback)

        self.shrinkedWidth = dugme.minimumWidth()
        self.setMaximumWidth(self.shrinkedWidth)

    def izbrisiDugme(self, dugme_id):
        self.dugmad.remove(dugme_id)
