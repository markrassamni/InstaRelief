from InstaReliefDesktop.Mapping.mapper import Mapper
from InstaReliefDesktop.UI.insta_relief_ui import Ui_MainWindow
from PyQt5 import QtGui, QtCore
import pyqtgraph as pg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import cv2



class Mapping_Ui(QtGui.QMainWindow):
    def __init__(self, mapper):
        super(Mapping_Ui, self).__init__(None)
        self.mapper = mapper
        self.ui_mainwindow = Ui_MainWindow()
        self.ui_mainwindow.setupUi(self)

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

    def firefighter_button_clicked(self):
        if self.total_fire_fighters > 0:
            self.total_fire_fighters -= 1
            self.ui_mainwindow.firefighter_button.setText(str(self.total_fire_fighters)+' Fire Fighters')

    def swat_button_clicked(self):
        if self.total_swat > 0:
            self.total_swat -= 1
            self.ui_mainwindow.swat_button.setText(str(self.total_swat)+' Swat Teams')

    def coastguard_button_clicked(self):
        if self.total_coast_guard > 0:
            self.total_coast_guard -= 1
            self.ui_mainwindow.coastguard_button.setText(str(self.total_coast_guard)+' Coast Guard Teams')

    def generate_map(self):

        self.mapper.geocode(self.addresses, self.cities)
        self.mapper.download_image(self.types)
        self.create_heatmap()

    def create_heatmap(self):
        w, h = self.mapper.image.shape[1], self.mapper.image.shape[0]
        #all_lat, all_lng = self.mapper.all_lat, self.mapper.all_lng
        #for lat, lng in zip(all)
        y, x = np.mgrid[0:h, 0:w]

        gauss = self.twoD_Gaussian(x, y, w/2, h/2, 0.05*x.max(), 0.05*y.max())

        fig = plt.figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        fig.tight_layout(pad=0)
        ax.axis('off')
        ax.imshow(cv2.cvtColor(self.mapper.image, cv2.COLOR_BGR2RGB))
        ax.contourf(x, y, gauss.reshape(x.shape[0], y.shape[1]), 15, cmap=self.zombie_cmap)
        canvas.draw()
        w, h = fig.get_size_inches()*fig.get_dpi()
        self.ui_mainwindow.maplayout.addWidget(canvas)
        image = np.fromstring(canvas.tostring_rgb(), dtype='uint8')
        image = np.reshape(image, (h, w, 3))


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


