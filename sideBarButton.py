from PyQt6.QtWidgets import QApplication, QPushButton, QSizePolicy
from PyQt6.QtGui import QPixmap, QPainter, QFontMetrics, QIcon
from PyQt6.QtCore import Qt, QRect, QSize, QPropertyAnimation

class SideBarButton(QPushButton):
    def __init__(self, *args, **kwargs):
        if type(args[0]) is QIcon:  # ako smo dobili ikonicu kao prvi argument cuvamo je
            self.icon = args[0]
            sargs = args[1:]  # QPushButton-u dajemo sve sem ikonice
        else:
            sargs = args

        super().__init__(*sargs, **kwargs)

        self.iconRect = QRect(0, 0, 35, 35)

        sp = self.sizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
        self.setSizePolicy(sp)

        self.setMinimumSize(self.iconRect.size())

        self.setStyleSheet(f"padding: 3px 5px 3px {self.iconRect.width()}px;")

    def animiraj(self):
        self.a = QPropertyAnimation(self, b"maximumSize")
        self.a.setDuration(500)
        self.a.setStartValue(self.size())
        self.a.setEndValue(self.iconRect.size())
        print(self.size(), self.iconRect.size())
        self.a.start()

    def shrink(self):
        self.setMaximumSize(self.iconRect.size())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        sirina = event.size().width() - self.iconRect.width()
        sirinaHint = self.sizeHint().width() - self.iconRect.width()
        self.setVidljivostTexta(sirina / sirinaHint)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        self.crtajIkonicu(painter)

    def crtajIkonicu(self, p):
        if not self.icon:
            return

        pixmap = self.icon.pixmap(self.iconRect.size() - QSize(4, 4))

        y = self.iconRect.height() // 2 - pixmap.height() // 2

        p.drawPixmap(2, y, pixmap)

    def setIcon(self, icon):
        self.icon = icon

    def setVidljivostTexta(self, opacity):
        if opacity > 1:  # ne moze da bude vece od 1 ili manje od 0
            opacity = 1
        elif opacity < 0:
            opacity = 0
        self.setStyleSheet(f"{self.styleSheet()}color: rgba(0, 0, 0, {opacity});")
