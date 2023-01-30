# This Python file uses the following encoding: utf-8
import sys
import os
import sqlite3


from PySide6.QtCore import QFile, Qt
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
connection_data.row_factory = lambda cursor, row: row[0]
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
        self.checkboxes = []
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
        self.ui.pushButton.clicked.connect(self.readfromdatabase)
        self.ui.pushButton_detail.clicked.connect(self.clear_checkboxes)

        self.graphWidget = ScatterPlot(self.xtext, self.xunit, self.ytext, self.yunit)
        self.graphWidget2 = ScatterPlot(self.xtext, self.xunit, self.ytext, self.yunit)

        self.ui.widget_top.setLayout(QVBoxLayout())
        self.ui.widget_top.layout().addWidget(self.graphWidget)
        self.ui.widget_bot.setLayout(QVBoxLayout())
        self.ui.widget_bot.layout().addWidget(self.graphWidget2)

    # Function to clear checkboxes - do not use this. It was only used for debugging.
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
        for i in self.ui.scrollAreaWidgetContents_A.findChildren(QCheckBox):
            i.deleteLater()
        for i in self.ui.scrollAreaWidgetContents_B.findChildren(QCheckBox):
            i.deleteLater()
        for i in self.ui.scrollAreaWidgetContents_F.findChildren(QCheckBox):
            i.deleteLater()
        for i in self.ui.scrollAreaWidgetContents_G.findChildren(QCheckBox):
            i.deleteLater()
        for i in self.ui.scrollAreaWidgetContents_speed.findChildren(QCheckBox):
            i.deleteLater()
        for i in self.ui.scrollAreaWidgetContents_cycles.findChildren(QCheckBox):
            i.deleteLater()
        for i in self.ui.scrollAreaWidgetContents_steps.findChildren(QCheckBox):
            i.deleteLater()
        
    def readfromdatabase(self):
        projectdata = []
        check = False
        datacursor.execute("SELECT project FROM database")
        projectdata = datacursor.fetchall()
        # remove duplicates
        projectdata = list(dict.fromkeys(projectdata))      
        # sort list by length and alphabet
        projectdata = sorted(projectdata, key=lambda x: (len(x), x))
        print(projectdata)
        for p in projectdata:
            ExistingProjects = [self.ui.comboBox_project.itemText(i) for i in range(self.ui.comboBox_project.count())]
            for obj in ExistingProjects:
                if p == obj:
                    check = True
            if check == False:
                self.ui.comboBox_project.addItems(projectdata)
            else:
                check = False 

    # Function to react to combox selection
    def on_cbproject_changed(self, value):
        print("Combox project changed to: " + value)
        # find the corresponding project in the database and create a temporary database containing the data of the selected project
        # datacursor.execute("CREATE TEMPORARY TABLE IF NOT EXISTS projectdatabase AS SELECT * FROM database WHERE project = ?", (value,))
        # uncheck all checkboxes
        for checkbox in self.checkboxes:
            checkbox.setCheckState(Qt.CheckState.Unchecked)
        # declare list parameters
        designdata = []
        sampledata = []
        materialdata = []
        printdata = []
        orientationdata = []
        Adata = []
        Bdata = []
        Fdata = []
        Gdata = []
        speeddata = []
        cyclesdata = []
        stepsdata = []
        check = False

        # get data from database corresponding to the selected project
        datacursor.execute("SELECT design FROM database WHERE project = ?", (value,))
        designdata = datacursor.fetchall()
        # remove duplicates
        designdata = list(dict.fromkeys(designdata))
        # sort list
        designdata = sorted(designdata, key = lambda x: (len(x), x))
        # create checkboxes
        for box in self.ui.scrollAreaWidgetContents_design.findChildren(QCheckBox):           
            if box.text() not in designdata:
                self.checkboxes.remove(box)
                box.deleteLater()
        for i in range(len(designdata)):
            #print(designdata[i])
            for box in self.ui.scrollAreaWidgetContents_design.findChildren(QCheckBox):
                if box.text() == designdata[i]:
                    check = True
            if check == False:    
                self.addCheckbox(designdata[i], self.ui.scrollAreaWidgetContents_design)
            else:
                check = False

        datacursor.execute("SELECT sample FROM database WHERE project = ?", (value,))
        sampledata = datacursor.fetchall()
        sampledata = list(dict.fromkeys(sampledata))
        sampledata = sorted(sampledata, key = lambda x: (len(x), x))
        # create checkboxes
        for box in self.ui.scrollAreaWidgetContents_sample.findChildren(QCheckBox):
            if box.text() not in sampledata:
                self.checkboxes.remove(box)
                box.deleteLater()
        for i in range(len(sampledata)):
            for box in self.ui.scrollAreaWidgetContents_sample.findChildren(QCheckBox):
                if box.text() == sampledata[i]:
                    check = True
            if check == False:    
                self.addCheckbox(sampledata[i], self.ui.scrollAreaWidgetContents_sample)
            else:
                check = False

        datacursor.execute("SELECT material FROM database WHERE project = ?", (value,))
        materialdata = datacursor.fetchall()
        materialdata = list(dict.fromkeys(materialdata))
        materialdata = sorted(materialdata, key=lambda x:(len(x), x))
        # create checkboxes
        for box in self.ui.scrollAreaWidgetContents_material.findChildren(QCheckBox):
            if box.text() not in materialdata:
                self.checkboxes.remove(box)
                box.deleteLater()
        for i in range(len(materialdata)):
            for box in self.ui.scrollAreaWidgetContents_material.findChildren(QCheckBox):
                if box.text() == materialdata[i]:
                    check = True
            if check == False:    
                self.addCheckbox(materialdata[i], self.ui.scrollAreaWidgetContents_material)
            else:
                check = False

        datacursor.execute("SELECT print FROM database WHERE project = ?", (value,))
        printdata = datacursor.fetchall()
        printdata = list(dict.fromkeys(printdata))
        printdata.sort()
        # create checkboxes
        for box in self.ui.scrollAreaWidgetContents_print.findChildren(QCheckBox):
            if box.text() not in printdata:
                self.checkboxes.remove(box)
                box.deleteLater()
        for i in range(len(printdata)):
            for box in self.ui.scrollAreaWidgetContents_print.findChildren(QCheckBox):
                if box.text() == printdata[i]:
                    check = True
            if check == False:    
                self.addCheckbox(printdata[i], self.ui.scrollAreaWidgetContents_print)
            else:
                check = False

        datacursor.execute("SELECT orientation FROM database WHERE project = ?", (value,))
        orientationdata = datacursor.fetchall()
        orientationdata = list(dict.fromkeys(orientationdata))
        orientationdata.sort()
        # create checkboxes
        for box in self.ui.scrollAreaWidgetContents_orientation.findChildren(QCheckBox):
            if box.text() not in orientationdata:
                self.checkboxes.remove(box)
                box.deleteLater()
        for i in range(len(orientationdata)):
            for box in self.ui.scrollAreaWidgetContents_orientation.findChildren(QCheckBox):
                if box.text() == orientationdata[i]:
                    check = True
            if check == False:    
                self.addCheckbox(orientationdata[i], self.ui.scrollAreaWidgetContents_orientation)
            else:
                check = False

        datacursor.execute("SELECT apara FROM database WHERE project = ?", (value,))
        Adata = datacursor.fetchall()
        Adata = list(dict.fromkeys(Adata))
        Adata.sort()
        # create checkboxes
        for box in self.ui.scrollAreaWidgetContents_A.findChildren(QCheckBox):
            if box.text() not in Adata:
                self.checkboxes.remove(box)
                box.deleteLater()
        for i in range(len(Adata)):
            for box in self.ui.scrollAreaWidgetContents_A.findChildren(QCheckBox):
                if box.text() == Adata[i]:
                    check = True
            if check == False:   
                if Adata[i] != None: 
                    self.addCheckbox(Adata[i], self.ui.scrollAreaWidgetContents_A)
            else:
                check = False

        datacursor.execute("SELECT bpara FROM database WHERE project = ?", (value,))
        Bdata = datacursor.fetchall()
        Bdata = list(dict.fromkeys(Bdata))
        Bdata.sort()
        for box in self.ui.scrollAreaWidgetContents_B.findChildren(QCheckBox):
            if box.text() not in Bdata:
                self.checkboxes.remove(box)
                box.deleteLater()
        for i in range(len(Bdata)):
            for box in self.ui.scrollAreaWidgetContents_B.findChildren(QCheckBox):
                if box.text() == Bdata[i]:
                    check = True
            if check == False: 
                if Bdata[i] != None:   
                    self.addCheckbox(Bdata[i], self.ui.scrollAreaWidgetContents_B)
            else:
                check = False

        datacursor.execute("SELECT fpara FROM database WHERE project = ?", (value,))
        Fdata = datacursor.fetchall()
        Fdata = list(dict.fromkeys(Fdata))
        Fdata.sort()
        for box in self.ui.scrollAreaWidgetContents_F.findChildren(QCheckBox):
            if box.text() not in Fdata:
                self.checkboxes.remove(box)
                box.deleteLater()
        for i in range(len(Fdata)):
            for box in self.ui.scrollAreaWidgetContents_F.findChildren(QCheckBox):
                if box.text() == Fdata[i]:
                    check = True
            if check == False: 
                if Fdata[i] != None:   
                    self.addCheckbox(Fdata[i], self.ui.scrollAreaWidgetContents_F)
            else:
                check = False

        datacursor.execute("SELECT gpara FROM database WHERE project = ?", (value,))
        Gdata = datacursor.fetchall()
        Gdata = list(dict.fromkeys(Gdata))
        Gdata.sort()
        for box in self.ui.scrollAreaWidgetContents_G.findChildren(QCheckBox):
            if box.text() not in Gdata:
                self.checkboxes.remove(box)
                box.deleteLater()
        for i in range(len(Gdata)):
            for box in self.ui.scrollAreaWidgetContents_G.findChildren(QCheckBox):
                if box.text() == Gdata[i]:
                    check = True
            if check == False:   
                if Gdata[i] != None: 
                    self.addCheckbox(Gdata[i], self.ui.scrollAreaWidgetContents_G)
            else:
                check = False

        datacursor.execute("SELECT speed FROM database WHERE project = ?", (value,))
        speeddata = datacursor.fetchall()
        speeddata = list(dict.fromkeys(speeddata))
        speeddata.sort()
        for box in self.ui.scrollAreaWidgetContents_speed.findChildren(QCheckBox):
            if box.text() not in speeddata:
                self.checkboxes.remove(box)
                box.deleteLater()
        for i in range(len(speeddata)):
            for box in self.ui.scrollAreaWidgetContents_speed.findChildren(QCheckBox):
                if box.text() == speeddata[i]:
                    check = True
            if check == False:    
                self.addCheckbox(str(speeddata[i]), self.ui.scrollAreaWidgetContents_speed)
            else:
                check = False

        datacursor.execute("SELECT cycles FROM database WHERE project = ?", (value,))
        cyclesdata = datacursor.fetchall()
        cyclesdata = list(dict.fromkeys(cyclesdata))
        cyclesdata.sort()
        for box in self.ui.scrollAreaWidgetContents_cycles.findChildren(QCheckBox):
            if box.text() not in cyclesdata:
                self.checkboxes.remove(box)
                box.deleteLater()
        for i in range(len(cyclesdata)):
            for box in self.ui.scrollAreaWidgetContents_cycles.findChildren(QCheckBox):
                if box.text() == cyclesdata[i]:
                    check = True
            if check == False:    
                self.addCheckbox(str(cyclesdata[i]), self.ui.scrollAreaWidgetContents_cycles)
            else:
                check = False

        datacursor.execute("SELECT steps FROM database WHERE project = ?", (value,))
        stepsdata = datacursor.fetchall()
        stepsdata = list(dict.fromkeys(stepsdata))
        stepsdata.sort()
        for box in self.ui.scrollAreaWidgetContents_steps.findChildren(QCheckBox):
            if box.text() not in stepsdata:
                self.checkboxes.remove(box)
                box.deleteLater()
        for i in range(len(stepsdata)):
            for box in self.ui.scrollAreaWidgetContents_steps.findChildren(QCheckBox):
                if box.text() == stepsdata[i]:
                    check = True
            if check == False:    
                self.addCheckbox(str(stepsdata[i]), self.ui.scrollAreaWidgetContents_steps)
            else:
                check = False
            
        #datacursor.execute(sqlstatement)
        
        
        


    def on_cbvalue_changed(self, value):
        

        if value == "Hysterese (mean)":
            data = ["2023.01.12-17.59.26"]
            self.splitData(data)
            
            


        else:
            print("Combox value changed to: " + value)
            self.xtext = "Entsprechendes x zu " + value
            self.ytext = "Entsprechendes y zu " + value
            self.xunit = "Einheit x zu " + value
            self.yunit = "Einheit y zu " + value
            self.graphWidget.refresh(self.xtext, self.xunit, self.ytext, self.yunit, self.x, self.y, self.coding)
            self.graphWidget2.refresh(self.xtext, self.xunit, self.ytext, self.yunit, self.x, self.y, self.coding)

    # this function strings together an sql statement to filter the data in the database according to the checkboxes that are checked
    def checkthedata(self):
        # the current project is always the first filter and taken from the combobox
        current_project = self.ui.comboBox_project.currentText()
        # notthefirst is a variable to control the "AND"s in the sql statement
        notthefirst = False
        # the sql statement is initialized as an empty string
        sqlcommand = ""
        # each filter has a list of checked checkboxes. if the list is not empty, the filtering sql statement is extended
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
        # if no filter was the first filter, the sql statement is empty and the function returns false
        if notthefirst == False:
            return False
        # if the sql statement is not empty, the current project is added to the beginning of the statement and this statement is returned
        else:
            sqlcommand = 'SELECT timestamp FROM database WHERE project = ' + "'" + str(current_project) + "'" + " AND " + sqlcommand
        return sqlcommand


    # Function to check all checkboxes in every scroll area to know which daat to filter
    def checktheboxes(self):
        # first the filters are reset
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
        # the checkboxes are ordered by the corresponding scroll areas. 
        # If any are checked, they are added to the corresponding list by their displayed names
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

    # Function to react to checkbox selection and update the graphs
    def on_checkbox_changed(self):
        current_project = self.ui.comboBox_project.currentText()   
        # iterate all checkboxes in all scroll areas and add those that are checked to a list
        self.checktheboxes()
        # A note to which box was changed, for debugging purposes
        value = self.sender().text()
        print("Checkbox " + value + " was changed.")
        # checkthedata() returns the sql command to be executed or, if no checkboxes are checked, False 
        if self.checkthedata():
            datacursor.execute(self.checkthedata())
        # if no checkbox is checked, all the data from current project is selected
        else:
            datacursor.execute("SELECT timestamp FROM database WHERE project = ?", (current_project, ))
        # print statement for debugging purposes
        #for i in datacursor:
        #    print(i)
        # get the data from the database into a temporary variable
        tempdata = datacursor.fetchall()
        # turn tempdata into a list (it is a tuple of tuples when using the fetchall method)
        # get the data from the database and make it usable for the graph
        self.splitData(tempdata)
        #print (self.otherdata)
        #self.graphWidget.refresh(self.xtext, self.xunit, self.ytext, self.yunit, self.x, self.y, self.coding)
        #self.graphWidget2.refresh(self.xtext, self.xunit, self.ytext, self.yunit, self.x, self.y, self.coding)



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
        print(projectdata, designdata, sampledata, materialdata, printdata, orientationdata)
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
            datacursor.execute("Select timestamp, project, design, sample, material, print, orientation, apara, bpara, fpara, gpara, speed, cycles, steps from database")
            for x in datacursor:
                print(x)       

        self.rawdata.clear()


    # Function to split the data bulk into different list. This is used when raw data shall be displayed.
    def splitData(self, timestamps = []):
        self.timecount.clear()
        self.stepcount.clear()
        self.R1.clear()
        self.R2.clear()    
        # get the data from the sql database depending on the timestamp
        for i in range(len(timestamps)):
            self.rawdata.clear()
            datacursor.execute("SELECT alldata FROM database WHERE timestamp = ?", (str(timestamps[i]),))
            #print (timestamps[i])
            for x in datacursor:
                # split data at \n
                self.rawdata = x.split('\n')  
                self.rawdata.pop()   
                #print(self.rawdata)
                # split the data into four lists  
                for i in range(len(self.rawdata)):
                    self.timecount.append(int(self.rawdata[i].split(',')[0])-int(self.rawdata[0].split(',')[0]))
                    self.stepcount.append(int(self.rawdata[i].split(',')[1]))
                    self.R1.append(int(self.rawdata[i].split(',')[2]))
                    self.R2.append(int(self.rawdata[i].split(',')[3]))

        
        # draw from data
        self.xtext = "Time"
        self.ytext = "Resistance"
        self.xunit = "ms"
        self.yunit = "Ohm"
        self.graphWidget.clear()
        self.graphWidget2.clear()
        self.graphWidget.plotline(self.timecount, self.R1, "timestamp here")
        self.graphWidget2.plotline(self.timecount, self.R2, "timestamp here")
        
        

    # Function to add checkboxes
    def addCheckbox(self, name, parent):
        parent.setLayout(QVBoxLayout())
        checkbox = QCheckBox(name)
        self.checkboxes.append(checkbox)
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
