import re
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
        installs = BSClassPageApp.find(string=re.compile('Installs')).next.findNext('span', {'class':'htlgb'}).next
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

    def writeLog(self):
        try:
            f = open('log_GoogleApp.txt', 'a', encoding='1252')
            f.write(self.nameApp + "\n")
            for i in self.categorysApp:
                f.write(str(i) + "; ")
            f.write("\n")
            f.write(str(self.installs) + "\n"
                + str(self.numberOfReviews) + "\n"
                + str(self.rating) + "\n"
                + str(self.getContentRating) + "\n"
                + str(self.link) + "\n\n")
            f.close
            print("Done")
        except:
            f.close
            print("Error")


    def __init__(self, appLink):
        self.link = "https://play.google.com" + appLink
        BSClassPageApp = BS(requests.get(self.link).content, 'html.parser')
        self.nameApp = GoogleApp.getNameApp(self, BSClassPageApp)
        self.categorysApp = GoogleApp.getCategoryApp(self, BSClassPageApp)
        self.installs = GoogleApp.getInstalls(self, BSClassPageApp)
        self.numberOfReviews = GoogleApp.getNumberOfReviews(self, BSClassPageApp)
        self.rating = GoogleApp.getRating(self, BSClassPageApp)
        self.getContentRating = GoogleApp.getContentRating(self, BSClassPageApp)
        GoogleApp.writeLog(self)


# --------------------------------------------------------
limit = 5
languages = {"ru":"&hl=ru", "en":"&hl=ru"}
# --------------------------------------------------------
apps = []

mainLink = "https://play.google.com"
r = requests.get(mainLink + "/store/apps")
html = BS(r.content, 'html.parser')
r = requests.get(mainLink + html.select('.LkLjZd')[2].attrs['href'])
html = BS(r.content, 'html.parser')
htmlBlockApps = html.find_all("div", {"class": "wXUyZd"}, limit=limit)
apps = [GoogleApp(i.next['href']) for i in htmlBlockApps]
