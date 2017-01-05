# -*- coding: utf-8 -*-

"""
Created on Jun 13, 2016
@author: TYchoi

naver_blog_crawler.py allows you to retrieve related blog posts of your interest.
You can feed a list of queries and different date ranges, 
so you can see what people are saying about certain things during a particular period of time.
"""

from selenium import webdriver
from bs4 import BeautifulSoup
from urllib import parse
import excelHandler as excel
import csvHandler as csv
    
def max_num_finder(soup):
    """Calculate the number of result pages.
    If there are no results regarding a given query, it simply returns zero.

    Args:
        soup: BeautifulSoup page source file 
    Returns:
        num_of_posts : the total number of posts created
        maxnum : the last page number of search results
    """
    num_of_posts = soup.find('span',{'class':'title_num'})

    if num_of_posts:
        num_of_posts = int(num_of_posts.text.split(' ')[-1].replace(',','')[:-1])
        
        # Naver show maximum of 1000 result pages
        # if there are more than 1000 result pages.
        if num_of_posts > 20:
            maxnum = 2
        else:
            if num_of_posts%10 == 0:
                maxnum = int(num_of_posts/10)
            else:
                maxnum = int(num_of_posts/10)+1
    else:
        num_of_posts = 0
        maxnum = 0   
    return num_of_posts, maxnum

def url_generator(search_query, from_date, to_date, page_num):
    """Generates url in an appropriate format.

    Args:
        search_query: search word
        from_date : starting date of the range
        to_date : ending date of the range
        page_num : current page number within the result pages
    Returns:
        search_url : url that we need to retrieve data from
    Raises:
        AttributeError : a query must be String
    """
    query=search_query.replace(search_query,parse.quote(search_query))
    search_url='https://search.naver.com/search.naver?where=post&query='+query+'&ie=utf8&st=sim&sm=tab_opt&date_from='+from_date+'&date_to='+to_date+'&date_option=8&srchby=all&dup_remove=1&post_blogurl=&post_blogurl_without=&nso=so%3Ar%2Ca%3Aall%2Cp%3Afrom'+from_date+'to'+to_date+'&mson=0'
    
    if page_num:
        search_url = search_url + '&start=' + page_num
    return search_url

def date_range_generator(starting_date, to_date):
    """Divides the date range into 3-month-periods
    Naver only displays 1000 results per search.
    For a longer period of time, we may lose a large amount of data.

    Args:
        starting_date : starting date of the range
        to_date : ending date of the range 
    Returns:
        three_months_periods : list of date ranges broken into 3-month-periods
    """
    
    if starting_date > to_date:
        print ("Inappropriate date range : ", "~".join([starting_date, to_date]))
        exit()
    
    starting_year = int(starting_date[:4])
    to_year = int(to_date[:4])

    
    date_list = ['0301','0601','0901','1201']
    from_to_date_list = {'0301':'0531','0601':'0831','0901':'1130','1201':'0228'}
    
    start = []
    end = []
    start.append(starting_date)
    for i in range(to_year-starting_year+1):
        year = starting_year+i
        for date in date_list:
            current_date = int(str(year)+date)
            if int(starting_date) < current_date and int(to_date) > current_date:
                start.append(current_date)
    
    for i in range(to_year-starting_year+1):
        year = starting_year+i
        for date in date_list:
            if date == '1201':
                current_date = int(str(year+1)+from_to_date_list[date])
            else:
                current_date = int(str(year)+from_to_date_list[date])
            if int(starting_date) < current_date and int(to_date) > current_date:
                end.append(current_date)
    end.append(to_date)
    
    three_months_periods = []
    for i in range(len(start)):
        three_months_periods.append([str(start[i]),str(end[i])])
    
    return three_months_periods

def page_source_retriever(driver, search_url):
    """Creates page source of a webpage as a BeautifulSoup file

    Args:
        driver : currently active webdriver
        search_url : a webpage we want to load 
    Returns:
        soup: BeautifulSoup page source file 
    """
    driver.get(search_url)
    r=driver.page_source
    soup=BeautifulSoup(r, "lxml") 
    return soup

