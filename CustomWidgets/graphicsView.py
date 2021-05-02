from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFileDialog
from PyQt6.QtGui import (QResizeEvent, QMouseEvent, QKeyEvent, QWheelEvent, QPixmap, QColor, QBrush, QImage,
                         QPainter)
from PyQt6.QtCore import Qt, QRectF, pyqtSignal
from CustomWidgets.drawing import Drawing
from enum import Enum

class GraphicsView(QGraphicsView):
    class NacinEnum(Enum):
        slika = 1
        items = 2
        custom = 3

    dimenzijeIzabrane = pyqtSignal(QRectF)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.imgControls = args[0].parentWidget()
        self.pixmapItem = QGraphicsPixmapItem()
        self.pixmap = QPixmap()
        self.scene_ = QGraphicsScene()
        self.scene_.setBackgroundBrush(QBrush(QColor("white")))
        self.previewScene = QGraphicsScene()  # scena za renderovanje itema koji su onda prikazani sa desne strane
        self.setScene(self.scene_)

        # metoda koja ceka dimenzije koje biramo kada cuvamo ili upload-ujemo slike, nemstamo po potrebi
        self.waitingCallback = None
        self.dimenzijeIzabrane.connect(self.dimenzijaIzabrana)

        self.drawing = Drawing(self)
        self.zoomLevel = 1.0
        self.zoomKorak = 0.1

        self.panPoint = None

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def keyReleaseEvent(self, event: QKeyEvent):
        if (event.keyCombination().key() == Qt.Key.Key_Z and
                event.keyCombination().keyboardModifiers() == Qt.KeyboardModifiers.ControlModifier):
            function_ = self.drawing.undoList.pop()
            function_()

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

    '''
    renderuje deo scene u zavisnosti od nacina koji je prosledjen
    dimenzije su potrebne ako je nacin NacinEnum.custom, a ako nisu prosledjenje bice pokrenuta metoda crtanja
    Rect-a kako bi korisnik izabrao dimenzije i onda ce ista funkcija biti pozvana samo sto sada imamo dimenzije.
    Drawing method ce emit-ovati signal koji joj je prosledjen
    '''
    def renderScene(self, nacin, dimenzije=None):
        if nacin == self.NacinEnum.slika:
            r = self.pixmapItem.pixmap().rect()
        elif nacin == self.NacinEnum.items:
            r = self.scene_.itemsBoundingRect().toRect()
        elif nacin == self.NacinEnum.custom:

            if not dimenzije:
                self.izaberiDimenzije()
                return
            r = dimenzije.toRect()
        else:
            return
        pix = QPixmap(r.size())
        p = QPainter(pix)
        self.scene_.render(p, QRectF(pix.rect()), QRectF(r))
        print(pix)
        return pix

    def spremiUpload(self, callback):
        self.waitingCallback = callback
        self.izaberiDimenzije()

    def uploadSpreman(self, dimenzije):
        self.waitingCallback(self.NacinEnum.custom, dimenzije)
        self.waitingCallback = None

    def izaberiDimenzije(self):
        self.drawing.namestiMetoduCrtanja(self.drawing.Rect, self.dimenzijeIzabrane)

    ''' ova metoda slusa za zavrsenje biranje dimenzija slike koju treba da renderujemo u renderScene'''
    def dimenzijaIzabrana(self, dimenzije):
        self.uploadSpreman(dimenzije)


    def sacuvajFajl(self, nacin, dimenzije=None):
        if nacin == self.NacinEnum.custom:
            if not dimenzije:
                # ovu funkciju ce pozvati dimenzijaIzabrana kada dobije dimenzije
                self.waitingCallback = self.sacuvajFajl
                self.renderScene(nacin)
                return  # nista ne radi dalje, radi cemo kada dobijemo dimenzije
            else:
                self.waitingCallback = None
                pixmap = self.renderScene(nacin, dimenzije)
        else:
            print("sta saljem", nacin)
            pixmap = self.renderScene(nacin)
            print("evo ga", pixmap)

        fileName, _ = QFileDialog.getSaveFileName(self, "Sacuvajte fajl")
        if not fileName:
            return
        pixmap.save(f"{fileName}.png")


    def sacuvajFajll(self, nacin, dimenzije=None):  # dimenzije su namestene samo ako je nacin == NacinEnum.custom
        if nacin == self.NacinEnum.slika:
            r = self.pixmapItem.pixmap().rect()
        elif nacin == self.NacinEnum.items:
            r = self.scene_.itemsBoundingRect().toRect()
        elif nacin == self.NacinEnum.custom:
            if not dimenzije:
                self.drawing.namestiMetoduCrtanja(self.drawing.Rect, self.dimenzijeIzabrane)
                return
            r = dimenzije.toRect()
        else:
            return

        fileName, _ = QFileDialog.getSaveFileName(self, "Sacuvajte fajl")
        if not fileName:
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
