'''
Created on Aug 1, 2016

@author: TYchoi
'''

from selenium import webdriver
from bs4 import BeautifulSoup
import csvHandler as csv
import pprint


def webtoon_day_mapping(driver):
    days_format = 'http://comic.naver.com/webtoon/weekdayList.nhn?week='
    days = ['mon','tue','wed','thu','fri','sat','sun']
    day_list = []
    for day in days:
        url = days_format+day
        driver.get(url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        webtoon_ids = soup.find('ul',{'class':'img_list'}).find_all('div',{'class':'thumb'})
        for webtoon_id in webtoon_ids:
            id_section = webtoon_id.find('a')['href']
            comic_id = id_section[id_section.find('titleId=')+8:id_section.find('&weekday')]
            day_list.append([comic_id,day])
    return day_list

def get_soup(driver, url):
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    return soup

def webtoon_genre_mapping(driver):
    url= 'http://comic.naver.com/webtoon/genre.nhn?genre=episode'
    soup = get_soup(driver, url)
    full_genre_list = [] 
    genre_list = []
    href_list = []
    for genre in soup.find('ul',{'class':'category_tab category_tab2'}).find_all('a'):
        genre_list.append(genre['href'][genre['href'].find('=')+1:])
        href_list.append('http://comic.naver.com'+genre['href'])
    for i in range(len(genre_list)):
        full_genre_list.append([href_list[i], genre_list[i]])
    return full_genre_list

def check_for_duplicates(webtoon_id, full_list):
    is_duplicate = False
    counter = 0
    for big_item in full_list:
        if str(webtoon_id) == str(big_item[0]):
            is_duplicate = True
            break
        else:
            counter +=1
    return is_duplicate, counter

def need_all_days(webtoon, day_list):
    ids = subimages = webtoon.find('div',{'class':'thumb'}).find_all('a')
    for iD in ids:
        this_id = iD['href'][iD['href'].find('titleId=')+8:]
        days = []
        for item in day_list:
            if str(item[0]) == str(this_id):
                days.append(item[1])
    return this_id, days

def get_datails(webtoon, day_list, big_list, genre):
    this_id, days = need_all_days(webtoon, day_list)
    is_duplicate, counter = check_for_duplicates(this_id, big_list)
    
    small_list = []
    title = webtoon.find('dl').find('dt').find('a')['title']
    author = webtoon.find('dl').find('dd',{'class':'desc'}).find('a').text
    if is_duplicate:
        big_list[counter][2] = big_list[counter][2] + '/' + genre
    else:      
        small_list.append(this_id)
        if len(days) == 0:
            small_list.append('완결')
        else:
            days = '/'.join(days)
            small_list.append(days)
        small_list.append(genre)
        small_list.append(title)
        small_list.append(author)
        subimages = webtoon.find('div',{'class':'thumb'}).find('a').find_all('img')
        if len(subimages) == 1:
            small_list.append(subimages[0]['src'])
            small_list.append('미완결')
        else :
            for subimage in subimages:
                if 'thumb' in subimage['src']:
                    small_list.append(subimage['src'])
                else:
                    small_list.append(subimage['alt'])
        webtoon_type = []
        for span in webtoon.find('a').find_all('span'):
            if span['class'] != ['mask'] and span.text != 'NEW':
                webtoon_type.append(span.text)
        if len(webtoon_type) == 0:
            webtoon_type.append('일반')
        small_list.append(webtoon_type[0])
    return small_list

def webtoon_sorted_by_genre(driver, genre_list ,day_list):
    big_list = []
    for url2 in genre_list:
        url = url2[0]
        genre = url2[1]
        soup = get_soup(driver, url)
        for webtoon in soup.find('ul',{'class':'img_list'}).find_all('li'):
            small_list = get_datails(webtoon, day_list, big_list, genre)     
            if not small_list == []:   
                big_list.append(small_list)
    return big_list


def execute():
    driver = webdriver.Chrome('/Users/taeyoungchoi/git/web-crawling-naver/chromedriver')
    day_list = webtoon_day_mapping(driver)
    genre_list = webtoon_genre_mapping(driver)
    big_list = webtoon_sorted_by_genre(driver, genre_list, day_list)
    driver.close()
    csv.csvWriter(big_list, 'webtoon_database.csv')    