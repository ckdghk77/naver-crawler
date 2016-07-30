'''
Created on Jun 20, 2016

@author: TYchoi
'''

from bs4 import BeautifulSoup

import urllib.request
 
client_id = 'qErSWJSDpwKsDm4SWGzx'
client_secret = 'McHJ2naEJd'
url = 'https://openapi.naver.com/v1/search/blog.xml?'
headers = {"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret}
query = urllib.parse.urlencode({'query':'자전거'})

url = url+query
request = urllib.request.Request(url, headers= headers)

response = urllib.request.urlopen(request)

soup = BeautifulSoup(response.read(), 'xml')
print(soup.prettify())
links = soup.find_all('link')
for link in links[1:]:
    print(link.text)
    request = urllib.request.Request(link.text, headers= headers)
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response.read(),'lxml')
    contents = soup.find_all('p')
    for line in contents:
        print(line.text)
    print(soup)
    break




