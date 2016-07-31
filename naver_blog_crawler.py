# -*- coding: utf-8 -*-
#
'''
Created on Jun 13, 2016

@author: TYchoi
'''

from selenium import webdriver
from bs4 import BeautifulSoup
from urllib import parse
import excelHandler as excel
import pickleHandler as pickle
import csvHandler as csv
    
def maxNumberFinder(soup):
    numOfPosts = soup.find('span',{'class':'title_num'})

    if numOfPosts:
        numOfPosts = int(numOfPosts.text.split(' ')[-1].replace(',','')[:-1])   
        if numOfPosts > 50:
            maxnum = 5
        else:
            if numOfPosts%10 == 0:
                maxnum = int(numOfPosts/10)
            else:
                maxnum = int(numOfPosts/10)+1
    else:
        numOfPosts = 0
        maxnum = 0   
    return numOfPosts, maxnum

def urlGenerator(searchQuery, fromDate, toDate, pageNum):
    query=searchQuery.replace(searchQuery,parse.quote(searchQuery))
    searchUrl='https://search.naver.com/search.naver?where=post&query='+query+'&ie=utf8&st=sim&sm=tab_opt&date_from='+fromDate+'&date_to='+toDate+'&date_option=8&srchby=all&dup_remove=1&post_blogurl=&post_blogurl_without=&nso=so%3Ar%2Ca%3Aall%2Cp%3Afrom'+fromDate+'to'+toDate+'&mson=0'
    if pageNum:
        searchUrl = searchUrl + '&start=' + pageNum
    return searchUrl

def dateRangeGenerator(startingDate, toDate):
    startingYear = int(startingDate[:4])
    toYear = int(toDate[:4])
    
    dateList = ['0301','0601','0901','1201']
    fromtoDateList = {'0301':'0531','0601':'0831','0901':'1130','1201':'0228'}
    
    start = []
    end = []
    start.append(startingDate)
    for i in range(toYear-startingYear+1):
        year = startingYear+i
        for date in dateList:
            currentDate = int(str(year)+date)
            if int(startingDate) < currentDate and int(toDate) > currentDate:
                start.append(currentDate)
    
    for i in range(toYear-startingYear+1):
        year = startingYear+i
        for date in dateList:
            if date == '1201':
                currentDate = int(str(year+1)+fromtoDateList[date])
            else:
                currentDate = int(str(year)+fromtoDateList[date])
            if int(startingDate) < currentDate and int(toDate) > currentDate:
                end.append(currentDate)
    end.append(toDate)
    
    listToReturn = []
    for i in range(len(start)):
        listToReturn.append([str(start[i]),str(end[i])])
    
    return listToReturn

def pageSourceRetriever(driver, searchUrl):
    driver.get(searchUrl)
    r=driver.page_source
    soup=BeautifulSoup(r, "lxml") 
    return soup

def getHrefs(soup):
    for item in soup.find_all('a', {'class':'sh_blog_title _sp_each_url _sp_each_title'}):
        href=item['href']
    return href

def getDate(soup):
    for item in soup.find_all('dd',{'class':'txt_inline'}):
        date = item.text.split(" ")[0]
    return date

def urlRetriever(queryList, dateRange):
    #Choose One
    driver = webdriver.PhantomJS(executable_path='/Users/TYchoi/PythonProjects/phantomjs/bin/phantomjs')
