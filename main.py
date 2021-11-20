from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import xlsxwriter
import asyncio
import sys

mainDir = os.getcwd()

now = datetime.now()
dt_string = now.strftime("%d.%m.%Y %H-%M-%S")
dirName = dt_string

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
loginData = {
    "kullaniciAdi": "R050",
    "sifre": "105222"
}


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('home.ui', self)

        self.chkImage = self.findChild(QtWidgets.QCheckBox, "chkImageDownload")
        self.userNameInput = self.findChild(QtWidgets.QTextEdit, 'textUsername').setText("Kullanıcı Adı Burada")
        self.passwordInput = self.findChild(QtWidgets.QTextEdit, 'txtPassword').setText("Şifre Burada")
        self.passwordInput = self.findChild(QtWidgets.QTextEdit, 'txtPassword')
        self.userNameInput = self.findChild(QtWidgets.QTextEdit, 'textUsername')
        self.tableType = self.findChild(QtWidgets.QComboBox, 'cmbTableType')
        self.lblItemLen = self.findChild(QtWidgets.QLabel, 'lblItemLen')
        self.lblPageLen = self.findChild(QtWidgets.QLabel, 'lblPageLen')
        self.lblProgressInfo = self.findChild(QtWidgets.QLabel, 'lblProgressInfo')

        self.table = self.findChild(QtWidgets.QTableWidget, "tableWidget")

        self.rows = [
            ["A1", "B1", "C1", "D1", "E1", "F1"],
            ["A2", "B2", "C2", "D2", "E2", "F2"],
            ["A3", "B3", "C3", "D3", "E3", "F3"],
            ["A4", "B4", "C4", "D4", "E4", "F4"],
            ["A5", "B5", "C5", "D5", "E5", "F5"],
            ["A6", "B6", "C6", "D6", "E6", "F6"],
            ["A7", "B7", "C7", "D7", "E7", "F7"],
            ["A8", "B8", "C8", "D8", "E8", "F8"],
            ["A9", "B9", "C9", "D9", "E9", "F9"],
            ["A10", "B10", "C10", "D10", "E10", "F10"],
            ["A11", "B11", "C11", "D11", "E11", "F11"],
            ["A12", "B12", "C12", "D12", "E12", "F12"],
            ["A13", "B13", "C13", "D13", "E13", "F13"],
            ["A14", "B14", "C14", "D14", "E14", "F14"],
            ["A15", "B15", "C15", "D15", "E15", "F15"],
            ["A16", "B16", "C16", "D16", "E16", "F16"],
            ["A17", "B17", "C17", "D17", "E17", "F17"],
            ["A18", "B18", "C18", "D18", "E18", "F18"],
            ["A19", "B19", "C19", "D19", "E19", "F19"],
            ["A20", "B20", "C20", "D20", "E20", "F20"],
            ["A21", "B21", "C21", "D21", "E21", "F21"],
            ["A22", "B22", "C22", "D22", "E22", "F22"],
        ]

        self.startButton = self.findChild(QtWidgets.QPushButton, 'btnStart')
        self.startButton.clicked.connect(self.printButtonPressed)

        self.show()

    def kacSayfa(self):
        sayfaSayisi = ""
        with requests.Session() as s:
            url = "https://ozerdemmotosiklet.com/Site/Giris"
            # r = s.get(url, headers=headers)
            r = s.post(url, data=loginData, headers=headers)

            sayfaInfo = s.get("https://ozerdemmotosiklet.com/Siparis/StokAra?Kategori=Tumu&sayfa=1&listeGorunumu=liste",
                              headers=headers)
            sayfaContent = BeautifulSoup(sayfaInfo.content, 'html.parser')
            sayfaSayisiText = sayfaContent.find("div", {"class": "mt20 text-center"})
            sayfaSayisi = sayfaSayisiText.span.text.split(": ")[1]
        return   sayfaSayisi

    def imgDowload(self, resimAdi, uzanti, img_data):
        with open(mainDir + "/" + dirName + "/" + resimAdi + "." + uzanti, "wb") as handler:
            handler.write(img_data)

    def firstList(self, imgDow=True, excelExport=True, excelName="", username="", password=""):
        islemBaslangic = datetime.now().strftime("%d.%m.%Y %H-%M-%S")
        if imgDow == True:
            os.mkdir(str(dirName))

        with requests.Session() as s:
            s.headers.update(headers)
            url = "https://ozerdemmotosiklet.com/Site/Giris"
            s.post(url, data=loginData)

            sayfaSayisi =  self.kacSayfa()

            row = 1

            if excelName == "":
                excelName = dt_string

            workbook = xlsxwriter.Workbook(excelName + '.xlsx')
            worksheet = workbook.add_worksheet()
            for x in range(int(sayfaSayisi)):
                sayfa = x + 1
                self.lblProgressInfo.setText("Sayfa " + str(sayfa) + " baslangıç:" + str(
                    datetime.now().strftime("%d.%m.%Y %H-%M-%S")) + " | Toplam " + str(row) + " ürün bulundu")
                print("Sayfa: " + str(sayfa))

                r2 = s.get(
                    "https://ozerdemmotosiklet.com/Siparis/StokAra?Kategori=Tumu&sayfa=" + str(
                        sayfa) + "&listeGorunumu=liste")
                soup = BeautifulSoup(r2.content, 'html.parser')

                table = soup.find("tbody", {"id": "Liste"})

                for tr in table.find_all("tr"):
                    datas = tr.find_all("td")
                    urunKodu = datas[1].text
                    urunAdi = datas[2].text
                    urunFiyati = datas[6].text[:-1]
                    resim = datas[0].img

                    if excelExport == True:
                        worksheet.write('A' + str(row), urunKodu)
                        worksheet.write('B' + str(row), urunAdi)
                        money_format = workbook.add_format({'num_format': '[$R]#,##0.00'})
                        worksheet.write('C' + str(row), urunFiyati, money_format)
                        worksheet.write('D' + str(row), "https://ozerdemmotosiklet.com/" + resim['src'])
                        row += 1

                    if imgDow == True and resim['src'].find("ResimYok") == -1:
                        img_data = requests.get("https://ozerdemmotosiklet.com/" + resim['src']).content
                        resimAdi = urunKodu.replace('/', "-")
                        uzanti = resim['src'].split(".")[-1]
                        self.imgDowload(resimAdi, uzanti, img_data)

                self.lblProgressInfo.setText("Sayfa " + str(sayfa) + " bitti:" + str(
                    datetime.now().strftime("%d.%m.%Y %H-%M-%S")) + " | Toplam " + str(row) + " ürün bulundu")

            print("kod: " + urunKodu + " Adı: " + urunAdi + " Fiyat: " + urunFiyati + " satir no : " + str(row))

            workbook.close()
            islemBitis = datetime.now().strftime("%d.%m.%Y %H-%M-%S")
            print("İşlem Başlangıcı:" + str(islemBaslangic) + " | İşlem Bitişi " + str(islemBitis))
            return  True

    def printButtonPressed(self):
        self.startButton.setText("Lütfen Bekleyin")
        self.startButton.setEnabled(False)
        sayfaSayisiLbl =  int(self.kacSayfa())
        itemLen = sayfaSayisiLbl * 100
        self.lblItemLen.setText("Hedef Sayfa Sayısı: " + str(sayfaSayisiLbl))
        self.lblPageLen.setText("Tahmini Hedef Ürün: " + str(itemLen))
        self.callTable()

    def callTable(self):
        imageDownload = self.chkImage.isChecked()
        userName = self.userNameInput.toPlainText()
        password = self.passwordInput.toPlainText()
        tableType = self.tableType.currentText()
        if tableType == "Gelişmiş Tablo":
            return  self.firstList(imageDownload, True, "", userName, password)

    def setCompareTable(self):
        self.table.setRowCount(len(self.rows))
        for row in enumerate(self.rows):
            for col in enumerate(row[1]):
                item = QtWidgets.QTableWidgetItem()
                item.setText(col[1])
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                if col[1] == "E5" or col[1] == "E22":
                    item.setBackground(QtGui.QColor(39, 174, 96))
                    item.setForeground(QtGui.QColor(255, 255, 255))
                if col[1] == "E12" or col[1] == "E8":
                    item.setBackground(QtGui.QColor(231, 76, 60))
                    item.setForeground(QtGui.QColor(255, 255, 255))

                self.table.setItem(row[0], col[0], item)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
