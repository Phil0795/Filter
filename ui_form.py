# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QMainWindow,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1305, 919)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pselectLayout = QHBoxLayout()
        self.pselectLayout.setObjectName(u"pselectLayout")
        self.pushButton_upload = QPushButton(self.centralwidget)
        self.pushButton_upload.setObjectName(u"pushButton_upload")

        self.pselectLayout.addWidget(self.pushButton_upload)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.pselectLayout.addWidget(self.pushButton)

        self.horizontalSpacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.pselectLayout.addItem(self.horizontalSpacer_left)

        self.label_project = QLabel(self.centralwidget)
        self.label_project.setObjectName(u"label_project")

        self.pselectLayout.addWidget(self.label_project)

        self.comboBox_project = QComboBox(self.centralwidget)
        self.comboBox_project.setObjectName(u"comboBox_project")

        self.pselectLayout.addWidget(self.comboBox_project)

        self.horizontalSpacer_mid = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.pselectLayout.addItem(self.horizontalSpacer_mid)

        self.label_value = QLabel(self.centralwidget)
        self.label_value.setObjectName(u"label_value")

        self.pselectLayout.addWidget(self.label_value)

        self.comboBox_value = QComboBox(self.centralwidget)
        self.comboBox_value.addItem("")
        self.comboBox_value.addItem("")
        self.comboBox_value.addItem("")
        self.comboBox_value.addItem("")
        self.comboBox_value.addItem("")
        self.comboBox_value.addItem("")
        self.comboBox_value.addItem("")
        self.comboBox_value.addItem("")
        self.comboBox_value.addItem("")
        self.comboBox_value.addItem("")
        self.comboBox_value.addItem("")
        self.comboBox_value.setObjectName(u"comboBox_value")

        self.pselectLayout.addWidget(self.comboBox_value)

        self.horizontalSpacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.pselectLayout.addItem(self.horizontalSpacer_right)


        self.verticalLayout.addLayout(self.pselectLayout)

        self.widget_top = QWidget(self.centralwidget)
        self.widget_top.setObjectName(u"widget_top")

        self.verticalLayout.addWidget(self.widget_top)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_detail = QPushButton(self.centralwidget)
        self.pushButton_detail.setObjectName(u"pushButton_detail")

        self.horizontalLayout.addWidget(self.pushButton_detail)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.widget_bot = QWidget(self.centralwidget)
        self.widget_bot.setObjectName(u"widget_bot")

        self.verticalLayout.addWidget(self.widget_bot)

        self.detailselectLayout = QGridLayout()
        self.detailselectLayout.setObjectName(u"detailselectLayout")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.detailselectLayout.addWidget(self.label_6, 0, 9, 1, 1)

        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")

        self.detailselectLayout.addWidget(self.label_14, 0, 6, 1, 1)

        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")

        self.detailselectLayout.addWidget(self.label_9, 0, 1, 1, 1)

        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")

        self.detailselectLayout.addWidget(self.label_11, 0, 3, 1, 1)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")

        self.detailselectLayout.addWidget(self.label_7, 0, 0, 1, 1)

        self.scrollArea_sample = QScrollArea(self.centralwidget)
        self.scrollArea_sample.setObjectName(u"scrollArea_sample")
        self.scrollArea_sample.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea_sample.setWidgetResizable(True)
        self.scrollAreaWidgetContents_sample = QWidget()
        self.scrollAreaWidgetContents_sample.setObjectName(u"scrollAreaWidgetContents_sample")
        self.scrollAreaWidgetContents_sample.setGeometry(QRect(0, 0, 83, 754))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents_sample)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.scrollArea_sample.setWidget(self.scrollAreaWidgetContents_sample)

        self.detailselectLayout.addWidget(self.scrollArea_sample, 1, 1, 1, 1)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")

        self.detailselectLayout.addWidget(self.label_8, 0, 10, 1, 1)

        self.label_15 = QLabel(self.centralwidget)
        self.label_15.setObjectName(u"label_15")

        self.detailselectLayout.addWidget(self.label_15, 0, 7, 1, 1)

        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")

        self.detailselectLayout.addWidget(self.label_12, 0, 4, 1, 1)

        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")

        self.detailselectLayout.addWidget(self.label_13, 0, 5, 1, 1)

        self.label_16 = QLabel(self.centralwidget)
        self.label_16.setObjectName(u"label_16")

        self.detailselectLayout.addWidget(self.label_16, 0, 8, 1, 1)

        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")

        self.detailselectLayout.addWidget(self.label_10, 0, 2, 1, 1)

        self.scrollArea_design = QScrollArea(self.centralwidget)
        self.scrollArea_design.setObjectName(u"scrollArea_design")
        self.scrollArea_design.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea_design.setWidgetResizable(True)
        self.scrollAreaWidgetContents_design = QWidget()
        self.scrollAreaWidgetContents_design.setObjectName(u"scrollAreaWidgetContents_design")
        self.scrollAreaWidgetContents_design.setGeometry(QRect(0, 0, 82, 754))
        self.verticalLayout_design = QVBoxLayout(self.scrollAreaWidgetContents_design)
        self.verticalLayout_design.setObjectName(u"verticalLayout_design")
        self.scrollArea_design.setWidget(self.scrollAreaWidgetContents_design)

        self.detailselectLayout.addWidget(self.scrollArea_design, 1, 0, 1, 1)

        self.label_17 = QLabel(self.centralwidget)
        self.label_17.setObjectName(u"label_17")

        self.detailselectLayout.addWidget(self.label_17, 0, 11, 1, 1)

        self.scrollArea_material = QScrollArea(self.centralwidget)
        self.scrollArea_material.setObjectName(u"scrollArea_material")
        self.scrollArea_material.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea_material.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.scrollArea_material.setWidgetResizable(True)
        self.scrollAreaWidgetContents_material = QWidget()
        self.scrollAreaWidgetContents_material.setObjectName(u"scrollAreaWidgetContents_material")
        self.scrollAreaWidgetContents_material.setGeometry(QRect(0, 0, 99, 754))
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents_material)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.scrollArea_material.setWidget(self.scrollAreaWidgetContents_material)

        self.detailselectLayout.addWidget(self.scrollArea_material, 1, 2, 1, 1)

        self.scrollArea_print = QScrollArea(self.centralwidget)
        self.scrollArea_print.setObjectName(u"scrollArea_print")
        self.scrollArea_print.setWidgetResizable(True)
        self.scrollAreaWidgetContents_print = QWidget()
        self.scrollAreaWidgetContents_print.setObjectName(u"scrollAreaWidgetContents_print")
        self.scrollAreaWidgetContents_print.setGeometry(QRect(0, 0, 100, 754))
        self.verticalLayout_7 = QVBoxLayout(self.scrollAreaWidgetContents_print)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setSizeConstraint(QLayout.SetNoConstraint)
        self.scrollArea_print.setWidget(self.scrollAreaWidgetContents_print)

        self.detailselectLayout.addWidget(self.scrollArea_print, 1, 3, 1, 1)

        self.scrollArea_orientation = QScrollArea(self.centralwidget)
        self.scrollArea_orientation.setObjectName(u"scrollArea_orientation")
        self.scrollArea_orientation.setWidgetResizable(True)
        self.scrollAreaWidgetContents_orientation = QWidget()
        self.scrollAreaWidgetContents_orientation.setObjectName(u"scrollAreaWidgetContents_orientation")
        self.scrollAreaWidgetContents_orientation.setGeometry(QRect(0, 0, 99, 754))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents_orientation)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea_orientation.setWidget(self.scrollAreaWidgetContents_orientation)

        self.detailselectLayout.addWidget(self.scrollArea_orientation, 1, 4, 1, 1)

        self.scrollArea_A = QScrollArea(self.centralwidget)
        self.scrollArea_A.setObjectName(u"scrollArea_A")
        self.scrollArea_A.setWidgetResizable(True)
        self.scrollAreaWidgetContents_A = QWidget()
        self.scrollAreaWidgetContents_A.setObjectName(u"scrollAreaWidgetContents_A")
        self.scrollAreaWidgetContents_A.setGeometry(QRect(0, 0, 99, 754))
        self.verticalLayout_8 = QVBoxLayout(self.scrollAreaWidgetContents_A)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.scrollArea_A.setWidget(self.scrollAreaWidgetContents_A)

        self.detailselectLayout.addWidget(self.scrollArea_A, 1, 5, 1, 1)

        self.scrollArea_B = QScrollArea(self.centralwidget)
        self.scrollArea_B.setObjectName(u"scrollArea_B")
        self.scrollArea_B.setWidgetResizable(True)
        self.scrollAreaWidgetContents_B = QWidget()
        self.scrollAreaWidgetContents_B.setObjectName(u"scrollAreaWidgetContents_B")
        self.scrollAreaWidgetContents_B.setGeometry(QRect(0, 0, 100, 754))
        self.verticalLayout_9 = QVBoxLayout(self.scrollAreaWidgetContents_B)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.scrollArea_B.setWidget(self.scrollAreaWidgetContents_B)

        self.detailselectLayout.addWidget(self.scrollArea_B, 1, 6, 1, 1)

        self.scrollArea_F = QScrollArea(self.centralwidget)
        self.scrollArea_F.setObjectName(u"scrollArea_F")
        self.scrollArea_F.setWidgetResizable(True)
        self.scrollAreaWidgetContents_F = QWidget()
        self.scrollAreaWidgetContents_F.setObjectName(u"scrollAreaWidgetContents_F")
        self.scrollAreaWidgetContents_F.setGeometry(QRect(0, 0, 99, 754))
        self.verticalLayout_10 = QVBoxLayout(self.scrollAreaWidgetContents_F)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.scrollArea_F.setWidget(self.scrollAreaWidgetContents_F)

        self.detailselectLayout.addWidget(self.scrollArea_F, 1, 7, 1, 1)

        self.scrollArea_G = QScrollArea(self.centralwidget)
        self.scrollArea_G.setObjectName(u"scrollArea_G")
        self.scrollArea_G.setWidgetResizable(True)
        self.scrollAreaWidgetContents_G = QWidget()
        self.scrollAreaWidgetContents_G.setObjectName(u"scrollAreaWidgetContents_G")
        self.scrollAreaWidgetContents_G.setGeometry(QRect(0, 0, 100, 754))
        self.verticalLayout_11 = QVBoxLayout(self.scrollAreaWidgetContents_G)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.scrollArea_G.setWidget(self.scrollAreaWidgetContents_G)

        self.detailselectLayout.addWidget(self.scrollArea_G, 1, 8, 1, 1)

        self.scrollArea_speed = QScrollArea(self.centralwidget)
        self.scrollArea_speed.setObjectName(u"scrollArea_speed")
        self.scrollArea_speed.setWidgetResizable(True)
        self.scrollAreaWidgetContents_speed = QWidget()
        self.scrollAreaWidgetContents_speed.setObjectName(u"scrollAreaWidgetContents_speed")
        self.scrollAreaWidgetContents_speed.setGeometry(QRect(0, 0, 99, 754))
        self.verticalLayout_12 = QVBoxLayout(self.scrollAreaWidgetContents_speed)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.scrollArea_speed.setWidget(self.scrollAreaWidgetContents_speed)

        self.detailselectLayout.addWidget(self.scrollArea_speed, 1, 9, 1, 1)

        self.scrollArea_cycles = QScrollArea(self.centralwidget)
        self.scrollArea_cycles.setObjectName(u"scrollArea_cycles")
        self.scrollArea_cycles.setWidgetResizable(True)
        self.scrollAreaWidgetContents_cycles = QWidget()
        self.scrollAreaWidgetContents_cycles.setObjectName(u"scrollAreaWidgetContents_cycles")
        self.scrollAreaWidgetContents_cycles.setGeometry(QRect(0, 0, 100, 754))
        self.verticalLayout_13 = QVBoxLayout(self.scrollAreaWidgetContents_cycles)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.scrollArea_cycles.setWidget(self.scrollAreaWidgetContents_cycles)

        self.detailselectLayout.addWidget(self.scrollArea_cycles, 1, 10, 1, 1)

        self.scrollArea_steps = QScrollArea(self.centralwidget)
        self.scrollArea_steps.setObjectName(u"scrollArea_steps")
        self.scrollArea_steps.setWidgetResizable(True)
        self.scrollAreaWidgetContents_steps = QWidget()
        self.scrollAreaWidgetContents_steps.setObjectName(u"scrollAreaWidgetContents_steps")
        self.scrollAreaWidgetContents_steps.setGeometry(QRect(0, 0, 99, 754))
        self.verticalLayout_14 = QVBoxLayout(self.scrollAreaWidgetContents_steps)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.scrollArea_steps.setWidget(self.scrollAreaWidgetContents_steps)

        self.detailselectLayout.addWidget(self.scrollArea_steps, 1, 11, 1, 1)


        self.verticalLayout.addLayout(self.detailselectLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1305, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_upload.setText(QCoreApplication.translate("MainWindow", u"Upload new samples", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.label_project.setText(QCoreApplication.translate("MainWindow", u"Project", None))
        self.label_value.setText(QCoreApplication.translate("MainWindow", u"Value", None))
        self.comboBox_value.setItemText(0, QCoreApplication.translate("MainWindow", u"Resistance / Time", None))
        self.comboBox_value.setItemText(1, QCoreApplication.translate("MainWindow", u"Resistance / Steps", None))
        self.comboBox_value.setItemText(2, QCoreApplication.translate("MainWindow", u"Hysterese (mean)", None))
        self.comboBox_value.setItemText(3, QCoreApplication.translate("MainWindow", u"Peaks over time", None))
        self.comboBox_value.setItemText(4, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBox_value.setItemText(5, QCoreApplication.translate("MainWindow", u"2", None))
        self.comboBox_value.setItemText(6, QCoreApplication.translate("MainWindow", u"3", None))
        self.comboBox_value.setItemText(7, QCoreApplication.translate("MainWindow", u"4", None))
        self.comboBox_value.setItemText(8, QCoreApplication.translate("MainWindow", u"5", None))
        self.comboBox_value.setItemText(9, QCoreApplication.translate("MainWindow", u"6", None))
        self.comboBox_value.setItemText(10, QCoreApplication.translate("MainWindow", u"7", None))

        self.pushButton_detail.setText(QCoreApplication.translate("MainWindow", u"Details", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Speed", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"B-Parameter", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Sample", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Print char.", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Design", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Cycles", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"F-Parameter", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Orientation", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"A-Parameter", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"G-Parameter", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Material", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Steps", None))
    # retranslateUi

