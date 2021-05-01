from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtGui import (QResizeEvent, QPaintEvent, QMouseEvent, QWheelEvent, QPixmap, QColor, QPen, QBrush, QImage,
                         QPainter)
from PyQt6.QtCore import Qt, QRectF, QPointF, QPoint, pyqtSignal
from ImageViewerRepo.CustomWidgets.drawing import Drawing

class GraphicsView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.imgControls = args[0].parentWidget()
        self.pixmapItem = QGraphicsPixmapItem()
        self.pixmap = QPixmap()

        self.scene_ = QGraphicsScene()
        self.scene_.setBackgroundBrush(QBrush(QColor("white")))
        self.previewScene = QGraphicsScene()  # scena za renderovanje itema koji su onda prikazani sa desne strane
        self.setScene(self.scene_)

        self.drawing = Drawing(self)
        self.zoomLevel = 1.0
        self.zoomKorak = 0.1

        self.panPoint = None

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButtons.LeftButton:
            self.drawing.pokreni(event)
        elif event.button() == Qt.MouseButtons.MiddleButton:
            self.panPoint = event.position()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.drawing.nastavi(event)
        self.panView(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButtons.LeftButton:
            self.drawing.zavrsi()
        elif event.button() == Qt.MouseButtons.MiddleButton:
            self.panPoint = None

    def wheelEvent(self, event: QWheelEvent):
        super().wheelEvent(event)
        if event.angleDelta().y() > 0:
            nz = self.zoomLevel + self.zoomKorak
        else:
            nz = self.zoomLevel - self.zoomKorak

        self.scale(nz, nz)
        self.resizeEvent(QResizeEvent(self.size(), self.size()))

    def panView(self, event: QMouseEvent):
        if not self.panPoint:
            return

        razlika = self.panPoint - event.position()
        cRect = self.scene_.sceneRect()
        nRect = QRectF(cRect.x() + razlika.x(), cRect.y() + razlika.y(), cRect.width(), cRect.height())
        self.scene_.setSceneRect(nRect)
        self.panPoint = event.position()

    def renderScene(self, nacin):
        if nacin == 1:
            r = self.pixmapItem.pixmap().rect()
        elif nacin == 2:
            r = self.scene_.itemsBoundingRect().toRect()
        else:
            return

        pix = QPixmap(r.size())
        p = QPainter(pix)
        self.scene_.render(p, QRectF(pix.rect()), QRectF(r))
        return pix

    def sacuvajFajl(self, fileName, nacin):
        if nacin == 1:
            r = self.pixmapItem.pixmap().rect()
        elif nacin == 2:
            r = self.scene_.itemsBoundingRect().toRect()
        else:
            return
        img = QImage(r.size(), QImage.Format.Format_A2BGR30_Premultiplied)
        p = QPainter(img)
        self.scene_.render(p, QRectF(img.rect()), QRectF(r))
        p.end()
        img.save(f"{fileName}.png")

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        pos = self.pixmapItem.scenePos()
        p = self.pixmapItem.pixmap()
        w, h = p.width(), p.height()
        self.centerOn(pos.x() + w / 2, pos.y() + h / 2)

    def namestiSliku(self, image):
        pixmap = QPixmap(image)

        pixmapItem = QGraphicsPixmapItem(pixmap)

        w, h = pixmap.width(), pixmap.height()
        self.scene_.setSceneRect(QRectF(-w / 2, -h / 2, w * 2, h * 2))
        pixmapItem.setTransformOriginPoint(w / 2, h / 2)
        pixmapItem.setPos(0, 0)

        self.scene_.addItem(pixmapItem)
        self.pixmapItem = pixmapItem
        self.pixmap = pixmap
