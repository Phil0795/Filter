# This Python file uses the following encoding: utf-8
import sys
import os
import sqlite3


from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QCheckBox, QVBoxLayout, QFileDialog
import pyqtgraph as pg


# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

#Create a database in RAM
connection_data = sqlite3.connect('testproject.db')
# Create a cursor to work with
datacursor = connection_data.cursor()
# Create a table if it doesn't exist
datacursor.execute("Create TABLE IF NOT EXISTS database (timestamp text PRIMARY KEY ON CONFLICT IGNORE, project int, design int, sample int, material int, print int, orientation int, apara int, bpara int, fpara int, gpara int, direction short int, speed short int, cycles int, steps int, contacts int, samplerate int, downsample int, reference str, alldata str, k_fac_mean float, k_fac_devi float, Hyst_mean float, Hyst_devi float)")
# Define commands to update the database
Q_timestamp = "INSERT OR IGNORE INTO database (timestamp) VALUES (?)"
Q_project = "UPDATE database SET project = ? WHERE timestamp = ?"
Q_design = "UPDATE database SET design = ? WHERE timestamp = ?"
Q_sample = "UPDATE database SET sample = ? WHERE timestamp = ?"
Q_material = "UPDATE database SET material = ? WHERE timestamp = ?"
Q_print = "UPDATE database SET print = ? WHERE timestamp = ?"
Q_orientation = "UPDATE database SET orientation = ? WHERE timestamp = ?"
Q_apara = "UPDATE database SET apara = ? WHERE timestamp = ?"
Q_bpara = "UPDATE database SET bpara = ? WHERE timestamp = ?"
Q_fpara = "UPDATE database SET fpara = ? WHERE timestamp = ?"
Q_gpara = "UPDATE database SET gpara = ? WHERE timestamp = ?"
Q_direction = "UPDATE database SET direction = ? WHERE timestamp = ?"
Q_speed = "UPDATE database SET speed = ? WHERE timestamp = ?"
Q_cycles = "UPDATE database SET cycles = ? WHERE timestamp = ?"
Q_steps = "UPDATE database SET steps = ? WHERE timestamp = ?"
Q_contacts = "UPDATE database SET contacts = ? WHERE timestamp = ?"
Q_samplerate = "UPDATE database SET samplerate = ? WHERE timestamp = ?"
Q_downsample = "UPDATE database SET downsample = ? WHERE timestamp = ?"
Q_reference = "UPDATE database SET reference = ? WHERE timestamp = ?"
Q_alldata = "UPDATE database SET alldata = ? WHERE timestamp = ?"
Q_k_fac_mean = "UPDATE database SET k_fac_mean = ? WHERE timestamp = ?"
Q_k_fac_devi = "UPDATE database SET k_fac_devi = ? WHERE timestamp = ?"
Q_Hyst_mean = "UPDATE database SET Hyst_mean = ? WHERE timestamp = ?"
Q_Hyst_devi = "UPDATE database SET Hyst_devi = ? WHERE timestamp = ?"



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.data = []
        self.rawdata = []
        self.otherdata = []
        self.stepcount = []
        self.timecount = []
        self.R1 = []
        self.R2 = []
        self.checkboxes_design = []
        self.checkboxes_sample = []
        self.checkboxes_material = []
        self.checkboxes_print = []
        self.checkboxes_orientation = []
        self.checkboxes_A = []
        self.checkboxes_B = []
        self.checkboxes_F = []
        self.checkboxes_G = []
        self.checkboxes_speed = []
        self.checkboxes_cycles = []
        self.checkboxes_steps = []
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
        self.ui.pushButton_upload.clicked.connect(self.selectDirectory)

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
        # find the corresponding project in the database and create a temporary database containing the data of the selected project
        datacursor.execute("CREATE TEMPORARY TABLE IF NOT EXISTS projectdatabase AS SELECT * FROM database WHERE project = ?", (value,))

        #datacursor.execute(sqlstatement)
        
        
        


    def on_cbvalue_changed(self, value):
        

        if value == "Hysterese (mean)":
            self.splitData(["2023.01.12-17.59.26"])
            self.xtext = "Time"
            self.ytext = "Resistance"
            self.xunit = "ms"
            self.yunit = "Ohm"
            self.graphWidget.clear()
            self.graphWidget2.clear()
            self.graphWidget.plotline(self.stepcount, self.R1, "timestamp goes here")
            self.graphWidget2.plotline(self.stepcount, self.R2, "timestamp goes here")
            


        else:
            print("Combox value changed to: " + value)
            self.xtext = "Entsprechendes x zu " + value
            self.ytext = "Entsprechendes y zu " + value
            self.xunit = "Einheit x zu " + value
            self.yunit = "Einheit y zu " + value
            self.graphWidget.refresh(self.xtext, self.xunit, self.ytext, self.yunit, self.x, self.y, self.coding)
            self.graphWidget2.refresh(self.xtext, self.xunit, self.ytext, self.yunit, self.x, self.y, self.coding)


    def checkthedata(self):
        notthefirst = False
        sqlcommand = ""
        if self.checkboxes_design:
            for value in self.checkboxes_design:
                sqlcommand = sqlcommand + "design = " + "'" + str(value) + "'" + " OR "
            sqlcommand = sqlcommand[:-4]
            notthefirst = True
        if self.checkboxes_sample:
            if notthefirst:
                sqlcommand = sqlcommand + " AND "
            for value in self.checkboxes_sample:
                sqlcommand = sqlcommand + "sample = " + "'" + str(value) + "'" + " OR "
            sqlcommand = sqlcommand[:-4]
            notthefirst = True
        if self.checkboxes_material:
            if notthefirst:
                sqlcommand = sqlcommand + " AND "
            for value in self.checkboxes_material:
                sqlcommand = sqlcommand + "material = " + "'" + str(value) + "'" + " OR "
            sqlcommand = sqlcommand[:-4]
            notthefirst = True
        if self.checkboxes_print:
            if notthefirst:
                sqlcommand = sqlcommand + " AND "
            for value in self.checkboxes_print:
                sqlcommand = sqlcommand + "print = " + "'" + str(value) + "'" + " OR "
            sqlcommand = sqlcommand[:-4]
            notthefirst = True
        if self.checkboxes_orientation:
            if notthefirst:
                sqlcommand = sqlcommand + " AND "
            for value in self.checkboxes_orientation:
                sqlcommand = sqlcommand + "orientation = " + "'" + str(value) + "'" + " OR "
            sqlcommand = sqlcommand[:-4]
            notthefirst = True
        if self.checkboxes_A:
            if notthefirst:
                sqlcommand = sqlcommand + " AND "
            for value in self.checkboxes_A:
                sqlcommand = sqlcommand + "A = " + "'" + str(value) + "'" + " OR "
            sqlcommand = sqlcommand[:-4]
            notthefirst = True
        if self.checkboxes_B:
            if notthefirst:
                sqlcommand = sqlcommand + " AND "
            for value in self.checkboxes_B:
                sqlcommand = sqlcommand + "B = " + "'" + str(value) + "'" + " OR "
            sqlcommand = sqlcommand[:-4]
            notthefirst = True
        if self.checkboxes_F:
            if notthefirst:
                sqlcommand = sqlcommand + " AND "
            for value in self.checkboxes_F:
                sqlcommand = sqlcommand + "F = " + "'" + str(value) + "'" + " OR "
            sqlcommand = sqlcommand[:-4]
            notthefirst = True
        if self.checkboxes_G:
            if notthefirst:
                sqlcommand = sqlcommand + " AND "
            for value in self.checkboxes_G:
                sqlcommand = sqlcommand + "G = " + "'" + str(value) + "'" + " OR "
            sqlcommand = sqlcommand[:-4]
            notthefirst = True
        if self.checkboxes_speed:
            if notthefirst:
                sqlcommand = sqlcommand + " AND "
            for value in self.checkboxes_speed:
                sqlcommand = sqlcommand + "speed = " + "'" + str(value) + "'" + " OR "
            sqlcommand = sqlcommand[:-4]
            notthefirst = True
        if self.checkboxes_cycles:
            if notthefirst:
                sqlcommand = sqlcommand + " AND "
            for value in self.checkboxes_cycles:
                sqlcommand = sqlcommand + "cycles = " + "'" + str(value) + "'" + " OR "
            sqlcommand = sqlcommand[:-4]
            notthefirst = True
        if self.checkboxes_steps:
            if notthefirst:
                sqlcommand = sqlcommand + " AND "
            for value in self.checkboxes_steps:
                sqlcommand = sqlcommand + "steps = " + "'" + str(value) + "'" + " OR "
            sqlcommand = sqlcommand[:-4]
            notthefirst = True
        if notthefirst == False:
            return False
        else:
            sqlcommand = 'SELECT timestamp FROM database WHERE ' + sqlcommand
        return sqlcommand
    # Function to react to checkbox selection and print the name of the checkbox
    def on_checkbox_changed(self):
        self.checkboxes_design = []
        self.checkboxes_sample = []
        self.checkboxes_material = []
        self.checkboxes_print = []
        self.checkboxes_orientation = []
        self.checkboxes_A = []
        self.checkboxes_B = []
        self.checkboxes_F = []
        self.checkboxes_G = []
        self.checkboxes_speed = []
        self.checkboxes_cycles = []
        self.checkboxes_steps = []
        current_project = self.ui.comboBox_project.currentText()
        print("Current project: " + current_project)
        tempdata2 = []
        value = self.sender().text()
        # iterate all checkboxes in all scroll areas
        for i in self.ui.scrollAreaWidgetContents_design.findChildren(QCheckBox):
            if i.isChecked():
                self.checkboxes_design.append(i.text())
        for i in self.ui.scrollAreaWidgetContents_sample.findChildren(QCheckBox):
            if i.isChecked():
                self.checkboxes_sample.append(i.text())
        for i in self.ui.scrollAreaWidgetContents_material.findChildren(QCheckBox):
            if i.isChecked():
                self.checkboxes_material.append(i.text())
        for i in self.ui.scrollAreaWidgetContents_print.findChildren(QCheckBox):
            if i.isChecked():
                self.checkboxes_print.append(i.text())
        for i in self.ui.scrollAreaWidgetContents_orientation.findChildren(QCheckBox):
            if i.isChecked():
                self.checkboxes_orientation.append(i.text())
        for i in self.ui.scrollAreaWidgetContents_A.findChildren(QCheckBox):
            if i.isChecked():
                self.checkboxes_A.append(i.text())
        for i in self.ui.scrollAreaWidgetContents_B.findChildren(QCheckBox):
            if i.isChecked():
                self.checkboxes_B.append(i.text())
        for i in self.ui.scrollAreaWidgetContents_F.findChildren(QCheckBox):
            if i.isChecked():
                self.checkboxes_F.append(i.text())
        for i in self.ui.scrollAreaWidgetContents_G.findChildren(QCheckBox):
            if i.isChecked():
                self.checkboxes_G.append(i.text())
        for i in self.ui.scrollAreaWidgetContents_speed.findChildren(QCheckBox):
            if i.isChecked():
                self.checkboxes_speed.append(i.text())
        for i in self.ui.scrollAreaWidgetContents_cycles.findChildren(QCheckBox):
            if i.isChecked():
                self.checkboxes_cycles.append(i.text())
        for i in self.ui.scrollAreaWidgetContents_steps.findChildren(QCheckBox):
            if i.isChecked():
                self.checkboxes_steps.append(i.text())
        
        print("Checkbox " + value + " was changed.")
        #print(self.checkthedata())
        if self.checkthedata():
            datacursor.execute(self.checkthedata())
        for i in datacursor:
            print(i)
        
        tempdata = datacursor.fetchall()
        # turn tempdata into a list
        tempdata = [item for t in tempdata for item in t]
        tempdata2.append(tempdata)
        #print (tempdata2)
        if self.sender().isChecked():
            for t in tempdata2:
                if t not in self.otherdata:
                    self.otherdata.append(t)
        else:
            for t in tempdata2:
                if t in self.otherdata:
                    self.otherdata.remove(t)
        #print (self.otherdata)
        self.graphWidget.refresh(self.xtext, self.xunit, self.ytext, self.yunit, self.x, self.y, self.coding)
        self.graphWidget2.refresh(self.xtext, self.xunit, self.ytext, self.yunit, self.x, self.y, self.coding)



    # Function to parse data
    def onclick_upload(self):
        acheck = False
        bcheck = False
        gcheck = False
        fcheck = False
        check = False
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
        projectdata.append(paraList[0])       
        designdata.append(paraList[1])
        sampledata.append(paraList[2])
        materialdata.append(paraList[3])
        printdata.append(paraList[4])
        orientationdata.append(paraList[5])
        # search for strings in the list beginning with A, B, G, F, T
        for i in range(len(paraList)):
            if paraList[i].startswith("A"):
                adata.append(paraList[i][1:])
                acheck = True
            elif paraList[i].startswith("B"):
                bdata.append(paraList[i][1:])
                bcheck = True
            elif paraList[i].startswith("G"):
                gdata.append(paraList[i][1:])
                gcheck = True
            elif paraList[i].startswith("F"):
                fdata.append(paraList[i][1:])
                fcheck = True
            elif paraList[i].startswith("T"):
                timestamp.append(paraList[i][1:])
        if acheck == False:
            adata.append(None)
        if bcheck == False:
            bdata.append(None)
        if gcheck == False:
            gdata.append(None)
        if fcheck == False:
            fdata.append(None)
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

        # Add the data to the database
        for i in range(len(timestamp)):
            datacursor.execute(Q_timestamp, (timestamp[i],))
            datacursor.execute(Q_project, (projectdata[i], timestamp[i]))
            datacursor.execute(Q_design, (designdata[i], timestamp[i]))
            datacursor.execute(Q_sample, (sampledata[i], timestamp[i]))
            datacursor.execute(Q_material, (materialdata[i], timestamp[i]))
            datacursor.execute(Q_print, (printdata[i], timestamp[i]))
            datacursor.execute(Q_orientation, (orientationdata[i], timestamp[i]))
            datacursor.execute(Q_apara, (adata[i], timestamp[i]))
            datacursor.execute(Q_bpara, (bdata[i], timestamp[i]))
            datacursor.execute(Q_gpara, (gdata[i], timestamp[i]))
            datacursor.execute(Q_fpara, (fdata[i], timestamp[i]))
            datacursor.execute(Q_direction, (directiondata[i], timestamp[i]))
            datacursor.execute(Q_speed, (speeddata[i], timestamp[i]))
            datacursor.execute(Q_cycles, (cyclesdata[i], timestamp[i]))
            datacursor.execute(Q_steps, (stepsdata[i], timestamp[i]))
            datacursor.execute(Q_contacts, (contactsdata[i], timestamp[i]))
            datacursor.execute(Q_samplerate, (sampleratedata[i], timestamp[i]))
            datacursor.execute(Q_downsample, (downsamplingdata[i], timestamp[i]))
            datacursor.execute(Q_reference, (referencedata[i], timestamp[i]))
            datacursor.execute(Q_alldata, (self.rawdata[i], timestamp[i]))
            connection_data.commit()
            datacursor.execute("Select timestamp, project, design, sample, material, print, orientation, apara, bpara, fpara, gpara, direction, speed, cycles, steps, contacts, samplerate, downsample, reference, alldata from database")
            #for x in datacursor:
            #    print(x)


        # Add the parsed data to the combox widget
        self.ui.comboBox_project.addItems(projectdata)

        # Add checkboxes based on the parsed data
        for y in self.ui.scrollAreaWidgetContents_design.findChildren(QCheckBox):
            if y.text() == designdata[0]:
                check=True
        if check == False:
            self.addCheckbox(designdata[0], self.ui.scrollAreaWidgetContents_design)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_sample.findChildren(QCheckBox):
            if y.text() == sampledata[0]:
                check=True
        if check == False:
            self.addCheckbox(sampledata[0], self.ui.scrollAreaWidgetContents_sample)
        else:
            check = False
        
        for y in self.ui.scrollAreaWidgetContents_material.findChildren(QCheckBox):
            if y.text() == materialdata[0]:
                check=True
        if check == False:
            self.addCheckbox(materialdata[0], self.ui.scrollAreaWidgetContents_material)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_print.findChildren(QCheckBox):
            if y.text() == printdata[0]:
                check=True
        if check == False:
            self.addCheckbox(printdata[0], self.ui.scrollAreaWidgetContents_print)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_orientation.findChildren(QCheckBox):
            if y.text() == orientationdata[0]:
                check=True
        if check == False:
            self.addCheckbox(orientationdata[0], self.ui.scrollAreaWidgetContents_orientation)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_A.findChildren(QCheckBox):
            if y.text() == adata[0]:
                check=True
        if check == False:
            if adata[0] != None:
                self.addCheckbox(adata[0], self.ui.scrollAreaWidgetContents_A)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_B.findChildren(QCheckBox):
            if y.text() == bdata[0]:
                check=True
        if check == False:
            if bdata[0] != None:
                self.addCheckbox(bdata[0], self.ui.scrollAreaWidgetContents_B)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_G.findChildren(QCheckBox):
            if y.text() == gdata[0]:
                check=True
        if check == False:
            if gdata[0] != None:
                self.addCheckbox(gdata[0], self.ui.scrollAreaWidgetContents_G)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_F.findChildren(QCheckBox):
            if y.text() == fdata[0]:
                check=True
        if check == False:
            if fdata[0] != None:
                self.addCheckbox(fdata[0], self.ui.scrollAreaWidgetContents_F)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_speed.findChildren(QCheckBox):
            if y.text() == speeddata[0]:
                check=True
        if check == False:
            self.addCheckbox(speeddata[0], self.ui.scrollAreaWidgetContents_speed)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_cycles.findChildren(QCheckBox):
            if y.text() == cyclesdata[0]:
                check=True
        if check == False:
            self.addCheckbox(cyclesdata[0], self.ui.scrollAreaWidgetContents_cycles)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_steps.findChildren(QCheckBox):
            if y.text() == stepsdata[0]:
                check=True
        if check == False:
            self.addCheckbox(stepsdata[0], self.ui.scrollAreaWidgetContents_steps)
        else:
            check = False

        self.rawdata.clear()


    #Function to split the data bulk into four lists
    def splitData(self, timestamps):
        self.timecount.clear()
        self.stepcount.clear()
        self.R1.clear()
        self.R2.clear()
        self.rawdata.clear()
        #get the data from the sql database depending on the timestamp
        for timestamp in timestamps:
            datacursor.execute("SELECT alldata FROM database WHERE timestamp = ?", (timestamp,))
            for x in datacursor:
                self.rawdata.append(x)           
        #split data at \n
        self.rawdata = self.rawdata[0][0].split('\n')
        self.rawdata.pop()
        #split the data into four lists
        for i in range(len(self.rawdata)):
            self.timecount.append(int(self.rawdata[i].split(',')[0])-int(self.rawdata[0].split(',')[0]))
            self.stepcount.append(int(self.rawdata[i].split(',')[1]))
            self.R1.append(int(self.rawdata[i].split(',')[2]))
            self.R2.append(int(self.rawdata[i].split(',')[3]))

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
                        lines[0] = lines[0][:-1]
                        self.data.append(lines[0].split(','))
                        self.rawdata.append("".join(lines[2:])) 
                    print("Data added")  
                    self.onclick_upload()
                    self.data.remove("File")
                    self.data.remove("Test")
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

    def plotline(self, x, y, coding):
        self.addItem(pg.ScatterPlotItem(x, y, pen='red', symbol='o', size=5, data=coding, hoverable=True, brush=pg.mkBrush(255, 0, 0, 120)))
        self.addItem(pg.PlotCurveItem(x, y, pen='r'))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
