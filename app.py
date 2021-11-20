import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import xlsxwriter


mainDir = os.getcwd()

now = datetime.now()
dt_string = now.strftime("%d.%m.%Y %H-%M-%S")
dirName = dt_string

islemBaslangic = datetime.now().strftime("%d.%m.%Y %H-%M-%S")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
loginData = {
    "kullaniciAdi": "R050",
    "sifre": "105222"
}


def kacSayfa():
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
    return sayfaSayisi


def imgDowload(resimAdi, uzanti, img_data):
    with open(mainDir + "/" + dirName + "/" + resimAdi + "." + uzanti, "wb") as handler:
        handler.write(img_data)


def firstList(imgDow=True, excelExport=True, excelName=""):
    if imgDow == True:
        os.mkdir(str(dirName))

    with requests.Session() as s:
        s.headers.update(headers)
        url = "https://ozerdemmotosiklet.com/Site/Giris"
        # r = s.get(url, headers=headers)
        s.post(url, data=loginData)

        sayfaSayisi = kacSayfa()
        row = 1

        if excelName == "":
            excelName = dt_string

        workbook = xlsxwriter.Workbook(excelName + '.xlsx')
        worksheet = workbook.add_worksheet()
        for x in range(int(sayfaSayisi)):
            sayfa = x + 1
            print("Sayfa " + str(sayfa) + " baslangıç:" + str(datetime.now().strftime("%d.%m.%Y %H-%M-%S")))

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
                    imgDowload(resimAdi, uzanti, img_data)

            print("Sayfa " + str(sayfa) + " bitis:" + str(datetime.now().strftime("%d.%m.%Y %H-%M-%S")))
            print("======================================")

            # print("kod: " + urunKodu + " Adı: " + urunAdi + " Fiyat: " + urunFiyati + " satir no : " + str(row))

        workbook.close()
        islemBitis = datetime.now().strftime("%d.%m.%Y %H-%M-%S")
        print("İşlem Başlangıcı:" + str(islemBaslangic) + " | İşlem Bitişi " + str(islemBitis))



