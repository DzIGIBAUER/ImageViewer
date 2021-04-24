from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QGraphicsItem
from PyQt6.QtGui import QIcon, QPainter, QPixmap
from PyQt6.QtCore import pyqtSignal, QRectF, QPropertyAnimation, QParallelAnimationGroup
from ImageViewerRepo.UI.imageControlsUI import Ui_imageControls

class ImageControls(QWidget):
    def __init__(self, main, image, *args, **kwargs):
        super().__init__(*args, **kwargs)
        main.ui.sideBar.dodajDugme(QIcon("icons:exit.png"), "Edit", self.toogleEdit)
        self.ui = Ui_imageControls()
        self.ui.setupUi(self)
        self.drawing = self.ui.graphicsView.drawing

        self.ui.graphicsView.namestiSliku(image)

        self.ui.penColorSelect.clicked.connect(lambda: self.drawing.izaberiPenBoju(self.ui.penColorSelect))
        self.ui.brushColorSelect.clicked.connect(lambda: self.drawing.izaberiBrushBoju(self.ui.brushColorSelect))
        self.ui.horizontalSlider.valueChanged.connect(self.sliderValueChanged)

        self.dodajMetoduCrtanja(QIcon("icons:exit.png"), self.drawing.Point)

        self.animGroup = QParallelAnimationGroup()
        self.namestiAnimacije()
        self.editMode = True

    def namestiAnimacije(self):
        itemListAnim = QPropertyAnimation(self.ui.itemsList, b"maximumWidth")
        itemListAnim.setStartValue(0)
        itemListAnim.setEndValue(self.ui.itemsList.sizeHint().height())
        itemListAnim.setDuration(500)
        toolBarAnim = QPropertyAnimation(self.ui.toolBar, b"maximumHeight")
        toolBarAnim.setStartValue(0)
        toolBarAnim.setEndValue(self.ui.toolBar.sizeHint().height())
        toolBarAnim.setDuration(500)
        self.animGroup.addAnimation(itemListAnim)
        self.animGroup.addAnimation(toolBarAnim)

    def toogleEdit(self):
        if self.editMode:
            self.animGroup.setDirection(QParallelAnimationGroup.Direction.Backward)
            self.editMode = False
        else:
            self.animGroup.setDirection(QParallelAnimationGroup.Direction.Forward)
            self.editMode = True

        self.animGroup.start()

    def dodajMetoduCrtanja(self, icon, drawingMethod):
        btn = QPushButton(icon, "")
        btn.clicked.connect(lambda: self.drawing.namestiMetoduCrtanja(drawingMethod))
        self.ui.buttonsFrame.layout().addWidget(btn)

    def sliderValueChanged(self):
        self.drawing.namestiDebljinuLinije(self.ui.horizontalSlider.value())
