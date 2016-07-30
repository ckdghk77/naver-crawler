
#!/usr/bin/python
# -​*- coding:utf-8 -*​-

###모바일 테더링으로 작업하세요


import pprint
from selenium import webdriver
from bs4 import BeautifulSoup
import time


def main():
	url='http://m.store.naver.com/restaurants/detail?id=21607745'
# 	driver = webdriver.Firefox()
	driver = webdriver.PhantomJS(executable_path='/Users/TYchoi/PythonProjects/phantomjs/bin/phantomjs')
	driver.get(url)
	r=driver.page_source
	soup = BeautifulSoup(r, 'lxml')
	
	name = soup.find('strong', {'class':'place_name ng-binding'})
	print(name.text)
	category = soup.find('span',{'class':'category ng-binding ng-scope'})
	print(category.text)
	address = soup.find('span',{'class': 'address_text ng-binding'})
	print(address.text)

	info = soup.find('ul',{'class':'list_info'})
	hours = info.find_all('span',{'class':'ng-binding ng-scope'})   
	for hour in hours:
		print(hour.text)

	extra = info.find('div',{'class':'text ng-binding'})
	print(extra.text)
	
	broadcasts = info.find_all('div',{'class':'tv ng-binding'})
	for broadcast in broadcasts:
		print (broadcast.text)
		
	homepage = info.find('a',{'class':'url ng-binding'})
	print (homepage.text)
	
	subways = soup.find_all('div',{'class':'station'})
	for item in subways:
		lines = item.find_all('a')
		for subway in lines:
			print(subway.text)
	
	bus = soup.find_all('ul',{'class':'list_bus'})
	for item in bus:
		lines = item.find_all('span',{'class':'bus_number ng-binding ng-scope'})
		for subway in lines:
			print(subway.text.replace(',',''))
	
	menuChart = soup.find('div',{'class':'menu_info_area ng-scope ng-isolate-scope'})
	menu = menuChart.find_all('span',{'class':'menu ng-binding'})
	price = menuChart.find_all('em',{'class':'price ng-binding ng-scope'})
		
	for i in range(len(menu)):
		print(menu[i].text, price[i].text)

	menu_picture = soup.find('div',{'class':'list_thumb carousel-container'})
	menu_picUrl = menu_picture.find_all('img')
	for item in menu_picUrl:
		print(item['src'])
	
	dataInfo = soup.find('div',{'class':'data_info_area ng-scope'})
	keywords = dataInfo.find_all('li',{'class':'list_item ng-scope'})
	for keyword in keywords:
		print(keyword.text)

	
	barCharts = soup.find('div',{'class':'chart_bar'})
	ranking = soup.find_all('div',{'class':'bar highrank', 'class':'bar'})
	age = barCharts.find_all('div',{'class':'label ng-binding'})
	
	popularity = {}
	for i in range(len(ranking)):
		popularity[age[i].text+'대'] =ranking[i]['style'].replace('height: ','').split('.')[0] 
	
	print(popularity)
		
	images = soup.find_all('div',{'class':'six_thumb'})
	for image in images:
		print(image['style'].replace('background-image:url(','').replace(')',''))
		
	similarPlaces = soup.find_all('li',{'class':'carousel-content list_item ng-scope'})
	for place in similarPlaces:
		link = place.find('a')
		name = place.find('strong',{'class': 'title ng-binding'})
		category = place.find('div',{'class':'category ng-binding'})
		print(name.text, category.text, link['href'])
	
	bestTimeList = []
	dayConverter={'tooltip0':'월','tooltip1':'화','tooltip2':'수','tooltip3':'목','tooltip4':'금','tooltip5':'토','tooltip6':'일' }
	
	day = 0
	while day < 7:
		bestTimes = soup.find_all('div',{'class':'tooltip rt'})
		for besttime in bestTimes:
			if besttime['id'] not in [row[0] for row in bestTimeList]:
				bestTimeList.append([besttime['id'], besttime.text])
		elem = driver.find_element_by_css_selector('a.btn_direction.btn_next')
		elem.click()	
		r=driver.page_source
		soup = BeautifulSoup(r, 'lxml')
		day += 1
		
	for i in range(len(bestTimeList)):
		bestTimeList[i][0] = dayConverter[bestTimeList[i][0]]
	
	pprint.pprint(bestTimeList)
	
	reviewLink = soup.find('a', {'mg-nclicks-action':'moreReviews'})
	moreReviews = reviewLink['href']
	driver.get(moreReviews)
	
	windowPosition = 0
	for i in range(2):	
		windowPosition += 3000
		code='window.scrollTo(0, {})'.format(str(windowPosition)) #3000 y 축 이동 값
		driver.execute_script(code)
		time.sleep(0.5)

	linksToBlog = driver.find_elements_by_tag_name('a')
	for item in range(len(linksToBlog)):
		print(linksToBlog[item].text)
		linksToBlog[item].click()
		print(driver.current_url)
		break
	

if __name__ == "__main__":
	main()


