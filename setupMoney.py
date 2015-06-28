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
categTransMatch = [
    ('gas', '5'), 
    ('WEGMANS', '2', '1'),
    ('SAFEWAY', '2', '1'),
    ('COCOS INTERNATIONAL', '2', '1'),
    ('ALDI', '2', '1'),
    ('GIANT', '2', '1'),
    ('FOOD LION', '2', '1'),
    ('LOTTE', '2', '1'),
    ('7-ELEVEN', '2', '2'),
    ('FIVE GUYS', '2', '2'),
    ('MICHAELS', '5'),
    ('OFFICE DEPOT', '5'),
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
    dbCur.execute('''CREATE TABLE matches (id INTEGER PRIMARY KEY, keyword TEXT, category_id INTEGER, subcategory_id TEXT) ''')
    
    dbConn.commit()
    
    dbCur.executemany('INSERT INTO categories (?,?)', categories)
    dbCur.executemany('INSERT INTO subcategories (?,?,?)', subcategories)
    dbCur.executemany('INSERT INTO matches (?,?,?)', categTransMatch)
    
    dbConn.close()

def createFolderStructure(basePath):
    curPath = os.path.join(basePath, appFolder, expFolder, bankStateFolder, statementSetupFolder)
    if not os.path.exists(curPath):
        os.makedirs(curPath)
        os.chdir(curPath)
        createCsv('banks.csv', ['bank prefix','Date','Check Number','Description','Debit','Credit'], [])
        createCsv('categories.csv', ['id','category'], categories)
        createCsv('subcategories.csv', ['sub_cat_id','cat_id','sub_cat'], subcategories)
        createCsv('category-transaction_matching.csv', ['keyword','category_id','subcategory_id'],categTransMatch)
    
    curPath = os.path.join(basePath, appFolder, expFolder, dbFolder)
    if not os.path.exists(curPath):
        os.makedirs(curPath)
    
    os.chdir(curPath)
    if not os.path.exists(os.path.join(basePath, appFolder, expFolder, dbFolder, dbName)):
        setupDatabase()