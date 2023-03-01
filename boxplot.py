import pyqtgraph as pg
import numpy as np
from PyQt6.QtWidgets import QApplication
from pyqtgraph import QtCore, QtGui
from scipy.stats import gaussian_kde
from scipy.ndimage import gaussian_filter

class BoxPlotItem(pg.GraphicsObject):
    def __init__(self, data, parent=None):
        pg.GraphicsObject.__init__(self, parent)
        self.data = data
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        painter = QtGui.QPainter(self.picture)
        painter.setPen(pg.mkPen('k'))
        painter.setBrush(pg.mkBrush('w'))

        for i in range(self.data.shape[1]):
            y = self.data[:, i]
            box = QtGui.QPainterPath()
            box.addRect(i-0.3, np.min(y), 0.6, np.max(y)-np.min(y))
            painter.drawPath(box)

        painter.end()

    def paint(self, painter, option, widget):
        painter.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())

class ViolinPlotItem(pg.GraphicsObject):
    def __init__(self, data, parent=None):
        pg.GraphicsObject.__init__(self)
        self.setData(data)
    
    def setData(self, data):
        self.data = data
        self.generatePicture()

    def generatePicture(self):
        data = self.data
        n = data.shape[1]
        x = np.zeros((n, 4))
        for i in range(n):
            y = data[:, i]
            kde = gaussian_kde(y)
            y = kde(y)
            y /= y.max()
            x[i] = [i+1, np.median(y), np.percentile(y, 25), np.percentile(y, 75)]
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('k'))
        for i in range(n):
            p.drawLine(x[i, 0], x[i, 2], x[i, 0], x[i, 3])
            p.drawLine(x[i, 0], x[i, 1], x[i, 0]+0.2, x[i, 1])
            p.drawLine(x[i, 0], x[i, 2], x[i, 0]+0.2, x[i, 2])
            p.drawLine(x[i, 0], x[i, 3], x[i, 0]+0.2, x[i, 3])
            p.setBrush(pg.mkBrush('k'))
            p.drawEllipse(QtCore.QPointF(x[i, 0], x[i, 1]), 0.1, 0.1)
            p.setBrush(pg.mkBrush(None))
        p.end()

app = QApplication([])
data = np.random.normal(size=(100,5))

win = pg.PlotWidget()

box_plot = BoxPlotItem(data, parent=win.plotItem)
win.addItem(box_plot)

violin_plot = ViolinPlotItem(data, parent=win.plotItem)
win.addItem(violin_plot)

win.show()

app.exec()