#     driver = webdriver.PhantomJS(executable_path='/Users/Kuk/celebtide/bin/phantomjs')
#     driver = webdriver.PhantomJS(executable_path='/Users/Mycelebscom/phantomjs/bin/phantomjs')
#     driver = webdriver.PhantomJS()

    buzzInfo = []
    listOfPosts = []
    for query in queryList:
        searchword = query[1] #Query located Column number    
        print (searchword)
        for date in dateRange:
            searchUrl = urlGenerator(searchword, date[0], date[1], '')
            print(searchUrl)
            soup = pageSourceRetriever(driver, searchUrl) 
            numOfPosts, maxNum = maxNumberFinder(soup)
            
            for i in range(maxNum):
                num = str(10*i+1)
                searchUrlByPage = urlGenerator(searchword, date[0], date[1], num)
                soup = pageSourceRetriever(driver, searchUrlByPage)
                
                sections = soup.find_all('li', {'class':'sh_blog_top'})
                for section in sections:
                    href = getHrefs(section)
                    datePosted = getDate(section)
                    listOfPosts.append([query[0],query[1], datePosted, date[0] ,href]) #1占쎈였占쎈퓠 idx, 2占쎈였占쎈퓠 占쎌뵠�뵳占�
            buzzInfo.append([query[0],query[1],date[0], numOfPosts]) #1占쎈였占쎈퓠 idx, 2占쎈였占쎈퓠 占쎌뵠�뵳占�

    driver.quit()
    
    return buzzInfo, listOfPosts

def blogContentsCrawler(urlList, pickleName):
    #Choose One
    driver = webdriver.PhantomJS(executable_path='/Users/TYchoi/PythonProjects/phantomjs/bin/phantomjs')
#     driver = webdriver.PhantomJS(executable_path='/Users/Kuk/celebtide/bin/phantomjs')
#     driver = webdriver.PhantomJS(executable_path='/Users/Mycelebscom/phantomjs/bin/phantomjs')
#     driver = webdriver.PhantomJS()
    
    driver.set_page_load_timeout(10)
    pickle.pickleSaver(urlList, pickleName)
    blogList = pickle.pickleLoader(pickleName)

    for i in range(len(blogList)): #1/n 筌띾슦寃� 占쎌삂占쎈씜占쎈뻻 占쎈링占쎌벥 占쎄땀占쎌뒠 癰귨옙野껋�鍮먲옙鍮욑옙釉�. 占쎌굙) 1/3占쎈뎃 占쎌삂占쎈씜占쎈뻻 int(len(blogList)/3)/ int(len(blogList)/3),int(len(blogList)*2/3) / int(len(blogList)*2/3),len(blogList)   
        print(i+1,"out of",len(blogList))
        if 'naver' in blogList[i][4]:
            url = blogList[i][4]
            url = url.replace('?Redirect=Log&logNo=', '/')
            url = url.replace('http://','http://m.')
            try:
                soup=pageSourceRetriever(driver, url)
                contents = ''
                contentBox = soup.find_all('div',{'class':'post_ct  '})
                if contentBox:
                    for j in contentBox:
                        lines = j.find_all('div')
                        lines = lines + j.find_all('p')
                        lines = lines + j.find_all('span')
                        if lines:
                            for m in lines:
                                if m.text:
                                    if (' '.join(m.text.split())) not in contents:
                                        contents = contents + ' ' + ' '.join(m.text.split())
                        print(contents[1:50])  
            except:
                print("Loading Failed! :  "  + url)
            
            if contents:
                blogList[i].append(contents[1:])
                blogList[i][4] = url
                pickle.pickleSaver(blogList, pickleName)
                blogList = pickle.pickleLoader(pickleName)
            else:
                print("No Content Error! :  " + url)
        else:
            print("Not a Naver blog ! :  " + blogList[i][4])
    
    driver.quit()
    return blogList
    
def main():

    queryList = excel.excelReader('test.xlsx')
    dateRange = dateRangeGenerator('20160504','20160704')
    print(dateRange)
    buzzInfo, listOfPosts = urlRetriever(queryList, dateRange)
     
    csv.csvWriter(listOfPosts, 'test_url')
    csv.csvWriter(buzzInfo, 'test_buzzinfo')
     
    # if we have the url file ready, comment out the lines above 
    # and run the 3 lines only below this comment
    # Make sure to run the line below that's been commented out.

#     listOfPosts = excel.excelReader('ramenList.xlsx')   
        
    blogContents = blogContentsCrawler(listOfPosts, 'test')
    csv.csvWriter(blogContents, 'testBlog')
     
if __name__ == "__main__":
    main()