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
    ('1','Transportation'),
    ('2','Food'),
    ('3','living expenses'),
    ('4','Clothing'),
    ('5','Bank Transactions'),
    ('6','Entertainment'),
    ('7','Hobbies'),
    ('8','Donations'),
    ('9','Other'),
    ('10','Credit Card'),
    ('11','Medical')
]
subcategories = [
    ('1','2','grocery'),
    ('2','2','eating out'),
    ('3','3','insurance'),
    ('4','3','utilities'),
    ('5','3','rent'),
    ('6','3','other living expenses'),
    ('7','5','Money Transfer'),
    ('8','5','Deposit'),
    ('9','5','Withdrawal')
]
categTransMatch = [
    ('WEGMANS', '2', '1','0'),
    ('SAFEWAY', '2', '1','0'),
    ('COCOS INTERNATIONAL', '2', '1','0'),
    ('ALDI', '2', '1','0'),
    ('GIANT', '2', '1','0'),
    ('FOOD LION', '2', '1','0'),
    ('LOTTE', '2', '1','0'),
    ('7-ELEVEN', '2', '2','0'),
    ('FIVE GUYS', '2', '2','0'),
    ('MICHAELS', '5', '','0'),
    ('OFFICE DEPOT', '5', '','0')
]
def createCsv(fileName, header, content, useHeader=True):
    openType = "wb"
    if useHeader == False:
        openType = "ab"
    with open(fileName, openType) as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        if useHeader == True:
            csvWriter.writerow(header)
        for row in content:
            csvWriter.writerow(row)
#        del csvWriter

def updateCsv(fileName, content):
    createCsv(fileName, [], content, False)

def setupDatabase(cat, subcat, matches, exists=True):
    #connect to/create the database
    dbConn = sqlite3.connect(dbName)
    dbCur = dbConn.cursor()
    
    # drop the tables is they already exist
    dbCur.execute('''DROP TABLE IF EXISTS categories ''')
    dbCur.execute('''DROP TABLE IF EXISTS subcategories ''')
    dbCur.execute('''DROP TABLE IF EXISTS matches ''')
    dbConn.commit()
    
    # add all appropriate tables
    if exists == False:
        dbCur.execute('''CREATE TABLE purchases (id INTEGER PRIMARY KEY, year INTEGER, month INTEGER, day INTEGER, check_num INTEGER, description text, debit real, credit real, category_id INTEGER, subcategory_id INTEGER, match_id INTEGER, notes TEXT)''')
    dbCur.execute('''CREATE TABLE categories (id INTEGER, category TEXT) ''')
    dbCur.execute('''CREATE TABLE subcategories (id INTEGER, category_id INTEGER, category TEXT) ''')
    dbCur.execute('''CREATE TABLE matches (id INTEGER PRIMARY KEY, keyword TEXT, category_id INTEGER, subcategory_id INTEGER, always_show INTEGER) ''')
#    dbCur.execute('''CREATE TABLE folder_path (path TEXT) ''')
    
    dbConn.commit()
    
    if exists == False:
        dbCur.execute('''CREATE INDEX year_idx ON purchases(year) ''')
        dbCur.execute('''CREATE INDEX month_idx ON purchases(month) ''')
        dbCur.execute('''CREATE INDEX day_idx ON purchases(day) ''')
        dbCur.execute('''CREATE INDEX check_num_idx ON purchases(check_num) ''')
        dbCur.execute('''CREATE INDEX description_idx ON purchases(description) ''')
        dbCur.execute('''CREATE INDEX debit_idx ON purchases(debit) ''')
        dbCur.execute('''CREATE INDEX credit_idx ON purchases(credit) ''')
    
    dbCur.executemany('INSERT INTO categories VALUES (?,?)', cat)
    dbCur.executemany('INSERT INTO subcategories VALUES (?,?,?)', subcat)
    dbCur.executemany('INSERT INTO matches (keyword, category_id, subcategory_id, always_show) VALUES (?,?,?,?)', matches)
#    dbCur.executemany('INSERT INTO folder_path VALUES (?)', [os.getcwd()])
    dbConn.commit();
    
    
    
    dbConn.close()

def createFolderStructure(basePath):
    global categories, subcategories, categTransMatch
    curPath = os.path.join(basePath, appFolder, expFolder, bankStateFolder, statementSetupFolder)
    if not os.path.exists(curPath):
        os.makedirs(curPath)
        os.chdir(curPath)
        createCsv('banks.csv', ['bank prefix','Date','Check Number','Description','Debit','Credit'], [])
        createCsv('categories.csv', ['id','category'], categories)
        createCsv('subcategories.csv', ['sub_cat_id','cat_id','sub_cat'], subcategories)
        createCsv('category-transaction_matching.csv', ['keyword','category_id','subcategory_id', 'always_ask'],categTransMatch)
    
    curPath = os.path.join(basePath, appFolder, expFolder, dbFolder)
    if not os.path.exists(curPath):
        os.makedirs(curPath)
    
    os.chdir(curPath)
    if not os.path.exists(os.path.join(basePath, appFolder, expFolder, dbFolder, dbName)):
        setupDatabase(categories, subcategories, categTransMatch, False)