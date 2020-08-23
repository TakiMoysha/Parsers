import re
import csv
import requests
from bs4 import BeautifulSoup as BS


class GoogleApp():
    def getNameApp(self, BSClassPageApp):
        name = BSClassPageApp.select('h1 > span')[0].next
        return name


    def getCategoryApp(self, BSClassPageApp):
        category = [i.next for i in (BSClassPageApp.findAll('a', {'class': 'hrTbp R8zArc'}))]
        return category


    def getInstalls(self, BSClassPageApp):
        installs = BSClassPageApp.find_all('div', {'class' : 'BgcNfc'})[2].next.findNext('span', {'class':'htlgb'}).findNext('span', {'class':'htlgb'}).next
        return installs


    def getNumberOfReviews(self, BSClassPageApp):
        numberOfReviews = str(BSClassPageApp.find('span', {"class":"AYi5wd TBRnV"}).next.next)
        return numberOfReviews


    def getRating(self, BSClassPageApp):
        rating = str(BSClassPageApp.find('div', {"class":"BHMmbe"})['aria-label'])
        return rating


    def getContentRating(self, BSClassPageApp):
        age = BSClassPageApp.find_all('div', {'class':'hAyfc'})[5].find('span', {'class':'htlgb'}).find('span', {'class':'htlgb'}).next.next
        return age

    def writeLog(self, filename):
        try:
            with open(filename, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerows([
                    [self.nameApp],
                    [i for i in self.categorysApp],
                    [self.installs],
                    [self.numberOfReviews],
                    [self.rating],
                    [self.getContentRating],
                    [self.link]
                ])
            print("Done")
        except:
            print("Error")


    def __init__(self, appLink, filename):
        self.link = "https://play.google.com" + appLink
        BSClassPageApp = BS(requests.get(self.link).content, 'html.parser')
        self.nameApp = GoogleApp.getNameApp(self, BSClassPageApp)
        self.categorysApp = GoogleApp.getCategoryApp(self, BSClassPageApp)
        self.installs = GoogleApp.getInstalls(self, BSClassPageApp)
        self.numberOfReviews = GoogleApp.getNumberOfReviews(self, BSClassPageApp)
        self.rating = GoogleApp.getRating(self, BSClassPageApp)
        self.getContentRating = GoogleApp.getContentRating(self, BSClassPageApp)
        GoogleApp.writeLog(self, filename)


# --------------------------------------------------------
limit = 10
languages = {"ru":"&hl=ru", "en":"&hl=ru"}
filename = 'log_GoogleApp.cvs'
# --------------------------------------------------------
apps = []

mainLink = "https://play.google.com"
r = requests.get(mainLink + "/store/apps")
html = BS(r.content, 'html.parser')
r = requests.get(mainLink + html.select('.LkLjZd')[2].attrs['href'])
html = BS(r.content, 'html.parser')
htmlBlockApps = html.find_all("div", {"class": "wXUyZd"}, limit=limit)
apps = [GoogleApp(i.next['href'], filename) for i in htmlBlockApps]
