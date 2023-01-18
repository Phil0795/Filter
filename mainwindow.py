# This Python file uses the following encoding: utf-8
import sys


from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QCheckBox, QVBoxLayout
import pyqtgraph as pg


# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

data1 = "P1_D1_S1_M1_C1_O1_T2023_01_12_17_59_26_bending_direction=0_bending_speed=2_cycles=1_steps=1200_contacts=1_sample_rate=100_downsample=1_reference=1kΩ"
data2 = "P1_D1_S2_M1_C1_O1_T2023_01_12_17_59_26_bending_direction=0_bending_speed=2_cycles=1_steps=1200_contacts=1_sample_rate=100_downsample=1_reference=1kΩ"
data3 = "P1_D1_S3_M1_C1_O1_T2023_01_12_17_59_26_bending_direction=0_bending_speed=2_cycles=1_steps=1200_contacts=1_sample_rate=100_downsample=1_reference=1kΩ"
data4 = "P1_D2_S1_M1_C1_O1_T2023_01_12_17_59_26_bending_direction=0_bending_speed=2_cycles=1_steps=1200_contacts=1_sample_rate=100_downsample=1_reference=1kΩ"
data5 = "P1_D2_S2_M1_C1_O1_T2023_01_12_17_59_26_bending_direction=0_bending_speed=2_cycles=1_steps=1200_contacts=1_sample_rate=100_downsample=1_reference=1kΩ"
data6 = "P1_D2_S3_M1_C1_O1_T2023_01_12_17_59_26_bending_direction=0_bending_speed=2_cycles=1_steps=1200_contacts=1_sample_rate=100_downsample=1_reference=1kΩ"
data7 = "P1_D3_S1_M1_C1_O1_T2023_01_12_17_59_26_bending_direction=0_bending_speed=2_cycles=1_steps=1200_contacts=1_sample_rate=100_downsample=1_reference=1kΩ"
data8 = "P1_D3_S2_M1_C1_O1_T2023_01_12_17_59_26_bending_direction=0_bending_speed=2_cycles=1_steps=1200_contacts=1_sample_rate=100_downsample=1_reference=1kΩ"
data9 = "P1_D3_S3_M1_C1_O1_T2023_01_12_17_59_26_bending_direction=0_bending_speed=2_cycles=1_steps=1200_contacts=1_sample_rate=100_downsample=1_reference=1kΩ"
data10 = "P1_D3_S4_M1_C1_O1_T2023_01_12_17_59_26_bending_direction=0_bending_speed=2_cycles=1_steps=1200_contacts=1_sample_rate=100_downsample=1_reference=1kΩ"
data11 = "P1_D3_S5_M1_C2_O1_T2023_01_12_17_59_26_bending_direction=0_bending_speed=2_cycles=1_steps=1200_contacts=1_sample_rate=100_downsample=1_reference=1kΩ"
data12 = "P1_D3_S5_M1_C3_O1_T2023_01_12_17_59_26_bending_direction=0_bending_speed=2_cycles=1_steps=1200_contacts=1_sample_rate=100_downsample=1_reference=1kΩ"

# A list of data to be used by the interface
data = [data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12]


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.data = None
        self.widget = QCheckBox()
        self.xtext= "Data"
        self.ytext= "k-factor"
        self.xunit= None
        self.yunit= None

        # Connect button to function
        self.ui.pushButton_upload.clicked.connect(self.onclick_upload)
        self.ui.pushButton.clicked.connect(self.clear_checkboxes)

        self.graphWidget = ScatterPlot(self.xtext, self.xunit, self.ytext, self.yunit)
        self.graphWidget2 = ScatterPlot(self.xtext, self.xunit, self.ytext, self.yunit)

        self.ui.widget_top.setLayout(QVBoxLayout())
        self.ui.widget_top.layout().addWidget(self.graphWidget)
        self.ui.widget_bot.setLayout(QVBoxLayout())
        self.ui.widget_bot.layout().addWidget(self.graphWidget2)

    # Function to clear checkboxes
    def clear_checkboxes(self):
        # Get all the checkboxes in the scroll area and delete them
        for i in self.ui.scrollAreaWidgetContents_design.findChildren(QCheckBox):
            i.deleteLater()
        for i in self.ui.scrollAreaWidgetContents_sample.findChildren(QCheckBox):
            i.deleteLater()
        for i in self.ui.scrollAreaWidgetContents_material.findChildren(QCheckBox):
            i.deleteLater()
        for i in self.ui.scrollAreaWidgetContents_print.findChildren(QCheckBox):
            i.deleteLater()
        for i in self.ui.scrollAreaWidgetContents_orientation.findChildren(QCheckBox):
            i.deleteLater()
        
        

    # Function to parse data
    def onclick_upload(self):
        global data
        # Get the data from data list
        self.data = data
        # Print the parsed data up to the first underscore
        projectdata = [i.split("_")[0] for i in self.data]
        #Remove the duplicate data
        projectdata = list(set(projectdata))
        projectdata.sort()
        # Add the parsed data to the combox widget
        self.ui.comboBox_project.addItems(projectdata)
        # Parse the data from the first underscore to the second underscore
        designdata = [i.split("_")[1] for i in self.data]
        # Remove the duplicate data
        designdata = list(set(designdata))
        # Order the data
        designdata.sort()
        # Parse the data from the second underscore to the third underscore
        sampledata = [i.split("_")[2] for i in self.data]
        sampledata = list(set(sampledata))
        sampledata.sort()
        # Parse the data from the third underscore to the fourth underscore
        materialdata = [i.split("_")[3] for i in self.data]
        materialdata = list(set(materialdata))
        materialdata.sort()
        # Parse the data from the fourth underscore to the fifth underscore
        printdata = [i.split("_")[4] for i in self.data]
        printdata = list(set(printdata))
        printdata.sort()

        orientationdata = [i.split("_")[5] for i in self.data]
        orientationdata = list(set(orientationdata))
        orientationdata.sort()


        for i in range(len(designdata)):
            self.addCheckbox(designdata[i], self.ui.scrollAreaWidgetContents_design)

        for i in range(len(sampledata)):
            self.addCheckbox(sampledata[i], self.ui.scrollAreaWidgetContents_sample)

        for i in range(len(materialdata)):
            self.addCheckbox(materialdata[i], self.ui.scrollAreaWidgetContents_material)

        for i in range(len(printdata)):
            self.addCheckbox(printdata[i], self.ui.scrollAreaWidgetContents_print)

        #for i in range(len(orientationdata)):
        for i in range(len(orientationdata)):
            self.addCheckbox(orientationdata[i], self.ui.scrollAreaWidgetContents_orientation)

        for i in range(100):
            self.addCheckbox(f"{i}", self.ui.scrollAreaWidgetContents_A)

    # Function to add checkboxes
    def addCheckbox(self, name, parent):
        parent.setLayout(QVBoxLayout())
        checkbox = QCheckBox(name)
        parent.layout().addWidget(checkbox)
        checkbox.setVisible(True)


class ScatterPlot(pg.PlotWidget):
    def __init__(self, xtext, xunit, ytext, yunit, **kargs):
        super().__init__(**kargs)
        self.setXRange(0, 200)
        self.setYRange(0, 3)
        self.setLabel(axis='bottom', text=xtext, units=xunit)
        self.setLabel(axis='left', text=ytext, units=yunit)
        self.showGrid(x=True, y=True, alpha=0.5)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
