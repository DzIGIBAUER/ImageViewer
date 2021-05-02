from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from CustomWidgets.sideBarButton import SideBarButton

class SideBar(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.expanded = False
        self.dugmad = []
        self.shrinkedWidth = 0
        self.animacija = QPropertyAnimation(self, b"maximumWidth")
        self.animacija.setEasingCurve(QEasingCurve(QEasingCurve.Type.InQuad))

    def toggleSideBar(self):
        if self.animacija.state() == QPropertyAnimation.State.Running:
            pValue = self.animacija.currentValue()
            self.animacija.stop()
        else:
            pValue = self.maximumWidth()

        if self.expanded:
            eValue = self.shrinkedWidth
            self.expanded = False
        else:
            eValue = 150
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
