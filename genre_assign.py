'''
Created on Jul 26, 2016

@author: TYchoi
'''
from ast import literal_eval
import os 
import csvHandler as csv
import excelHandler as excel
import pprint
genreList = ['action','comic', 'sports', 'episode','daily','drama','fantasy','historical','omnibus','pure','sensibility','story','thrill']
genreAssigner = []
for genre in genreList:
    for root, dirs, files in os.walk("/Users/TYchoi/git/MyTestProject/src/naverCrawler/webtoon/{}".format(genre)):
        for file in files:
            if file.endswith(".jpg"):
                genreAssigner.append([genre,file.replace('.jpg','')])
excel.writeToExcel(genreAssigner, 'genreAssign')        
csv.csvWriter(genreAssigner, 'genreAssign.csv')

# webtoon_DB = csv.csvReader_toList('webtoonTitle_current')
# genreAssign = csv.csvReader_toList('genreAssign.csv')
#     
# genreAdded = []
# for webtoon in webtoon_DB:
#     name = webtoon[0]
#     for genre in genreAssign:
#         weneedList = [x for x in genre]
#         weneedList2 = weneedList[1:]
#         print(len(webtoon[0]),len(weneedList2[1]))
#         if webtoon[0] in weneedList2:
#             genreAdded.append([webtoon[0],webtoon[1],genre[0]])
#         else:
#             genreAdded.append([webtoon[0],webtoon[1],'please add genre'])
#     break
# pprint.pprint(genreAdded)

# csv.csvWriter(genreAdded, 'genreAdded')