'''
Created on Jul 13, 2016

@author: TYchoi
'''

from selenium import webdriver
from bs4 import BeautifulSoup
import excelHandler as excel
import time

def ButtonClicker(driver):
    gotNextButton = True
    while gotNextButton:
        try:
            num = driver.find_element_by_css_selector('#cbox_module > div > div.u_cbox_paginate > a > span > span > span.u_cbox_page_more')
            num.click()
            time.sleep(1)
        except:
            gotNextButton = False

def main():
    completeList = []
    newslist = excel.excelReader('ranking news list_3.xlsx')
    newslist = newslist[1:]
    driver = webdriver.Firefox()
    for news in newslist:
        date = news[0]
        media = news[1]
        title = news[2]
        url = news[3]
        url2 = url + '&m_view=1'
        print (url2)
        driver.get(url2)
        time.sleep(2)
        ButtonClicker(driver)
        r=driver.page_source
        soup=BeautifulSoup(r, "lxml")
        comments = soup.find_all('span',{'class':'u_cbox_contents'})
        dates = soup.find_all('span',{'class':'u_cbox_date'})
        recoms = soup.find_all('em',{'class':'u_cbox_cnt_recomm'})
        unrecoms = soup.find_all('em',{'class':'u_cbox_cnt_unrecomm'})
        counts = soup.find_all('span',{'class':'u_cbox_reply_cnt'})
        ids = soup.find_all('span',{'class':'u_cbox_nick'})
        for i in range(len(comments)):
            timestamp = dates[i]['data-value'].replace('T',' ')
            timestampSlice = timestamp.find('+')
            timestamp = timestamp[:timestampSlice]
            timestamp = timestamp.split(' ')
            completeList.append([date,media,title,url,ids[i].text,comments[i].text,timestamp[0],timestamp[1],recoms[i].text,unrecoms[i].text,counts[i].text])
#             print([date,media,title,url,ids[i].text,comments[i].text,timestamp[0],timestamp[1],recoms[i].text,unrecoms[i].text,counts[i].text])
    driver.close()
    excel.writeToExcel(completeList, 'naverNews3')

if __name__ == "__main__":
    main()
    