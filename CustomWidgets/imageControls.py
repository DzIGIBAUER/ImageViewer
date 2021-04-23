from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QGraphicsItem
from PyQt6.QtGui import QIcon, QPainter, QPixmap
from PyQt6.QtCore import pyqtSignal, QRectF
from ImageViewerRepo.UI.imageControlsUI import Ui_imageControls

class ItemPreview(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ImageControls(QWidget):
    dodatItem = pyqtSignal(QGraphicsItem)

    def __init__(self, image, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_imageControls()
        self.ui.setupUi(self)
        self.drawing = self.ui.graphicsView.drawing

        self.ui.graphicsView.namestiSliku(image)
        self.dodatItem.connect(self.azurirajItemListu)

        self.ui.penColorSelect.clicked.connect(lambda: self.drawing.izaberiPenBoju(self.ui.penColorSelect))
        self.ui.brushColorSelect.clicked.connect(lambda: self.drawing.izaberiBrushBoju(self.ui.brushColorSelect))
        self.ui.horizontalSlider.valueChanged.connect(self.sliderValueChanged)

        self.dodajMetoduCrtanja(QIcon("icons:exit.png"), self.drawing.Point)

    # FIXME: izbacuje ludacke boje umesto slike
    def azurirajItemListu(self, grupa):
        previewLabel = ItemPreview()
        pixmap = QPixmap(35, 35)
        self.ui.graphicsView.previewScene.addItem(grupa)
        p = QPainter(pixmap)
        self.ui.graphicsView.previewScene.render(p, QRectF(pixmap.rect()))
        p.end()
        self.ui.graphicsView.scene_.addItem(grupa)
        previewLabel.setPixmap(pixmap)
        self.ui.itemsList.layout().insertWidget(0, previewLabel)

    def dodajMetoduCrtanja(self, icon, drawingMethod):
        btn = QPushButton(icon, "")
        btn.clicked.connect(lambda: self.drawing.namestiMetoduCrtanja(drawingMethod))
        self.ui.buttonsFrame.layout().addWidget(btn)

    def sliderValueChanged(self):
        self.drawing.namestiDebljinuLinije(self.ui.horizontalSlider.value())
