from InstaReliefDesktop.Mapping.mapper import Mapper
from InstaReliefDesktop.UI.insta_relief_ui import Ui_MainWindow
from PyQt5 import QtGui, QtCore,QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime
import cv2
from imgurpython import ImgurClient
import configparser
import glob
import pyrebase
import time
import random

config = {
  "apiKey": "AIzaSyAFjbldaX_ZJw_yOLahlYJNFtlBbxP8hTg",
  "authDomain": "ngcode-9f40c.firebaseapp.com",
  "databaseURL": "https://ngcode-9f40c.firebaseio.com",
  "storageBucket": "ngcode-9f40c.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

class Mapping_Ui(QtWidgets.QMainWindow):
    def __init__(self, mapper):
        super(Mapping_Ui, self).__init__(None)
        self.mapper = mapper
        self.ui_mainwindow = Ui_MainWindow()
        self.ui_mainwindow.setupUi(self)

        self.button_pressed = False

        self.fig = plt.figure(figsize=(7,7))
        self.ax = self.fig.add_subplot(111)
        self.image = None
        self.first = True

        self.total_fire_fighters = 20
        self.total_swat = 10
        self.total_coast_guard = 5
        self.ui_mainwindow.firefighter_button.setText(str(self.total_fire_fighters)+' Fire Fighters')
        self.ui_mainwindow.swat_button.setText(str(self.total_swat)+' Swat Teams')
        self.ui_mainwindow.coastguard_button.setText(str(self.total_coast_guard)+' Coast Guard Teams')
        self.ui_mainwindow.firefighter_button.clicked.connect(self.firefighter_button_clicked)
        self.ui_mainwindow.swat_button.clicked.connect(self.swat_button_clicked)
        self.ui_mainwindow.coastguard_button.clicked.connect(self.coastguard_button_clicked)
        self.ui_mainwindow.generatemap_button.clicked.connect(self.generate_map)
        self.ui_mainwindow.uploadmap_button.clicked.connect(self.upload_map)

        self.setWindowTitle('Insta Relief')

        self.fire_cmap = self.transparent_cmap(plt.cm.Reds)
        self.zombie_cmap = self.transparent_cmap(plt.cm.Greens)
        self.water_cmap = self.transparent_cmap(plt.cm.Blues)

        self.addresses = ['1800 Rosecrans Ave', '2213 Warfield Ave', '2617 Manhattan Beach Blvd']
        self.cities = ['Manhattan Beach', 'Redondo Beach', 'Redondo Beach']
        self.types = ['Zombie', 'Fire', 'Hurricane']

        self.canvas = None
        self.setMouseTracking(True)

        self.config = configparser.ConfigParser()
        self.config.read('/home/ryan/yokosuka/auth.ini')
        self.client_id = self.config.get('credentials', 'client_id')
        self.client_secret = self.config.get('credentials', 'client_secret')

        self.client = ImgurClient(self.client_id, self.client_secret)
        self.place_files = ['/home/ryan/yokosuka/imgs/gas_station.png',
                            '/home/ryan/yokosuka/imgs/police_station.png',
                            '/home/ryan/yokosuka/imgs/shop.png']

    def mousePressEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.dragstart = event.pos()
            if self.ui_mainwindow.firefighter_button.isDown():
                print ("Add Fire Fighter")
                if self.total_fire_fighters > 0 and self.ui_mainwindow.firefighter_button.isDown():
                    self.total_fire_fighters -= 1
                    self.ui_mainwindow.firefighter_button.setText(str(self.total_fire_fighters) + ' Fire Fighters')
                    self.add_element_to_map('FireFighter', event.pos(), event.globalPos())
            elif self.ui_mainwindow.swat_button.isDown():
                print ("Add Swat")
                if self.total_swat > 0 and self.ui_mainwindow.swat_button.isDown():
                    self.total_swat -= 1
                    self.ui_mainwindow.swat_button.setText(str(self.total_swat) + ' Swat Teams')
                    self.add_element_to_map('Swat', event.pos(), event.globalPos())
            elif self.ui_mainwindow.coastguard_button.isDown():
                print ("Add coast guard")
                if self.total_coast_guard > 0 and self.ui_mainwindow.coastguard_button.isDown():
                    self.total_coast_guard -= 1
                    self.ui_mainwindow.coastguard_button.setText(str(self.total_coast_guard)+' Coast Guard Teams')
                    self.add_element_to_map('CoastGuard', event.pos(), event.globalPos())

    def upload_map(self):
        fp = 'map.png'
        cv2.imwrite(fp, cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR))
        a = self.client.upload_from_path(fp, config=None, anon=True)
        db.child("Images").child(self.mapper.city).child('url').set(a['link'])
        db.child("Images").child(self.mapper.city).child('updateTime').set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def add_element_to_map(self, type, pos, globalpos):
        if type == 'FireFighter':
            icon = cv2.imread('/home/ryan/yokosuka/imgs/fire_truck.jpg', 1)
        elif type == 'Swat':
            icon = cv2.imread('/home/ryan/yokosuka/imgs/police_car.png', 1)
        elif type == 'CoastGuard':
            icon = cv2.imread('/home/ryan/yokosuka/imgs/coast_guard.png', 1)

        icon = cv2.resize(icon, (30,30))
        icon = cv2.cvtColor(icon, cv2.COLOR_BGR2RGB)
        w = icon.shape[1]
        h = icon.shape[0]
        w2, h2 = self.fig.get_size_inches()*self.fig.get_dpi()
        width = self.ui_mainwindow.maplayout.geometry().width()
        height = self.ui_mainwindow.maplayout.geometry().height()
        space_width = width - w2
        space_height = height - h2
        curr_ratio = 2
        x = pos.x()
        y = pos.y()


        try:
            self.image[y:y+h, x:x+w] = icon
            self.ax.imshow(self.image)
            self.canvas.draw()
            self.ui_mainwindow.plainTextEdit.insertPlainText("Deployed " + type + "\n")
        except:
            self.ui_mainwindow.plainTextEdit.insertPlainText("Coordinates Not Valid.\n")
            #self.ui_mainwindow.maplayout.addWidget(self.canvas)


    def firefighter_button_clicked(self):
        if self.button_pressed:
            self.ui_mainwindow.firefighter_button.setDown(False)
            self.button_pressed = False
        else:
            self.ui_mainwindow.firefighter_button.setDown(True)
            self.button_pressed = True

    def swat_button_clicked(self):
        if self.button_pressed:
            self.ui_mainwindow.swat_button.setDown(False)
            self.button_pressed = False
        else:
            self.ui_mainwindow.swat_button.setDown(True)
            self.button_pressed = True


    def coastguard_button_clicked(self):
        if self.button_pressed:
            self.ui_mainwindow.coastguard_button.setDown(False)
            self.button_pressed = False
        else:
            self.ui_mainwindow.coastguard_button.setDown(True)
            self.button_pressed = True


    def generate_map(self):
        if not self.first:
            self.ui_mainwindow.maplayout.removeWidget(self.canvas)
        else:
            self.first = False
        self.mapper.geocode(self.addresses, self.cities)
        self.mapper.download_image(self.types)
        self.create_iconmap()

    def create_iconmap(self):
        w, h = self.mapper.image.shape[1], self.mapper.image.shape[0]
        self.ax.axis('off')
        self.ax.imshow(cv2.cvtColor(self.mapper.image, cv2.COLOR_BGR2RGB))
        self.fig.tight_layout()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()
        w, h = self.fig.get_size_inches()*self.fig.get_dpi()
        self.ui_mainwindow.maplayout.addWidget(self.canvas)
        self.canvas.mousePressEvent = self.mousePressEvent
        self.image = np.fromstring(self.canvas.tostring_rgb(), dtype='uint8')
        self.image = np.reshape(self.image, (h, w, 3))


    def twoD_Gaussian(self, x, y, xo, yo, sigma_x, sigma_y):
        a = 1. / (2 * sigma_x ** 2) + 1. / (2 * sigma_y ** 2)
        c = 1. / (2 * sigma_x ** 2) + 1. / (2 * sigma_y ** 2)
        g = np.exp(- (a * ((x - xo) ** 2) + c * ((y - yo) ** 2)))
        return g.ravel()

    def transparent_cmap(self, cmap, N=255):
        "Copy colormap and set alpha values"
        #
        mycmap = cmap
        mycmap._init()
        mycmap._lut[:,-1] = np.linspace(0, 0.8, N+4)
        return mycmap


