# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'insta-relief.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1618, 645)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.interactlayout = QtWidgets.QHBoxLayout()
        self.interactlayout.setObjectName("interactlayout")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.firefighter_button = QtWidgets.QPushButton(self.centralwidget)
        self.firefighter_button.setObjectName("firefighter_button")
        self.verticalLayout_8.addWidget(self.firefighter_button)
        self.swat_button = QtWidgets.QPushButton(self.centralwidget)
        self.swat_button.setObjectName("swat_button")
        self.verticalLayout_8.addWidget(self.swat_button)
        self.coastguard_button = QtWidgets.QPushButton(self.centralwidget)
        self.coastguard_button.setObjectName("coastguard_button")
        self.verticalLayout_8.addWidget(self.coastguard_button)
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setObjectName("spinBox")
        self.verticalLayout_8.addWidget(self.spinBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_8.addWidget(self.plainTextEdit)
        self.interactlayout.addLayout(self.verticalLayout_8)
        self.horizontalLayout.addLayout(self.interactlayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.maplayout = QtWidgets.QHBoxLayout()
        self.maplayout.setObjectName("maplayout")
        self.horizontalLayout.addLayout(self.maplayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.firefighter_button.setText(_translate("MainWindow", "Fire Fighters"))
        self.swat_button.setText(_translate("MainWindow", "Swat"))
        self.coastguard_button.setText(_translate("MainWindow", "Coast Guard"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

