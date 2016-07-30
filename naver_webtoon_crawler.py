# -*- coding: utf-8 -*-
'''
Created on Jun 13, 2016

@author: TYchoi
'''

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csvHandler as csv
import pickleHandler as pickle
import urllib.request

def getListOfWebtoon(soup):
    listOfCartoon = {}
    titles = soup.find_all('a',{'class':'title'})
    for comment in titles:
        hyperLink = comment['href']
        idFinderFront = hyperLink.find('titleId=')+8
        idFinderEnd = hyperLink.find('&weekday')
        webToonID = hyperLink[idFinderFront : idFinderEnd]
        listOfCartoon[comment.text] = webToonID
    return listOfCartoon

def pageSourceRetriever(driver, searchUrl):
    driver.get(searchUrl)
    # change time.sleep to be appropriate to your internet connection.
    time.sleep(1.5)
    r=driver.page_source
    soup=BeautifulSoup(r, "lxml") 
    return soup

def getBestComments(newUrlList, bestCommentFile):
    print('Best Comments Downloader Launching....................')
    driver = initializeWebdriver()
    
    completeList = []
    pickle.pickleSaver(completeList, 'webtoonBestComment.pkl')
    completeList = pickle.pickleLoader('webtoonBestComment.pkl')
        
    for i in range(len(newUrlList)):
        print('-------------------------------------------------------------------------------')
        print(i+1,newUrlList[i][1],newUrlList[i][2])
        url = newUrlList[i][5].replace("http://","http://m.")
        episodeLinkNumber = newUrlList[i][3]
        updateDate = newUrlList[i][4]
        print(url)
        soup=pageSourceRetriever(driver, url)  
        dates = soup.find_all('div',{'class':'u_comment_info'})
        comments = soup.find_all('p',{'class':'u_comment_text u_comment_txt1'})
        likes = soup.find_all('div',{'class':'u_comment_recomm __comment_recomm'})
        numbOfCuts = soup.find('div',{'class':'toon_view_lst'})
        cutCounter = -1
        if numbOfCuts:
            numbOfCuts = numbOfCuts.find_all('li')
            for item in numbOfCuts:
                cutCounter += 1
        n = 1
        for date in range(len(dates)):
            times = dates[date].text[dates[date].text.find(")")+2:dates[date].text.find(" |")]
            comment = comments[date].text.replace("BEST","") 
            numbOfLikes = likes[date].find_all('em')
            likeCounts = []
            if numbOfLikes:
                for item in numbOfLikes:
                    likeCounts.append(int(item.text))
            idx = int(newUrlList[i][0])
            name = newUrlList[i][1]
            episode = newUrlList[i][2]
            listToAdd = [idx, name, episode, episodeLinkNumber, updateDate, str(date+1), times, likeCounts[0], likeCounts[1], cutCounter ,comment]
            print(listToAdd)
            completeList.append(listToAdd)            
            n+=1
    driver.close()
    csv.csvWriter(completeList, bestCommentFile)
    print('Done with Best Comments Downloader !!!!')

def getCurrentlyPublishedWebtoon(driver):
    url = 'http://comic.naver.com/webtoon/weekday.nhn'
    soup = pageSourceRetriever(driver, url)
    currentWebtoonTitles = getListOfWebtoon(soup)
    
    return currentWebtoonTitles

def initializeWebdriver():
    baseurl = 'https://nid.naver.com/nidlogin.login'
    myId = 'stayoungchoi'
    pw = 'Xodud128411#'
    xpaths = {'id': "//input[@name='id']", 'pw':"//input[@name='pw']"}
    driver = webdriver.Chrome()

    driver.get(baseurl)
    driver.find_element_by_xpath(xpaths['id']).send_keys(myId)
    driver.find_element_by_xpath(xpaths['pw']).send_keys(pw)
    btn = driver.find_element_by_css_selector('.int_jogin')
    btn.click()
    driver.implicitly_wait(10)
    
    return driver

def urlBuilder(webtoonID, episodeNum):
    if episodeNum == '':
        url = 'http://comic.naver.com/webtoon/list.nhn?titleId={}'.format(webtoonID)
    else:
        url = 'http://comic.naver.com/webtoon/detail.nhn?titleId={0}&no={1}'.format(webtoonID,episodeNum)
    return url

def updateWebToonList(webToonTitleFile):
    #Choose One
    driver = webdriver.PhantomJS(executable_path='/Users/TYchoi/PythonProjects/phantomjs/bin/phantomjs')
#     driver = webdriver.PhantomJS(executable_path='/Users/Kuk/celebtide/bin/phantomjs')
#     driver = webdriver.PhantomJS(executable_path='/Users/Mycelebscom/phantomjs/bin/phantomjs')
#     driver = webdriver.PhantomJS()
    currentWebtoon = getCurrentlyPublishedWebtoon(driver)
    driver.close()

    try:
        savedWebtoon = csv.csvReader_toDict(webToonTitleFile)
        print("sucessfully loaded", webToonTitleFile,'.csv') 
    except:
        savedWebtoon = {}
        
    currentWebtoonKeys = list(currentWebtoon)
    savedWebtoonKeys = list(savedWebtoon)
    print (len(currentWebtoonKeys), len(savedWebtoonKeys))
    numberOfChanges = 0
    
    addedList = []
    deletedList = []
    
    for item in currentWebtoonKeys:
        if item not in savedWebtoonKeys:
            savedWebtoon[item] = currentWebtoon[item]
            addedList.append(currentWebtoon[item])
            numberOfChanges += 1
    
    for item in savedWebtoonKeys:
        if item not in currentWebtoonKeys:
            deletedList.append(savedWebtoon[item])
            del savedWebtoon[item]
            numberOfChanges += 1
    
    if numberOfChanges == 0 :
        print("No Webtoon List Updates Required")
    else:
        print("Webtoon List Has Been Updated. Automatically overwrites webtoonTitle_current.csv.")
        if len(deletedList) == 0:
            deletedList.append("NONE")
        elif len(addedList) == 0:
            addedList.append("NONE")    
        print("Added:",", ".join(addedList),"Deleted:",", ".join(deletedList))
        csv.csvDictWriter(savedWebtoon, webToonTitleFile)
    
    return savedWebtoon, deletedList

