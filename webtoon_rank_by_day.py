'''
Created on Aug 5, 2016

@author: TYchoi
'''

import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import csvHandler as csv

def updated_today_question():
    try:
        ranking_db = csv.csvReader_toList('webtoon_ranking_by_day.csv')
    except:
        ranking_db = []
        
    dates_of_db = [x[0] for x in ranking_db]
    today = datetime.datetime.now()
    today_date = today.strftime('%Y-%m-%d')
    return today_date in dates_of_db, today_date, ranking_db

def update_database(today_date, ranking_db):
    driver = webdriver.Chrome()
    url = 'http://comic.naver.com/webtoon/weekday.nhn'
    driver.get(url)
    r = driver.page_source
    soup = BeautifulSoup(r, 'lxml')
    for day in soup.find('div',{'class':'list_area daily_all'}).find_all('div',{'class':'col'}):
        what_day = day.find('h4')['class'][0]
        counter = 1
        rank_dict = {}
        for webtoon in day.find('ul').find_all('a'):
            link = webtoon['href']
            link_index_start = link.find('titleId=')+8
            link_index_end = link.find('&weekday')
            webtoon_id = link[link_index_start:link_index_end]
            rank_dict[counter] = webtoon_id
            counter += 1
        list_to_add = [today_date, what_day, rank_dict]
        ranking_db.append(list_to_add)
        
    csv.csvWriter(ranking_db, 'webtoon_ranking_by_day.csv')
    driver.close()

def main():
    do_we_need_to_update, today_date, ranking_db = updated_today_question()
    if do_we_need_to_update:
        print("we've already added today's ranking")
    else:
        update_database(today_date, ranking_db)

if __name__ == "__main__":
    main()
