from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QPropertyAnimation, QParallelAnimationGroup
from ImageViewerRepo.UI.imageControlsUI import Ui_imageControls

class ImageControls(QWidget):
    def __init__(self, main, image, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_imageControls()
        self.ui.setupUi(self)
        self.lastGridPos = [-1, 0]  # da bih znao gde da stavim dugme
        self.drawing = self.ui.graphicsView.drawing

        self.ui.graphicsView.namestiSliku(image)

        self.ui.penColorSelect.clicked.connect(lambda: self.drawing.izaberiPenBoju(self.ui.penColorSelect))
        self.ui.penColorSelect.setStyleSheet(f"background-color: {self.drawing.pen.color().name()}")

        self.ui.brushColorSelect.clicked.connect(lambda: self.drawing.izaberiBrushBoju(self.ui.brushColorSelect))
        self.ui.brushColorSelect.setStyleSheet(f"background-color: {self.drawing.brush.color().name()}")

        self.ui.horizontalSlider.valueChanged.connect(self.sliderValueChanged)

        self.dodajMetoduCrtanja(self.drawing.Point, QIcon("icons:exit.png"))
        self.dodajMetoduCrtanja(self.drawing.Line, QIcon("icons:mainIcon.ico"))
        self.dodajMetoduCrtanja(self.drawing.Image, QIcon("icons:home.png"))

        self.animGroup = QParallelAnimationGroup()
        self.namestiAnimacije()
        self.editMode = False

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

    def toggleEdit(self):
        if self.editMode:
            self.animGroup.setDirection(QParallelAnimationGroup.Direction.Backward)
            self.editMode = False
        else:
            self.animGroup.setDirection(QParallelAnimationGroup.Direction.Forward)
            self.editMode = True

        self.animGroup.start()

    def dodajMetoduCrtanja(self, drawingMethod, icon=None, text=None):
        btn = QPushButton(icon, text)
        btn.clicked.connect(lambda: self.drawing.namestiMetoduCrtanja(drawingMethod))
        lyt = self.ui.buttonsFrame.layout()

        # ovo redja ikonice za crtanje
        if self.lastGridPos[0] >= self.lastGridPos[1]:
            self.lastGridPos[1] += 1
        elif self.lastGridPos[0] < self.lastGridPos[1]:
            self.lastGridPos[0] += 1
        rc, cc = self.lastGridPos[0], self.lastGridPos[1]

        lyt.addWidget(btn, rc, cc)


    def sliderValueChanged(self):
        self.drawing.namestiDebljinuLinije(self.ui.horizontalSlider.value())
