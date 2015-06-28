import os, sys, sqlite3, csv

__author__ = "Tannerism"
__date__ = "$Jun 27, 2015 7:46:45 PM$"

    
appFolder = "Money_Talks"
expFolder = "Expenses"
dbFolder = ".db"
dbName = "transactions.db"
bankStateFolder = "Bank_Statements"
statementSetupFolder = "setup"

def createCsv(fileName, content):
    with open(fileName, 'wb') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        csvWriter.writerow(content)
        del csvWriter

def createFolderStructure(basePath):
    curPath = os.path.join(basePath, appFolder, expFolder, bankStateFolder, statementSetupFolder)
    if not os.path.exists(curPath):
        os.makedirs(curPath)
        os.chdir(curPath)
        createCsv('banks.csv', ['bank prefix','Date','Check Number','Description','Debit','Credit'])
    curPath = os.path.join(basePath, appFolder, expFolder, dbFolder)
    if not os.path.exists(curPath):
        os.makedirs(curPath)
        os.chdir(curPath)
        conn = sqlite3.connect(dbName)
        
    elif not os.path.exists(os.path.join(basePath, appFolder, expFolder, dbFolder, dbName)):
        os.chdir(curPath)
        conn = sqlite3.connect(dbName)
        conn.commit()
        
#def setupDatabase(filePath):