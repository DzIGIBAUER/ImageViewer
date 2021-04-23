from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtGui import QResizeEvent, QPaintEvent, QMouseEvent, QPixmap, QColor, QPen, QBrush, QImage, QPainter
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal
from ImageViewerRepo.CustomWidgets.drawing import Drawing

class GraphicsView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.imgControls = args[0].parentWidget()
        self.pixmapItem = QGraphicsPixmapItem()
        self.pixmap = QPixmap()

        self.scene_ = QGraphicsScene()
        self.previewScene = QGraphicsScene()  # scena za renderovanje itema koji su onda prikazani sa desne strane
        self.setScene(self.scene_)

        self.drawing = Drawing(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButtons.LeftButton:
            self.drawing.pokreni(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.drawing.nastavi(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButtons.LeftButton:
            self.drawing.zavrsi()

    def sacuvaj(self):
        r = self.pixmapItem.pixmap().rect()
        img = QImage(r.size(), QImage.Format.Format_A2BGR30_Premultiplied)
        p = QPainter(img)
        self.scene_.render(p, QRectF(img.rect()), QRectF(r))
        p.end()
        img.save("resi.png")

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
