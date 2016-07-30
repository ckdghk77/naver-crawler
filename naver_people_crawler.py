'''
Created on Jul 13, 2016

@author: TYchoi
'''

from selenium import webdriver
from bs4 import BeautifulSoup
import pprint

def ButtonClicker(driver, soup, category ,number):
    bigList=[]
    gotNextButton = True

    bigList = get_contents(soup, bigList, category, number) 
    while gotNextButton:
        try:
            num = driver.find_element_by_css_selector('#pagination_{} > span:nth-child(4) > a'.format(number))
            num.click()
            r=driver.page_source
            soup=BeautifulSoup(r, "lxml")
            bigList = get_contents(soup,bigList, category,number)
        except:
            gotNextButton = False
    return bigList

def get_contents(soup, bigList, category, number):
    section = soup.find('ul',{'id':'listUI_{}'.format(number)})
    if section:
        grids = section.find_all('li')
        for grid in grids:
            littleList = [category]
            for line in grid.find_all('span',{'class':['tit_wrap','dsc_area']}):
                littleList.append(line.text)
            bigList.append(littleList)
    else:
        bigList = [category,None,None,None]
    return bigList

def get_records(soup):
    careerDict = {0:'경력사항', 1:'수상내역'}
    items = soup.find_all('div',{'class':'record'})
    recordList = []
    counter = 0
    for item in items:
        records= item.find_all('p')
        dates= item.find_all('dt')
        for item2 in range(len(records)):
            recordList.append([careerDict[counter], dates[item2].text, records[item2].text])
        counter += 1
    return recordList

def main():
    url = 'http://people.search.naver.com/search.naver?where=nexearch&query=%EC%9D%B4%EB%AF%BC%ED%98%B8&sm=tab_etc&ie=utf8&key=PeopleService&os=143015'
    driver = webdriver.PhantomJS(executable_path='/Users/TYchoi/PythonProjects/phantomjs/bin/phantomjs')
    codeDict = {77:'concert', 81:'music video', 82:'cf', 80:'books', 76:'tv show', 78:'movie',  79:'album'}
    driver.get(url)
    r=driver.page_source
    soup=BeautifulSoup(r, "lxml")
    recordList = get_records(soup)
    pprint.pprint(recordList)    
    for item in sorted(codeDict.keys()):
        eachList = ButtonClicker(driver, soup, codeDict[item] ,item)
        pprint.pprint(eachList)
if __name__ == "__main__":
    main()