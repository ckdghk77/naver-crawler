'''
Created on Jun 16, 2016

@author: TYchoi
'''
from selenium import webdriver
from bs4 import BeautifulSoup
import xlsxwriter
import pickle
from openpyxl.compat import range

def pageSourceRetriever(driver, searchUrl):
    driver.get(searchUrl)
    r=driver.page_source
    soup=BeautifulSoup(r, "lxml") 
    return soup

def createListOfCartoonTitlesAndLastUpdates(soup, whatWeWant):
    titleList = []
    lastUpdateList = []
    completeList = []
    titles = soup.find_all('td',{'class':'subject'})
    for title in titles:
        titleList.append(title.find('a').text)
    lastUpdates = soup.find_all('td',{'class':'date'})
    for lastUpdate in lastUpdates:
        lastUpdateList.append(lastUpdate.text.split(' ')[0])                          
        
    for i in range(len(titleList)):
        if titleList[i] not in [row[0] for row in whatWeWant]:
            completeList.append([titleList[i],' ',lastUpdateList[i]])
    
    return completeList

def getFistUpdateDate(driver, url, completeList):
    for i in range(len(completeList)):
        driver.get(url)
        print(completeList[i][0])
        link = driver.find_element_by_link_text(completeList[i][0])
        link.click()
        link = driver.find_element_by_link_text('첫회보기')
        link.click()
        r=driver.page_source
        soup=BeautifulSoup(r, "lxml") 
        date = soup.find('dd',{'class':'date'})
        if date:
            completeList[i][1] = date.text
        else:
            completeList[i][1] = ""
    return completeList

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
    baseurl = 'https://nid.naver.com/nidlogin.login'
    myId = 'stayoungchoi'
    pw = 'Xodud128411#'
    xpaths = {'id': "//input[@name='id']", 'pw':"//input[@name='pw']"}

    driver = webdriver.PhantomJS(executable_path='/Users/TYchoi/PythonProjects/phantomjs/bin/phantomjs')
    driver.get(baseurl)
    driver.find_element_by_xpath(xpaths['id']).send_keys(myId)
    driver.find_element_by_xpath(xpaths['pw']).send_keys(pw)
    btn = driver.find_element_by_css_selector('.int_jogin')
    btn.click()
    driver.implicitly_wait(10)
    
#     driver = webdriver.Firefox()
    
    listOfSearchUrls = []
    whatWeWant = []
    for i in range(2005,2017):
        listOfSearchUrls.append('http://comic.naver.com/webtoon/period.nhn?period='+str(i)+'&view=list')
    
    for url in listOfSearchUrls:
        soup = pageSourceRetriever(driver,url)
        listOfWebToon = createListOfCartoonTitlesAndLastUpdates(soup, whatWeWant)
        whatWeWant = whatWeWant + getFistUpdateDate(driver, url, listOfWebToon)
        with open('webtoonDates.pkl','wb') as pickle_file:
            pickle.dump(whatWeWant, pickle_file)  
        with open('webtoonDates.pkl','rb') as pickle_load:
            whatWeWant=pickle.load(pickle_load)
    writeToExcel(whatWeWant, '웹툰날짜')
main()