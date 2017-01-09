# -*- coding: utf-8 -*-

"""
Created on Jun 13, 2016

@author: TYchoi


"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csvHandler as csv
import urllib.request
import webtoon_cut_counter as cut_count
import webtoon_database

def get_list_of_webtoon(soup):
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
    driver.get(search_url)
    # change time.sleep to be appropriate to your internet connection.
    time.sleep(1.5)
    r=driver.page_source
    soup=BeautifulSoup(r, "lxml") 
    return soup

def get_best_comments(new_url_list, best_comment_file):
    print('Best Comments Downloader Launching....................')
    driver = initialize_webdriver()
    
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
    url = 'http://comic.naver.com/webtoon/weekday.nhn'
    soup = page_source_retriever(driver, url)
    current_webtoon_titles = get_list_of_webtoon(soup)
    
    return current_webtoon_titles

def initialize_webdriver():
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

def url_builder(webtoon_id, episode_num):
    if episode_num == '':
        url = 'http://comic.naver.com/webtoon/list.nhn?titleId={}'.format(webtoon_id)
    else:
        url = 'http://comic.naver.com/webtoon/detail.nhn?titleId={0}&no={1}'.format(webtoon_id,episode_num)
    return url

def update_webtoon_list(web_toon_title_file):

    driver = webdriver.PhantomJS(executable_path='/Users/taeyoungchoi/git/web-crawling-naver/phantomjs/bin/phantomjs')

    current_webtoon = get_currently_publishing_webtoon(driver)
    driver.close()

    try:
        saved_webtoon = csv.csvReader_toDict(web_toon_title_file)
        print("sucessfully loaded", web_toon_title_file,'.csv') 
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
        webtoon_database.execute()
        print("Webtoon List Has Been Updated. Automatically overwrites webtoonTitle_current.csv.")
        if len(deleted_list) == 0:
            deleted_list.append("NONE")
        elif len(added_list) == 0:
            added_list.append("NONE")    
        print("Added:",", ".join(added_list),"Deleted:",", ".join(deleted_list))
        csv.csvDictWriter(saved_webtoon, web_toon_title_file)
    
    return saved_webtoon, deleted_list

def get_dates(soup):
    dates = []
    date_list = soup.find_all('td',{'class':'num'})
    for date in date_list:
        dates.append(date.text.replace(".",""))
    return dates

def get_new_thumbnail_episode_url(webtoon_list, url_data_base):

    driver = webdriver.PhantomJS(executable_path='/Users/taeyoungchoi/git/web-crawling-naver/phantomjs/bin/phantomjs')

    driver2 = webdriver.Chrome('/Users/taeyoungchoi/git/web-crawling-naver/chromedriver')
    
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
                        cut_counts = cut_count.count_cuts(url.replace("http://","http://m."),driver2, webtoon_list[name], episodeLinkNumber)
                        list_to_add = [webtoon_list[name], recom_num,name,item['title'],episodeLinkNumber,dates[num_count], cut_counts,url,thumbnail_link]
                        if list_to_add not in url_data_base:
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
            """
            """
            break
    driver.close()
    driver2.close()
    return new_list

def thumbnail_downloader(new_url_list):
    print("downloading thumbnails................")
    counter = 1
    for url in new_url_list:
        try:
            urllib.request.urlretrieve(url[-1], "thumbnail/"+url[0]+"_"+url[4]+"_"+url[3]+".jpg")
            print("Done With ",counter,"out of ",len(new_url_list))
            counter += 1
        except:
            print('we have a problem with !!'+url[-1])
            counter += 1
    print("done downloading thumbnails!!!")
    
def data_base_update(deleted_list, web_toon_url_file):
    # if we don't have url database created, we make one.  
    try:
        url_data_base = csv.csvReader_toList(web_toon_url_file)
        print("sucessfully loaded", web_toon_url_file,'.csv')        
    except:
        url_data_base = []       
    
    if deleted_list:
        print('deleting',", ".join(deleted_list),"from",web_toon_url_file)
        for item in url_data_base:
            if item[0] in deleted_list:
                url_data_base.remove(item)
    return url_data_base

def main():
    # you can change the names of csv files as you wish.
    webtoon_url_file = 'webToonUrl_current'
    webtoon_title_file = 'webtoonTitle_current'
    best_comment_file = 'webtoonBestComments'
    
    # This function opens webtoonTitle_current.csv file,
    # which contains the list of webtoon in our database.
    # Then connects to Naver webtoon page that contains the most current webtoon list.
    # we then compare two lists and updates our webtoon database.
    # it returns the updated webtoon database and webtoon titles that have been removed.
    webToonList, deletedList = update_webtoon_list(webtoon_title_file)
    
    # update url_database with webtoons that are currently being published ONLY
    url_database = data_base_update(deletedList, webtoon_url_file)
     
    # checks if there are new episodes
    # returns urls of thumbnails and episodes that need to be added to database. 
    new_url_list = get_new_thumbnail_episode_url(webToonList, url_database)
 
    # if no updates required, pass
    # else, we 
    # 1. download its thumbnail
    # 2. update our url database
    # 3. retrieve best comments for each episode
#     new_url_list = csv.csvReader_toList(webtoon_url_file)
    if len(new_url_list) > 0 :
        thumbnail_downloader(new_url_list)
        url_database = url_database + new_url_list
        csv.csvWriter(url_database, webtoon_url_file)
        get_best_comments(new_url_list, best_comment_file)    
     
    else:
        print("No Webtoon To Update.")
     
if __name__ == "__main__":
    main()