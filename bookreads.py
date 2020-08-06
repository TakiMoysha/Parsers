import requests
from bs4 import BeautifulSoup as BS


def writeInfo(file, name, author, pages, imageUrl, description):
    f.write(
        'name = ' + '\"' + name + '\"' + '\n' +
        'author = ' + '\"' + author + '\"' + '\n' +
        'pages = ' + '\"' + pages[0:pages.find(' ')] + '\"' + '\n' +
        'imageUrl = ' + '\"' + imageUrl + '\"' + '\n' +
        'description = ' + '\"' + description + '\"' + '\n\n'
    )
    print("Done")


def pageProcessing():
    r = requests.get("https://www.goodreads.com/choiceawards/best-fantasy-books-2019")
    html = BS(r.content, 'html.parser')
    arr = []
    for el in html.select('.pollAnswer__bookLink'):
        arr.append('https://www.goodreads.com' + el.get('href'))
    return(arr)


def getInfo(link):
    page = requests.get(link)
    html = BS(page.content, 'html.parser')
    
    name = str(html.find('h1', id='bookTitle').next.strip())
    author = str(html.find('span', itemprop='name').next.strip())
    pages = str(html.find('span', itemprop='numberOfPages').next.strip())
    imageUrl = str(html.find('img', id='coverImage')['src'])
    try:
        description = str(html.find('div', id='description').next.next.next.strip())
    except TypeError:
        description = "TypeError"
    return name, author, pages, imageUrl, description
    # print(name, author, pages, imageUrl)
    # print(type(name), type(author), type(pages), type(imageUrl))


f = open('info.txt', 'w', encoding='utf8')
linksBook = pageProcessing()
for link in linksBook:
    print(link)
    writeInfo(f, *getInfo(link))


f.close()
