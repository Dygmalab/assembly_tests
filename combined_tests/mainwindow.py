# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(714, 524)
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
        self.logoLabel.setPixmap(QtGui.QPixmap(":/images/Dygma_logo_color.png"))
        self.logoLabel.setObjectName("logoLabel")
        self.verticalLayout.addWidget(self.logoLabel)
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 0))
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
        self.light_off = QtWidgets.QPushButton(self.light)
        self.light_off.setObjectName("light_off")
        self.gridLayout.addWidget(self.light_off, 4, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.tabWidget.addTab(self.light, "")
        self.individualleds = QtWidgets.QWidget()
        self.individualleds.setObjectName("individualleds")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.individualleds)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.led_next = QtWidgets.QPushButton(self.individualleds)
        self.led_next.setEnabled(True)
        self.led_next.setObjectName("led_next")
        self.gridLayout_4.addWidget(self.led_next, 0, 0, 1, 1)
        self.led_prev = QtWidgets.QPushButton(self.individualleds)
        self.led_prev.setEnabled(True)
        self.led_prev.setObjectName("led_prev")
        self.gridLayout_4.addWidget(self.led_prev, 1, 0, 1, 1)
        self.led_num = QtWidgets.QLCDNumber(self.individualleds)
        self.led_num.setObjectName("led_num")
        self.gridLayout_4.addWidget(self.led_num, 2, 0, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_4)
        self.tabWidget.addTab(self.individualleds, "")
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
        self.magnet_joined.setEnabled(True)
        self.magnet_joined.setObjectName("magnet_joined")
        self.gridLayout_2.addWidget(self.magnet_joined, 0, 0, 1, 1)
        self.magnet_split = QtWidgets.QPushButton(self.magnet)
        self.magnet_split.setEnabled(False)
        self.magnet_split.setObjectName("magnet_split")
        self.gridLayout_2.addWidget(self.magnet_split, 1, 0, 1, 1)
        self.magnet_level = QtWidgets.QProgressBar(self.magnet)
        self.magnet_level.setMinimum(500)
        self.magnet_level.setMaximum(800)
        self.magnet_level.setProperty("value", 600)
        self.magnet_level.setTextVisible(True)
        self.magnet_level.setObjectName("magnet_level")
        self.gridLayout_2.addWidget(self.magnet_level, 3, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.tabWidget.addTab(self.magnet, "")
        self.defaults_tab = QtWidgets.QWidget()
        self.defaults_tab.setObjectName("defaults_tab")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.defaults_tab)
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.load_defaults = QtWidgets.QPushButton(self.defaults_tab)
        self.load_defaults.setObjectName("load_defaults")
        self.gridLayout_3.addWidget(self.load_defaults, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 1, 0, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout_3)
        self.tabWidget.addTab(self.defaults_tab, "")
        self.side_firmware = QtWidgets.QWidget()
        self.side_firmware.setObjectName("side_firmware")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.side_firmware)
        self.horizontalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.verify_left = QtWidgets.QPushButton(self.side_firmware)
        self.verify_left.setObjectName("verify_left")
        self.gridLayout_5.addWidget(self.verify_left, 0, 0, 1, 1)
        self.verify_right = QtWidgets.QPushButton(self.side_firmware)
        self.verify_right.setObjectName("verify_right")
        self.gridLayout_5.addWidget(self.verify_right, 1, 0, 1, 1)
        self.flash_right = QtWidgets.QPushButton(self.side_firmware)
        self.flash_right.setObjectName("flash_right")
        self.gridLayout_5.addWidget(self.flash_right, 4, 0, 1, 1)
        self.flash_left = QtWidgets.QPushButton(self.side_firmware)
        self.flash_left.setObjectName("flash_left")
        self.gridLayout_5.addWidget(self.flash_left, 3, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem2, 2, 0, 1, 1)
        self.horizontalLayout_4.addLayout(self.gridLayout_5)
        self.tabWidget.addTab(self.side_firmware, "")
        self.focus = QtWidgets.QWidget()
        self.focus.setObjectName("focus")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.focus)
        self.horizontalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label = QtWidgets.QLabel(self.focus)
        self.label.setObjectName("label")
        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem3, 2, 0, 1, 1)
        self.focus_cmd = QtWidgets.QLineEdit(self.focus)
        self.focus_cmd.setObjectName("focus_cmd")
        self.gridLayout_6.addWidget(self.focus_cmd, 1, 0, 1, 1)
        self.horizontalLayout_5.addLayout(self.gridLayout_6)
        self.tabWidget.addTab(self.focus, "")
        self.info_tab = QtWidgets.QWidget()
        self.info_tab.setObjectName("info_tab")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.info_tab)
        self.horizontalLayout_6.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.info_tab)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_6.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.info_tab)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_6.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.info_tab)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_6.addWidget(self.label_4)
        self.horizontalLayout_7.addLayout(self.verticalLayout_6)
        self.line = QtWidgets.QFrame(self.info_tab)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_7.addWidget(self.line)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.keyscan_label = QtWidgets.QLabel(self.info_tab)
        self.keyscan_label.setObjectName("keyscan_label")
        self.verticalLayout_7.addWidget(self.keyscan_label)
        self.layout_label = QtWidgets.QLabel(self.info_tab)
        self.layout_label.setObjectName("layout_label")
        self.verticalLayout_7.addWidget(self.layout_label)
        self.version_label = QtWidgets.QLabel(self.info_tab)
        self.version_label.setObjectName("version_label")
        self.verticalLayout_7.addWidget(self.version_label)
        self.horizontalLayout_7.addLayout(self.verticalLayout_7)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_7)
        self.tabWidget.addTab(self.info_tab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.log_messages = QtWidgets.QPlainTextEdit(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.log_messages.sizePolicy().hasHeightForWidth())
        self.log_messages.setSizePolicy(sizePolicy)
        self.log_messages.setReadOnly(True)
        self.log_messages.setObjectName("log_messages")
        self.verticalLayout.addWidget(self.log_messages)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 714, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuDygma_Raise_Assembly_Tests = QtWidgets.QMenu(self.menuBar)
        self.menuDygma_Raise_Assembly_Tests.setObjectName("menuDygma_Raise_Assembly_Tests")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionCopy_log = QtWidgets.QAction(MainWindow)
        self.actionCopy_log.setObjectName("actionCopy_log")
        self.actionClear_log = QtWidgets.QAction(MainWindow)
        self.actionClear_log.setObjectName("actionClear_log")
        self.menuDygma_Raise_Assembly_Tests.addAction(self.actionCopy_log)
        self.menuDygma_Raise_Assembly_Tests.addAction(self.actionClear_log)
        self.menuBar.addAction(self.menuDygma_Raise_Assembly_Tests.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dygma Raise Assembly Tests"))
        self.light_white.setText(_translate("MainWindow", "White"))
        self.light_red.setText(_translate("MainWindow", "Red"))
        self.light_blue.setText(_translate("MainWindow", "Blue"))
        self.light_green.setText(_translate("MainWindow", "Green"))
        self.light_off.setText(_translate("MainWindow", "Off"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.light), _translate("MainWindow", "All LEDs"))
        self.led_next.setText(_translate("MainWindow", "Next"))
        self.led_prev.setText(_translate("MainWindow", "Prev"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.individualleds), _translate("MainWindow", "Single LEDs"))
        self.magnet_joined.setText(_translate("MainWindow", "Press when keyboard is Joined"))
        self.magnet_split.setText(_translate("MainWindow", "Press when keyboard is Split"))
        self.magnet_level.setFormat(_translate("MainWindow", "%v"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.magnet), _translate("MainWindow", "Magnet Calibrate"))
        self.load_defaults.setText(_translate("MainWindow", "Load Defaults (will wipe all settings)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.defaults_tab), _translate("MainWindow", "Load Defaults"))
        self.verify_left.setText(_translate("MainWindow", "Verify Left"))
        self.verify_right.setText(_translate("MainWindow", "Verify Right"))
        self.flash_right.setText(_translate("MainWindow", "Flash Right"))
        self.flash_left.setText(_translate("MainWindow", "Flash Left"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.side_firmware), _translate("MainWindow", "Side Firmware"))
        self.label.setText(_translate("MainWindow", "Type commands below (type help to show available commands)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.focus), _translate("MainWindow", "Focus"))
        self.label_2.setText(_translate("MainWindow", "Keyscan"))
        self.label_3.setText(_translate("MainWindow", "Layout"))
        self.label_4.setText(_translate("MainWindow", "Firmware version"))
        self.keyscan_label.setText(_translate("MainWindow", "TextLabel"))
        self.layout_label.setText(_translate("MainWindow", "TextLabel"))
        self.version_label.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.info_tab), _translate("MainWindow", "Info"))
        self.menuDygma_Raise_Assembly_Tests.setTitle(_translate("MainWindow", "Logs"))
        self.actionCopy_log.setText(_translate("MainWindow", "Copy log"))
        self.actionClear_log.setText(_translate("MainWindow", "Clear log"))


import image_rc
