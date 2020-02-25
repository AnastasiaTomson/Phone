from PyQt5 import QtCore, QtGui, QtWidgets
import re
import sys
import threading
import webbrowser
from PyQt5.QtWidgets import QMainWindow
import mysql.connector
import telnetlib


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(320, 240)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("favicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(0.8)
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
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "АПЕКС"))
        self.label.setText(_translate("MainWindow", "Номер оператора"))
        self.connect.setText(_translate("MainWindow", "Подключиться"))
        self.disconnect.setText(_translate("MainWindow", "Отключиться"))


NEW_LINE = '\r\n'.encode('ascii')
shutdown_flag = threading.Event()
f = open("log.txt", 'w', encoding="utf-8")
file = open("log.txt", 'a', encoding="utf-8")

# Подключение к базе данных
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="username",
    passwd="password",
    database="database"
)
mycursor = mydb.cursor(dictionary=True)

# Подключение и аутертификация на сервере
telnet = telnetlib.Telnet(host='127.0.0.1', port=8000)
telnet.read_until(NEW_LINE)
auth_commands = ('Action: Login\n'.encode('ascii'),
                 'Username: {}\n'.format('username').encode('ascii'),
                 'Secret: {}\n'.format("123456").encode('ascii'),
                 NEW_LINE)
for i in auth_commands:
    telnet.write(i)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.connect.clicked.connect(self.start)
        self.ui.connect.setAutoDefault(True)
        self.ui.numOperate.returnPressed.connect(self.ui.connect.click)
        self.ui.disconnect.clicked.connect(self.stop)

    '''
        После нажатия на кнопку подключить:
        Проверяем заполнено ли поле номер оператора, если да, то:
            Проверяем подключение к серверу функцией telnet_connect, которая возвращает True или False.
            Если подключение успешно, тогда:
                Обращаемся к методу is_connect, который изменит интерфейс.
                Очищаем глобальный флаг shutdown_flag, который отвечает за отключение потока.
                Запускаем поток.
            Иначе:
                Обращаемся к методу is_error, который изменит интерфейс.
        иначе выводим сообщение в radioButton
    '''
    def start(self):
        if self.ui.numOperate.text() != "":
            if telnet_connect():
                self.is_connect()
                shutdown_flag.clear()
                threading.Thread(target=listen_telnet, args=(self.ui.numOperate.text(),)).start()
            else:
                self.is_error()
        else:
            self.ui.radioButton.setText("Введите номер оператора!")
            self.ui.radioButton.setStyleSheet("color: darkblue; font: 14pt \"Ubuntu\";")

    '''
        После нажатия на кнопку отключить:
        Обращаемся к методу is_disconnect, который изменит интерфейс.
        Меняем глобальный флаг shutdown_flag, который инициирует отключение потока
    '''

    def stop(self):
        self.is_disconnect()
        shutdown_flag.set()

    ''' 
        Если подключние прошло успешно:
        Изменяем идентификатор (radioButton) на True и меняем текст на "Подключено".
        Блокируем кнопку "подключить", а кнопку "отключить" делаем активной.
        Блокируем доступ к полю "Номер оператора".
    '''

    def is_connect(self):
        radio = self.ui.radioButton
        radio.setChecked(True)
        radio.setText("Подключено")
        radio.setStyleSheet("color: #23973e; font: 14pt \"Ubuntu\";")
        self.ui.connect.setDisabled(True)
        self.ui.numOperate.setDisabled(True)
        self.ui.disconnect.setDisabled(False)

    '''
        После нажатия на кнопку отключить:
        Изменяем идентификатор (radioButton) на False и меняем текст на "Отключено".
        Блокируем кнопку "отключить", а кнопку "подключить" делаем активной.
        Разрешаем доступ к полю "Номер оператора".        
    '''

    def is_disconnect(self):
        radio = self.ui.radioButton
        radio.setChecked(False)
        radio.setText("Отключено")
        radio.setStyleSheet("color: darkgrey; font: 14pt \"Ubuntu\";")
        self.ui.connect.setDisabled(False)
        self.ui.numOperate.setDisabled(False)
        self.ui.disconnect.setDisabled(True)

    '''
        Если произошла ошибка при соединении с сервером:
        Изменяем идентификатор (radioButton) на False и меняем текст на "Ошибка подключения".
        Блокируем кнопку "отключить", а кнопку "подключить" делаем активной.
        Разрешаем доступ к полю "Номер оператора".     
    '''

    def is_error(self):
        radio = self.ui.radioButton
        radio.setChecked(False)
        radio.setText("Ошибка подключения")
        radio.setStyleSheet("color: #ac1d28; font: 14pt \"Ubuntu\";")
        self.ui.connect.setDisabled(False)
        self.ui.numOperate.setDisabled(False)
        self.ui.disconnect.setDisabled(True)


# Функция проверки подключения к серверу
def telnet_connect():
    out = telnet.read_until(NEW_LINE * 2).decode("utf-8")
    if re.search(r"\bError\b", out):
        file.writelines(out)
        return 0
    else:
        return 1


# Основная функция, которая принимает ответ от сервера
def listen_telnet(OPERATOR_NUM):
    first_phone = ''
    while not shutdown_flag.is_set():
        out = telnet.read_until(NEW_LINE * 2).decode("utf-8")
        print(out)
        file.writelines(out)
        if re.search(r"\bBridge\b", out):
            phone = ''
            operator_num = ''
            for line in out.split('\r\n'):
                if re.search(r'CallerID1:', line):
                    phone = line.split(':')[1].strip().replace("'", '')
                elif re.search(r'Channel2:', line):
                    operator_num = line.split(':')[1].strip().replace("'", '')
            print('Входящий {} - Оператор {}'.format(phone, operator_num))
            if len(phone) > 4 and OPERATOR_NUM in operator_num and first_phone != phone:
                mycursor.execute("SQL request".format(phone))
                search_customers = mycursor.fetchall()
                if len(search_customers) == 0:
                    webbrowser.open('http://test.com/')
                elif len(search_customers) == 1:
                    webbrowser.open('http://test.com/{}'.format(search_customers[0]['login']))
                else:
                    webbrowser.open(
                        'http://test.com/{}'.format(search_customers[0]['phone']))
                first_phone = phone


app = QtWidgets.QApplication([])
application = Window()
application.show()
if not app.exec_():
    application.stop()
    sys.exit(0)
