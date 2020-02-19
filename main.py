# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(320, 240)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("favicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(0.7)
        MainWindow.setWindowFlags(
            QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowCloseButtonHint
        )
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        self.label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label.setStyleSheet("font: 14pt \"Ubuntu\";")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.numOperate = QtWidgets.QLineEdit(self.centralwidget)
        self.numOperate.setObjectName("numOperate")
        self.verticalLayout.addWidget(self.numOperate)
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.radioButton.setStyleSheet("font: 14pt \"Ubuntu\";")
        self.radioButton.setCheckable(True)
        self.radioButton.setChecked(False)
        self.radioButton.setDisabled(True)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout.addWidget(self.radioButton)
        self.connect = QtWidgets.QPushButton(self.centralwidget)
        self.connect.setMaximumSize(QtCore.QSize(16777215, 30))
        self.connect.setStyleSheet("QPushButton:hover\n"
            "{\n"
            "   background-color: #23973e;\n"
            "}\n"
            "QPushButton{\n"
            "    background-color: #28a745;\n"
            "    border: 1px solid #28a745; \n"
            "    border-radius: 5px; \n"
            "    color: white;         \n"
            "    font-weight: 700; \n"
            "    font: 14pt \"Ubuntu\";\n"
            "}\n"
            "")
        self.connect.setObjectName("connect")
        self.verticalLayout.addWidget(self.connect)
        self.disconnect = QtWidgets.QPushButton(self.centralwidget)
        self.disconnect.setMaximumSize(QtCore.QSize(16777215, 30))
        self.disconnect.setStyleSheet("QPushButton:hover\n"
            "{\n"
            "   background-color: #ac1d28;\n"
            "}\n"
            "QPushButton{\n"
            "    background-color: #cb2431;\n"
            "    border: 1px solid #cb2431; \n"
            "    border-radius: 5px; \n"
            "    color: white;         \n"
            "    font-weight: 700; \n"
            "    font: 14pt \"Ubuntu\";\n"
            "}")
        self.disconnect.setObjectName("disconnect")
        self.verticalLayout.addWidget(self.disconnect)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "АПЕКС"))
        self.label.setText(_translate("MainWindow", "Номер оператора"))
        self.connect.setText(_translate("MainWindow", "Подключиться"))
        self.disconnect.setText(_translate("MainWindow", "Отключиться"))
