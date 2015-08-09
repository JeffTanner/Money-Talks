import setupMoney, os, sys, sqlite3, csv, json, stats
from optparse import OptionParser
from os import listdir
from os.path import isfile, join

__author__ = "Tannerism"
__date__ = "$Jun 27, 2015 7:45:55 PM$"

dbConn = ""
dbCur = ""
allCategories = []
basePath = ""
# matchesLen stores the current length of the matches table, so when
# assigning the match_id to a new entry, it takes the matchesLen and adds 1
# which will be the id of the newly created entry in the matches table
matchesLen = 0

def readInCsv(csvFilePath):
    rows = []
    with open(csvFilePath, 'rb') as csvFile:
        reader = csv.reader(csvFile, delimiter=",")
        header = None
        rowLen = 0
        for row in reader:
            if header == None:
                header = row
                rowLen = len(header)
            else:
                while len(row) < rowLen:
                    row.append('')
                rows.append(row)
    return rows
    

def exportJson():
    matches = {}
    categories = {}
    subCategories = {}
    purchases = []
    jsonExp = {}
    
    for row in dbCur.execute("SELECT * FROM matches"):
        matches[row[0]] = row[1]
    
    for row in dbCur.execute("SELECT * FROM categories"):
        categories[row[0]] = row[1]
    
    for row in dbCur.execute("SELECT * FROM subcategories"):
        subCategories[row[0]] = row[2]
    
    for row in dbCur.execute("SELECT * FROM purchases"):
#        print row
        transObj = {}
        transObj['id'] = row[0]
        transObj['year'] = row[1]
        transObj['month'] = row[2]
        transObj['day'] = row[3]
        transObj['check_num'] = row[4]
        transObj['description'] = row[5]
        transObj['debit'] = row[6]
        transObj['credit'] = row[7]
        transObj['category'] = categories[row[8]]
        try:
            transObj['subcategory'] = subCategories[row[9]]
        except:
            transObj['subcategory'] = ''
        try:
            transObj['match'] = matches[row[10]]
        except:
            transObj['match'] = ''
        transObj['notes'] = row[11]
        purchases.append(transObj)

    jsonExp['transactions'] = purchases
    jsonExp['aggregates'] = stats.aggregateData(purchases)
    os.chdir(os.path.join(basePath, setupMoney.exportFolder))
    with open('money-talks.json', 'w') as jsonFile:
        json.dump(jsonExp, jsonFile)

def formatTransactionForPrint(trans):
    transStr = ""
    transStr = str(trans[1]) + "/" + str(trans[2]) + "/" + str(trans[0]) + "\t"
    transStr += ' '.join(trans[4].split())+ "\t"
    if trans[6] == '':
        transStr += trans[5]
    else: 
        if float(trans[5]) > 0:
            transStr += "-" + trans[5]
        else:
            transStr += trans[6]
    return transStr

def formatCategoryOptions():
    categStr = ""
    for i in range(len(allCategories)):
        categStr += "(" + str(i) + ") - "
        categStr += allCategories[i][(len(allCategories[i])-1)] + ";  "
    return categStr

def queryUserForCategory(trans, alwaysShow):
    isMatched = False
    inputStr = '\nPlease enter the number corresponding to the the category for this entry: '
    inputStr += "\n----------  TRANSACTION:  ----------\n"
    inputStr += formatTransactionForPrint(trans) 
    inputStr += "\n----------  CATEGORIES:  ----------\n"
    inputStr += formatCategoryOptions() 
    inputStr += "\n:"
    categId = ''
    try:
        categId = input(inputStr)
        if int(categId) < len(allCategories):
            isMatched = True
            if len(allCategories[categId]) == 2:
                trans[7] = allCategories[categId][0]
                trans[8] = ''
            else:
                trans[7] = allCategories[categId][1]
                trans[8] = allCategories[categId][0]
            if alwaysShow != 1:
                trans[9] = matchesLen
                desc = raw_input("Please enter the name to store for future categorizing:\nExample: \nFrom bank statement: MY STORE 0154 OMAHA\nName for future categorizing: MY STORE\nTo keep the bank statement description enter 0 \n:")
                if desc == 0:
                    desc = trans[4]
                setupMoney.updateCsv('setup/category-transaction_matching.csv', [[desc, trans[7], trans[8], 0]])
                dbCur.execute("INSERT INTO matches (keyword, category_id, subcategory_id, always_show) VALUES (?,?,?,?)", [desc, trans[7], trans[8], 0])# + curEntry[0] + ", " + curEntry[1] + ", " + curEntry[2] + ", " + curEntry[3] + ", \"" + curEntry[4] + "\", " + curEntry[5] + ", " + curEntry[6] +")")
                dbConn.commit()
            else:
                notes = raw_input("Please enter transaction details. \nExample: watch, shoes, and belt for Bobby\n:")
                trans[10] = notes
                    

    except Exception, e:
        print e
        isMatched = False
        print "::INVALID CATEGORY-ENTER THE NUMBER CORRESPONDING TO THE CATEGORY::" + str(categId)
    return {'trans': trans, 'isMatched':isMatched, 'alwaysShow': alwaysShow}

def categorizeTransaction(trans):
    isMatched = False
    alwaysShow = 0
    for match in dbCur.execute("SELECT * FROM matches"):
        if trans[4].lower().find(match[1].lower()) > -1:
            trans[7] = match[2]
            trans[8] = match[3]
            trans[9] = match[0]
            alwaysShow = match[4]
            if alwaysShow == 1:
                isMatched = False
            else:
                isMatched = True
            break

    return {'trans':trans, 'isMatched': isMatched, 'alwaysShow':alwaysShow}

