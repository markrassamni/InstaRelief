from PyQt5 import QtCore, QtGui
import pyqtgraph as pg
from InstaReliefDesktop.Mapping.mapper import Mapper
from InstaReliefDesktop.UI.mapping_ui import Mapping_Ui
from InstaReliefDesktop.UI.insta_relief_ui import Ui_MainWindow

import sys

def main():
    app = QtGui.QApplication([])

    app.setStyle(QtGui.QStyleFactory.create("plastique"))
    pal = QtGui.QPalette()
    pal.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 255, 255))
    pal.setColor(QtGui.QPalette.Base, QtGui.QColor(15, 15, 15))
    pal.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    pal.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(255, 255, 255))
    pal.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(255, 255, 255))
    pal.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 255, 255))
    pal.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    pal.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255, 255, 255))
    pal.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(255, 255, 255))
    pal.setColor(QtGui.QPalette.BrightText, QtGui.QColor(255, 0, 0))
    pal.setColor(QtGui.QPalette.Highlight, QtGui.QColor(144, 216, 255).darker())
    app.setPalette(pal)
    app.setStyleSheet("QSeparator { foreground-color: white }")


    mapper = Mapper('AIzaSyDW6MkN0YmFQd2m3XD7ySG0GbsqcQDd5TE')
    mapping_window = Mapping_Ui(mapper)
    mapping_window.resize(800,800)
    mapping_window.generate_map()
    mapping_window.show()
    mapping_window.setWindowTitle('Insta-Relief')
    QtGui.QApplication.instance().exec_()

main()

