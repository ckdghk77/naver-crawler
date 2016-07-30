'''
Created on Jul 1, 2016

@author: TYchoi

This module can save a list as an Excel Document
and creates a list from an Excel Document 
'''

import xlrd
import xlsxwriter

def excelReader(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = [[sheet.cell_value(r,col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]
    return data

def writeToExcel(wantToSave,name):
    numberOfRows = len(wantToSave)
    numberOfCols = len(wantToSave[0])
    workbook = xlsxwriter.Workbook(name+'.xlsx')
    workseet = workbook.add_worksheet()
    for i in range(numberOfRows):
        for j in range(numberOfCols):
            workseet.write(i,j, str(wantToSave[i][j]))
    workbook.close()