def processBankStatement(data, schema):
    global dbConn, dbCur
    entries = []
    
    for row in dbCur.execute('SELECT COALESCE(MAX(id)+1, 0) FROM matches'):
        matchesLen = row[0]
    for entry in data:
        curEntry = []
        selEntry = []
        
        # Setup the date of the current transaction
        datePieces = entry[(int(schema[1])-1)].split('/');
        curEntry.append(datePieces[2]) # Adding the year [0]
        curEntry.append(datePieces[0]) # Adding the month [1]
        curEntry.append(datePieces[1]) # Adding the day [2]
        
        # Add the check number [3]
        try:
            curEntry.append(entry[(int(schema[2])-1)])
        except:
            curEntry.append('')
        
        # Add the description [4]
        curEntry.append(entry[(int(schema[3])-1)])
        
        # Add the debit [5]
        curEntry.append(entry[(int(schema[4])-1)])
        
        # Add the credit [6]
        try:
            curEntry.append(entry[(int(schema[5])-1)])
        except:
            curEntry.append('')
        # create the object to be used in the SELECT statement
        for part in curEntry:
            selEntry.append(part)
        # Add default values for category [7] and subcategory [8] ids
        curEntry.append(-999)
        curEntry.append(-999)
        
        # Add defalut values for keyword_id [9]
        curEntry.append(-999)
        
        # Add defalut value for notes [10]
        curEntry.append('')
        
        # Add the curEntry to the entries list
        entries.append(curEntry)
        
        #TODO:: CATEGORIZE THE TRANSACTIONS
        for row in dbCur.execute("SELECT count(*) FROM purchases WHERE year=? AND month=? AND day=? AND check_num=? AND description=? AND debit=? AND credit=?", selEntry):
            if row[0] == 0:
                result = categorizeTransaction(curEntry)
                while result['isMatched'] == False:
                    result = queryUserForCategory(curEntry, result['alwaysShow'])
                curEntry = result['trans']
                dbCur.execute("INSERT INTO purchases (year, month, day, check_num, description, debit, credit, category_id, subcategory_id, match_id, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?)", curEntry)# + curEntry[0] + ", " + curEntry[1] + ", " + curEntry[2] + ", " + curEntry[3] + ", \"" + curEntry[4] + "\", " + curEntry[5] + ", " + curEntry[6] +")")
                dbConn.commit()
                
                
#        dbConn.commit()
#    dbCur.executemany("INSERT INTO purchases VALUES (year, month, day, description, debit, credit)", entries)
#    dbConn.commit()

def createAllCategoriesTable(categ, subcateg):
    global allCategories
    dontUse = {}
    for sub in subcateg:
        dontUse[sub[1]] = sub[2]
        allCategories.append(sub)
    for cat in categ:
        try:
            if dontUse[cat[0]] == None:
                allCategories.append(cat)
        except:
            allCategories.append(cat)

def setupDatabase(dontReset=True):
    global dbConn, dbCur
    categories = readInCsv('categories.csv')
    subcategories = readInCsv('subcategories.csv')
    createAllCategoriesTable(categories, subcategories)
    matches = readInCsv('category-transaction_matching.csv')
    os.chdir('../../' + setupMoney.dbFolder)
    if dontReset == False and os.path.exists(setupMoney.dbName):
        os.remove(setupMoney.dbName)
    setupMoney.setupDatabase(categories, subcategories, matches, dontReset)
    dbConn = sqlite3.connect(setupMoney.dbName)
    dbCur = dbConn.cursor()

parser = OptionParser()
parser.add_option("-r", "--reset", action="store_false", default=True, help="reset the database and recategorize based on the updated CSV files")
parser.add_option("-s", "--setup", dest="setupPath", help="Setup the folder structure for the Money_Talks application", metavar="SETUP")
parser.add_option("-e", "--export", action="store_true", default=False, help="Export the data (as .json) for use in an HTML product into the 'Export' folder", metavar="SETUP")

options, args = parser.parse_args()

# if the setup flag was passed it will create the necessary folder structure
if options.setupPath != None:
    print "Setting up 'Money Talks' folder structure . . ."
    setupMoney.createFolderStructure(options.setupPath)
    print "Complete: Folder structure created in " + os.path.join(options.setupPath, setupMoney.appFolder)
elif len(args) == 1:
    basePath = args[0];
    
    if options.export == True:
        os.chdir(os.path.join(basePath, setupMoney.expFolder, setupMoney.dbFolder))
        dbConn = sqlite3.connect(setupMoney.dbName)
        dbCur = dbConn.cursor()
        exportJson()
    else:
        os.chdir(os.path.join(basePath, setupMoney.expFolder, setupMoney.bankStateFolder, setupMoney.statementSetupFolder))
        print "Updating based on user settings . . . "
        # Read in the various tables and replace the tables in the database with them
        setupDatabase(options.reset)
        os.chdir('../Bank_Statements/setup')
        print "Reading in your bank statements . . . "
        # Read in the bank statement and start categorizing
        bankSchema = readInCsv('banks.csv')
        os.chdir('../')
        statements = [ f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(),f)) ]
        for indvStat in statements:
            for bank in bankSchema:
                if indvStat.lower().find(bank[0].lower()) > -1:
                    statementCont = readInCsv(indvStat)
                    # Now iterate through the statement and add it to the database
                    processBankStatement(statementCont, bank)

        # Prompt user if it doesn't know where to put something

        print "Money Talks is Complete"