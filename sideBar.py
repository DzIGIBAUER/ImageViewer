from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import QPropertyAnimation, QSize
from time import clock

class SideBar(QFrame):
    def __init__(self, *args, **kwargs):
        super(SideBar, self).__init__(*args, **kwargs)
        self.expanded = False
        self.kolonaWidth = None
        self.kolone = []

        self.animTrajanje = 250
        self.sideBarAnim = None

    '''
    Ova klasa je ucitana u konvertovanom .py fajlu  u setupUi metodi
    pre nego sto su ucitani svi elementi koji su nam potrebni.
    Zato iz main.py nakon zavrsene setupUi metode naknadno zovemo ovu metodu da
    napravimo listu elemenata u sideBaru kako bi manipulisali njima.
    '''
    def osposobi(self):
        self.kolonaWidth = self.property("prvaKolona")

        hc = self.findChild(QFrame, "hContainer")
        self.kolone = [kolona for kolona in hc.children() if type(kolona) == QFrame]

        self.sideBarAnim = QPropertyAnimation(self.kolone[0], b"minimumSize")
        self.sideBarAnim.setDuration(self.animTrajanje)

    def toggleSideBar(self):
        pocetnaVrednost = self.kolone[0].minimumSize()
        if self.expanded:
            krajnjaVrednost = QSize(0, 0)
            self.expanded = False

        else:
            krajnjaVrednost = self.kolonaWidth
            self.expanded = True

        self.sideBarAnim.setStartValue(pocetnaVrednost)
        self.sideBarAnim.setEndValue(krajnjaVrednost)
        self.sideBarAnim.start()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # print(event)
