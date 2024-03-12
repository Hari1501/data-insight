import requests
from bs4 import BeautifulSoup
import pandas as pd

# Globals
url = 'http://items.toscrape.com'
url_list = [url,]
pages = []
soup_list = []
not_last_page = True

#1: Pull the requests
def pullUrl(func):
    def inner(*args, **kwargs):
        page = requests.get(url_list[-1])
        if page.status_code == 200:
            pages.append(page)
            func(*args, **kwargs)
        else:
            print(f'The url {url} returned a status of {page.status_code}')
    return inner
    
#2: Make some soup
def makeSoup(func):
    def inner(*args, **kwargs):
        soup = BeautifulSoup(pages[-1].content, 'html.parser')
        soup_list.append(soup)
        func(*args, **kwargs)
    return inner
    
#3: Parse the URLs
@pullUrl
@makeSoup
def getURLs():
    global not_last_page
    try:
        next_page = url+soup_list[-1].find('li', {'class': 'next'}).find('a')['href']
        print(next_page)
        url_list.append(next_page)
    except:
        not_last_page = False

## Syntax and example output for page 1:
# next_page = url+soup.find('li', {'class': 'next'}).find('a')['href']
# print(next_page)

while not_last_page:
    getURLs()

# Start with an empty Data Frame:
items_df = pd.DataFrame(columns=['Item', 'Summary'])
#

# Add in the items dictionary:
items_dict = {}

try:
    for i in range(len(soup_list)):
        items = soup_list[i].find_all('div', {'class': 'quote'})
        for j in range(len(items)):
            v = items[j].find('small', {'class': 'item'}).text
            k = items[j].find('span', {'class': 'text'}).text
            items_dict[k] = v
except: print('issue with', {i, j})

items_df = pd.DataFrame(list(items_dict.items()), columns=['Summary', 'Item'])[['Item', 'Summary']].sort_values('Item')

print(items_df)