'''
Created on Jul 19, 2016

@author: TYchoi
'''

from selenium import webdriver
from bs4 import BeautifulSoup
import csvHandler as csv
import time

def urlBuilder():
    driver = webdriver.Firefox()
    urlList = []
    dateRange =['http://news.naver.com/main/ranking/popularWeek.nhn?rankingType=popular_week&sectionId={}&date=20160608',
            'http://news.naver.com/main/ranking/popularWeek.nhn?rankingType=popular_week&sectionId={}&date=20160615',
            'http://news.naver.com/main/ranking/popularWeek.nhn?rankingType=popular_week&sectionId={}&date=20160622',
            'http://news.naver.com/main/ranking/popularWeek.nhn?rankingType=popular_week&sectionId={}&date=20160629',
            'http://news.naver.com/main/ranking/popularWeek.nhn?rankingType=popular_week&sectionId={}&date=20160706',
            'http://news.naver.com/main/ranking/popularWeek.nhn?rankingType=popular_week&sectionId={}&date=20160713']
    newsCategory = {107:'스포츠',100:'정치',101:'경제',102:'사회',103:'생활/문화',104:'세계',105:'IT/과학',106:'연예'}
    for section in sorted(newsCategory.keys()):
        for date in dateRange:
            url = date.format(section)
            driver.get(url)
            r=driver.page_source
            soup=BeautifulSoup(r, "lxml")
            ranking = soup.find('td',{'class':'content'})
            allRanking = ranking.find_all(True,{'class':['ranking_top3','ranking_section ranfir2','ranking_section']})
            dateList =[]
            for dates in allRanking:
                date = dates.find_all('span',{'class':'num'})
                for day in date:
                    dateList.append(day.text)
            urls = []
            for eachArticle in allRanking:
                for topThirty in eachArticle.find_all('dl'):
                    for article in topThirty.find_all('a'):
                        if 'sports' not in article['href']:
                            urls.append('http://news.naver.com'+article['href'])
                        else:
                            urls.append(article['href'].replace('http//','http://'))
            for i in range(len(dateList)):
                urlList.append([newsCategory[section], urls[i], dateList[i]])
    driver.close()
    return urlList

def getDetails(urlList):
    driver = webdriver.Firefox()
    info = []
    for eachUrl in urlList:
        smallList = []
        section = eachUrl[0]
        url = eachUrl[1]
        date = eachUrl[2]
        driver.get(url)
        time.sleep(3)
        r=driver.page_source
        soup=BeautifulSoup(r, "lxml")
        titleSection = soup.find('div',{'class':'article_info'})
        if titleSection:
            title = titleSection.find(True,{'class':'font1 tts_head'})
            if not title:
                title = soup.find('p',{'class':'end_tit'})
        else:
            title= soup.find('h4',{'class':'title'})
        replyNum = soup.find('span',{'class':'u_cbox_count'})
        recomNum = soup.find('em',{'class':['u_cnt _cnt','u_cnt']})
        if not recomNum:
            recomNum = 0
        else:
            recomNum = recomNum.text
        sexPercent = soup.find_all('span',{'class':'u_cbox_chart_per'})
        smallList.append(section)
        smallList.append(date)
        smallList.append(title.text)
        smallList.append(replyNum.text)
        smallList.append(recomNum)
        for sex in sexPercent:
            smallList.append(sex.text)
        print(smallList)
        info.append(smallList)
    
    driver.close()
    return info

def main():
    urlList = urlBuilder()
    infoList = getDetails(urlList)
    csv.csvWriter(infoList, 'naver_news.csv')
if __name__ == "__main__":
    main()