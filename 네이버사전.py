'''
Created on Jun 13, 2016

@author: TYchoi
'''

from bs4 import BeautifulSoup
import xlsxwriter
from openpyxl.compat import range
import pickle
import urllib.request
import urllib.parse
import xlrd

def writeToExcel(wantToSave,name):
    numberOfRows = len(wantToSave)
    numberOfCols = len(wantToSave[0])
    workbook = xlsxwriter.Workbook(name+'.xlsx')
    workseet = workbook.add_worksheet()
    for i in range(numberOfRows):
        for j in range(numberOfCols):
            workseet.write(i,j, str(wantToSave[i][j]))

def excelReader(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = [[sheet.cell_value(r,col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]
    return data


def main():
    data = excelReader('연관어.xlsx')
    for i in range(4684,len(data)):
        name = data[i][0]
        print ('----------------------------------------')
        print ('검색단어 : '+ data[i][0])
        print ('----------------------------------------')
        query=name.replace(name,urllib.parse.quote(name))
        searchUrl = 'http://cndic.naver.com/search/all?q='+query
        req = urllib.request.Request(searchUrl)
        r = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(r,'lxml')
        whichDoYouWannaSave = ['']
        wordList =soup.find('div',{'class':'word_result '})
        if wordList:
            wordList = wordList.find_all('li') 
        
        translation = soup.find('div',{'class':'trans_result line_b_none'})
        word = translation.find('dd')
        whichDoYouWannaSave.append(word.text.strip())
        
        print ("1." + word.text.strip())
        count = 2
        
        if wordList:
            for word in wordList:
                word = word.text.strip().replace("1", str(count))
                word = word.replace("2", str(count))
                word = word.replace("4", str(count))
                showing =word.replace("3", str(count)).replace(" ","").replace("。"," ")
                while '[' in showing:
                    showing = showing.replace(showing[showing.find("["):showing.find("]")+1],"")
                print(showing)
                whichDoYouWannaSave.append(showing[2:])
                count += 1
            print ('----------------------------------------')
            choice = input("맞는단어 고르세요: ")
            if int(choice) == 0 :
                print ("선택단어 : 없음")
            else:
                print ("선택단어 : {}".format(whichDoYouWannaSave[int(choice)]))
                data[i][2] = whichDoYouWannaSave[int(choice)]
        else:
            print(name+'사전 결과없음')
            print ('----------------------------------------')
            choice = input("맞는단어 고르세요: ")
            if int(choice) == 0 :
                print ("선택단어 : 없음")
            else:
                print ("선택단어 : {}".format(whichDoYouWannaSave[int(choice)]))
                data[i][2] = whichDoYouWannaSave[int(choice)]
                
        with open('dictionary.pkl','wb') as pickle_file:
            pickle.dump(data, pickle_file)  
        with open('dictionary.pkl','rb') as pickle_load:
            data=pickle.load(pickle_load)

    writeToExcel(data, '사전결과')
main()