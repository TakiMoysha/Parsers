# Парсинг раздела "Грузовые автомобили и техника"
# рубрика, название компании, сайт, адрес, О компании, телефон 1, телефон 2, телефон 3
# — xlrd – дает возможность читать файлы Excel
# — xlwt – создание и заполнение файлов Excel
# lxml библиотека для парсинга
import requests
import xlwt
import lxml.html
from lxml import etree


class Company():
    def __init__(self, link):
        self.nameCompany = getNameCompany(self)
        self.telephones = getTelephones(self)
        self.address = getAddress(self)
        self.aboutCompany = getAboutCompany(self)
        self.siteLink = getSiteLink(self)
        self.link = link

    
    def getNameCompany(self):
        pass


    def getTelephones(self):
        pass
    
    
    def getAddress(self):
        pass
    
    
    def getAboutCompany(self):
        pass
    

    def getSiteLink(self):
        pass




def main():
    mainLink = "https://moscow.big-book-avto.ru"
    sectionTrucks = "/gruzovye_avtomobili__tehnika/"
    # //*[@id="company_info"]/div[1]/div[1]/h1/span
    r = requests.get(mainLink + sectionTrucks).text
    tree = lxml.html.document_fromstring(r)
    # получить кол-во страниц
    pages = int(tree.xpath("//*[@class='paginator']/a")[-1].text)
    # Выцепление ссылок на компании
    html_blocks = tree.xpath('//*[@class="catalog-item balloon_info waves-effect waves-ripple animation"]')
    # Переход по страницам и записи каждой найденной компании в документ
    for i in range(2, pages+1):
        linksCompany = getLinks(html_blocks)
        companies = [Company(mainLink + i) for i in linksCompany]
        for i in companies:
            writeLog(i)
        r = requests.get(mainLink + sectionTrucks + "?page=" + str(i)).text
        lxml.html.document_fromstring(r).xpath('//*[@class="catalog-item balloon_info waves-effect waves-ripple animation"]')

def getLinks(html):
    arr = []
    for i in html:
        if str(i.get('data-url')) is 'None':
            continue
        else:
            arr.append(str(i.get('data-url')))
    return arr


def writeLog(object):
    pass


if __name__ == "__main__":
    main()
