from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QMouseEvent

class ClickabeFrame(QFrame):
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.setObjectName("cfr")

        self.setFixedSize(150, 150)

        self.setStyleSheet(
            "#cfr{border: 1px solid auqa; border-radius: 2px;}"
            "#cfr:hover{background-color: rgba(0, 0, 0, 0.3);}"
        )

    def mousePressEvent(self, event: QMouseEvent):
        self.clicked.emit()

class RenderPreview(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.sizePolicy().setVerticalPolicy(QSizePolicy.Policy.Expanding)
        # self.sizePolicy().setHorizontalPolicy(QSizePolicy.Policy.Expanding)
        self.setAlignment(Qt.Alignment.AlignCenter)
        self.originalPixmap = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.originalPixmap:
            scaled = self.originalPixmap.scaled(event.size(),
                                                Qt.AspectRatioMode.KeepAspectRatio,
                                                Qt.TransformationMode.SmoothTransformation)
            super().setPixmap(scaled)

    def setPixmap(self, pixmap):
        super().setPixmap(pixmap)
        self.originalPixmap = pixmap

class RenderNacin(QDialog):
    def __init__(self, parent, graphicsView):
        super().__init__(parent)

        self.nacin = None
        self.graphicsView = graphicsView

        self.setStyleSheet("font-size: 25px;")

        hBox = QHBoxLayout(self)

        nacinEnum = self.graphicsView.NacinEnum

        self.frame1, self.sPreview = self.napraviPolje("Samo slika", nacinEnum.slika)
        self.frame2, self.iPreview = self.napraviPolje("Svi itemi", nacinEnum.items)
        self.frame3, self.cPreview = self.napraviPolje("Izaberi sam", nacinEnum.custom)

        hBox.addWidget(self.frame1)
        hBox.addWidget(self.frame2)
        hBox.addWidget(self.frame3)

        self.setLayout(hBox)
        self.renderujPrikaze()

    def izabrano(self, nacin):
        self.nacin = nacin
        self.close()

    def renderujPrikaze(self):
        pixS = self.graphicsView.renderScene(self.graphicsView.NacinEnum.slika)
        pixI = self.graphicsView.renderScene(self.graphicsView.NacinEnum.items)

        self.sPreview.setPixmap(pixS)

        if pixS.width() == pixI.width() and pixS.height() == pixI.height():
            self.frame2.hide()
        else:
            self.iPreview.setPixmap(pixI)

        self.setFixedSize(self.sizeHint())

    def napraviPolje(self, labelText, nacin):
        frame = ClickabeFrame(self)

        label = QLabel(labelText, frame)

        preview = RenderPreview(frame)

        frame.layout().setContentsMargins(1, 2, 1, 2)
        frame.layout().addStretch()

        frame.layout().addWidget(label)
        frame.layout().addWidget(preview)

        frame.layout().addStretch()

        frame.clicked.connect(lambda: self.izabrano(nacin))
        return frame, preview

    @classmethod
    def izaberiNacinCuvanja(cls, parent, graphicsView):
        dialog = cls(parent, graphicsView)
        dialog.exec()
        return dialog.nacin
