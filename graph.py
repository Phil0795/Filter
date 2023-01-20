import sys
from PyQt6.QtWidgets import QApplication
import pyqtgraph as pg
import numpy as np

app = QApplication(sys.argv)
x = np.arange(1000)
y = np.random.normal(size=(3,1000))
plotWidget = pg.plot(title = "a crowded plot")

for i in range(4):
    plotWidget.plot(x, y[2], pen= (i, 3), symbol=None)


status = app.exec()
sys.exit(status)