def get_hrefs(soup):
    """Creates a list of urls to the blog posts on a search page 

    Args:
        soup: BeautifulSoup page source file 
    Returns:
        href: a list of hrefs to the blog posts on web 
    """
    for item in soup.find_all('a', {'class':'sh_blog_title _sp_each_url _sp_each_title'}):
        href=item['href']
    return href

def get_date(soup):
    """Creates a list of created dates of the blog posts on a search page 

    Args:
        soup: BeautifulSoup page source file 
    Returns:
        date: a list of created dates of the blog posts on a search page 
    """
    for item in soup.find_all('dd',{'class':'txt_inline'}):
        date = item.text.split(" ")[0]
    return date

def build_blog_list(query_list, date_range):
    """Creates a full list of blog posts 

    Args:
        query_list : list of queries
        date_rage : a user set date range 
    Returns:
        buzz_info : the total number of posts created of queries 
        list_of_poists : a list of all posts that contains queries, dates created, date ranges and urls of each blog post
    Raises:
        selenium.common.exceptions.WebDriverException: webdriver cannot be found
    """
    
    driver = webdriver.PhantomJS(executable_path='/Users/taeyoungchoi/git/web-crawling-naver/phantomjs/bin/phantomjs')

    buzz_info = []
    list_of_posts = []
    for query in query_list:
        searchword = query[0]     
        print (searchword)
        for date in date_range:
            search_url = url_generator(searchword, date[0], date[1], '')
            print(search_url)
            soup = page_source_retriever(driver, search_url) 
            num_of_posts, max_num = max_num_finder(soup)
            
            for i in range(max_num):
                current_page = str(10*i+1)
                search_url_by_page = url_generator(searchword, date[0], date[1], current_page)
                soup = page_source_retriever(driver, search_url_by_page)
                
                sections = soup.find_all('li', {'class':'sh_blog_top'})
                for section in sections:
                    href = get_hrefs(section)
                    date_posted = get_date(section)
                    list_of_posts.append([searchword, date_posted,href]) 
            buzz_info.append([searchword,date[0],date[1], num_of_posts]) 

    driver.quit()
    
    return buzz_info, list_of_posts

def blog_contents_crawler(list_of_posts):
    """Appends actual text of each blog post to the list of posts by visiting each page
    Visits Naver blogs ONLY.

    Args:
        list_of_poists : a list of all posts that contains queries, dates created, date ranges and urls of each blog post
    Returns:
        list_of_poists : updated list of all posts with text data
    Raises:
        selenium.common.exceptions.WebDriverException: webdriver cannot be found
    """

    driver = webdriver.PhantomJS(executable_path='/Users/taeyoungchoi/git/web-crawling-naver/phantomjs/bin/phantomjs')
    
    driver.set_page_load_timeout(10)
    for i in range(len(list_of_posts)):    
        print(i+1,"out of",len(list_of_posts))
        if 'naver' in list_of_posts[i][2]:
            url = list_of_posts[i][2]
            url = url.replace('?Redirect=Log&logNo=', '/')
            url = url.replace('http://','http://m.')
            try:
                soup=page_source_retriever(driver, url)
                contents = ''
                content_box = soup.find_all('div',['post_ct ','se_textView'])
                if content_box:
                    for j in content_box:
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
                list_of_posts[i].append(contents[1:])
                list_of_posts[i][2] = url
            else:
                print("No Content Error! :  " + url)
        else:
            print("Not a Naver blog ! :  " + list_of_posts[i][2])
    
    driver.quit()
    return list_of_posts
    
def main():
    """Read an excel file that contains a list of queries then outputs two csv files with gathered information

    Raises : 
        FileNotFoundError: an excel file that contains a list of queries cannot be found
    """
    
    qury_list_file = 'test.xlsx'
    starting_date = '20160103'
    ending_date = '20160103'
    
    buzz_output_file = 'buzz_test.csv'
    blog_text_output_file = 'blog_test.csv'

    query_list = excel.excelReader(qury_list_file)
    date_range = date_range_generator(starting_date, ending_date)
    
    buzz_info, list_of_posts = build_blog_list(query_list, date_range)
    csv.csvWriter(buzz_info, buzz_output_file) 
        
    blog_contents = blog_contents_crawler(list_of_posts)
    csv.csvWriter(blog_contents, blog_text_output_file)
     
if __name__ == "__main__":
    main()