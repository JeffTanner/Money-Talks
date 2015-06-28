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

def setupDatabase():
    global dbConn, dbCur
#    dbConn = sqlite3.connect('transactions.db')
#    dbCur = dbConn.cursor()
    categories = readInCsv('categories.csv')
    subcategories = readInCsv('subcategories.csv')
    matches = readInCsv('category-transaction_matching.csv')
    os.chdir('../../.db')
    setupMoney.setupDatabase(categories, subcategories, matches)

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
    print bankSchema
    os.chdir('../')
    statements = [ f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(),f)) ]
    
    for indvStat in statements:
        for bank in bankSchema:
            if indvStat.lower().find(bank[0].lower()) > -1:
                print indvStat + " found " + bank[0]
                break
    print statements
    # Prompt user if it doesn't know where to put something