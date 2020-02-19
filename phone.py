import sys

from main import *
from PyQt5 import QtWidgets
import multiprocessing
from multiprocessing import Process, Manager

import threading
import telnetlib
import webbrowser
from datetime import datetime
import re

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('mysql://phones:tyjvaL8N@192.168.88.48/billing?charset=utf8')
Session = sessionmaker(bind=engine)
session = Session()
NEW_LINE = '\r\n'.encode('ascii')
f = open("log.txt", 'w', encoding="utf-8")
file = open("log.txt", 'a', encoding="utf-8")

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), index=True)
    login = Column(String(64), index=True, unique=True)
    password = Column(String(64), index=True)
    phone = Column(String(64), index=True)


tn = telnetlib.Telnet(host='192.168.88.200', port=5038)
tn.read_until(NEW_LINE)
auth_commands = ('Action: Login\n'.encode('ascii'),
                 'Username: {}\n'.format('admin').encode('ascii'),
                 'Secret: {}\n'.format("123456").encode('ascii'),
                 NEW_LINE)
for i in auth_commands:
    tn.write(i)
radio_text = ''

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.connect.clicked.connect(self.start)
        self.ui.disconnect.clicked.connect(self.stop)
        self.ui.disconnect.setDisabled(True)
        self.timer = QtCore.QTimer(parent=self)
        self.timer.setInterval(1000)
        self.timer.start()

    def start(self):
        if self.ui.numOperate.text() != "":
            self.ui.connect.setDisabled(True)
            self.ui.disconnect.setDisabled(False)
            if connect_telnet():
                self.proc = Process(target=tel, args=(True, self.ui.numOperate.text()))
                self.proc.start()
                self.ui.radioButton.setText("Подключено")
                self.ui.radioButton.setChecked(True)
                color = "color: #28a745; "
            else:
                self.ui.radioButton.setText("Ошибка подключения")
                self.ui.radioButton.setChecked(False)
                color = "color: darkgrey; "
            self.ui.radioButton.setStyleSheet("font: 14pt \"Ubuntu\"; {}".format(color))

    def stop(self):
        if self.ui.numOperate.text() != "":
            self.ui.radioButton.setText("Отключено")
            self.ui.radioButton.setChecked(False)
            self.ui.radioButton.setStyleSheet("font: 14pt \"Ubuntu\"; color: darkgrey; ")
            self.ui.connect.setDisabled(False)
            self.ui.disconnect.setDisabled(True)
            self.proc.terminate()
            print('СТОП')


def connect_telnet():
    out = tn.read_until(NEW_LINE * 2)
    file.writelines(out.decode('utf-8') + '\n')
    if re.search(r"\bError\b", str(out)):
        return 0
    else:
        return 1


def tel(action, OPERATOR_NUM):
    while action:
        out = tn.read_until(NEW_LINE * 2)
        file.writelines(out.decode('utf-8') + '\n')
        print(str(out.decode('utf-8')))
        if 'Bridge' in str(out):
            timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')
            print(timestamp)
            caller_num = ''
            operator_num = ''
            for line in out.split(NEW_LINE):
                print(str(line))
                if re.search(r'CallerID1:', str(line)):
                    print(str(line))
                    caller_num = str(line).split(':')[1].strip().replace("'", '')
                elif re.search(r'Channel2:', str(line)):
                    operator_num = str(line).split(':')[1].strip().replace("'", '')
            print('%s -> %s' % (caller_num, operator_num))
            if len(caller_num) > 4 and OPERATOR_NUM in operator_num:
                phone_filter = Customer.phone.like('%' + caller_num[1:] + '%')
                found_customers = session.query(Customer).filter(phone_filter).all()
                for cu in found_customers:
                    print(NEW_LINE)
                    print('%s\r\n%s' % (cu.login, cu.name))
                if len(found_customers) == 0:
                    webbrowser.open('http://billing.apex-crimea.com/customers')
                elif len(found_customers) == 1:
                    webbrowser.open('http://billing.apex-crimea.com/customers/%s' % found_customers[0].login)
                elif len(found_customers) > 1:
                    webbrowser.open('http://billing.apex-crimea.com/customers/search_phone/%s' % caller_num[1:])


app = QtWidgets.QApplication([])
application = Window()
application.show()
if not app.exec_():
    application.stop()
    sys.exit(0)
