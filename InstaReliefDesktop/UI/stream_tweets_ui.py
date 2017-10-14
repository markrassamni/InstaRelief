from PyQt5.QtWidgets import *
from PyQt5.QtGui import QTextCursor
import pyrebase
from PyQt5.QtCore import QTimer
import time

config = {
  "apiKey": "AIzaSyAFjbldaX_ZJw_yOLahlYJNFtlBbxP8hTg",
  "authDomain": "ngcode-9f40c.firebaseapp.com",
  "databaseURL": "https://ngcode-9f40c.firebaseio.com",
  "storageBucket": "ngcode-9f40c.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

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

        self.pullTweetsFromBase()

    def add_tweet(self, name, text, time):
        self.logOutput.moveCursor(QTextCursor.End)
        self.logOutput.append(name+" tweeted: " + text + " at: " + time)
        sb = self.logOutput.verticalScrollBar()
        sb.setValue(sb.maximum())

    def add_basic_tweet(self, text):
        self.logOutput.moveCursor(QTextCursor.End)
        text = str(text)
        self.logOutput.append(text)
        sb = self.logOutput.verticalScrollBar()
        b = self.logOutput.horizontalScrollBar()
        sb.setValue(sb.maximum())
        b.setValue(b.minimum())
        time.sleep(.1)


    def pullTweetsFromBase(self):
        my_stream = db.child("Tweets").stream(self.stream_handler)

    def stream_handler(self, message):
        screen.add_basic_tweet(message)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    screen = Form()
    screen.show()

    sys.exit(app.exec_())
