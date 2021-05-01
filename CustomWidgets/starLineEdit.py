from PyQt6.QtWidgets import QLineEdit, QCheckBox

class StarLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.raw = None
        self.checkBox = None
        self.textEdited.connect(self._textEdited)

    def poveziCheckBox(self, checkBox: QCheckBox):
        checkBox.toggled.connect(self.togglePrikaz)
        self.checkBox = checkBox

    def togglePrikaz(self):
        if self.checkBox.isChecked():
            self.prikazi()
        else:
            self.sakrij()

    def sakrij(self):
        super().setText("*" * len(self.raw))

    def prikazi(self):
        super().setText(self.raw)

    def _textEdited(self, text):
        if not self.checkBox.isChecked():
            self.sakrij()
        else:
            self.setText(text)

    def setText(self, text):
        super().setText(text)
        self.raw = text
        self.togglePrikaz()

