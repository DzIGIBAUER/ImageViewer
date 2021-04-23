from PyQt6.QtWidgets import QPushButton, QGraphicsScene, QGraphicsItemGroup, QGraphicsEllipseItem, QColorDialog
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QMouseEvent

class Drawing:
    # ove klase su drawingMethod
    class Point:
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.rad, self.pen, self.brush = None, None, None
            self.group = Group()

        def start(self, pos, rad, pen, brush):
            self.rad = rad
            self.pen = pen
            self.brush = brush
            self.dodajPoint(pos)
            return self.group

        def continue_(self, pos):
            self.dodajPoint(pos)

        def end(self):
            print("KRAJ")

        def dodajPoint(self, pos):
            x, y = pos.x(), pos.y()
            item = QGraphicsEllipseItem(x - self.rad, y - self.rad, self.rad * 2.0, self.rad * 2.0)
            item.setPen(self.pen)
            item.setBrush(self.brush)
            self.group.addToGroup(item)

    def __init__(self, graphicsView):
        self.graphicsView = graphicsView
        self.scene: QGraphicsScene = graphicsView.scene_
        self.pen = QPen(QColor("black"))
        self.brush = QBrush(QColor("black"))
        self.debljinaLinije = 1

        self.method = None  # Item koji crtamo koji ima metode potrebe za crtanje
        self.active = False

    def pokreni(self, event: QMouseEvent):
        if not self.method:
            return
        self.active = True
        self.graphicsView.setInteractive(False)
        pos = self.graphicsView.mapToScene(event.position().toPoint())
        itemGroup = self.method.start(pos, self.debljinaLinije, self.pen, self.brush)

        self.scene.addItem(itemGroup)
        self.graphicsView.imgControls.dodatItem.emit(itemGroup)

    def nastavi(self, event: QMouseEvent):
        if not self.active:
            return

        pos = self.graphicsView.mapToScene(event.position().toPoint())
        self.method.continue_(pos)

    def zavrsi(self):
        if self.active:
            self.active = False
            self.graphicsView.setInteractive(True)
            self.method = False

    def namestiDebljinuLinije(self, debljina):
        self.debljinaLinije = debljina or 0

    def izaberiPenBoju(self, clickedButton: QPushButton):
        color = QColorDialog.getColor(title="Izaberite pen boju")
        self.pen.setColor(color)
        clickedButton.setStyleSheet(f"background-color: {color.name()};")

    def izaberiBrushBoju(self, clickedButton: QPushButton):
        color = QColorDialog.getColor(title="Izaberite brush boju")
        self.brush.setColor(color)
        clickedButton.setStyleSheet(f"background-color: {color.name()};")

    def namestiMetoduCrtanja(self, drawingMethod):
        self.method = drawingMethod()

class Group(QGraphicsItemGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFlag(QGraphicsItemGroup.GraphicsItemFlags.ItemIsMovable |
                     QGraphicsItemGroup.GraphicsItemFlags.ItemIsSelectable)

    def paint(self, painter: QPainter, *args):
        if self.isSelected():
            painter.setPen(QColor("aqua"))
            painter.setBrush(QColor("transparent"))
            painter.drawRect(self.boundingRect())
        super().paint(painter, *args)
