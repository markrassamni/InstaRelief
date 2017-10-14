from PyQt5.QtWidgets import *
from PyQt5.QtGui import QTextCursor
import pyrebase
import json

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


    def pullTweetsFromBase(self):
        my_stream = db.child("Tweets").stream(self.stream_handler)

    def stream_handler(self, message):
        print(message)
        current_name = message['name']
        current_text = message['text']
        current_time = message['user']['created_at']
        screen.add_tweet(current_name, current_text, current_time)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    screen = Form()
    screen.show()

    sys.exit(app.exec_())
