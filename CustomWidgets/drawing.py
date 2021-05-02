from PyQt6.QtWidgets import (QPushButton, QGraphicsScene, QGraphicsItemGroup, QGraphicsEllipseItem,
                             QColorDialog, QLabel, QGraphicsLineItem, QGraphicsPixmapItem, QFileDialog,
                             QGraphicsRectItem)
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QMouseEvent, QPaintEvent, QPixmap
from PyQt6.QtCore import pyqtSignal, Qt, QPointF, QRectF


class ItemPreview(QLabel):
    itemUpdated = pyqtSignal(QPixmap)

    def __init__(self, item, glavnaScena, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(50, 50)
        self.item = item
        self.glavnaScena: QGraphicsScene = glavnaScena
        self.glavnaScena.selectionChanged.connect(self.promenjenaSelekcija)

    def updatePreview(self, pixmap):
        self.setPixmap(pixmap)

    def promenjenaSelekcija(self):
        self.repaint()

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)
        if self.item.isSelected():
            p = QPainter(self)
            sz = self.size()
            p.setPen(QColor("aqua"))
            p.drawRect(0, 0, sz.width() - 1, sz.height() - 1)

    def mousePressEvent(self, event: QMouseEvent):
        if self.item.isSelected():
            self.item.setSelected(False)
        else:
            self.item.setSelected(True)


# ovu klasu inherituje svaki drawingMethod
class Item:
    def __init__(self, glavnaScena, signal=None, callback=None):
        self.debljinaLinije, self.pen, self.brush = None, None, None
        self.group = Group()
        self.signal = signal
        self.callback = callback
        # ne korisimo previewScene trenutno, pogledaj ispod
        self.previewScene = QGraphicsScene()
        # self.previewScene.setBackgroundBrush(QBrush(QColor("white")))
        self.previewItem = ItemPreview(self.group, glavnaScena)

    def end(self):
        self.previewScene.addItem(self.group)
        self.previewItem.updatePreview(self.itemPreview())
        return self.group

    # FIXME: slike su nikakve nmp sto, dok se ne popravi redefinisi ovu metodu
    def itemPreview(self):
        pv = self.previewItem.size()
        pix = QPixmap(pv.width(), pv.height())
        p = QPainter(pix)
        self.previewScene.render(p, self.previewScene.sceneRect())
        return pix


