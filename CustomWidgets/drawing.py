from PyQt6.QtWidgets import QPushButton, QGraphicsScene, QGraphicsItemGroup, QGraphicsEllipseItem, QColorDialog, QLabel
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QMouseEvent, QPixmap, QPainterPath
from PyQt6.QtCore import pyqtSignal, Qt, QPointF

class ItemPreview(QLabel):
    itemUpdated = pyqtSignal(QPixmap)

    def __init__(self, glavnaScena, item, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(50, 50)
        self.item = item
        self.glavnaScena: QGraphicsScene = glavnaScena

    def updatePreview(self, pixmap):
        scaledPixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.setPixmap(scaledPixmap)

    def mousePressEvent(self, event: QMouseEvent):
        rect = self.item.boundingRect()
        path = QPainterPath(QPointF(rect.x(), rect.y()))
        path.addRect(1, 1, 1, 1)
        self.glavnaScena.setSelectionArea(path)

# ovu klasu inherituje svaki drawingMethod
class Item:
    def __init__(self, glavnaScena):
        self.debljinaLinije, self.pen, self.brush = None, None, None
        self.group = Group()
        self.previewScene = QGraphicsScene()
        self.previewScene.setBackgroundBrush(QBrush(QColor("white")))
        self.previewItem = ItemPreview(glavnaScena, self.group)

    def itemPreview(self):
        pv = self.previewItem.size()
        pix = QPixmap(pv.width(), pv.height())
        p = QPainter(pix)
        self.previewScene.render(p, self.previewScene.sceneRect())
        return pix

class Drawing:
    # ove klase su drawingMethod
    class Point(Item):
        def __init__(self, scena):
            super().__init__(scena)

        def start(self, pos, rad, pen, brush):
            self.debljinaLinije = rad
            self.pen = pen
            self.brush = brush
            self.dodajPoint(pos)
            return self.group

        def continue_(self, pos):
            self.dodajPoint(pos)

        def end(self):
            self.previewScene.addItem(self.group)
            self.previewItem.updatePreview(self.itemPreview())
            return self.group

        def dodajPoint(self, pos):
            x, y = pos.x(), pos.y()
            rad = self.debljinaLinije

            item = QGraphicsEllipseItem(x - rad, y - rad, rad * 2.0, rad * 2.0)
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
        self.scene.clearSelection()
        pos = self.graphicsView.mapToScene(event.position().toPoint())
        itemGroup = self.method.start(pos, self.debljinaLinije, self.pen, self.brush)
        self.graphicsView.imgControls.ui.itemsList.layout().insertWidget(0, self.method.previewItem)

        self.scene.addItem(itemGroup)

    def nastavi(self, event: QMouseEvent):
        if not self.active:
            return

        pos = self.graphicsView.mapToScene(event.position().toPoint())
        self.method.continue_(pos)

    def zavrsi(self):
        if self.active:
            self.active = False
            self.graphicsView.setInteractive(True)
            item = self.method.end()
            self.scene.addItem(item)
            self.method = None

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
        self.method = drawingMethod(self.scene)

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
