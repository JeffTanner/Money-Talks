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
    ('1','Gas'),
    ('2','Food'),
    ('3','living expenses'),
    ('4','Clothing'),
    ('5','Other'),
]
subcategories = [
    ('1','2','grocery'),
    ('2','2','eating out'),
    ('3','3','insurance'),
    ('4','3','utilities'),
    ('5','3','rent'),
    ('6','3','other')
]

def createCsv(fileName, header, content):
    with open(fileName, 'wb') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        csvWriter.writerow(header)
        for row in content:
            csvWriter.writerow(row)
#        del csvWriter

def setupDatabase():
    #connect to/create the database
    dbConn = sqlite3.connect(dbName)
    dbCur = dbConn.cursor()
    
    # add all appropriate tables
    dbCur.execute('''CREATE TABLE purchases (id INTEGER PRIMARY KEY, date text, description text, debit real, credit real, category_id INTEGER, subcategory_id INTEGER)''')
    dbCur.execute('''CREATE TABLE categories (id INTEGER, category TEXT) ''')
    dbCur.execute('''CREATE TABLE subcategories (id INTEGER, category_id INTEGER, category TEXT) ''')
    
    dbConn.commit()
    dbConn.close()

def createFolderStructure(basePath):
    curPath = os.path.join(basePath, appFolder, expFolder, bankStateFolder, statementSetupFolder)
    if not os.path.exists(curPath):
        os.makedirs(curPath)
        os.chdir(curPath)
        createCsv('banks.csv', ['bank prefix','Date','Check Number','Description','Debit','Credit'], [])
        createCsv('categories.csv', ['id','category'], categories)
        createCsv('subcategories.csv', ['sub_cat_id','cat_id','sub_cat'], subcategories)
        createCsv('category-transaction_matching.csv', ['keyword','category','subcategory'],[['gas', '5', '3']])
    
    curPath = os.path.join(basePath, appFolder, expFolder, dbFolder)
    if not os.path.exists(curPath):
        os.makedirs(curPath)
    
    os.chdir(curPath)
    if not os.path.exists(os.path.join(basePath, appFolder, expFolder, dbFolder, dbName)):
        setupDatabase()