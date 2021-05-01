# Form implementation generated from reading ui file '..\UI\mainWindow.ui'
#
# Created by: PyQt6 UI code generator 6.0.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(652, 469)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setAutoFillBackground(False)
        self.centralWidget.setStyleSheet("#centralWidget{background-color: rgb(97, 97, 97);}")
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sideBar = SideBar(self.centralWidget)
        self.sideBar.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sideBar.sizePolicy().hasHeightForWidth())
        self.sideBar.setSizePolicy(sizePolicy)
        self.sideBar.setMinimumSize(QtCore.QSize(0, 0))
        self.sideBar.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.sideBar.setStyleSheet("#sideBar{\n"
"    background-color: rgb(49, 203, 0);\n"
"}\n"
"\n"
"QPushButton{\n"
"    border: 1px solid orange;\n"
"    border-radius: 2px;\n"
"    background-color: rgb(35, 152, 0);\n"
"}")
        self.sideBar.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.sideBar.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.sideBar.setLineWidth(0)
        self.sideBar.setObjectName("sideBar")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.sideBar)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.sideBar)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralWidget)
        self.stackedWidget.setStyleSheet("QLabel{ font-size: 15px; }\n"
"#frame_2, #upsLista { border: 1px solid orange; }\n"
"#frame_3, #frame {border-top: 1px solid orange}")
        self.stackedWidget.setObjectName("stackedWidget")
        self.main = QtWidgets.QWidget()
        self.main.setObjectName("main")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main)
        self.verticalLayout.setObjectName("verticalLayout")
        self.upsLista = QtWidgets.QScrollArea(self.main)
        self.upsLista.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.upsLista.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.upsLista.setWidgetResizable(True)
        self.upsLista.setObjectName("upsLista")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 134, 59))
        self.scrollAreaWidgetContents.setStyleSheet("background-color: rgb(97, 97, 97)")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setContentsMargins(-1, 9, -1, 0)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.upsLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.upsLabel.setObjectName("upsLabel")
        self.verticalLayout_3.addWidget(self.upsLabel)
        self.frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3.addWidget(self.frame)
        spacerItem1 = QtWidgets.QSpacerItem(20, 77, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.upsLista.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.upsLista)
        self.stackedWidget.addWidget(self.main)
        self.podesavanja = QtWidgets.QWidget()
        self.podesavanja.setStyleSheet("")
        self.podesavanja.setObjectName("podesavanja")
        self.gridLayout = QtWidgets.QGridLayout(self.podesavanja)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.podesavanja)
        self.label.setStyleSheet("color: orange")
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 1, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.podesavanja)
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.pushButtonSacuvaj = QtWidgets.QPushButton(self.frame_4)
        self.pushButtonSacuvaj.setObjectName("pushButtonSacuvaj")
        self.horizontalLayout_5.addWidget(self.pushButtonSacuvaj)
        self.gridLayout.addWidget(self.frame_4, 4, 1, 1, 1)
        self.labelClientID = QtWidgets.QLabel(self.podesavanja)
        self.labelClientID.setObjectName("labelClientID")
        self.gridLayout.addWidget(self.labelClientID, 0, 0, 1, 1)
        self.lineEditClientID = StarLineEdit(self.podesavanja)
        self.lineEditClientID.setObjectName("lineEditClientID")
        self.gridLayout.addWidget(self.lineEditClientID, 0, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem3, 3, 0, 1, 2)
        self.checkBox = QtWidgets.QCheckBox(self.podesavanja)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 1, 1, 1, 1)
        self.stackedWidget.addWidget(self.podesavanja)
        self.tb = QtWidgets.QWidget()
        self.tb.setObjectName("tb")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tb)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.tb)
        self.tabWidget.setStyleSheet("QTabWidget::pane{\n"
"    border-top: 2px solid #C2C7CB;\n"
"}\n"
"QTabBar::tab{\n"
"    border: 1px solid red;\n"
"    padding: 5px;\n"
"    background-color: rgb(51, 167, 255);\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(49, 203, 0, 255), stop:1                     rgba(34, 135, 0, 255));\n"
"}\n"
"QTabBar::tab:selected{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(51, 124, 160, 255), stop:1 rgba(34, 135, 0, 255));\n"
"}")
        self.tabWidget.setObjectName("tabWidget")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        self.stackedWidget.addWidget(self.tb)
        self.horizontalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar_2 = QtWidgets.QMenuBar(MainWindow)
        self.menuBar_2.setGeometry(QtCore.QRect(0, 0, 652, 21))
        self.menuBar_2.setObjectName("menuBar_2")
        self.menuFile = QtWidgets.QMenu(self.menuBar_2)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menuBar_2)
        self.actionnest = QtGui.QAction(MainWindow)
        self.actionnest.setObjectName("actionnest")
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionUpload = QtGui.QAction(MainWindow)
        self.actionUpload.setObjectName("actionUpload")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionUpload)
        self.menuBar_2.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(2)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.upsLabel.setText(_translate("MainWindow", "Uploadovane Slike"))
        self.label.setText(_translate("MainWindow", "Client ID vam nije potreban za anonimno upload-ovanje slika ali vam je potreban za brisanje istih pomoću kljuca koji dobijete prilikom upload-a i koji aplikacija čuva."))
        self.pushButtonSacuvaj.setText(_translate("MainWindow", "Sacuvaj"))
        self.labelClientID.setText(_translate("MainWindow", "Client ID"))
        self.checkBox.setText(_translate("MainWindow", "Prikaži"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionnest.setText(_translate("MainWindow", "nest"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionUpload.setText(_translate("MainWindow", "Upload"))
from ImageViewerRepo.CustomWidgets.sideBar import SideBar
from ImageViewerRepo.CustomWidgets.starLineEdit import StarLineEdit


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
