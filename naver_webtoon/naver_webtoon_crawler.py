# -*- coding: utf-8 -*-

"""
Created on Jun 13, 2016

@author: TYchoi

naver_webtoon_crawler.py allows you to retrieve meta data of webtoon episodes on Naver.
It automatically updates database by accessing the most current page. 
Meta data includes: episode title, episode number, date published, length of episode (number of cuts), 
URL, thumbnail URL, best comments submitted by users, number of recommendations.
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csvHandler as csv
import urllib.request
import webtoon_cut_counter as cut_counter
import webtoon_database

def get_list_of_webtoon(soup):
    """
    Retrieves most up-to-date webtoon list

    Args:
        soup: BeautifulSoup page source file 
    Returns:
        list_of_cartoon : most up-to-date webtoon list
    """
    list_of_cartoon = {}
    titles = soup.find_all('a',{'class':'title'})
    for comment in titles:
        hyperLink = comment['href']
        id_finder_front = hyperLink.find('titleId=')+8
        id_finder_end = hyperLink.find('&weekday')
        webtoon_id = hyperLink[id_finder_front : id_finder_end]
        list_of_cartoon[comment.text] = webtoon_id
    return list_of_cartoon

def page_source_retriever(driver, search_url):
    """
    Creates page source of a webpage as a BeautifulSoup file

    Args:
        driver : currently active webdriver
        search_url : a webpage we want to load 
    Returns:
        soup: BeautifulSoup page source file 
    """

    driver.get(search_url)
    # change time.sleep to be appropriate to your internet connection.
    time.sleep(1.5)
    r=driver.page_source
    soup=BeautifulSoup(r, "lxml") 
    return soup

def get_best_comments(new_url_list, best_comment_file, myId, pw):
    """
    Gathers best comments for each episode of a webtoon which are submitted and evaluated by user  

    Args:
        new_url_list : a list of URLs to webtoon episodes that we need to add to database
        best_comment_file : a name of file that stores best comments
        myId : your Naver id
        pw : your Naver password 
    Raises:
        NoSuchElementException: 1. Wrong id or password information
                                2. Naver is not static 
    """
    
    print('Best Comments Downloader Launching....................')
    driver = initialize_webdriver(myId, pw)
    
    completeList = []
        
    for i in range(len(new_url_list)):
        print('-------------------------------------------------------------------------------')
        print(i+1,new_url_list[i][1],new_url_list[i][2])
        url = new_url_list[i][5].replace("http://","http://m.")
        episode_link_number = new_url_list[i][3]
        update_date = new_url_list[i][4]
        print(url)
        soup=page_source_retriever(driver, url)  
        dates = soup.find_all('div',{'class':'u_comment_info'})
        comments = soup.find_all('p',{'class':'u_comment_text u_comment_txt1'})
        likes = soup.find_all('div',{'class':'u_comment_recomm __comment_recomm'})
        for date in range(len(dates)):
            times = dates[date].text[dates[date].text.find(")")+2:dates[date].text.find(" |")]
            comment = comments[date].text.replace("BEST","") 
            numb_of_likes = likes[date].find_all('em')
            like_counts = []
            if numb_of_likes:
                for item in numb_of_likes:
                    like_counts.append(int(item.text))
            idx = int(new_url_list[i][0])
            name = new_url_list[i][1]
            episode = new_url_list[i][2]
            list_to_add = [idx, name, episode, episode_link_number, update_date, str(date+1), times, like_counts[0], like_counts[1], comment]
            print(list_to_add)
            completeList.append(list_to_add)            
    driver.close()
    csv.csvWriter(completeList, best_comment_file)
    print('Done with Best Comments Downloader !!!!')

def get_currently_publishing_webtoon(driver):
    """
    Creates most up-to-date webtoon list

    Args:
        driver: a webdriver object  
    Returns:
        current_webtoon_titles : most up-to-date webtoon list
    """
    
    url = 'http://comic.naver.com/webtoon/weekday.nhn'
    soup = page_source_retriever(driver, url)
    current_webtoon_titles = get_list_of_webtoon(soup)
    
    return current_webtoon_titles

def initialize_webdriver(myId, pw):
    """
    Intitialize webdriver and logs in with given user information
    some of webtoons requires log-in information because of different ratings.

    Args:
        myId : your Naver id
        pw : your Naver password 
    Returns:
        driver : a logged-in webdriver
    Raises:
        NoSuchElementException: Wrong id or password information
    """

    baseurl = 'https://nid.naver.com/nidlogin.login'
    xpaths = {'id': "//input[@name='id']", 'pw':"//input[@name='pw']"}
    driver = webdriver.Chrome()

    driver.get(baseurl)
    driver.find_element_by_xpath(xpaths['id']).send_keys(myId)
    driver.find_element_by_xpath(xpaths['pw']).send_keys(pw)
    btn = driver.find_element_by_css_selector('.int_jogin')
    btn.click()
    driver.implicitly_wait(10)
    
    return driver

def url_builder(webtoon_id, episode_num):
    """
    Generates url in an appropriate format.

    Args:
        webtoon_id: a webtoon id
        episode_num : a webtoon episode number 
    Returns:
        url : a url to an appropriate webtoon episode  
    Raises:
        AttributeError : a query must be String
    """

    if episode_num == '':
        url = 'http://comic.naver.com/webtoon/list.nhn?titleId={}'.format(webtoon_id)
    else:
        url = 'http://comic.naver.com/webtoon/detail.nhn?titleId={0}&no={1}'.format(webtoon_id,episode_num)
    return url

def check_updates(webtoon_title_file, phantom_path, chrome_path):
    """
    Checks if updates on webtoon database are required
    Compares database against current webtoon list then make appropriate changes

    Args:
        webtoon_title_file: the name of webtoon title database file
        phantom_path : the executable PhantomJS path
        chrome_path : the executable Chrome driver path
    Returns:
        saved_webtoon : a list of ids of webtoons that are newly added 
        deleted_list :  a list of ids of webtoons that have been deleted from database
    """
    
    driver = webdriver.PhantomJS(executable_path=phantom_path)
    current_webtoon = get_currently_publishing_webtoon(driver)
    driver.close()

    try:
        saved_webtoon = csv.csvReader_toDict(webtoon_title_file)
        print("sucessfully loaded", webtoon_title_file,'.csv') 
    except:
        saved_webtoon = {}
        
    current_webtoon_keys = list(current_webtoon)
    saved_webtoon_keys = list(saved_webtoon)
    print (len(current_webtoon_keys), len(saved_webtoon_keys))
    number_of_changes = 0
    
    added_list = []
    deleted_list = []
    
    for item in current_webtoon_keys:
        if item not in saved_webtoon_keys:
            saved_webtoon[item] = current_webtoon[item]
            added_list.append(current_webtoon[item])
            number_of_changes += 1
    
    for item in saved_webtoon_keys:
        if item not in current_webtoon_keys:
            deleted_list.append(saved_webtoon[item])
            del saved_webtoon[item]
            number_of_changes += 1
    
    if number_of_changes == 0 :
        print("No Webtoon List Updates Required")
    else:
        webtoon_database.execute(chrome_path)
        print("Webtoon List Has Been Updated. Automatically overwrites webtoonTitle_current.csv.")
        if len(deleted_list) == 0:
            deleted_list.append("NONE")
        elif len(added_list) == 0:
            added_list.append("NONE")    
        print("Added:",", ".join(added_list),"Deleted:",", ".join(deleted_list))
        csv.csvDictWriter(saved_webtoon, webtoon_title_file)
    
    return saved_webtoon, deleted_list

def get_dates(soup):
    """
    Retrieves dates that webtoon episodes are published

    Args:
        soup: BeautifulSoup page source file 
    Returns:
        dates : a list of dates
    """
    
    dates = []
    date_list = soup.find_all('td',{'class':'num'})
    for date in date_list:
        dates.append(date.text.replace(".",""))
    return dates

def get_new_thumbnail_episode_url(webtoon_list, url_database, phantom_path, chrome_path):
    """
    Creates a list of URLs to each webtoon episode and its thumbnail image
    As we build list, we gather meta data as well.

    Args:
        webtoon_list: updated webtoon id database
        url_databse : url_database that we want to update
        phantom_path : the executable PhantomJS path
        chrome_path : the executable Chrome driver path
    Returns:
        new_list : a crawl queue to webtoon episode and its thumbnail image
    """
    
    driver = webdriver.PhantomJS(executable_path=phantom_path)
    driver2 = webdriver.Chrome(chrome_path)
    
    new_list = []
    for name in sorted(webtoon_list.keys()):
        print('-----------------------------------')
        print(name)
        print('-----------------------------------')
        url = url_builder(webtoon_list[name], '')
        next_button_exists = True
        while next_button_exists:
            print(url)
            soup = page_source_retriever(driver, url)
            num_count = 0
            dates = get_dates(soup)
            last_episode_num = soup.find('tbody').find_all('td')
            recom_num = soup.find('em',{'class':'u_cnt'}).text
            duplicates_appeared = False            
            for each in last_episode_num:
                list_of_images = each.find_all('img')
                for item in list_of_images:
                    if 'title' in str(item) and '배경음악 있음' not in item['title']:
                        thumbnail_link = item['src']
                        episode_num_finder_1 = thumbnail_link.find(webtoon_list[name])+len(webtoon_list[name])+1
                        episodeNmeFinder2 = thumbnail_link.find('/inst_thumbnail')
                        episodeLinkNumber = thumbnail_link[episode_num_finder_1:episodeNmeFinder2]
                        url = url_builder(webtoon_list[name], episodeLinkNumber)
                        cut_counts = cut_counter.count_cuts(url.replace("http://","http://m."),driver2, webtoon_list[name], episodeLinkNumber)
                        list_to_add = [webtoon_list[name], recom_num,name,item['title'],episodeLinkNumber,dates[num_count], cut_counts,url,thumbnail_link]
                        if list_to_add not in url_database:
                            print(list_to_add)
                            new_list.append(list_to_add)
                            num_count+=1
                        else:
                            num_count+=1
                            next_button_exists = False
                            duplicates_appeared = True
                if duplicates_appeared:
                    break
                else:
                    pass
            if next_button_exists:
                try :
                    next_button = driver.find_element_by_css_selector('a.next')
                    next_button.click()
                    url = driver.current_url
                    time.sleep(0.5)
                except:
                    next_button_exists=False
            else:
                break

    driver.close()
    driver2.close()
    return new_list

def thumbnail_downloader(new_urllist):
    """
    Downloads thumbnail images 

    Args:
        new_urllist: a crawl queue to webtoon episode and its thumbnail image
    """    
    
    print("downloading thumbnails................")
    counter = 1
    for url in new_urllist:
        try:
            urllib.request.urlretrieve(url[-1], "thumbnail/"+url[0]+"_"+url[4]+"_"+url[3]+".jpg")
            print("Done With ",counter,"out of ",len(new_urllist))
            counter += 1
        except:
            print('we have a problem with !!'+url[-1])
            counter += 1
    print("done downloading thumbnails!!!")
    
def database_update(deleted_list, webtoon_url_file):
    """
    Delete Webtoon episodes that are completed publishing

    Args:
        deleted_list: a list of webtoons that are completed
        webtoon_url_file : un-updated URL database 
    Returns:
        url_database : a updated URL databse
    """

    # if we don't have url database created, we make one.  
    try:
        url_database = csv.csvReader_toList(webtoon_url_file)
        print("sucessfully loaded", webtoon_url_file,'.csv')        
    except:
        url_database = []       
    
    if deleted_list:
        print('deleting',", ".join(deleted_list),"from",webtoon_url_file)
        for item in url_database:
            if item[0] in deleted_list:
                url_database.remove(item)
    return url_database

def main():
    """
    1. check_updates opens webtoon title database.
    connects to Naver webtoon page and updates our webtoon database.
    2. updates url_database with webtoons that are currently being published ONLY.
    3. checks if there are new episodes. Returns urls of thumbnails and episodes that we need to add to database.
    4. download thumbnail images
    5. update our url database
    6. retrieve best comments for each episode 
    Raises:
        selenium.common.exceptions.WebDriverException: the webdriver cannot be found
    """    
    
    myId = ''
    pw = ''
    phantom_path = ''
    chrome_path = ''
    
    webtoon_url_file = ''
    webtoon_title_file = ''
    best_comment_file = ''
    
    webToonList, deletedList = check_updates(webtoon_title_file, phantom_path, chrome_path) 
    url_database = database_update(deletedList, webtoon_url_file)
     
 
    new_url_list = get_new_thumbnail_episode_url(webToonList, url_database, phantom_path, chrome_path)
 
    if len(new_url_list) > 0 :
        thumbnail_downloader(new_url_list)
        url_database = url_database + new_url_list
        csv.csvWriter(url_database, webtoon_url_file)
        get_best_comments(new_url_list, best_comment_file, myId, pw)    
     
    else:
        print("No Webtoon To Update.")
     
if __name__ == "__main__":
    main()