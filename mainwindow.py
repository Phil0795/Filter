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
        self.x = [1,2,3,4,5,6,7,8,9,10]
        self.y = [3,3,3,4,4,5,5,5,5,5]
        self.coding = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]


        # Connect combox to funtion
        self.ui.comboBox_project.currentTextChanged.connect(self.on_cbproject_changed)
        self.ui.comboBox_value.currentTextChanged.connect(self.on_cbvalue_changed)
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
        
        

    # Function to react to combox selection
    def on_cbproject_changed(self, value):
        print("Combox project changed to: " + value)

    def on_cbvalue_changed(self, value):
        print("Combox value changed to: " + value)
        self.xtext = "Entsprechendes x zu " + value
        self.ytext = "Entsprechendes y zu " + value
        self.xunit = "Einheit x zu " + value
        self.yunit = "Einheit y zu " + value
        self.graphWidget.refresh(self.xtext, self.xunit, self.ytext, self.yunit, self.x, self.y, self.coding)
        self.graphWidget2.refresh(self.xtext, self.xunit, self.ytext, self.yunit, self.x, self.y, self.coding)

    # Function to react to checkbox selection and print the name of the checkbox
    def on_checkbox_changed(self):
        name = self.sender().text()
        print("Checkbox " + name + " was cahnged.")
        self.graphWidget.refresh(self.xtext, self.xunit, self.ytext, self.yunit, self.x, self.y, self.coding)
        self.graphWidget2.refresh(self.xtext, self.xunit, self.ytext, self.yunit, self.x, self.y, self.coding)



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

        designdata.append(paraList[1])
        sampledata.append(paraList[2])
        materialdata.append(paraList[3])
        printdata.append(paraList[4])
        orientationdata.append(paraList[5])
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
        checkbox.stateChanged.connect(self.on_checkbox_changed)
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
                            # Add the line to the list if it is not the second line
                            if line[0] != "timestamp":
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
        self.setBackground('w')
        self.setLabel(axis='bottom', text=xtext, units=xunit)
        self.setLabel(axis='left', text=ytext, units=yunit)
        self.showGrid(x=True, y=True, alpha=0.5)

    def refresh(self, xtext, xunit, ytext, yunit, x, y, coding):
        self.clear()
        self.setLabel(axis='bottom', text=xtext, units=xunit)
        self.setLabel(axis='left', text=ytext, units=yunit)
        self.plotnew(x, y, coding)

    def plotnew(self, x, y, coding):
        self.addItem(pg.ScatterPlotItem(x, y, pen='red', symbol='o', size=5, data=coding, hoverable=True, brush=pg.mkBrush(255, 0, 0, 120)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
