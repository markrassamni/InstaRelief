from PyQt5.QtWidgets import *
from PyQt5.QtGui import QTextCursor


class Form(QWidget):

    def __init__(self, *args):
        QWidget.__init__(self, *args)

        self.setWindowTitle('Tweet Stream')

        self.logOutput = QTextEdit()
        self.logOutput.setReadOnly(True)
        self.logOutput.setLineWrapMode(QTextEdit.NoWrap)
        self.setMinimumWidth(600)
        font = self.logOutput.font()
        font.setFamily("Courier")
        font.setPointSize(10)

        self.theLayout = QVBoxLayout(self)
        self.theLayout.addWidget(self.logOutput)
        self.setLayout(self.theLayout)

    def add_tweet(self, name, text, time):
        self.logOutput.moveCursor(QTextCursor.End)
        self.logOutput.append(name+" tweeted: " + text + " at: " + time)
        sb = self.logOutput.verticalScrollBar()
        sb.setValue(sb.maximum())


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    screen = Form()
    screen.show()
    screen.add_tweet("Mark Something", "Fire's burning and a roaring blah blah blah blah !", "2pm april 20th yeee")

    sys.exit(app.exec_())
