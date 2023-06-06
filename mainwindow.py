# This Python file uses the following encoding: utf-8
import sys
import os
import sqlite3




from PySide6.QtGui import QBrush, QColor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QCheckBox, QVBoxLayout, QHBoxLayout, QFileDialog
import pyqtgraph as pg
import numpy as np
from scipy.interpolate import interp1d
from scipy import signal, ndimage
#from operator import itemgetter

import matplotlib
matplotlib.use('QtAgg')

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar, FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# Important:
# You need to run the following command to generate the ui_form.py file! This has to be done when the file was updated using QTCreator!
#     pyside6-uic form.ui -o ui_form.py, and
#     pyside6-uic detailwindow.ui -o ui_detailwindow.py    - here you also have to rename the class Ui_MainWindow to Ui_DetWindow afterwards

from ui_form import Ui_MainWindow
from ui_detailwindow import Ui_DetWindow

#Create a database in RAM
connection_data = sqlite3.connect('InitialDB.db')
connection_data.row_factory = lambda cursor, row: row[0]
# Create a cursor to work with
datacursor = connection_data.cursor()

connection_data.row_factory = None
datacursor_tuple = connection_data.cursor()

# Create a table if it doesn't exist
datacursor.execute("Create TABLE IF NOT EXISTS database (timestamp text PRIMARY KEY ON CONFLICT IGNORE, project int, design int, sample int, material int, print int, orientation int, apara int, bpara int, fpara int, gpara int, direction short int, speed short int, cycles int, steps int, contacts int, samplerate int, downsample int, reference str, alldata str, k_fac_mean float, k_fac_devi float, Hyst_mean float, Hyst_devi float)")
# Define commands to update the database, this is done in SQLite syntax
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
    # This is the initialisation of the main window. It is called when the program is started. It is the first function that is called.
    # Here, all "global" variables are defined and the GUI is created. 
    # Subwindows and Widgets are created here as well.
    # functions are bound to buttons and other widgets here.
    def __init__(self, parent=None):
        super().__init__(parent)
        # The GUI is created using the ui_form.py file that was generated using the command above.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # -"These variables are used for"- parsing 
        self.data = []
        self.rawdata = []
        self.otherdata = []
        self.stepcount = []
        self.timecount = []
        self.R1 = []
        self.R2 = []
        # -""- setting the color of the graphs
        self.colors = ["b", "g", "r", "c", "m", "y", "k"]
        self.color = self.colors[0]
        # -""- parsing
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
        self.timestamp = []
        # -""- plotting
        self.cycle = None
        self.cycleEnd = None
        self.toplot = None
        self.widget = QCheckBox()
        self.xtext= None
        self.ytext= None
        self.xunit= None
        self.yunit= None
        self.coding = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]


        # Connect combox to funtion
        self.ui.comboBox_project.currentTextChanged.connect(self.on_cbproject_changed)
        self.ui.comboBox_value.currentTextChanged.connect(self.on_cbvalue_changed)
        # Connect button to function
        self.ui.pushButton_upload.clicked.connect(self.selectDirectory)
        self.ui.pushButton.clicked.connect(self.readfromdatabase)
        self.ui.pushButton_detail.clicked.connect(self.onclick_detail)
        # These are the graphs that are shown in the main window. The ScatterPlot class uses pyqtgraph to create the graphs. This is a quick and dirty solution and legacy code.
        self.graphWidget = ScatterPlot(self.xtext, self.xunit, self.ytext, self.yunit)
        self.graphWidget2 = ScatterPlot(self.xtext, self.xunit, self.ytext, self.yunit)
        # The Canvas class uses matplotlib to create the graphs. This is the new and better solution. (This can easily do boxplots etc and could even be further improved with seaborn etc.)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas2 = MplCanvas(self, width=5, height=4, dpi=100)
        # These are the toolbars that are shown in the main window. They are used control mouse interactions with the canvases. One bar per canvas is needed.(afaik)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar2 = NavigationToolbar(self.canvas2, self)
        # This is the detail window. It is created here but not shown yet. It is shown when the user clicks the "Detail" button. It is used to filter the data in detail.
        self.detailwindow = DetailWindow()
        self.detailwindow.ui.pushButton_update.clicked.connect(self.detailwindow_buttonpress)

        # The following code gives a layout to the areas of the main window which are filled with the widgets defined above. (Which could not be created in the QTCreator)
        # QVBoxLayout places all widgets on top of each other. QHBoxLayout places all widgets next to each other.
        self.ui.frame_toolbar.setLayout(QVBoxLayout())
        # The widgets itself are then added to the layout().
        self.ui.frame_toolbar.layout().addWidget(self.toolbar)
        self.ui.frame_toolbar.layout().addWidget(self.toolbar2)
        #This is done for the graphs as well.
        self.ui.widget_top.setLayout(QVBoxLayout())
        self.ui.widget_top.layout().addWidget(self.canvas)
        self.ui.widget_bot.setLayout(QVBoxLayout())
        self.ui.widget_bot.layout().addWidget(self.canvas2)
        # connecting spinboxes to functions.
        self.ui.spinBox_cycle.valueChanged.connect(self.whatcyclesir)
        self.ui.spinBox_cycleEnd.valueChanged.connect(self.uppercyclechanged)

    def detailwindow_buttonpress(self):
        timestamps = self.detailwindow.get_timestamps()
        self.splitData(timestamps)
        
    def readfromdatabase(self):
        # This function reads the data from the database and makes it available for plotting.
        # An empty list is created as a placeholder for the data.
        projectdata = []
        # A variable for double-checking for duplicates is created.
        check = False
        # All projects are read from the database. The data is stored in a the list.
        datacursor.execute("SELECT project FROM database")
        projectdata = datacursor.fetchall()
        # remove duplicates
        projectdata = list(dict.fromkeys(projectdata))      
        # sort list by length and alphabet (makes it nice to look at)
        projectdata = sorted(projectdata, key=lambda x: (len(x), x))
        # add the projects to the combobox in the main window. duplicates are filtered out(again) Just to be sure.
        for p in projectdata:
            ExistingProjects = [self.ui.comboBox_project.itemText(i) for i in range(self.ui.comboBox_project.count())]
            for obj in ExistingProjects:
                if p == obj:
                    check = True
            if check == False:
                self.ui.comboBox_project.addItems(projectdata)
            else:
                check = False 

    # toggle detail window
    def onclick_detail(self):
        if self.detailwindow.isVisible():
            self.detailwindow.hide()
        else:
            self.detailwindow.show()
    
    # Function to react to project selection in the combox
    def on_cbproject_changed(self, value):
        print("Combox project changed to: " + value)
        # uncheck all checkboxes
        self.toplot = self.ui.comboBox_value.currentText()
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
        directiondata = []
        speeddata = []
        cyclesdata = []
        stepsdata = []
        check = False

        # find all values for design in the database where the project is the selected project
        datacursor.execute("SELECT design FROM database WHERE project = ?", (value,))
        designdata = datacursor.fetchall()
        # remove duplicates
        designdata = list(dict.fromkeys(designdata))
        # sort list to make navigation easier
        designdata = sorted(designdata, key = lambda x: (len(x), x))
        # create a checkbox for each design
        # first look at all the checkboxes that are already there and remove the ones that are not needed anymore
        for box in self.ui.scrollAreaWidgetContents_design.findChildren(QCheckBox):           
            if box.text() not in designdata:
                self.checkboxes.remove(box)
                box.deleteLater()
        # then create the checkboxes that are still missing
        for i in range(len(designdata)):
            for box in self.ui.scrollAreaWidgetContents_design.findChildren(QCheckBox):
                if box.text() == designdata[i]:
                    check = True
            if check == False:    
                self.addCheckbox(designdata[i], self.ui.scrollAreaWidgetContents_design)
            else:
                check = False

        # Same procedure for the other parameters - sample, material, print, orientation, A, B, F, G, direction, speed, cycles, steps
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
        for i in range(len(Adata)):
            if Adata[i] == None:
                Adata[i] = "A0"
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
        for i in range(len(Bdata)):
            if Bdata[i] == None:
                Bdata[i] = "B0"
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
        for i in range(len(Fdata)):
            if Fdata[i] == None:
                Fdata[i] = "F0"
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
        for i in range(len(Gdata)):
            if Gdata[i] == None:
                Gdata[i] = "G0"
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

        datacursor.execute("SELECT direction FROM database WHERE project = ?", (value,))
        directiondata = datacursor.fetchall()
        directiondata = list(dict.fromkeys(directiondata))
        directiondata.sort()
        for box in self.ui.scrollAreaWidgetContents_direction.findChildren(QCheckBox):
            if box.text() not in directiondata:
                self.checkboxes.remove(box)
                box.deleteLater()
        for i in range(len(directiondata)):
            for box in self.ui.scrollAreaWidgetContents_direction.findChildren(QCheckBox):
                if box.text() == directiondata[i]:
                    check = True
            if check == False:    
                self.addCheckbox(str(directiondata[i]), self.ui.scrollAreaWidgetContents_direction)
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
        # update the detail window to be empty again.    
        self.set_detailWindow()
        
        


    # this function reacts to the second combox being changed. It contains the different ways the data can be plotted
    def on_cbvalue_changed(self, value):
        # global value is saved to be used in other functions
        self.toplot = value
        # check which data was selected to be plotted
        self.checktheboxes()
        # if any data is selected, use it to plot. Otherwise, plot all possible data
        if self.checkthedata():
            datacursor.execute(self.checkthedata())
        else:
            datacursor.execute("SELECT timestamp FROM database WHERE project = ?", (self.ui.comboBox_project.currentText(),))
        tempdata = datacursor.fetchall()
        # update detail window to contain all selected datasets
        self.set_detailWindow(tempdata)
        # this functions gets all the raw data from the database and then triggers the plotting function
        self.splitData(tempdata)



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
                sqlcommand = sqlcommand + "apara = " + "'" + str(value) + "'" + " OR "
            sqlcommand = sqlcommand[:-4]
            notthefirst = True
        if self.checkboxes_B:
            if notthefirst:
                sqlcommand = sqlcommand + " AND "
            for value in self.checkboxes_B:
                sqlcommand = sqlcommand + "bpara = " + "'" + str(value) + "'" + " OR "
            sqlcommand = sqlcommand[:-4]
            notthefirst = True
        if self.checkboxes_F:
            if notthefirst:
                sqlcommand = sqlcommand + " AND "
            for value in self.checkboxes_F:
                sqlcommand = sqlcommand + "fpara = " + "'" + str(value) + "'" + " OR "
            sqlcommand = sqlcommand[:-4]
            notthefirst = True
        if self.checkboxes_G:
            if notthefirst:
                sqlcommand = sqlcommand + " AND "
            for value in self.checkboxes_G:
                sqlcommand = sqlcommand + "gpara = " + "'" + str(value) + "'" + " OR "
            sqlcommand = sqlcommand[:-4]
            notthefirst = True
        if self.checkboxes_direction:
            if notthefirst:
                sqlcommand = sqlcommand + " AND "
            for value in self.checkboxes_direction:
                sqlcommand = sqlcommand + "direction = " + "'" + str(value) + "'" + " OR "
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


    # Function to check all checkboxes in every scroll area to know which data was selected
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
        self.checkboxes_direction = []
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
        for i in self.ui.scrollAreaWidgetContents_direction.findChildren(QCheckBox):
            if i.isChecked():
                self.checkboxes_direction.append(i.text())
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
        self.toplot = self.ui.comboBox_value.currentText() 
        # iterate all checkboxes in all scroll areas and add those that are checked to a list
        self.checktheboxes()
        # A note to which box was changed, for debugging purposes
        #value = self.sender().text()
        #print("Checkbox " + value + " was changed.")
        # checkthedata() returns the sql command to be executed or, if no checkboxes are checked, False is returned
        if self.checkthedata():
            datacursor.execute(self.checkthedata())
        # if no checkbox is checked, all the data from current project is selected
        else:
            datacursor.execute("SELECT timestamp FROM database WHERE project = ?", (current_project, ))
        # get the data from the database into a temporary variable
        tempdata = datacursor.fetchall()
        # update the detail window with the selected data
        self.set_detailWindow(tempdata)
        # get the data from the database and make it usable for the graph
        self.splitData(tempdata)


    # Function to parse data from a .csv file and add it to the database
    # The file has to follow specific guidelines to be parsed correctly. The bend.py script is used to create the .csv file. (March 2023)
    def onclick_upload(self):
        def parsetestdata(str):
            indicator = str.rfind("=")
            print (str[indicator+1:])
            return str[indicator+1:]
        acheck = False
        bcheck = False
        gcheck = False
        fcheck = False
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
        searchkey_timestamp = "Timestamp"
        searchkey_sample = "Sample"
        searchkey_test = "Test"
        index_timestamp = self.data.index(searchkey_timestamp)+1
        index_sample = self.data.index(searchkey_sample)+1
        index_test = self.data.index(searchkey_test)+1
        timestamp.append(self.data[index_timestamp])
        samplelist = self.data[index_sample]
        testList = self.data[index_test]
        print(samplelist)
        print(testList)
        projectdata.append(samplelist[0])       
        designdata.append(samplelist[1])
        sampledata.append(samplelist[2])
        materialdata.append(samplelist[3])
        printdata.append(samplelist[4])
        orientationdata.append(samplelist[5])
        # print(projectdata, designdata, sampledata, materialdata, printdata, orientationdata)
        # search for strings in the list beginning with A, B, G, F, T
        for i in range(len(samplelist)):
            if samplelist[i].startswith("A"):
                adata.append(samplelist[i])
                acheck = True
            elif samplelist[i].startswith("B"):
                bdata.append(samplelist[i])
                bcheck = True
            elif samplelist[i].startswith("F"):
                fdata.append(samplelist[i])
                fcheck = True
            elif samplelist[i].startswith("G"):
                gdata.append(samplelist[i])
                gcheck = True
        if acheck == False:
            adata.append("A0")
        if bcheck == False:
            bdata.append("B0")
        if fcheck == False:
            fdata.append("F0")
        if gcheck == False:
            gdata.append("G0")
        # print(adata, bdata, gdata, fdata, timestamp)
        directiondata.append(parsetestdata(testList[0]))
        speeddata.append(parsetestdata(testList[1]))
        cyclesdata.append(parsetestdata(testList[2]))
        stepsdata.append(parsetestdata(testList[3]))
        contactsdata.append(parsetestdata(testList[4]))
        sampleratedata.append(parsetestdata(testList[5]))
        downsamplingdata.append(parsetestdata(testList[6]))
        referencedata.append(parsetestdata(testList[7]))
        # print (directiondata, speeddata, cyclesdata, stepsdata, contactsdata, sampleratedata, downsamplingdata, referencedata)

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
            datacursor_tuple.execute("Select timestamp, project, design, sample, material, print, orientation, apara, bpara, fpara, gpara, speed, cycles, steps from database")
            for x in datacursor_tuple:
                print(x)       
        # clear the rawdata list after adding it to the database
        self.rawdata.clear()

    def set_detailWindow(self, timestamps = []):
        timestampslong = []
        for stamp in timestamps:
            timestampslong.append(self.findbytimestamp(stamp))
        self.detailwindow.renew_checkboxes(timestampslong)


    # Function to split the data bulk into different list. This is used when raw data shall be displayed.
    def splitData(self, timestamps = []):
        self.timecount.clear()
        self.stepcount.clear()
        self.R1.clear()
        self.R2.clear() 
        self.timestamp.clear()
        # if no timestamp are left, clear both canvas and return
        if len(timestamps) == 0:
            print ("no timestamps left")
            self.canvas.clear()
            self.canvas2.clear()
            return
        #remove all timestamps that are not also in self.detailwindow.checked_cb
        for stamp in timestamps:
            if self.findbytimestamp(stamp) in self.detailwindow.unchecked_cb:
                timestamps.remove(stamp)
            else:
                pass     
        # get the data from the sql database depending on the timestamp
        for t in range(len(timestamps)):
            self.rawdata.clear()
            datacursor.execute("SELECT alldata FROM database WHERE timestamp = ?", (str(timestamps[t]),))
            self.timestamp.append(timestamps[t])  #.replace(".", ""))
            tc = []
            sc = []
            r1 = []
            r2 = []
            #print (timestamps[i])
            for x in datacursor:
                # split data at \n
                self.rawdata = x.split('\n')  
                self.rawdata.pop()   
                #print(self.rawdata)
                # split the data into four lists  
                # normalise resistances to the first value
                for raw in range(len(self.rawdata)):
                    self.timecount.append(int(self.rawdata[raw].split(',')[0])-int(self.rawdata[0].split(',')[0]))
                    tc.append(int(self.rawdata[raw].split(',')[0])-int(self.rawdata[0].split(',')[0]))
                    self.stepcount.append(int(self.rawdata[raw].split(',')[1]))
                    sc.append(int(self.rawdata[raw].split(',')[1]))
                    self.R1.append(100*(int(self.rawdata[raw].split(',')[2])-int(self.rawdata[0].split(',')[2]))/int(self.rawdata[0].split(',')[2]))
                    r1.append(100*(int(self.rawdata[raw].split(',')[2])-int(self.rawdata[0].split(',')[2]))/int(self.rawdata[0].split(',')[2]))
                    self.R2.append(100*(int(self.rawdata[raw].split(',')[3])-int(self.rawdata[0].split(',')[3]))/int(self.rawdata[0].split(',')[3]))
                    r2.append(100*(int(self.rawdata[raw].split(',')[3])-int(self.rawdata[0].split(',')[3]))/int(self.rawdata[0].split(',')[3]))
                #self.save_table(timestamps[t], tc, sc, r1, r2)
            self.stepcount.append("Next")
            self.R1.append("Next")
            self.R2.append("Next")
            self.timecount.append("Next")

        # this calls the function to plot the data
        self.plotupdate()
        
    def plotupdate(self):
        # everything using the self.graphwidgets is commented out because it is not used anymore. self.canvas is used instead.
        #self.graphWidget.clear()
        #self.graphWidget2.clear()
        keyword = "Next"
        if self.toplot == "Resistance / Time":
            self.xtext = "Time"
            self.ytext = "Change in Resistance"
            self.xunit = "(ms)"
            self.yunit = "(%)"
            #self.graphWidget.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            #self.graphWidget2.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            counter = 0
            self.canvas.clear()
            self.canvas2.clear()

            for t in range(len(self.timestamp)):
                label = self.findbytimestamp(self.timestamp[t])
                self.color = self.colors[counter % 6]
                # get the list up to but not including the next keyword
                temp_timecount = self.timecount[:self.timecount.index(keyword)]
                temp_R1 = self.R1[:self.R1.index(keyword)]
                temp_R2 = self.R2[:self.R2.index(keyword)]
                #self.graphWidget.plotline(temp_timecount, temp_R1, self.findbytimestamp(self.timestamp[t]), self.color)
                #self.graphWidget2.plotline(temp_timecount, temp_R2, self.findbytimestamp(self.timestamp[t]), self.color)
                self.canvas.plot_line(temp_timecount, temp_R1, self.color, label)
                self.canvas.update_axes(self.toplot, self.xtext + " " + self.xunit, self.ytext + " " + self.yunit)
                self.canvas2.plot_line(temp_timecount, temp_R2, self.color, label)
                self.canvas2.update_axes(self.toplot, self.xtext + " " + self.xunit, self.ytext + " " + self.yunit)
                # delete the list up to the next keyword
                del self.timecount[:self.timecount.index(keyword)+1]
                del self.R1[:self.R1.index(keyword)+1]
                del self.R2[:self.R2.index(keyword)+1]
                counter += 1

        elif self.toplot == "Resistance / Steps":
            self.xtext = "Step"
            self.ytext = "Change in Resistance"
            self.xunit = ""
            self.yunit = "(%)"
            #self.graphWidget.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            #self.graphWidget2.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            counter = 0
            maxstepreached = False
            cyclebreaks = [0]
            self.canvas.clear()
            self.canvas2.clear()
            

            for t in range(len(self.timestamp)):
                label = self.findbytimestamp(self.timestamp[t])
                datacursor.execute("SELECT steps FROM database WHERE timestamp = ?", (self.timestamp[t],))
                max_step = datacursor.fetchall()[0]
                self.color = self.colors[counter % 6]
                # get the list up to but not including the next keyword
                temp_stepcount = self.stepcount[:self.stepcount.index(keyword)]
                temp_R1 = self.R1[:self.R1.index(keyword)]
                temp_R2 = self.R2[:self.R2.index(keyword)]
                for i in range(len(temp_stepcount)):
                    if max_step-temp_stepcount[i] <=15:
                        maxstepreached = True
                    if maxstepreached == True and temp_stepcount[i] <= 15:
                        cyclebreaks.append(i)
                        maxstepreached = False
                    elif maxstepreached == True and i == len(temp_stepcount)-1:
                        cyclebreaks.append(i)
                        maxstepreached = False

                # create a list from temp_stepcount from cyclebreak to cyclebreak
                temp_stepcount = temp_stepcount[cyclebreaks[self.ui.spinBox_cycle.value()-1]:cyclebreaks[self.ui.spinBox_cycleEnd.value()]]
                temp_R1 = temp_R1[cyclebreaks[self.ui.spinBox_cycle.value()-1]:cyclebreaks[self.ui.spinBox_cycleEnd.value()]]
                temp_R2 = temp_R2[cyclebreaks[self.ui.spinBox_cycle.value()-1]:cyclebreaks[self.ui.spinBox_cycleEnd.value()]]
                #self.graphWidget.plotline(temp_stepcount, temp_R1, self.findbytimestamp(self.timestamp[t]), self.color)
                #self.graphWidget2.plotline(temp_stepcount, temp_R2, self.findbytimestamp(self.timestamp[t]), self.color)
                self.canvas.plot_dot(temp_stepcount, temp_R1, self.color, 5, label)
                self.canvas.update_axes(self.toplot, self.xtext + " " + self.xunit, self.ytext + " " + self.yunit)
                self.canvas2.plot_dot(temp_stepcount, temp_R2, self.color, 5, label)
                self.canvas2.update_axes(self.toplot, self.xtext + " " + self.xunit, self.ytext + " " + self.yunit)
                # delete the list up to the next keyword
                del self.stepcount[:self.stepcount.index(keyword)+1]
                del self.R1[:self.R1.index(keyword)+1]
                del self.R2[:self.R2.index(keyword)+1]
                counter += 1

        elif self.toplot == "Hysteresis interpol.":
            self.xtext = "Step"
            self.ytext = "Change in Resistance"
            self.xunit = ""
            self.yunit = "(%)"
            #self.graphWidget.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            #self.graphWidget2.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            counter = 0
            maxstepreached = False
            cyclebreaks = [0]
            halfcyclebreaks = [0]
            self.canvas.clear()
            self.canvas2.clear()
            
            

            for t in range(len(self.timestamp)):
                datacursor.execute("SELECT steps FROM database WHERE timestamp = ?", (self.timestamp[t],))
                max_step = datacursor.fetchall()[0]
                label = self.findbytimestamp(self.timestamp[t])
                self.color = self.colors[counter % 6]
                halfcyclebreaks = [0]
                cyclebreaks = [0]
                # get the list up to but not including the next keyword
                temp_stepcount = self.stepcount[:self.stepcount.index(keyword)]
                temp_R1 = self.R1[:self.R1.index(keyword)]
                temp_R2 = self.R2[:self.R2.index(keyword)]
                for i in range(len(temp_stepcount)):
                    if  maxstepreached == False and max_step-temp_stepcount[i] <=4:
                        halfcyclebreaks.append(i)
                        maxstepreached = True
                    if maxstepreached == True and temp_stepcount[i] <= 4:
                        cyclebreaks.append(i)
                        halfcyclebreaks.append(i)
                        maxstepreached = False
                    elif maxstepreached == True and i == len(temp_stepcount)-1:
                        cyclebreaks.append(i)
                        halfcyclebreaks.append(i)
                        maxstepreached = False

                #function to interpolate the data 
                #print(halfcyclebreaks)  
                iternum = self.ui.spinBox_cycleEnd.value() - self.ui.spinBox_cycle.value() + 1
                for iter in range(iternum):
                    if iter > 0:
                        label = None
                    lowercycle = self.ui.spinBox_cycle.value()+iter
                    upwardssteps = temp_stepcount[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]                
                    downwardssteps = temp_stepcount[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    upwardsR1 = temp_R1[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]
                    downwardsR1 = temp_R1[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    upwardsR2 = temp_R2[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]
                    downwardsR2 = temp_R2[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    #find indices of duplicates
                    seen = set()
                    indices = [i for i, x in enumerate(upwardssteps) if upwardssteps.count(x) > 1 and x not in seen and not seen.add(x)]
                    #delete duplicates
                    if indices:
                        for index in reversed(indices):
                            del upwardssteps[index]
                            del upwardsR1[index]
                            del upwardsR2[index]
                    seen = set()
                    indices = [i for i, x in enumerate(downwardssteps) if downwardssteps.count(x) > 1 and x not in seen and not seen.add(x)]
                    if indices:
                        for index in reversed(indices):
                            del downwardssteps[index]
                            del downwardsR1[index]
                            del downwardsR2[index]
                    mykind = 'cubic'
                    predictupwards_r1 = interp1d(upwardssteps, upwardsR1, kind=mykind, bounds_error=False, fill_value=(upwardsR1[0], upwardsR1[-1]))
                    predictdownwards_r1 = interp1d(downwardssteps, downwardsR1, kind=mykind, bounds_error=False, fill_value=(downwardsR1[-1], downwardsR1[0]))
                    predictupwards_r2 = interp1d(upwardssteps, upwardsR2, kind=mykind, bounds_error=False, fill_value=(upwardsR2[0], upwardsR2[-1]))
                    predictdownwards_r2 = interp1d(downwardssteps, downwardsR2, kind=mykind, bounds_error=False, fill_value=(downwardsR2[-1], downwardsR2[0]))
                    stepcount_detail = list(range(0, max_step+1))
                    pu_r1 = ndimage.gaussian_filter1d(predictupwards_r1(stepcount_detail), 5)
                    pd_r1 = ndimage.gaussian_filter1d(predictdownwards_r1(stepcount_detail), 5)
                    pu_r2 = ndimage.gaussian_filter1d(predictupwards_r2(stepcount_detail), 5)
                    pd_r2 = ndimage.gaussian_filter1d(predictdownwards_r2(stepcount_detail), 5)
                    error1 = np.mean(np.abs(pu_r1 - pd_r1))
                    error2 = np.mean(np.abs(pu_r2 - pd_r2))
                    #print (stepcount_detail)
                    #upwardcurve = np.array([predictupwards(x) for x in stepcount_detail])
                    #print(upwardcurve)
                    #downwardcurve = np.array([predictdownwards(x) for x in stepcount_detail])
                    #self.graphWidget.plotline(stepcount_detail, upwardcurve, self.findbytimestamp(self.timestamp[t]), self.color)
                    #self.graphWidget.plotline(stepcount_detail, downwardcurve, self.findbytimestamp(self.timestamp[t]), self.color)
                    #counter+=1
                    #self.color = self.colors[counter % 6]
                    #self.graphWidget.plotline(stepcount_detail, pu_r1, self.findbytimestamp(self.timestamp[t]), self.color)
                    #self.graphWidget.plotline(stepcount_detail, pd_r1, str(error1), self.color)
                    self.canvas.plot_line(stepcount_detail, pu_r1, self.color, label)
                    counter += 1
                    self.color = self.colors[counter % 6]
                    self.canvas.plot_line(stepcount_detail, pd_r1, self.color, None)
                    counter -= 1
                    self.color = self.colors[counter % 6]
                    self.canvas.update_axes(self.toplot, self.xtext+" "+self.xunit, self.ytext+" "+self.yunit)
                    self.canvas2.plot_line(stepcount_detail, pu_r2, self.color, label)
                    counter += 1
                    self.color = self.colors[counter % 6]
                    self.canvas2.plot_line(stepcount_detail, pd_r2, self.color, None)
                    self.canvas2.update_axes(self.toplot, self.xtext+" "+self.xunit, self.ytext+" "+self.yunit)
                    #self.graphWidget2.plotline(stepcount_detail, pu_r2, self.findbytimestamp(self.timestamp[t]), self.color)
                    #self.graphWidget2.plotline(stepcount_detail, pd_r2, str(error2), self.color)
                # create a list from temp_stepcount from cyclebreak to cyclebreak
                #temp_stepcount = temp_stepcount[cyclebreaks[self.ui.spinBox_cycle.value()-1]:cyclebreaks[self.ui.spinBox_cycleEnd.value()]]
                #temp_R1 = temp_R1[cyclebreaks[self.ui.spinBox_cycle.value()-1]:cyclebreaks[self.ui.spinBox_cycleEnd.value()]]
                #temp_R2 = temp_R2[cyclebreaks[self.ui.spinBox_cycle.value()-1]:cyclebreaks[self.ui.spinBox_cycleEnd.value()]]
                #self.graphWidget.plotline(temp_stepcount, temp_R1, self.findbytimestamp(self.timestamp[t]), self.color)
                #self.graphWidget2.plotline(temp_stepcount, temp_R2, self.findbytimestamp(self.timestamp[t]), self.color)
                # delete the list up to the next keyword
                del self.stepcount[:self.stepcount.index(keyword)+1]
                del self.R1[:self.R1.index(keyword)+1]
                del self.R2[:self.R2.index(keyword)+1]
                counter += 1

        elif self.toplot == "1":
            self.xtext = "Step"
            self.ytext = "Change in Resistance"
            self.xunit = ""
            self.yunit = "(%)"
            #self.graphWidget.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            #self.graphWidget2.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            counter = 0
            maxstepreached = False
            cyclebreaks = [0]
            halfcyclebreaks = [0]
            self.canvas.clear()
            self.canvas2.clear()
            
            

            for t in range(len(self.timestamp)):
                datacursor.execute("SELECT steps FROM database WHERE timestamp = ?", (self.timestamp[t],))
                max_step = datacursor.fetchall()[0]
                label = self.findbytimestamp(self.timestamp[t])
                self.color = self.colors[counter % 6]
                halfcyclebreaks = [0]
                cyclebreaks = [0]
                # get the list up to but not including the next keyword
                temp_stepcount = self.stepcount[:self.stepcount.index(keyword)]
                temp_R1 = self.R1[:self.R1.index(keyword)]
                temp_R2 = self.R2[:self.R2.index(keyword)]
                for i in range(len(temp_stepcount)):
                    if  maxstepreached == False and max_step-temp_stepcount[i] <=4:
                        halfcyclebreaks.append(i)
                        maxstepreached = True
                    if maxstepreached == True and temp_stepcount[i] <= 4:
                        cyclebreaks.append(i)
                        halfcyclebreaks.append(i)
                        maxstepreached = False
                    elif maxstepreached == True and i == len(temp_stepcount)-1:
                        cyclebreaks.append(i)
                        halfcyclebreaks.append(i)
                        maxstepreached = False

                #function to interpolate the data 
                #print(halfcyclebreaks)  
                iternum = self.ui.spinBox_cycleEnd.value() - self.ui.spinBox_cycle.value() + 1
                for iter in range(iternum):
                    if iter > 0:
                        label = None
                    lowercycle = self.ui.spinBox_cycle.value()+iter
                    upwardssteps = temp_stepcount[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]                
                    downwardssteps = temp_stepcount[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    upwardsR1 = temp_R1[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]
                    downwardsR1 = temp_R1[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    upwardsR2 = temp_R2[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]
                    downwardsR2 = temp_R2[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    #find indices of duplicates
                    seen = set()
                    indices = [i for i, x in enumerate(upwardssteps) if upwardssteps.count(x) > 1 and x not in seen and not seen.add(x)]
                    #delete duplicates
                    if indices:
                        for index in reversed(indices):
                            del upwardssteps[index]
                            del upwardsR1[index]
                            del upwardsR2[index]
                    seen = set()
                    indices = [i for i, x in enumerate(downwardssteps) if downwardssteps.count(x) > 1 and x not in seen and not seen.add(x)]
                    if indices:
                        for index in reversed(indices):
                            del downwardssteps[index]
                            del downwardsR1[index]
                            del downwardsR2[index]
                    mykind = 'cubic'
                    predictupwards_r1 = interp1d(upwardssteps, upwardsR1, kind=mykind, bounds_error=False, fill_value=(upwardsR1[0], upwardsR1[-1]))
                    predictdownwards_r1 = interp1d(downwardssteps, downwardsR1, kind=mykind, bounds_error=False, fill_value=(downwardsR1[-1], downwardsR1[0]))
                    predictupwards_r2 = interp1d(upwardssteps, upwardsR2, kind=mykind, bounds_error=False, fill_value=(upwardsR2[0], upwardsR2[-1]))
                    predictdownwards_r2 = interp1d(downwardssteps, downwardsR2, kind=mykind, bounds_error=False, fill_value=(downwardsR2[-1], downwardsR2[0]))
                    stepcount_detail = list(range(0, max_step+1))
                    pu_r1 = ndimage.gaussian_filter1d(predictupwards_r1(stepcount_detail), 5)
                    pd_r1 = ndimage.gaussian_filter1d(predictdownwards_r1(stepcount_detail), 5)
                    pu_r2 = ndimage.gaussian_filter1d(predictupwards_r2(stepcount_detail), 5)
                    pd_r2 = ndimage.gaussian_filter1d(predictdownwards_r2(stepcount_detail), 5)
                    error1 = np.mean(np.abs(pu_r1 - pd_r1))
                    error2 = np.mean(np.abs(pu_r2 - pd_r2))
                    #print (stepcount_detail)
                    #upwardcurve = np.array([predictupwards(x) for x in stepcount_detail])
                    #print(upwardcurve)
                    #downwardcurve = np.array([predictdownwards(x) for x in stepcount_detail])
                    #self.graphWidget.plotline(stepcount_detail, upwardcurve, self.findbytimestamp(self.timestamp[t]), self.color)
                    #self.graphWidget.plotline(stepcount_detail, downwardcurve, self.findbytimestamp(self.timestamp[t]), self.color)
                    #counter+=1
                    #self.color = self.colors[counter % 6]
                    #self.graphWidget.plotline(stepcount_detail, pu_r1, self.findbytimestamp(self.timestamp[t]), self.color)
                    #self.graphWidget.plotline(stepcount_detail, pd_r1, str(error1), self.color)
                    self.canvas.plot_line(stepcount_detail, pu_r1, self.color, label)
                    self.canvas.plot_line(stepcount_detail, pd_r1, self.color, None)
                    self.canvas.update_axes(self.toplot, self.xtext+" "+self.xunit, self.ytext+" "+self.yunit)
                    self.canvas2.plot_line(stepcount_detail, pu_r2, self.color, label)
                    self.canvas2.plot_line(stepcount_detail, pd_r2, self.color, None)
                    self.canvas2.update_axes(self.toplot, self.xtext+" "+self.xunit, self.ytext+" "+self.yunit)
                    #self.graphWidget2.plotline(stepcount_detail, pu_r2, self.findbytimestamp(self.timestamp[t]), self.color)
                    #self.graphWidget2.plotline(stepcount_detail, pd_r2, str(error2), self.color)
                # create a list from temp_stepcount from cyclebreak to cyclebreak
                counter +=1
                self.color = self.colors[counter % 6]
                temp_stepcount = temp_stepcount[cyclebreaks[self.ui.spinBox_cycle.value()-1]:cyclebreaks[self.ui.spinBox_cycleEnd.value()]]
                temp_R1 = temp_R1[cyclebreaks[self.ui.spinBox_cycle.value()-1]:cyclebreaks[self.ui.spinBox_cycleEnd.value()]]
                temp_R2 = temp_R2[cyclebreaks[self.ui.spinBox_cycle.value()-1]:cyclebreaks[self.ui.spinBox_cycleEnd.value()]]
                self.canvas.plot_line(temp_stepcount, temp_R1, self.color, label)
                self.canvas2.plot_line(temp_stepcount, temp_R2, self.color, label)
                # delete the list up to the next keyword
                del self.stepcount[:self.stepcount.index(keyword)+1]
                del self.R1[:self.R1.index(keyword)+1]
                del self.R2[:self.R2.index(keyword)+1]
                counter += 1

    # Mean Absolute Error
        elif self.toplot == "Boxplot MAE Hysteresis":
            self.xtext = "Sample #"
            self.ytext = "MAE in Hysteresis _ Each Cycle"
            self.xunit = ""
            self.yunit = "(%)"
            self.graphWidget.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            self.graphWidget2.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            counter = 0
            maxstepreached = False
            cyclebreaks = [0]
            halfcyclebreaks = [0]
            all_data1 = []
            all_data2 = []
            labels = []
            

            for t in range(len(self.timestamp)):
                datacursor.execute("SELECT steps FROM database WHERE timestamp = ?", (self.timestamp[t],))
                max_step = datacursor.fetchall()[0]
                counter = 0
                halfcyclebreaks = [0]
                cyclebreaks = [0]
                labels.append(self.findbytimestamp(self.timestamp[t]))
                alldata1_cycle= []
                alldata2_cycle = []
                # get the list up to but not including the next keyword
                temp_stepcount = self.stepcount[:self.stepcount.index(keyword)]
                temp_R1 = self.R1[:self.R1.index(keyword)]
                temp_R2 = self.R2[:self.R2.index(keyword)]
                for i in range(len(temp_stepcount)):
                    if  maxstepreached == False and max_step-temp_stepcount[i] <=15:
                        halfcyclebreaks.append(i)
                        maxstepreached = True
                    if maxstepreached == True and temp_stepcount[i] <= 15:
                        cyclebreaks.append(i)
                        halfcyclebreaks.append(i)
                        maxstepreached = False
                    elif maxstepreached == True and i == len(temp_stepcount)-1:
                        cyclebreaks.append(i)
                        halfcyclebreaks.append(i)
                        maxstepreached = False

                #function to interpolate the data 
                iternum = self.ui.spinBox_cycleEnd.value() - self.ui.spinBox_cycle.value() + 1
                for iter in range(iternum):
                    lowercycle = self.ui.spinBox_cycle.value()+iter
                    upwardssteps = temp_stepcount[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]                
                    downwardssteps = temp_stepcount[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    upwardsR1 = temp_R1[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]
                    downwardsR1 = temp_R1[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    upwardsR2 = temp_R2[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]
                    downwardsR2 = temp_R2[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    #find indices of duplicates
                    seen = set()
                    indices = [i for i, x in enumerate(upwardssteps) if upwardssteps.count(x) > 1 and x not in seen and not seen.add(x)]
                    #delete duplicates
                    if indices:
                        for index in reversed(indices):
                            del upwardssteps[index]
                            del upwardsR1[index]
                            del upwardsR2[index]
                    seen = set()
                    indices = [i for i, x in enumerate(downwardssteps) if downwardssteps.count(x) > 1 and x not in seen and not seen.add(x)]
                    if indices:
                        for index in reversed(indices):
                            del downwardssteps[index]
                            del downwardsR1[index]
                            del downwardsR2[index]
                    mykind = 'cubic'
                    predictupwards_r1 = interp1d(upwardssteps, upwardsR1, kind=mykind, bounds_error=False, fill_value=(upwardsR1[0], upwardsR1[-1]))
                    predictdownwards_r1 = interp1d(downwardssteps, downwardsR1, kind=mykind, bounds_error=False, fill_value=(downwardsR1[-1], downwardsR1[0]))
                    predictupwards_r2 = interp1d(upwardssteps, upwardsR2, kind=mykind, bounds_error=False, fill_value=(upwardsR2[0], upwardsR2[-1]))
                    predictdownwards_r2 = interp1d(downwardssteps, downwardsR2, kind=mykind, bounds_error=False, fill_value=(downwardsR2[-1], downwardsR2[0]))
                    stepcount_detail = list(range(0, max_step+1))
                    pu_r1 = ndimage.gaussian_filter1d(predictupwards_r1(stepcount_detail), 5)
                    pd_r1 = ndimage.gaussian_filter1d(predictdownwards_r1(stepcount_detail), 5)
                    pu_r2 = ndimage.gaussian_filter1d(predictupwards_r2(stepcount_detail), 5)
                    pd_r2 = ndimage.gaussian_filter1d(predictdownwards_r2(stepcount_detail), 5)
                    div1 = np.abs(max(pu_r1)-min(pu_r1))
                    div2 = np.abs(max(pu_r2)-min(pu_r2))
                    #error1 = np.mean(np.abs(pu_r1 - pd_r1)/div1)
                    #error2 = np.mean(np.abs(pu_r2 - pd_r2)/div2)
                    for xvar in range(1, max_step, 10):
                        alldata1_cycle.append(np.abs(pu_r1[xvar] - pd_r1[xvar]))
                        alldata2_cycle.append(np.abs(pu_r2[xvar] - pd_r2[xvar]))

                    # delete the list up to the next keyword
                all_data1.append(alldata1_cycle)
                all_data2.append(alldata2_cycle)
                del self.stepcount[:self.stepcount.index(keyword)+1]
                del self.R1[:self.R1.index(keyword)+1]
                del self.R2[:self.R2.index(keyword)+1]
            # the following steps order the data so the big numbers are displayed at the right side of the graph.
            # create a tuple containing all_data1 and the labels
            tuple_data1 = zip(all_data1, labels)
            tuple_data2 = zip(all_data2, labels)
            # sort the tuple by the first element, descending
            tuple_data1 = sorted(tuple_data1, key=lambda x: x[0], reverse=True)
            tuple_data2 = sorted(tuple_data2, key=lambda x: x[0], reverse=True)
            # unzip the tuple into two lists
            labels_1 = []
            labels_2 = []
            all_data1, labels_1 = zip(*tuple_data1)
            all_data2, labels_2 = zip(*tuple_data2)


            self.canvas.plot_box(all_data1, self.canvas.axes, True, True, labels_1)
            self.canvas.update_axes(self.toplot, self.xtext+" "+self.xunit, self.ytext+" "+self.yunit)
            self.canvas2.plot_box(all_data2, self.canvas2.axes, True, True, labels_2)
            self.canvas2.update_axes(self.toplot, self.xtext+" "+self.xunit, self.ytext+" "+self.yunit)


        elif self.toplot == "2":
            self.xtext = "Step"
            self.ytext = "Resistance"
            self.xunit = ""
            self.yunit = "(Ohm)"
            #self.graphWidget.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            #self.graphWidget2.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            counter = 0
            maxstepreached = False
            cyclebreaks = [0]
            halfcyclebreaks = [0]
            self.canvas.clear()
            self.canvas2.clear()
            
            

            for t in range(len(self.timestamp)):
                origindata = []
                R1_origin = 1
                R2_origin = 1
                datacursor.execute("SELECT steps FROM database WHERE timestamp = ?", (self.timestamp[t],))
                max_step = datacursor.fetchall()[0]
                label = self.findbytimestamp(self.timestamp[t])
                datacursor.execute("SELECT alldata FROM database WHERE timestamp = ?", (str(self.timestamp[t]),))
                for x in datacursor:
                    origindata = x.split('\n')  
                    origindata.pop()   
                    R1_origin=int(origindata[0].split(',')[2])
                    R2_origin=int(origindata[0].split(',')[3])
                self.color = self.colors[counter % 6]
                halfcyclebreaks = [0]
                cyclebreaks = [0]
                # get the list up to but not including the next keyword
                temp_stepcount = self.stepcount[:self.stepcount.index(keyword)]
                temp_R1 = [x/100*R1_origin+R1_origin for x in self.R1[:self.R1.index(keyword)]]
                temp_R2 = [x/100*R2_origin+R2_origin for x in self.R2[:self.R2.index(keyword)]]
                for i in range(len(temp_stepcount)):
                    if  maxstepreached == False and max_step-temp_stepcount[i] <=4:
                        halfcyclebreaks.append(i)
                        maxstepreached = True
                    if maxstepreached == True and temp_stepcount[i] <= 4:
                        cyclebreaks.append(i)
                        halfcyclebreaks.append(i)
                        maxstepreached = False
                    elif maxstepreached == True and i == len(temp_stepcount)-1:
                        cyclebreaks.append(i)
                        halfcyclebreaks.append(i)
                        maxstepreached = False

                #function to interpolate the data 
                #print(halfcyclebreaks)  
                iternum = self.ui.spinBox_cycleEnd.value() - self.ui.spinBox_cycle.value() + 1
                for iter in range(iternum):
                    if iter > 0:
                        label = None
                    lowercycle = self.ui.spinBox_cycle.value()+iter
                    upwardssteps = temp_stepcount[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]                
                    downwardssteps = temp_stepcount[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    upwardsR1 = temp_R1[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]
                    downwardsR1 = temp_R1[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    upwardsR2 = temp_R2[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]
                    downwardsR2 = temp_R2[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    #find indices of duplicates
                    seen = set()
                    indices = [i for i, x in enumerate(upwardssteps) if upwardssteps.count(x) > 1 and x not in seen and not seen.add(x)]
                    #delete duplicates
                    if indices:
                        for index in reversed(indices):
                            del upwardssteps[index]
                            del upwardsR1[index]
                            del upwardsR2[index]
                    seen = set()
                    indices = [i for i, x in enumerate(downwardssteps) if downwardssteps.count(x) > 1 and x not in seen and not seen.add(x)]
                    if indices:
                        for index in reversed(indices):
                            del downwardssteps[index]
                            del downwardsR1[index]
                            del downwardsR2[index]
                    mykind = 'cubic'
                    predictupwards_r1 = interp1d(upwardssteps, upwardsR1, kind=mykind, bounds_error=False, fill_value=(upwardsR1[0], upwardsR1[-1]))
                    predictdownwards_r1 = interp1d(downwardssteps, downwardsR1, kind=mykind, bounds_error=False, fill_value=(downwardsR1[-1], downwardsR1[0]))
                    predictupwards_r2 = interp1d(upwardssteps, upwardsR2, kind=mykind, bounds_error=False, fill_value=(upwardsR2[0], upwardsR2[-1]))
                    predictdownwards_r2 = interp1d(downwardssteps, downwardsR2, kind=mykind, bounds_error=False, fill_value=(downwardsR2[-1], downwardsR2[0]))
                    stepcount_detail = list(range(0, max_step+1))
                    pu_r1 = ndimage.gaussian_filter1d(predictupwards_r1(stepcount_detail), 5)
                    pd_r1 = ndimage.gaussian_filter1d(predictdownwards_r1(stepcount_detail), 5)
                    pu_r2 = ndimage.gaussian_filter1d(predictupwards_r2(stepcount_detail), 5)
                    pd_r2 = ndimage.gaussian_filter1d(predictdownwards_r2(stepcount_detail), 5)
                    error1 = np.mean(np.abs(pu_r1 - pd_r1))
                    error2 = np.mean(np.abs(pu_r2 - pd_r2))
                    #print (stepcount_detail)
                    #upwardcurve = np.array([predictupwards(x) for x in stepcount_detail])
                    #print(upwardcurve)
                    #downwardcurve = np.array([predictdownwards(x) for x in stepcount_detail])
                    #self.graphWidget.plotline(stepcount_detail, upwardcurve, self.findbytimestamp(self.timestamp[t]), self.color)
                    #self.graphWidget.plotline(stepcount_detail, downwardcurve, self.findbytimestamp(self.timestamp[t]), self.color)
                    #counter+=1
                    #self.color = self.colors[counter % 6]
                    #self.graphWidget.plotline(stepcount_detail, pu_r1, self.findbytimestamp(self.timestamp[t]), self.color)
                    #self.graphWidget.plotline(stepcount_detail, pd_r1, str(error1), self.color)
                    self.canvas.plot_line(stepcount_detail, (1/(pu_r1/pu_r2+1)), self.color, label)
                    self.canvas.plot_line(stepcount_detail, (1/(pd_r1/pd_r2+1)), self.color, None)
                    self.canvas.update_axes(self.toplot, self.xtext+" "+self.xunit, "1/(r1/r2+1)")
                    self.canvas2.plot_line(stepcount_detail, pu_r1, self.color, label)
                    self.canvas2.plot_line(stepcount_detail, pd_r1, self.color, None)
                    self.canvas2.plot_line(stepcount_detail, pu_r2, self.color, label)
                    self.canvas2.plot_line(stepcount_detail, pd_r2, self.color, None)
                    self.canvas2.update_axes(self.toplot, self.xtext+" "+self.xunit, self.ytext+" "+self.yunit)
                    #self.graphWidget2.plotline(stepcount_detail, pu_r2, self.findbytimestamp(self.timestamp[t]), self.color)
                    #self.graphWidget2.plotline(stepcount_detail, pd_r2, str(error2), self.color)
                # create a list from temp_stepcount from cyclebreak to cyclebreak
                counter +=1
                self.color = self.colors[counter % 6]
                temp_stepcount = temp_stepcount[cyclebreaks[self.ui.spinBox_cycle.value()-1]:cyclebreaks[self.ui.spinBox_cycleEnd.value()]]
                temp_R1 = temp_R1[cyclebreaks[self.ui.spinBox_cycle.value()-1]:cyclebreaks[self.ui.spinBox_cycleEnd.value()]]
                temp_R2 = temp_R2[cyclebreaks[self.ui.spinBox_cycle.value()-1]:cyclebreaks[self.ui.spinBox_cycleEnd.value()]]
                # delete the list up to the next keyword
                del self.stepcount[:self.stepcount.index(keyword)+1]
                del self.R1[:self.R1.index(keyword)+1]
                del self.R2[:self.R2.index(keyword)+1]
                counter += 1



    def uppercyclechanged(self):
        if self.ui.spinBox_cycleEnd.value() < self.ui.spinBox_cycle.value():
            self.ui.spinBox_cycle.setValue(self.ui.spinBox_cycleEnd.value())
        self.whatcyclesir()

    def whatcyclesir(self):
        if self.ui.spinBox_cycle.value() > self.ui.spinBox_cycleEnd.value():
            self.ui.spinBox_cycleEnd.setValue(self.ui.spinBox_cycle.value())
        self.cycle = self.ui.spinBox_cycle.value()
        self.cycleEnd = self.ui.spinBox_cycleEnd.value()
        self.checktheboxes()
        if self.checkthedata():
            datacursor.execute(self.checkthedata())
        else:
            datacursor.execute("SELECT timestamp FROM database WHERE project = ?", (self.ui.comboBox_project.currentText(),))
        tempdata = datacursor.fetchall()
        self.set_detailWindow(tempdata)
        self.splitData(tempdata)



    def findbytimestamp(self, timestamp):
        datacursor_tuple.execute("SELECT design, sample, material, print, orientation, apara, bpara, fpara, gpara, direction, speed, cycles, steps FROM database WHERE timestamp = ?", (timestamp,))
        x = datacursor_tuple.fetchall()
        # remove None values from the list
        x = [[i for i in sublist if i is not None] for sublist in x]
        # remove given characters from the list
        notinteresting = ["A0", "B0", "F0", "G0"]
        x = [[i for i in sublist if i not in notinteresting] for sublist in x]
        x = ["_".join(str(i) for i in sublist) for sublist in x]
        string = timestamp + "_" + x[0]
        return string


    # this function is bad practice*, but could be used to quicken the calculations
    # *bad practice because creating new tables with variable names is not good practice
    # However, calculation times are so short that it is not needed.
    def save_table(self, timestamp, timecount, stepcount, R1, R2):
        # create a new table with the data from the selected timestamp
        # this is done by creating a new table with the same name as the timestamp
        # the data is then taken from the database, split into cycles and saved into the new table
        timestamp = str(timestamp).replace(".", "_")
        timestamp =str(timestamp).replace(" ", "_")
        command = "CREATE TABLE IF NOT EXISTS \"" + timestamp + "\" (timecount int PRIMARY KEY ON CONFLICT IGNORE, stepcount int, R1 real, R2 real)"
        datacursor.execute(command)
        for i in range(len(timecount)):
            datacursor.execute("INSERT OR IGNORE INTO \"" + timestamp + "\" (timecount) VALUES (?)", (timecount[i],))
            datacursor.execute("UPDATE \"" + timestamp + "\" SET stepcount = ? WHERE timecount = ?", (stepcount[i], timecount[i]))
            datacursor.execute("UPDATE \"" + timestamp + "\" SET R1 = ? WHERE timecount = ?", (R1[i], timecount[i]))
            datacursor.execute("UPDATE \"" + timestamp + "\" SET R2 = ? WHERE timecount = ?", (R2[i], timecount[i]))



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
        #files = os.listdir(directory)
        for root, dirs, files in os.walk(directory):
        # Create a list to store the data
        # Loop through the files
            for i in files:
                # Check if the file is a .csv file
                if i.endswith(".csv"):
                    for duplicate in self.data:
                        if i[:-4] in duplicate:
                            dupcheck = True
                    # Check for duplicate files. Altough this is not needed, because the database uses unique timestamps to make dups impossible,
                    # this is a good check to save on computing time
                    if dupcheck == False:
                        # Save the file name without .csv to the list, it is the unique timestamp of this test
                        self.data.append("Timestamp")
                        self.data.append(i[:-4])
                        # Parse the contents of the file line by line and save to a list
                        with open(os.path.join(root,i), "r") as f:
                            # Read the lines and save them in a list
                            lines = f.readlines()
                            # first line contains the sample parameters and the second line contains the test parameters
                            # Remove the newline character from the end of these lines fisrt
                            lines[0] = lines[0][:-1]
                            lines[1] = lines[1][:-1]
                            # Now we split the lines into a list of parameters
                            self.data.append("Sample")
                            self.data.append(lines[0].split('_'))
                            self.data.append("Test")
                            self.data.append(lines[1].split(','))
                            # Line 2 is the header for the raw data, so we skip it and add the rest of the lines to the list
                            self.rawdata.append("".join(lines[7:])) 
                        print("Data added")  
                        # Now we add the parsed data into the database according to the parameters in the file
                        self.onclick_upload()
                        # Remove the keywords used in the onclick_upload function so we do not try to upload the same data again
                        self.data.remove("Timestamp")
                        self.data.remove("Sample")
                        self.data.remove("Test")
                    else:
                        # If the file is a duplicate, skip it
                        print("Duplicate file found: "+i)
                        dupcheck = False
                        continue           

# this class uses pyqtgraph to plot the data, it is not used anymore, but it is kept here for reference
class ScatterPlot(pg.PlotWidget):
    def __init__(self, xtext, xunit, ytext, yunit, **kargs):
        super().__init__(**kargs)
        self.setBackground('w')
        self.setLabel(axis='bottom', text=xtext, units=xunit)
        self.setLabel(axis='left', text=ytext, units=yunit)
        self.showGrid(x=True, y=True, alpha=0.5)

    def refresh(self, xtext, xunit, ytext, yunit):
        self.clear()
        self.setLabel(axis='bottom', text=xtext + " " + xunit)
        self.setLabel(axis='left', text=ytext + " " + yunit)

    def plotnew(self, x, y, coding, color, size):
        self.addItem(pg.ScatterPlotItem(x, y, symbol='o', size=size, data=coding, hoverable=True, brush=QBrush(QColor(*color))))

    def plotline(self, x, y, coding, color):
        self.addItem(pg.ScatterPlotItem(x, y, symbol='o', size=5, data=coding, hoverable=True, brush=QBrush(QColor(*color))))
        self.addItem(pg.PlotCurveItem(x, y, pen=pg.mkPen(color=color, width=2)))

# this class is used to plot the data using matplotlib.
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(1, 1, 1)
        #self.axes2 = fig.add_subplot(2, 1, 2)
        super(MplCanvas, self).__init__(fig)

    def plot_box(self, all_data, ax, vert=True, color=False, labels=["x1"]):
        ax.cla() #clear self
        defaultlabels = []
        for i in range(len(all_data)):
            defaultlabels.append(str(i+1))
        ax.boxplot(all_data,
                         vert=vert,  # vertical box alignment
                         patch_artist=color,  # fill with color
                         labels=defaultlabels)  # will be used to label x-ticks
        #combine both lists to say which label is which
        legendlabels = []
        for i in range(len(defaultlabels)):
            legendlabels.append(defaultlabels[i] + ": " + labels[i])      
        ax.legend(legendlabels, facecolor = 'lightgray', loc=1, fontsize=7)
        # Trigger the canvas to update and redraw.
        self.draw()
    
    def clear(self):
        #clear the plottet items
        self.axes.cla()
        # Trigger the canvas to update and redraw.
        self.draw()

    def update_axes(self, titletext, xtext, ytext):
        self.axes.set_title(titletext)
        self.axes.set_xlabel(xtext)
        self.axes.set_ylabel(ytext)
        self.axes.xaxis.set_label_coords(-0.01, -0.04)
        self.draw()


    def plot_dot(self, x, y, color, size, label):
        self.axes.scatter(x, y, c=color, s=size, label=label)
        self.axes.legend(facecolor = 'lightgray', loc=0, fontsize=7)
        # Trigger the canvas to update and redraw.
        self.draw()


    def plot_line(self, x, y, color, label):
        self.axes.plot(x, y, color=color, label=label)
        self.axes.legend(facecolor = 'lightgray', loc=0, fontsize=7)
        self.draw()

class DetailWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DetWindow()
        self.ui.setupUi(self)
        self.checkboxes = []
        self.checked_cb = []
        self.unchecked_cb = []
        self.parent_to_boxes = self.ui.scrollAreaWidgetContents
    
    def renew_checkboxes(self, timestamps):
        check = False
        for box in self.parent_to_boxes.findChildren(QCheckBox):           
            if box.text() not in timestamps:
                self.checkboxes.remove(box)
                box.deleteLater()
        for i in range(len(timestamps)):
            for box in self.parent_to_boxes.findChildren(QCheckBox):
                if box.text() == timestamps[i]:
                    check = True
            if check == False:    
                self.addCheckbox(timestamps[i])
            else:
                check = False
        self.checktheboxes()

    def addCheckbox(self, name):
        self.parent_to_boxes.setLayout(QVBoxLayout())
        checkbox = QCheckBox(name)
        self.checkboxes.append(checkbox)
        self.parent_to_boxes.layout().addWidget(checkbox)
        checkbox.stateChanged.connect(self.on_checkbox_changed)
        checkbox.setChecked(True)
        checkbox.setVisible(True)

    def checktheboxes(self):
        # first the filters are reset
        self.checked_cb = []
        self.unchecked_cb = []
        # If any are checked, they are added to the corresponding list by their displayed names
        for i in self.parent_to_boxes.findChildren(QCheckBox):
            #if i is checked
            if i.isChecked():
                self.checked_cb.append(i.text()[0:20])

            #if i is not checked
            else:
                self.unchecked_cb.append(i.text())

    def on_checkbox_changed(self):
        self.checktheboxes()
        #print (self.unchecked_cb)

    def get_timestamps(self):
        return self.checked_cb
    
    def testfunction(self):
        print("test")
    

# This function is called when the user starts the program. It creates the main window and starts the program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())