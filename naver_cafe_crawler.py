'''
Created on Aug 3, 2016

@author: TYchoi
'''

import math
import requests
from urllib import parse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def get_webbrowser_with_log_in():
    baseurl = 'https://nid.naver.com/nidlogin.login'
    id = 'stayoungchoi'
    pw = 'Xodud128411#'
    xpaths = {'id': "//input[@name='id']", 'pw':"//input[@name='pw']"}
    
    driver = webdriver.Chrome()
    driver.get(baseurl)
    driver.find_element_by_xpath(xpaths['id']).send_keys(id)
    driver.find_element_by_xpath(xpaths['pw']).send_keys(pw)
    btn = driver.find_element_by_css_selector('.int_jogin')
    btn.click()
    driver.implicitly_wait(10)
    return driver 

def cafe_search_url(searchQuery):
    query=searchQuery.replace(searchQuery,parse.quote(searchQuery))
    url = 'http://m.cafe.naver.com/SectionArticleSearch.nhn?page=1&sortBy=0&query={}'.format(query)
    return url

def get_soup(driver, url):
    driver.get(url)
    r=driver.page_source
    soup=BeautifulSoup(r, "lxml") 
    return soup

def main():
    driver = get_webbrowser_with_log_in()
    url = cafe_search_url('올림픽')
    soup = get_soup(driver, url)
    for url in soup.find('ul',{'id':'sectionArticleSearchList'}).find_all('a'):
        print(url['href'])
    time.sleep(10)
if __name__ == "__main__":
    main()