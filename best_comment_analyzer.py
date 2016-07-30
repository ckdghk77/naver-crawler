'''
Created on Jul 28, 2016

@author: TYchoi
'''

import requests
from bs4 import BeautifulSoup
import excelHandler as excel

bestCom1 = excel.excelReader('webtoonBestComments2.xlsx')
# bestCom2 = excel.excelReader('webtoonBestComments2.xlsx')
analysis_result2= []
analysis_result = []
for i in range(len(bestCom1)):
    title = bestCom1[i][1]+' '+bestCom1[i][2]
    is_in_list = False
    for j in range(len(analysis_result)):
        if title in analysis_result[j]:
            analysis_result[j][1] = str(analysis_result[j][1]) +' ' + str(bestCom1[i][5])
            is_in_list = True
            break
    if not is_in_list:
        analysis_result.append([title,bestCom1[i][5]])
print('done loading')
for comments in analysis_result:
    query = comments[1]
    episode = comments[0]

    url = 'http://dev.celebtide.com:9190/ka_web/morph.ka'
    data_format = {'message': query}
    r=requests.post(url, data=data_format).text
    soup = BeautifulSoup(r,'lxml')
     
    result_table = soup.find('table',{'sytle':'border=1;'})
    # print(result_table)
    items =result_table.find_all('td')
    result_dict = {}
    for i in range(0,len(items),2):
        if i <21:
            result_dict[items[i].text.strip()] = items[i+1].text.strip()
        else:
            break
    print([episode, result_dict])
    analysis_result2.append([episode, result_dict])

excel.writeToExcel(analysis_result2, 'webtoon_NLP_2')
     
    