def getDates(soup):
    dates = []
    dateList = soup.find_all('td',{'class':'num'})
    for date in dateList:
        dates.append(date.text.replace(".",""))
    return dates

def getNewThumbnailEpisodeUrl(webToonList, urlDataBase):
    #Choose One
    driver = webdriver.PhantomJS(executable_path='/Users/TYchoi/PythonProjects/phantomjs/bin/phantomjs')
#     driver = webdriver.PhantomJS(executable_path='/Users/Kuk/celebtide/bin/phantomjs')
#     driver = webdriver.PhantomJS(executable_path='/Users/Mycelebscom/phantomjs/bin/phantomjs')
#     driver = webdriver.PhantomJS()
    newList = []
    for name in sorted(webToonList.keys()):
        print('-----------------------------------')
        print(name)
        print('-----------------------------------')
        url = urlBuilder(webToonList[name], '')
        nextButtonExists = True
        while nextButtonExists:
            soup = pageSourceRetriever(driver, url)
            numCount = 0
            dates = getDates(soup)
            lastEpisodeNum = soup.find('tbody').find_all('td')
            duplicates_appeared = False            
            for each in lastEpisodeNum:
                listOfImages = each.find_all('img')
                for item in listOfImages:
                    if 'title' in str(item) and '배경음악 있음' not in item['title']:
                        thumbnailLink = item['src']
                        episodeNumFinder1 = thumbnailLink.find(webToonList[name])+len(webToonList[name])+1
                        episodeNmeFinder2 = thumbnailLink.find('/inst_thumbnail')
                        episodeLinkNumber = thumbnailLink[episodeNumFinder1:episodeNmeFinder2]
                        url = urlBuilder(webToonList[name], episodeLinkNumber)
                        listToAdd = [webToonList[name],name,item['title'],episodeLinkNumber,dates[numCount],url,thumbnailLink]
                        if listToAdd not in urlDataBase:
                            print(listToAdd)
                            newList.append(listToAdd)
                            numCount+=1
                        else:
                            numCount+=1
                            nextButtonExists = False
                            duplicates_appeared = True
                if duplicates_appeared:
                    break
                else:
                    pass
            if nextButtonExists:
                try :
                    nextButton = driver.find_element_by_css_selector('a.next')
                    nextButton.click()
                    url = driver.current_url
                    time.sleep(0.5)
                except:
                    nextButtonExists=False
            else:
                break
    driver.close()
    return newList

def thumbNailDownloader(newUrlList):
    print("downloading thumbnails................")
    counter = 1
    for url in newUrlList:
        try:
            urllib.request.urlretrieve(url[-1], "thumbnail/"+url[0]+"_"+url[4]+"_"+url[3]+".jpg")
            print("Done With ",counter,"out of ",len(newUrlList))
            counter += 1
        except:
            print('we have a problem with !!'+url[-1])
            counter += 1
    print("done downloading thumbnails!!!")
    
def dataBaseUpdate(deletedList, webToonUrlFile):
    # if we don't have url database created, we make one.  
    try:
        urlDataBase = csv.csvReader_toList(webToonUrlFile)
        print("sucessfully loaded", webToonUrlFile,'.csv')        
    except:
        urlDataBase = []       
    
    if deletedList:
        print('deleting',", ".join(deletedList),"from",webToonUrlFile)
        for item in urlDataBase:
            if item[0] in deletedList:
                urlDataBase.remove(item)
    return urlDataBase

def main():
    # you can change the names of csv files as you wish.
    webToonUrlFile = 'webToonUrl_current'
    webToonTitleFile = 'webtoonTitle_current'
    bestCommentFile = 'webtoonBestComments'
    
    # This function opens webtoonTitle_current.csv file,
    # which contains the list of webtoon in our database.
    # Then connects to Naver webtoon page that contains the most current webtoon list.
    # we then compare two lists and updates our webtoon database.
    # it returns the updated webtoon database and webtoon titles that have been removed.
    webToonList, deletedList = updateWebToonList(webToonTitleFile)
    
    # update urlDataBase with webtoons that are currently being published ONLY
    urlDataBase = dataBaseUpdate(deletedList, webToonUrlFile)
     
    # checks if there are new episodes
    # returns urls of thumbnails and episodes that need to be added to database. 
    newUrlList = getNewThumbnailEpisodeUrl(webToonList, urlDataBase)
 
    # if no updates required, pass
    # else, we 
    # 1. download its thumbnail
    # 2. update our url database
    # 3. retrieve best comments for each episode
#     newUrlList = csv.csvReader_toList(webToonUrlFile)
    if len(newUrlList) > 0 :
        thumbNailDownloader(newUrlList)
        urlDataBase = urlDataBase + newUrlList
        csv.csvWriter(urlDataBase, webToonUrlFile)
        getBestComments(newUrlList, bestCommentFile)    
     
    else:
        print("No Webtoon To Update.")
     
if __name__ == "__main__":
    main()