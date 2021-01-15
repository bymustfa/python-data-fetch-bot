import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import xlsxwriter
import urllib.request

mainDir = os.getcwd()

now = datetime.now()
dt_string = now.strftime("%d.%m.%Y %H-%M-%S")
dirName = dt_string
os.mkdir(str(dirName))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}


def firstList():
    loginData = {
        "kullaniciAdi": "R050",
        "sifre": "105222"
    }

    with requests.Session() as s:
        url = "https://ozerdemmotosiklet.com/Site/Giris"
        # r = s.get(url, headers=headers)
        r = s.post(url, data=loginData, headers=headers)

        sayfaInfo = s.get("https://ozerdemmotosiklet.com/Siparis/StokAra?Kategori=Tumu&sayfa=1&listeGorunumu=liste",
                          headers=headers)
        sayfaContent = BeautifulSoup(sayfaInfo.content, 'html.parser')
        sayfaSayisiText = sayfaContent.find("div", {"class": "mt20 text-center"})
        sayfaSayisi = sayfaSayisiText.span.text.split(": ")[1]
        row = 1
        for x in range(int(sayfaSayisi)):
            sayfa = x + 1

            r2 = s.get(
                "https://ozerdemmotosiklet.com/Siparis/StokAra?Kategori=Tumu&sayfa=" + str(
                    sayfa) + "&listeGorunumu=liste",
                headers=headers)
            soup = BeautifulSoup(r2.content, 'html.parser')

            table = soup.find("tbody", {"id": "Liste"})
            number = 1;
            for tr in table.find_all("tr"):
                datas = tr.find_all("td")
                urunKodu = datas[1].text
                urunAdi = datas[2].text
                urunFiyati = datas[6].text[:-1]
                resim = datas[0].img
                img_data = requests.get("https://ozerdemmotosiklet.com/" + resim['src']).content

                resimAdi = urunKodu.replace('/', "-")

                if resim['src'].find("ResimYok") == -1:
                    print(resimAdi, " https://ozerdemmotosiklet.com/" + resim['src'])
                    with open(mainDir + "/" + dirName + "/" + resimAdi + ".jpg", "wb") as handler:
                        handler.write(img_data)

                number = number + 1

                # print("kod: " + urunKodu + " Adı: " + urunAdi + " Fiyat: " + urunFiyati + " satir no : " + str(row))
                print("==============================================")


firstList()


def tekSayfa():
    loginData = {
        "kullaniciAdi": "R050",
        "sifre": "105222"
    }
    with requests.Session() as s:
        url = "https://ozerdemmotosiklet.com/Site/Giris"
        # r = s.get(url, headers=headers)
        r = s.post(url, data=loginData, headers=headers)

        sayfaInfo = s.get("https://ozerdemmotosiklet.com/Siparis/StokAra?Kategori=Tumu&sayfa=1&listeGorunumu=liste",
                          headers=headers)
        soup = BeautifulSoup(sayfaInfo.content, 'html.parser')

        table = soup.find("tbody", {"id": "Liste"})
        number = 1;
        for tr in table.find_all("tr"):
            datas = tr.find_all("td")
            urunKodu = datas[1].text
            urunAdi = datas[2].text
            urunFiyati = datas[6].text[:-1]
            resim = datas[0].img
            img_data = requests.get("https://ozerdemmotosiklet.com/" + resim['src']).content
            with open(dirName + "/" + urunKodu + ".jpg", "wb") as handler:
                handler.write(img_data)

            number = number + 1
            # print("kod: " + urunKodu + " Adı: " + urunAdi + " Fiyat: " + urunFiyati + " satir no : " + str(row))

# tekSayfa()
