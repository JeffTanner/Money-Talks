import setupMoney, os, sys, sqlite3, csv
from optparse import OptionParser
from os import listdir
from os.path import isfile, join

__author__ = "Tannerism"
__date__ = "$Jun 27, 2015 7:45:55 PM$"

dbConn = ""
dbCur = ""


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

def processBankStatement(data, schema):
    global dbConn, dbCur
    entries = []
    for entry in data:
        curEntry = []
        
        # Setup the date of the current transaction
        datePieces = entry[(int(schema[1])-1)].split('/');
        curEntry.append(datePieces[2]) # Adding the year
        curEntry.append(datePieces[0]) # Adding the month
        curEntry.append(datePieces[1]) # Adding the day
        
        # Add the check number
        curEntry.append(entry[(int(schema[2])-1)])
        
        # Add the description
        curEntry.append(entry[(int(schema[3])-1)])
        
        # Add the debit
        curEntry.append(entry[(int(schema[4])-1)])
        
        # Add the credit
        curEntry.append(entry[(int(schema[5])-1)])
        
        # Add the curEntry to the entries list
        entries.append(curEntry)
        
        #TODO:: CATEGORIZE THE TRANSACTIONS
        
        for row in dbCur.execute("SELECT count(*) FROM purchases WHERE year=? AND month=? AND day=? AND check_num=? AND description=? AND debit=? AND credit=?", curEntry):
            print row[0]
            if row[0] == 0:
                dbCur.execute("INSERT INTO purchases (year, month, day, check_num, description, debit, credit) VALUES (" + curEntry[0] + ", " + curEntry[1] + ", " + curEntry[2] + ", " + curEntry[3] + ", \"" + curEntry[4] + "\", " + curEntry[5] + ", " + curEntry[6] +")")
                dbConn.commit()
                
#        dbConn.commit()
#        print dbCur.rowcount
#    dbCur.executemany("INSERT INTO purchases VALUES (year, month, day, description, debit, credit)", entries)
#    dbConn.commit()

def setupDatabase():
    global dbConn, dbCur
    categories = readInCsv('categories.csv')
    subcategories = readInCsv('subcategories.csv')
    matches = readInCsv('category-transaction_matching.csv')
    os.chdir('../../.db')
    setupMoney.setupDatabase(categories, subcategories, matches)
    dbConn = sqlite3.connect('transactions.db')
    dbCur = dbConn.cursor()

parser = OptionParser()
parser.add_option("-s", "--setup", dest="setupPath", help="Setup the folder structure for the Money_Talks application", metavar="SETUP")

options, args = parser.parse_args()

# if the setup flag was passed it will create the necessary folder structure
if options.setupPath != None:
    print "Setting up 'Money Talks' folder structure . . ."
    setupMoney.createFolderStructure(options.setupPath)
    print "Complete: Folder structure created in " + os.path.join(options.setupPath, setupMoney.appFolder)
else:
    print "Updating based on user settings . . . "
    
    # Read in the various tables and replace the tables in the database with them
    os.chdir("C:/Users/Tannerism/Documents/Money_Talks/Expenses/Bank_Statements/setup")
    setupDatabase()
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