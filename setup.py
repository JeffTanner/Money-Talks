import os, sys, sqlite3, csv

__author__ = "Tannerism"
__date__ = "$Jun 27, 2015 7:46:45 PM$"

    
appFolder = "Money_Talks"
expFolder = "Expenses"
dbFolder = ".db"
dbName = "transactions.db"
bankStateFolder = "Bank_Statements"
statementSetupFolder = "setup"
categories = [
    ['id','category'],
    ['1','Gas'],
    ['2','Food'],
    ['3','living expenses'],
    ['4','Clothing'],
    ['5','Other'],
]
subcategories = [
    ['sub_cat_id','cat_id','sub_cat'],
    ['1','2','grocery'],
    ['2','2','eating out'],
    ['3','3','insurance'],
    ['4','3','utilities'],
    ['5','3','rent'],
    ['6','3','other']
]

def createCsv(fileName, content):
    with open(fileName, 'wb') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for row in content:
            csvWriter.writerow(row)
#        del csvWriter



def createFolderStructure(basePath):
    curPath = os.path.join(basePath, appFolder, expFolder, bankStateFolder, statementSetupFolder)
    if not os.path.exists(curPath):
        os.makedirs(curPath)
        os.chdir(curPath)
        createCsv('banks.csv', [['bank prefix','Date','Check Number','Description','Debit','Credit']])
        createCsv('categories.csv', categories)
        createCsv('subcategories.csv', subcategories)
        createCsv('category-transaction_matching.csv', [['keyword','category','subcategory'],['gas', '5', '3']])
    curPath = os.path.join(basePath, appFolder, expFolder, dbFolder)
    if not os.path.exists(curPath):
        os.makedirs(curPath)
        os.chdir(curPath)
        conn = sqlite3.connect(dbName)
        
    elif not os.path.exists(os.path.join(basePath, appFolder, expFolder, dbFolder, dbName)):
        os.chdir(curPath)
        conn = sqlite3.connect(dbName)