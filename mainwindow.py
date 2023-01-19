# This Python file uses the following encoding: utf-8
import sys
import os


from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QCheckBox, QVBoxLayout, QFileDialog
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
        self.data = []
        self.widget = QCheckBox()
        self.xtext= "Data"
        self.ytext= "k-factor"
        self.xunit= None
        self.yunit= None

        # Connect button to function
        self.ui.pushButton_upload.clicked.connect(self.onclick_upload)
        self.ui.pushButton.clicked.connect(self.selectDirectory)

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
        projectdata = []
        designdata = []
        sampledata = []
        materialdata = []
        printdata = []
        orientationdata = []
        adata = []
        bdata = []
        gdata = []
        fdata = []
        timestamp = []
        directiondata = []
        speeddata = [] 
        cyclesdata = []
        stepsdata = []
        contactsdata = []
        sampleratedata = []
        downsamplingdata = []
        referencedata = []

        # Parse the first object in data list up to the first underscore
        searchkey_file = "File"
        searchkey_test = "Test"
        index_file = self.data.index(searchkey_file)+1
        index_test = self.data.index(searchkey_test)+1
        paraList = self.data[index_file].split("_")
        testList = self.data[index_test]
        print(paraList)
        print(testList)
        # Get the first two characters of the string
        projectdata.append(paraList[0])
        # Add the parsed data to the combox widget
        self.ui.comboBox_project.addItems(projectdata)

        designdata.append(paraList[1][1:])
        sampledata.append(paraList[2][1:])
        materialdata.append(paraList[3][1:])
        printdata.append(paraList[4][1:])
        orientationdata.append(paraList[5][1:])
        # search for strings in the list beginning with A, B, G, F, T
        for i in range(len(paraList)):
            if paraList[i].startswith("A"):
                adata.append(paraList[i][1:])
            elif paraList[i].startswith("B"):
                bdata.append(paraList[i][1:])
            elif paraList[i].startswith("G"):
                gdata.append(paraList[i][1:])
            elif paraList[i].startswith("F"):
                fdata.append(paraList[i][1:])
            elif paraList[i].startswith("T"):
                timestamp.append(paraList[i][1:])
        print(adata, bdata, gdata, fdata, timestamp)

        directiondata.append(testList[0][18:])
        speeddata.append(testList[1][14:])
        cyclesdata.append(testList[2][7:])
        stepsdata.append(testList[3][6:])
        contactsdata.append(testList[4][9:])
        sampleratedata.append(testList[5][12:])
        downsamplingdata.append(testList[6][11:])
        referencedata.append(testList[7][10:])
        print (directiondata, speeddata, cyclesdata, stepsdata, contactsdata, sampleratedata, downsamplingdata, referencedata)

        for i in range(len(designdata)):
            self.addCheckbox(designdata[i], self.ui.scrollAreaWidgetContents_design)

        for i in range(len(sampledata)):
            self.addCheckbox(sampledata[i], self.ui.scrollAreaWidgetContents_sample)

        for i in range(len(materialdata)):
            self.addCheckbox(materialdata[i], self.ui.scrollAreaWidgetContents_material)

        for i in range(len(printdata)):
            self.addCheckbox(printdata[i], self.ui.scrollAreaWidgetContents_print)

        for i in range(len(orientationdata)):
            self.addCheckbox(orientationdata[i], self.ui.scrollAreaWidgetContents_orientation)

        if adata != None:
            for i in range(len(adata)):
                self.addCheckbox(f"{i}", self.ui.scrollAreaWidgetContents_A)
        
        if bdata != None:
            for i in range(len(bdata)):
                self.addCheckbox(f"{i}", self.ui.scrollAreaWidgetContents_B)
        
        if fdata != None:
            for i in range(len(fdata)):
                self.addCheckbox(f"{i}", self.ui.scrollAreaWidgetContents_F)

        if gdata != None:
            for i in range(len(gdata)):
                self.addCheckbox(f"{i}", self.ui.scrollAreaWidgetContents_G)
        
        for i in range(len(speeddata)):
            self.addCheckbox(speeddata[i], self.ui.scrollAreaWidgetContents_speed)
        
        for i in range(len(cyclesdata)):
            self.addCheckbox(cyclesdata[i], self.ui.scrollAreaWidgetContents_cycles)

        for i in range(len(stepsdata)):
            self.addCheckbox(stepsdata[i], self.ui.scrollAreaWidgetContents_steps)

    # Function to add checkboxes
    def addCheckbox(self, name, parent):
        parent.setLayout(QVBoxLayout())
        checkbox = QCheckBox(name)
        parent.layout().addWidget(checkbox)
        checkbox.setVisible(True)

    def selectDirectory(self):
        dupcheck = False
        # Get the directory from the user
        directory = QFileDialog.getExistingDirectory(None, "Select Directory")
        # Get the files from the directory
        files = os.listdir(directory)
        # Create a list to store the data
        # Loop through the files
        for i in files:
            # Check if the file is a .csv file
            if i.endswith(".csv"):
                for duplicate in self.data:
                    if i[:-4] in duplicate:
                        dupcheck = True
                #Check for duplicate files
                if dupcheck == False:
                    # Save the file name without .csv to the list
                    self.data.append("File")
                    self.data.append(i[:-4])
                    # Parse the contents of the file line by line and save to a list
                    with open(directory + "/" + i, "r") as f:
                        # Read the lines
                        lines = f.readlines()
                        self.data.append("Test")
                        # Loop through the lines
                        for line in lines:
                            # Split the line by commas
                            line = line.split(",")
                            # Remove the new line character
                            line[-1] = line[-1][:-1]
                            # Add the line to the list
                            self.data.append(line)  
                    print("Data added")  
                else:
                    # If the file is a duplicate, skip it
                    print("Duplicate file found: "+i)
                    dupcheck = False
                    continue           


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
