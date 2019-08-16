# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(792, 537)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.logoLabel = QtWidgets.QLabel(self.centralWidget)
        self.logoLabel.setText("")
        self.logoLabel.setPixmap(QtGui.QPixmap("Dygma_logo_color.png"))
        self.logoLabel.setObjectName("logoLabel")
        self.verticalLayout.addWidget(self.logoLabel)
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.light = QtWidgets.QWidget()
        self.light.setObjectName("light")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.light)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.light_white = QtWidgets.QPushButton(self.light)
        self.light_white.setObjectName("light_white")
        self.gridLayout.addWidget(self.light_white, 3, 0, 1, 1)
        self.light_red = QtWidgets.QPushButton(self.light)
        self.light_red.setObjectName("light_red")
        self.gridLayout.addWidget(self.light_red, 0, 0, 1, 1)
        self.light_blue = QtWidgets.QPushButton(self.light)
        self.light_blue.setObjectName("light_blue")
        self.gridLayout.addWidget(self.light_blue, 2, 0, 1, 1)
        self.light_green = QtWidgets.QPushButton(self.light)
        self.light_green.setObjectName("light_green")
        self.gridLayout.addWidget(self.light_green, 1, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.tabWidget.addTab(self.light, "")
        self.magnet = QtWidgets.QWidget()
        self.magnet.setObjectName("magnet")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.magnet)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.magnet_joined = QtWidgets.QPushButton(self.magnet)
        self.magnet_joined.setObjectName("magnet_joined")
        self.gridLayout_2.addWidget(self.magnet_joined, 0, 0, 1, 1)
        self.magnet_split = QtWidgets.QPushButton(self.magnet)
        self.magnet_split.setObjectName("magnet_split")
        self.gridLayout_2.addWidget(self.magnet_split, 1, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.tabWidget.addTab(self.magnet, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.log_messages = QtWidgets.QPlainTextEdit(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.log_messages.sizePolicy().hasHeightForWidth())
        self.log_messages.setSizePolicy(sizePolicy)
        self.log_messages.setObjectName("log_messages")
        self.verticalLayout.addWidget(self.log_messages)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 792, 27))
        self.menuBar.setObjectName("menuBar")
        self.menuDygma_Raise_Assembly_Tests = QtWidgets.QMenu(self.menuBar)
        self.menuDygma_Raise_Assembly_Tests.setObjectName("menuDygma_Raise_Assembly_Tests")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar.addAction(self.menuDygma_Raise_Assembly_Tests.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dygma Raise Assembly Tests"))
        self.light_white.setText(_translate("MainWindow", "White"))
        self.light_red.setText(_translate("MainWindow", "Red"))
        self.light_blue.setText(_translate("MainWindow", "Blue"))
        self.light_green.setText(_translate("MainWindow", "Green"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.light), _translate("MainWindow", "Light control"))
        self.magnet_joined.setText(_translate("MainWindow", "Keyboard is Joined"))
        self.magnet_split.setText(_translate("MainWindow", "Keyboard is Split"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.magnet), _translate("MainWindow", "Magnet Calibrate"))
        self.menuDygma_Raise_Assembly_Tests.setTitle(_translate("MainWindow", "Dygma Raise Assembly Tests"))