class Drawing:
    # ove klase su drawingMethod
    class Rect(Item):
        def start(self, pos, *_):
            self.konstruisiRect(pos)
            return self.group

        def continue_(self, pos):
            item: QGraphicsRectItem = self.group.childItems()[0]
            x, y = item.pos().x(), item.pos().y()
            w, h = abs(pos.x() - x), abs(pos.y() - y)
            item.setRect(0, 0, w, h)

        def end(self):
            if not self.signal:
                super().end()
                return
            itm = self.group.childItems()[0]
            br = itm.boundingRect().size()

            r = QRectF(itm.x(), itm.y(), br.width(), br.height())
            self.signal.emit(r)
            [self.group.removeFromGroup(item) for item in self.group.childItems()]

        def konstruisiRect(self, pos):
            item = QGraphicsRectItem(0, 0, 0, 0)
            item.setPos(pos)
            self.group.addToGroup(item)

    class Image(Item):
        def __init__(self, gs):
            super().__init__(gs)
            self.imgPath, _ = QFileDialog.getOpenFileName(caption="Izaberite sliku")

            if self.imgPath:
                self.pixmap = QPixmap(self.imgPath)

        def start(self, pos, *_):
            if self.pixmap.isNull():
                return

            self.konstruisiSliku(self.pixmap, pos)
            return self.group

        def continue_(self, pos):
            item: QGraphicsPixmapItem = self.group.childItems()[0]
            w, h = abs(pos.x() - item.pos().x()), abs(pos.y() - item.pos().y())
            item.setPixmap(self.pixmap.scaled(w, h, Qt.AspectRatioMode.IgnoreAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation))

        def konstruisiSliku(self, pixmap, pos):
            item = QGraphicsPixmapItem(pixmap.scaled(1, 1, Qt.AspectRatioMode.IgnoreAspectRatio,
                                                     Qt.TransformationMode.SmoothTransformation))
            item.setPos(pos.x(), pos.y())
            self.group.addToGroup(item)

    class Line(Item):
        def start(self, pos, debljinaLinije, pen, brush):
            self.debljinaLinije = debljinaLinije
            self.pen = pen
            self.brush = brush
            self.konstruisiLiniju(pos)
            return self.group

        def continue_(self, pos):
            self.namestiKranjuTacku(pos)

        def konstruisiLiniju(self, pos):
            for i in range(self.debljinaLinije):
                x, y = pos.x(), pos.y()
                item = QGraphicsLineItem(x, y + i, x + 1, y + 1)
                item.setPen(self.pen)
                self.group.addToGroup(item)

        def namestiKranjuTacku(self, pos):
            for idx, lineItem in enumerate(self.group.childItems()):
                line = lineItem.line()
                line.setP1(QPointF(line.x1(), line.y1()))
                line.setP2(QPointF(pos.x(), pos.y() + idx))
                lineItem.setLine(line)

        def itemPreview(self):
            ps = self.previewItem.size()
            pix = QPixmap(ps)
            p = QPainter(pix)
            p.setBackgroundMode(Qt.BGMode.OpaqueMode)
            p.setPen(self.pen)
            p.setBackground(self.brush)
            p.drawText(0, 0, ps.width(), ps.height(), Qt.Alignment.AlignCenter, "Line")
            return pix

    class Point(Item):
        # self.item je u ovoj klasi Group
        def start(self, pos, rad, pen, brush):
            self.group = Group()
            self.debljinaLinije = rad
            self.pen = pen
            self.brush = brush
            self.dodajPoint(pos)
            return self.group

        def continue_(self, pos):
            self.dodajPoint(pos)

        def dodajPoint(self, pos):
            x, y = pos.x(), pos.y()
            rad = self.debljinaLinije

            point = QGraphicsEllipseItem(x - rad, y - rad, rad * 2.0, rad * 2.0)
            point.setPen(self.pen)
            point.setBrush(self.brush)

            self.group.addToGroup(point)

        def itemPreview(self):
            ps = self.previewItem.size()
            pix = QPixmap(ps)
            p = QPainter(pix)
            p.setBackgroundMode(Qt.BGMode.OpaqueMode)
            p.setPen(self.pen)
            p.setBackground(self.brush)
            p.drawText(0, 0, ps.width(), ps.height(), Qt.Alignment.AlignCenter, "Point")
            return pix

    def __init__(self, graphicsView):
        self.graphicsView = graphicsView
        self.scene: QGraphicsScene = graphicsView.scene_
        self.pen = QPen(QColor("black"))
        self.brush = QBrush(QColor("black"))
        self.debljinaLinije = 1

        self.undoList = []

        self.method = None  # ima metode potrebe za crtanje
        self.active = False

    def pokreni(self, event: QMouseEvent):
        if not self.method:
            return
        self.active = True
        self.graphicsView.setInteractive(False)
        self.scene.clearSelection()
        pos = self.graphicsView.mapToScene(event.position().toPoint())
        item = self.method.start(pos, self.debljinaLinije, self.pen, self.brush)
        if not item:
            self.active = False
            return
        self.graphicsView.imgControls.ui.itemsList.layout().insertWidget(0, self.method.previewItem)


        self.scene.addItem(item)

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
            if item:
                self.scene.addItem(item)
                self.undoList.append(lambda: self.scene.removeItem(item))
            self.method = None

    def namestiDebljinuLinije(self, debljina):
        self.debljinaLinije = debljina or 0

    def izaberiPenBoju(self, clickedButton: QPushButton):
        color = QColorDialog.getColor(title="Izaberite pen boju", initial=self.pen.color())
        self.pen.setColor(color)
        clickedButton.setStyleSheet(f"background-color: {color.name()};")

    def izaberiBrushBoju(self, clickedButton: QPushButton):
        color = QColorDialog.getColor(title="Izaberite brush boju", initial=self.brush.color())
        self.brush.setColor(color)
        clickedButton.setStyleSheet(f"background-color: {color.name()};")

    # signal ce biti pozvan kada se zavrsi crtanje, a funkcija koje slusa signal ce na kraju da pozove callback
    def namestiMetoduCrtanja(self, drawingMethod, signal=None, callback=None):
        self.method = drawingMethod(self.scene, signal, callback)


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
