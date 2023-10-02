import datetime
import sys

from PyQt5.QtCore import QTimer, QDate
from PyQt5.QtGui import QPixmap
from requests import post
from PyQt5 import uic

from API.db.connect import Staff, Clients, Services, OrdersServices
from captcha import main_capt
from json import loads, dumps
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from db.connect import connect, init_data, Orders

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QMessageBox, QTableWidget, \
    QCompleter, QFileDialog, QCheckBox, QComboBox, QListWidget, QListWidgetItem, QDateEdit

login = None
data = None
role = {
    1: 'Лаборант',
    2: 'Бухгалтер',
    3: 'Администратор'
}
photo = {
    1: 'laborant_2.png',
    2: 'Администратор.png',
    3: 'Бухгалтер.jpeg'
}


class LoginWin(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('win/LoginWin.ui', self)
        self.label_3.setVisible(False)
        self.pushButton_2.setVisible(False)
        self.lineEdit_3.setVisible(False)
        self.pushButton_3.clicked.connect(self.vis)
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.pushButton.clicked.connect(self.check)
        self.pushButton_2.clicked.connect(self.reca)
        self.lineEdit_3.textChanged.connect(self.check_cap)
        self.word = ''
        self.cap_mode = False

    def check_cap(self):
        if len(self.lineEdit_3.text()) == 4:
            if self.lineEdit_3.text().lower() == self.word.lower():
                self.pushButton.setEnabled(True)
                self.label_3.setVisible(False)
                self.pushButton_2.setVisible(False)
                self.lineEdit_3.setVisible(False)
                self.cap_mode = False
                self.lineEdit_3.clear()
            else:
                self.ms = QMessageBox()
                self.ms.setWindowTitle('Ошбика ввода Captcha')
                self.ms.setText('Окно заблокировано на 10 секунд')
                self.ms.show()
                self.lineEdit_3.clear()
                self.block()

    def block(self):
        self.reca()
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.pushButton.setEnabled(False)
        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.lineEdit_3.setEnabled(False)
        QTimer.singleShot(10000, self.unblock)

    def unblock(self):
        self.lineEdit.setEnabled(True)
        self.lineEdit_2.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.lineEdit_3.setEnabled(True)

    def reca(self):
        self.word = main_capt()
        self.lineEdit_3.clear()
        self.label_3.setPixmap(QPixmap('code.jpg'))

    def log_block(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.pushButton.setEnabled(False)
        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.lineEdit_3.setEnabled(False)
        self.label_3.setVisible(False)
        self.pushButton_2.setVisible(False)
        self.lineEdit_3.setVisible(False)
        QTimer.singleShot(10000, self.unblock_log)

    def unblock_log(self):
        self.pushButton.setEnabled(True)
        self.lineEdit.setEnabled(True)
        self.lineEdit_2.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.lineEdit_3.setEnabled(True)

    def check(self):
        global data
        global login
        resp = post('http://localhost:5000/login',
                    data={'login': self.lineEdit.text(), 'password': self.lineEdit_2.text()})
        if resp.status_code == 200:
            login = [self.lineEdit.text(), self.lineEdit_2.text()]
            data = resp.json()[:]
            logs = loads(open('logs.json', 'r', encoding='utf-8').read())
            logs.append(
                [data[1], datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%Y %H:%M'), self.lineEdit.text(),
                 200])
            open('logs.json', 'w', encoding='utf-8').write(dumps(logs))
            self.main = MainWin(self)
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.main.show()
            self.close()
        else:
            logs = loads(open('logs.json', 'r', encoding='utf-8').read())
            logs.append(
                ['Неизвестно', datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%Y %H:%M'),
                 self.lineEdit.text(),
                 403])
            open('logs.json', 'w', encoding='utf-8').write(dumps(logs))
            self.word = main_capt()
            self.ms = QMessageBox()
            self.ms.setWindowTitle('Ошбика входа')
            self.ms.setText('Данные введены неправильно')
            self.ms.show()
            self.pushButton.setEnabled(False)
            self.label_3.setVisible(True)
            self.pushButton_2.setVisible(True)
            self.lineEdit_3.setVisible(True)
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.cap_mode = True
            self.label_3.setPixmap(QPixmap('code.jpg'))

    def vis(self):
        self.lineEdit_2.setEchoMode(
            QLineEdit.Password if self.lineEdit_2.echoMode() != QLineEdit.Password else QLineEdit.Normal)


class MainWin(QMainWindow):
    def __init__(self, log_win):
        super().__init__()
        global role
        global data
        global photo
        uic.loadUi('win/MainWin.ui', self)
        self.log_win = log_win
        self.label.setPixmap(QPixmap(f'img/{photo[data[4]]}'))
        self.label_2.setText(data[2])
        self.label_3.setText(data[3])
        self.label_5.setText(role[data[4]])
        self.setWindowTitle(f'ПСОО "Не навреди" - {role[data[4]]}')
        self.time = 120
        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.showTime)
        self.pushButton_5.clicked.connect(self.back)
        if data[4] == 1:
            self.pushButton.setText('Прием отходов')
            self.pushButton.clicked.connect(self.order)
            self.pushButton_2.setText("Формирование отчета")
            self.pushButton_3.setText("Работа с утилизатором")
            self.pushButton_4.setVisible(False)
        elif data[4] == 2:
            self.pushButton.setText("Просмотр отчетов")
            self.pushButton_2.setText("Формирование счета")
            self.pushButton_2.clicked.connect(self.pay)
            self.pushButton_3.setVisible(False)
            self.pushButton_4.setVisible(False)
        elif data[4] == 3:
            self.pushButton.setText("Контроль пользователей")
            self.pushButton_2.setText("Формирование отчета")
            self.pushButton_3.setText("Данные о расходных материалах")
            self.pushButton_4.setText("История входа")
            self.pushButton_4.clicked.connect(self.loggs_win)

    def pay(self):
        self.py = PayRec()
        self.py.show()

    def order(self):
        self.ord = OrderWin()
        self.ord.show()

    def back(self):
        self.log_win.show()
        self.destroy()

    def loggs_win(self):
        self.loggs = LogsWin()
        self.loggs.show()

    def showTime(self):
        self.time -= 1
        if self.time == 60:
            self.ms = QMessageBox()
            self.ms.setWindowTitle('Внимание')
            self.ms.setText('Время сеанса скоро закончится')
            self.ms.show()
        elif self.time == 0:
            self.ms = QMessageBox()
            self.ms.setWindowTitle('Время сеанса закончилось')
            self.ms.setText('Вход заблокирован на время кварцевания (1мин)')
            self.ms.show()
            self.log_win.show()
            self.log_win.log_block()
            self.destroy()
        self.label_6.setText(
            f'{str(self.time // 60)}:{"" if len(str(self.time % 60)) == 2 else "0"}{str(self.time % 60)}')


class PayRec(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('win/InvoWin.ui', self)
        self.pushButton.clicked.connect(self.make_org)
        self.pushButton_2.clicked.connect(self.make_poup)

    def make_org(self):
        pass

    def make_org(self):
        pass


class LogsWin(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('win/LoggsWin.ui', self)
        self.logs = loads(open('logs.json', 'r', encoding='utf-8').read())
        self.tableWidget.setRowCount(len(self.logs))
        self.pushButton_3.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.time_str)
        self.pushButton.clicked.connect(self.login_str)
        self.tableWidget.setHorizontalHeaderLabels(['IP адрес', 'Время входа', 'Логин', 'Авторизация'])
        for i in range(len(self.logs)):
            lbl = QLabel()
            lbl.setText(self.logs[i][0])
            self.tableWidget.setCellWidget(i, 0, lbl)
            lbl = QLabel()
            lbl.setText(self.logs[i][1])
            self.tableWidget.setCellWidget(i, 1, lbl)
            lbl = QLabel()
            lbl.setText(self.logs[i][2])
            self.tableWidget.setCellWidget(i, 2, lbl)
            lbl = QLabel()
            lbl.setText("Успешная" if self.logs[i][3] == 200 else "Ошибочная")
            self.tableWidget.setCellWidget(i, 3, lbl)

    def time_str(self):
        self.logs.sort(key=lambda x: datetime.datetime.strptime(x[1], '%d.%m.%Y %H:%M'))
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(['IP адрес', 'Время входа', 'Логин', 'Авторизация'])
        for i in range(len(self.logs)):
            lbl = QLabel()
            lbl.setText(self.logs[i][0])
            self.tableWidget.setCellWidget(i, 0, lbl)
            lbl = QLabel()
            lbl.setText(self.logs[i][1])
            self.tableWidget.setCellWidget(i, 1, lbl)
            lbl = QLabel()
            lbl.setText(self.logs[i][2])
            self.tableWidget.setCellWidget(i, 2, lbl)
            lbl = QLabel()
            lbl.setText("Успешная" if self.logs[i][3] == 200 else "Ошибочная")
            self.tableWidget.setCellWidget(i, 3, lbl)

    def login_str(self):
        self.logs.sort(key=lambda x: x[2])
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(['IP адрес', 'Время входа', 'Логин', 'Авторизация'])
        for i in range(len(self.logs)):
            lbl = QLabel()
            lbl.setText(self.logs[i][0])
            self.tableWidget.setCellWidget(i, 0, lbl)
            lbl = QLabel()
            lbl.setText(self.logs[i][1])
            self.tableWidget.setCellWidget(i, 1, lbl)
            lbl = QLabel()
            lbl.setText(self.logs[i][2])
            self.tableWidget.setCellWidget(i, 2, lbl)
            lbl = QLabel()
            lbl.setText("Успешная" if self.logs[i][3] == 200 else "Ошибочная")
            self.tableWidget.setCellWidget(i, 3, lbl)


class OrderWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ms = None
        uic.loadUi('win/OrdersWin.ui', self)
        self.pushButton_5.clicked.connect(self.close)
        con = connect()
        self.last_order = max(con.query(Orders.id).all())[0]
        self.lineEdit.setPlaceholderText(str(self.last_order + 1))
        self.clients = con.query(Clients).all()
        self.comboBox.addItems([f"{i.surname} {i.name}" for i in self.clients])
        self.services = con.query(Services).all()
        services = []
        self.serv_dict = {}
        for i in services:
            check = QCheckBox()
            check.stateChanged.connect(self.sums)
            check.setText(i.name)
            item = QListWidgetItem()
            self.serv_dict[check] = i
            self.services.append(check)
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, check)
        con.close()
        self.sum = 0
        self.comboBox.setVisible(False)
        self.checkBox.setVisible(False)
        self.listWidget.setVisible(False)
        self.label_6.setVisible(False)
        self.groupBox.setVisible(False)
        self.pushButton.setVisible(False)
        self.pushButton_2.setVisible(False)
        self.lineEdit_2.setVisible(False)
        self.lineEdit_2.textChanged.connect(self.find)
        self.checkBox.stateChanged.connect(self.client)
        self.lineEdit.returnPressed.connect(self.entr)
        self.pushButton.clicked.connect(self.conf)
        self.pushButton_2.clicked.connect(self.add_user)

    def add_user(self):
        try:
            client = Clients(
                name=self.lineEdit_9.text(),
                surname=self.lineEdit_10.text(),
                login=self.lineEdit_3.text(),
                password=self.lineEdit_4.text(),
                patronymic=self.lineEdit_14.text(),
                birthday=self.dateEdit_2.date().toPyDate(),
                serial=self.lineEdit_15.text(),
                number=self.lineEdit_13.text()
            )
            con = connect()
            con.add(client)
            con.commit()
            con.close()
            self.checkBox.setChecked(False)
            self.clients.append(client)
            self.comboBox.addItem(f'{client.surname} {client.name}')
        except Exception as e:
            print(e)
            self.ms = QMessageBox()
            self.ms.setWindowTitle('Ошибка заполнения формы')
            self.ms.setText('Данные пользователя заполнены неправильно')
            self.ms.show()

    def conf(self):
        im = Image.new('RGB', (950, 950), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        lst = ['Дата заказа', 'Номер заказа', 'Предприятие', 'ФИО', 'Дата рождения', 'Перечень услуг', 'Стоимость']
        clnt = list(filter(lambda x: f'{x.surname} {x.name}' == self.comboBox.currentText(), self.clients))[0]
        lst2 = [str(datetime.date.today()), self.lineEdit.text(), '-',
                f'{clnt.surname} {clnt.name} {clnt.patronymic if clnt.patronymic else ""}', str(clnt.birthday), list(
                filter(lambda x: x != False, [self.serv_dict[i] if i.isChecked() else False for i in self.services])),
                str(round(self.sum, 2)) + ' руб.']
        start_x = 10
        start_y = 10
        font = ImageFont.truetype('Ubuntu-Th.ttf', 30)
        for i in range(len(lst)):
            if i != 5:
                draw.text((start_x, start_y), lst[i] + ': ' + lst2[i], font=font, fill='black')
                start_y += 35
            else:
                draw.text((start_x, start_y), 'Услуги:', font=font, fill='black')
                start_y += 35
                for j in lst2[i]:
                    draw.text((start_x + 40, start_y), j.name, font=font, fill='black')
                    start_y += 35

        path = QFileDialog.getExistingDirectory(parent=self, caption='Выберите путь сохранения', directory='~', )
        im.save(path + '/Заказ.pdf')
        with open(path + '/Ссылка.txt', 'w', encoding='utf-8') as file:
            st = '\n'.join([str(lst[i]) + ': ' + str(lst2[i]) if i != 5 else str(lst[i]) + ':\n ' + '\n'.join(
                [j.name for j in lst2[i]]) for i in range(len(lst))])
            file.write(st)
        con = connect()
        order = Orders(
            id=int(self.lineEdit.text()),
            date=datetime.date.today(),
            client_id=list(filter(lambda x:
                                  x.surname == self.comboBox.currentText().split()[0] and x.name ==
                                  self.comboBox.currentText().split()[1], self.clients))[0].id
        )
        con.add(order)
        con.commit()
        services = list(filter(lambda x: x.isChecked(), self.services))
        for i in services:
            or_serv = OrdersServices(
                service_id=self.serv_dict[i].id,
                order_id=int(self.lineEdit.text())
            )
            con.add(or_serv)
        con.commit()
        con.close()
        self.ms = QMessageBox()
        self.ms.setWindowTitle('Заказ создан')
        self.ms.setText('Новый заказ успешно создан')
        self.ms.show()
        self.destroy()

    def find(self):
        self.listWidget.clear()
        con = connect()
        services = con.query(Services).all()
        self.serv_dict = {}
        self.services = []
        for i in services:
            if (self.lineEdit_2.text().lower().strip()
                    in i.name.lower().strip() or i.name.lower().strip() in self.lineEdit_2.text().lower().strip()):
                check = QCheckBox()
                check.stateChanged.connect(self.sums)
                check.setText(i.name)
                item = QListWidgetItem()
                self.services.append(check)
                self.serv_dict[check] = i
                self.listWidget.addItem(item)
                self.listWidget.setItemWidget(item, check)
        con.close()

    def sums(self):
        sender = self.sender()
        if sender.isChecked():
            self.sum += self.serv_dict[sender].price
        else:
            self.sum -= self.serv_dict[sender].price
        self.label_3.setText(str(abs(round(self.sum, 2))) + ', руб.')

    def client(self):
        if self.checkBox.isChecked():
            self.comboBox.setVisible(False)
            self.groupBox.setVisible(True)
            self.pushButton.setVisible(False)
            self.pushButton_2.setVisible(True)
        else:
            self.comboBox.setVisible(True)
            self.groupBox.setVisible(False)
            self.pushButton.setVisible(True)
            self.pushButton_2.setVisible(False)

    def entr(self):
        if self.lineEdit.text():
            self.lets_bar()
        else:
            self.lineEdit.setText(str(self.last_order + 1))

    def lets_bar(self):
        from barcode import generate_code, draw_code
        path = QFileDialog.getExistingDirectory(parent=self, caption='Выбирете путь сохранения', directory='~')
        draw_code(generate_code(), path)
        self.label_2.setPixmap(QPixmap(path + '/barcode.pdf'))
        self.lineEdit.setEnabled(False)
        self.comboBox.setVisible(True)
        self.checkBox.setVisible(True)
        self.listWidget.setVisible(True)
        self.label_6.setVisible(True)
        self.pushButton.setVisible(True)
        self.lineEdit_2.setVisible(True)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    init_data()
    app = QApplication(sys.argv)
    win = LoginWin()
    win.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
