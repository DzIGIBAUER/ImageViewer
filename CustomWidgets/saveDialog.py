from PyQt6.QtWidgets import (QDialog, QPushButton, QGridLayout, QLabel, QFileDialog, QColorDialog, QCheckBox, QFrame,
                             QVBoxLayout)
from PyQt6.QtGui import QBrush
from PyQt6.QtCore import Qt

class SaveDialog(QDialog):
    def __init__(self, parent, graphicsView):
        super().__init__(parent)

        self.nacin = None
        self.fileName = None

        self.graphicsView = graphicsView

        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.setMaximumSize(400, 400)

        self.slikaPrikazFrame = QFrame(self)

        self.slikaPrikaz = QLabel(self)
        self.slikaButton = QPushButton("SAMO SLIKA", self)
        self.slikaButton.clicked.connect(lambda: self.klik(1))

        self.itemsPrikazFrame = QFrame(self)

        self.itemsPrikaz = QLabel(self)
        self.itemsButton = QPushButton("SVI ITEMI", self)
        self.itemsButton.clicked.connect(lambda: self.klik(2))

        self.bojaPozadineButton = QPushButton("Namesti pozadinu")
        self.bojaPozadineButton.clicked.connect(self.namestiBojuPozadine)
        self.opomena = QLabel("Boja pozadine nema efekta ako je pozadina providna")

        self.providnaPozadinaButton = QCheckBox("Providna Pozadina")
        self.providnaPozadinaButton.clicked.connect(self.namestiProvidnostPozadine)

        self.renderujPrikaze()

        self.slikaPrikazFrame.setLayout(QVBoxLayout())
        self.slikaPrikazFrame.layout().addWidget(self.slikaPrikaz)
        self.slikaPrikazFrame.layout().addWidget(self.slikaButton)

        self.itemsPrikazFrame.setLayout(QVBoxLayout())
        self.itemsPrikazFrame.layout().addWidget(self.itemsPrikaz)
        self.itemsPrikazFrame.layout().addWidget(self.itemsButton)

        self.grid.addWidget(self.slikaPrikazFrame, 0, 0)
        self.grid.addWidget(self.itemsPrikazFrame, 0, 1)

        self.grid.addWidget(self.bojaPozadineButton, 2, 0)
        self.grid.addWidget(self.providnaPozadinaButton, 2, 1)
        self.grid.addWidget(self.opomena, 3, 0)

    def klik(self, id_):
        self.nacin = id_
        self.fileName, _type = QFileDialog.getSaveFileName()
        if self.fileName:
            self.close()

    def namestiProvidnostPozadine(self):
        self.graphicsView.scene_.setBackgroundBrush(QBrush(Qt.GlobalColor.transparent))
        self.renderujPrikaze()

    def namestiBojuPozadine(self):
        color = QColorDialog.getColor(initial=self.graphicsView.scene_.backgroundBrush().color())
        self.graphicsView.scene_.setBackgroundBrush(QBrush(color))
        self.renderujPrikaze()
        self.providnaPozadinaButton.setChecked(False)

    def renderujPrikaze(self):
        pixS, pixI = self.graphicsView.renderScene(1), self.graphicsView.renderScene(2)
        if pixS.width() == pixI.width() and pixS.height() == pixI.height():
            self.itemsPrikazFrame.hide()
        self.slikaPrikaz.setPixmap(pixS.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))
        self.itemsPrikaz.setPixmap(pixI.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))

    @classmethod
    def izaberiNacinCuvanja(cls, parent, graphicsView):

        dialog = cls(parent, graphicsView)

        dialog.exec()
        return dialog.fileName, dialog.nacin
