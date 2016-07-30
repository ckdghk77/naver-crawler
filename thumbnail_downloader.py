'''
Created on Jul 27, 2016

@author: TYchoi
'''

import urllib.request
import excelHandler as excel
import pprint

excel_file = excel.excelReader('july_episodes.xlsx')

list_to_download = []
for i in range(1,len(excel_file)):
    list_to_download.append([int(excel_file[i][0])]+ excel_file[i][-5:])

for j in range(len(list_to_download)):
    for k in range(len(list_to_download[j])-1):
        fileName = '-{}.jpg'.format(str(k+1))
        fileName = str(list_to_download[j][0])+str(fileName)
        fileName = 'july/'+fileName
        urllib.request.urlretrieve(list_to_download[j][k+1], fileName)