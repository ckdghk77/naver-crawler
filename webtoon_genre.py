'''
Created on Aug 1, 2016

@author: TYchoi
'''

from selenium import webdriver
from bs4 import BeautifulSoup
import pprint

driver = webdriver.Chrome()
url= 'http://comic.naver.com/webtoon/genre.nhn?genre=episode'
driver.get(url)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')
genre_dict = {}
genre_list = []
href_list = []
for genre in soup.find('ul',{'class':'category_tab category_tab2'}).find_all('a'):
    genre_list.append(genre['href'][genre['href'].find('=')+1:])
    href_list.append('http://comic.naver.com'+genre['href'])
driver.close()
for i in range(len(genre_list)):
    genre_dict[href_list[i]] = genre_list[i]
driver = webdriver.Chrome()
for url in sorted(genre_dict.keys()):
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    for webtoon in soup.find('ul',{'class':'img_list'}).find_all('li'):
        title = webtoon.find('dl').find('dt').find('a')['title']
        author = webtoon.find('dl').find('dd',{'class':'desc'}).find('a').text
        print(genre_dict[url])
        print(title)
        print(author)
        subimages = webtoon.find('div',{'class':'thumb'}).find('a').find_all('img')
        if len(subimages) == 1:
            print(subimages[0]['src'])
            print('미완결')
        else :
            for subimage in subimages:
                if 'thumb' in subimage['src']:
                    subimage['src']
                else:
                    print(subimage['alt'])
        for span in webtoon.find('a').find_all('span'):
            if span['class'] != ['mask'] and span.text != 'NEW':
                print(span.text)
        print('--------')
    print(url)
    break

driver.close()