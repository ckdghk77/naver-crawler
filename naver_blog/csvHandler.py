'''
Created on Jul 4, 2016

@author: TYchoi
'''
import csv

def csvReader_toList(datafile):
    with open(datafile, newline='',encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        csvreader = list(csvreader)
        csvfile.close()
    return csvreader

def csvWriter(wantToSave,name):
    with open(name, 'w', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for i in range(len(wantToSave)):
            csvwriter.writerow(wantToSave[i])
        csvfile.close()    

def csvDictWriter(wantToSave, name):
    with open(name, 'w', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for key in sorted(wantToSave.keys()):
            csvwriter.writerow([key,wantToSave[key]])
        csvfile.close()    

def csvReader_toDict(datafile):
    with open(datafile, newline='',encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        mydict = {rows[0]:rows[1] for rows in csvreader}
        csvfile.close()
    return mydict
