from PyQt6.QtWidgets import QWidget, QApplication
import sys

class Main(QWidget):
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = Main()
    mainWindow.show()

    sys.exit(app.exec())
