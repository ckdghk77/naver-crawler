'''
Created on Jun 27, 2016

@author: TYchoi
'''

import urllib.parse
from selenium import webdriver
import xlsxwriter
import re
import xlrd
import time

def excelReader(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = [[sheet.cell_value(r,col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]
    return data

def pageSourceRetreiver(driver, searchUrl):
    driver.get(searchUrl)
    pageSource=driver.page_source
    
    return pageSource

def queryBuilder(name):
    query=name.replace(name,urllib.parse.quote(name))
    searchUrl = 'http://m.store.naver.com/restaurants/list?query={}&skip=0&rs=Liph64'.format(query)
    return searchUrl

def totalPostCounter(pageSource):
    total=re.findall('전체<em class="count ng-binding">([\d]+)', pageSource)
    print(total)
    if len(total)!=0:
        totalcount=int(total[0])
    else:
        totalcount=0
        
    return totalcount

def idCollector(pageSource, id_list):
    potentialId=re.findall('mg-nclicks-item-id=([\" \d]+)',pageSource)
    if len(potentialId)!=0:
        for item in potentialId:
            item=item.replace('"','').replace(' ','')
            if item.isdigit() :
                id_list.add(item)
    else:
        pass
    
    return id_list

def windowScroller(driver, windowPosition):
    windowPosition += 3000
    code='window.scrollTo(0, {})'.format(str(windowPosition)) #3000 y 축 이동 값
    driver.execute_script(code) 

def writeToExcel(wantToSave,name):
    numberOfRows = len(wantToSave)
    numberOfCols = len(wantToSave[0])
    workbook = xlsxwriter.Workbook(name+'.xlsx')
    workseet = workbook.add_worksheet()
    for i in range(numberOfRows):
        for j in range(numberOfCols):
            workseet.write(i,j, str(wantToSave[i][j]))
    workbook.close()

def main():
    driver = webdriver.Firefox()
#     driver = webdriver.PhantomJS(executable_path='/Users/TYchoi/PythonProjects/phantomjs/bin/phantomjs')
#     data = excelReader('enterFileName.xlsx')
#     data = '강남맛집'
    id_list=set()
    
#     for queryKey in data:
        
    queryKey = '안심리맛집'
    searchUrl = queryBuilder(queryKey)
#     pageSource = pageSourceRetreiver(driver, searchUrl)
    driver.get(searchUrl)
    pageSource=driver.page_source
    totalCount = totalPostCounter(pageSource)
    
    goUntilEnd =True
    windowPosition=0
    
    while goUntilEnd:
        time.sleep(1)
        pageSource=driver.page_source
        id_list = idCollector(pageSource, id_list)
        print(id_list)
        windowScroller(driver, windowPosition)
        if totalCount == len(id_list):
            goUntilEnd = False
            
    print(id_list)
    writeToExcel(list(id_list), '네이버맛집url')
    
if __name__ == "__main__":
    main()
    