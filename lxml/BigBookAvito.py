# Парсинг раздела "Грузовые автомобили и техника"
# рубрика, название компании, сайт, адрес, О компании, телефон 1, телефон 2, телефон 3
# — xlrd – дает возможность читать файлы Excel
# — xlwt – создание и заполнение файлов Excel
# lxml библиотека для парсинга
import os
import xlwt
import xlrd
import requests
import lxml.html
from lxml import etree
from datetime import datetime
from xlutils.copy import copy


class Company():
    def __init__(self, link):
        html = lxml.html.document_fromstring(requests.get(link).text).xpath("//*[@id='company_info']")[0]
        print(link)
        self.nameCompany = Company.initNameCompany(self, html)
        self.heading = Company.initHeading(self, html)
        self.telephones = Company.initTelephones(self, html)
        self.address = Company.initAddress(self, html)
        self.aboutCompany = Company.initDescriptionCompany(self, html)
        self.siteLink = Company.initSiteLinks(self, html)
        self.link = link

    
    def initNameCompany(self, html):
        return html.xpath("//*[@class='fn org']")[0].text


    def initHeading(self, html):
        pass


    def initTelephones(self, html):
        return [str(i.text+" ") for i in html.xpath("//*[@class='phone-item animation fly-right']/span")]
    
    
    def initAddress(self, html):
        street = html.xpath("//*[@itemprop='streetAddress']")
        locality = html.xpath("//*[@itemprop='addressLocality']")
        try:
            address = street[0].text + " "
        except IndexError:
            address = ""
        try:
             address += locality[0].text
        except IndexError:
            address += ""
        return address
    

    def initDescriptionCompany(self, html):
        try:
            description = html.xpath("//*[@class='description-content']")[0].getchildren()
            if description == []:
                description = html.xpath("//*[@class='description-content']")[0].text
            else:
                text = ""
                for i in description:
                    text += str(i.text + "\n")
                description = text
        except IndexError:
            description = "No description"
        except:
            description = "Unidentified error"
        return str(description).replace("&nbsp", "\n")
            

    def initSiteLinks(self, html):
        try:
            siteLinks = [siteLink.text for siteLink in html.xpath("//*[@class='urls']/a")]
        except IndexError:
            siteLinks = "No links"
        except:
            siteLinks = "Unidentified error"
        return siteLinks


def main():
    mainLink = "https://moscow.big-book-avto.ru"
    sectionTrucks = "/gruzovye_avtomobili__tehnika/"
    companies = []
    pages = int(lxml.html.document_fromstring(requests.get(mainLink + sectionTrucks).text)
        .xpath("//*[@class='paginator']/a")[-1].text)
    for i in range(1, 2): # TODO 33 -> 1
        print("Page: " + str(i))
        r = requests.get(mainLink + sectionTrucks + "?page=" + str(i)).text
        html_blocks = lxml.html.document_fromstring(r).xpath('//*[@class="catalog-item balloon_info waves-effect waves-ripple animation"]')
        linksCompany = getLinks(html_blocks)
        pageCompany = [Company(mainLink + companyPageHref) for companyPageHref in linksCompany]
        companies.extend(pageCompany)
    writeLog(companies, "log_BigBookAvito")


def getLinks(html):
    """Принимает однотипные блоки и выцепляет ключ 'data-url'"""
    arr = []
    for i in html:
        if str(i.get('data-url')) in 'None':
            continue
        else:
            arr.append(str(i.get('data-url')))
    return arr


def writeLog(companies, logFileName):
    """Запись в документ информации о объекте"""
    num = 1
    while os.path.isfile(logFileName + ".xls"):
        rb = xlrd.open_workbook(logFileName + ".xls")
        wb = copy(rb)
        logFileName = logFileName[:16] + "_" + str(num)
        num+=1
    else:
        wb = xlwt.Workbook()
    ws = wb.add_sheet(str(datetime.date(datetime.now())))
    # Создание разметки
    ws.write(0, 0, 'Number')
    ws.write(0, 1, 'Name')
    ws.write(0, 2, 'Heading')
    ws.write(0, 3, 'Telephone 1')
    ws.write(0, 4, 'Address')
    ws.write(0, 5, 'About')
    ws.write(0, 6, 'Site Link')
    ws.write(0, 7, 'Link')
    # Запись данных об объекте
    for y in range(1, len(companies)):
        print("Start\t", companies[y-1].link)
        ws.write(y, 0, y)
        ws.write(y, 1, companies[y-1].nameCompany)
        ws.write(y, 2, companies[y-1].heading)
        # for j in range(len(companies[y-1].telephones)):
            # ws.write(y, j+3, companies[y-1].telephones[j])
        ws.write(y, 3, companies[y-1].telephones)
        ws.write(y, 4, companies[y-1].address)
        ws.write(y, 5, companies[y-1].aboutCompany)
        ws.write(y, 6, companies[y-1].siteLink)
        ws.write(y, 7, companies[y-1].link)
        print("Done!\t", companies[y-1].link)
    # Сохранение
    wb.save(logFileName + ".xls")


if __name__ == "__main__":
    main()
