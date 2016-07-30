'''
Created on Jul 20, 2016

@author: TYchoi
'''

import time
from urllib import parse 
from selenium import webdriver
import csvHandler as csv

def initializeWebdriver():
    baseurl = 'https://nid.naver.com/nidlogin.login'
    myId = 'stayoungchoi'
    pw = 'Xodud128411#'
    xpaths = {'id': "//input[@name='id']", 'pw':"//input[@name='pw']"}
    driver = webdriver.Firefox()

    driver.get(baseurl)
    driver.find_element_by_xpath(xpaths['id']).send_keys(myId)
    driver.find_element_by_xpath(xpaths['pw']).send_keys(pw)
    btn = driver.find_element_by_css_selector('.int_jogin')
    btn.click()
    driver.implicitly_wait(10)
    
    return driver

def textParser(text):
    returnText = text.split('/')[-1].replace(',','').replace('건','').strip()
    return returnText

def searchUrlParser(searchQuery):
    resultList = []
    
    url="https://search.naver.com/search.naver.com?q=뉴발란스"
    query=searchQuery.replace(searchQuery,parse.quote(searchQuery))
    formats = {'https://search.naver.com/search.naver?where=post&sm=tab_jum&ie=utf8&query={}':'#main_pack > div.blog.section._blogBase > div > span',
               'https://search.naver.com/search.naver?where=article&sm=tab_jum&ie=utf8&query={}':'#_cafe_section > div > span',
               'https://search.naver.com/search.naver?where=webkr&sm=tab_jum&ie=utf8&query={}':'#main_pack > div.webdoc.section > div > span'}
    for urlformat in sorted(formats.keys()):
        values = formats[urlformat]
        url = urlformat.format(query)
        resultList.append([searchQuery,url,values])
    return resultList

def buzzSelector(driver, searchUrl):
    counterDict = {'#_cafe_section > div > span':'카페', '#main_pack > div.blog.section._blogBase > div > span':'블로그', '#main_pack > div.webdoc.section > div > span':'웹문서'}
    resultSet = [searchUrl[0], counterDict[searchUrl[2]]]
    try :
        buzz = driver.find_element_by_css_selector(searchUrl[2])
        buzz = textParser(buzz.text)
    except :
        buzz = 0
    resultSet.append(buzz)
    return resultSet

def main():
    driver =initializeWebdriver()
    weWantToSave = []
    searchQueryList = csv.csvReader_toList('.csv')
    searchUrls = []
    for searchQuery in searchQueryList:
        searchUrls +=searchUrlParser(searchQuery[0])
    for searchUrl in searchUrls:
        try:
            driver.get(searchUrl[1])
            resultSet = buzzSelector(driver, searchUrl)
        except:
            time.sleep(120)
            try:
                driver.get(searchUrl[1])
                resultSet = buzzSelector(driver, searchUrl)
            except:
                resultSet = []
        weWantToSave.append(resultSet)
     
    csv.csvWriter(weWantToSave, 'naver_buzz.csv')
    driver.close()
if __name__ == "__main__":
    main()