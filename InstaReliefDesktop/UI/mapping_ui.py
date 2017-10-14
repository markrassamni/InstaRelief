from InstaReliefDesktop.Mapping.mapper import Mapper
from InstaReliefDesktop.UI.insta_relief_ui import Ui_MainWindow
from PyQt5 import QtGui, QtCore,QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import cv2


class Mapping_Ui(QtWidgets.QMainWindow):
    def __init__(self, mapper):
        super(Mapping_Ui, self).__init__(None)
        self.mapper = mapper
        self.ui_mainwindow = Ui_MainWindow()
        self.ui_mainwindow.setupUi(self)

        self.button_pressed = False

        self.fig, self.ax, self.image = None, None, None

        self.total_fire_fighters = 20
        self.total_swat = 10
        self.total_coast_guard = 5
        self.ui_mainwindow.firefighter_button.setText(str(self.total_fire_fighters)+' Fire Fighters')
        self.ui_mainwindow.swat_button.setText(str(self.total_swat)+' Swat Teams')
        self.ui_mainwindow.coastguard_button.setText(str(self.total_coast_guard)+' Coast Guard Teams')
        self.ui_mainwindow.firefighter_button.clicked.connect(self.firefighter_button_clicked)
        self.ui_mainwindow.swat_button.clicked.connect(self.swat_button_clicked)
        self.ui_mainwindow.coastguard_button.clicked.connect(self.coastguard_button_clicked)

        self.setWindowTitle('Insta Relief')

        self.fire_cmap = self.transparent_cmap(plt.cm.Reds)
        self.zombie_cmap = self.transparent_cmap(plt.cm.Greens)
        self.water_cmap = self.transparent_cmap(plt.cm.Blues)

        self.addresses = ['1800 Rosecrans Ave', '2213 Warfield Ave', '2617 Manhattan Beach Blvd']
        self.cities = ['Manhattan Beach', 'Redondo Beach', 'Redondo Beach']
        self.types = ['Zombie', 'Fire', 'Water']

        self.canvas = None
        self.setMouseTracking(True)

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
            elif self.ui_mainwindow.coastguard_button.isDown():
                print ("Add coast guard")
                if self.total_coast_guard > 0 and self.ui_mainwindow.coastguard_button.isDown():
                    self.total_coast_guard -= 1
                    self.ui_mainwindow.coastguard_button.setText(str(self.total_coast_guard)+' Coast Guard Teams')

    def add_element_to_map(self, type, pos, globalpos):
        if type == 'FireFighter':
            icon = cv2.imread('/home/ryan/yokosuka/imgs/fire_station.png', 1)

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
            print (self.image.shape)
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

        if not self.ui_mainwindow.swat_button.isDown():
            self.ui_mainwindow.swat_button.setDown(False)
        else:
            self.ui_mainwindow.swat_button.setDown(True)

    def coastguard_button_clicked(self):

        if not self.ui_mainwindow.coastguard_button.isDown():
            self.ui_mainwindow.coastguard_button.setDown(False)
        else:
            self.ui_mainwindow.coastguard_button.setDown(True)

    def generate_map(self):

        self.mapper.geocode(self.addresses, self.cities)
        self.mapper.download_image(self.types)
        self.create_iconmap()

    def create_iconmap(self):
        w, h = self.mapper.image.shape[1], self.mapper.image.shape[0]
        #all_lat, all_lng = self.mapper.all_lat, self.mapper.all_lng
        #for lat, lng in zip(all)
        y, x = np.mgrid[0:h, 0:w]

        gauss = self.twoD_Gaussian(x, y, w/2, h/2, 0.05*x.max(), 0.05*y.max())

        self.fig = plt.figure(figsize=(7,7))
        self.ax = self.fig.add_subplot(111)
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
        mycmap = cmap
        mycmap._init()
        mycmap._lut[:,-1] = np.linspace(0, 0.8, N+4)
        return mycmap


