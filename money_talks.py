import setupMoney, os, sys, sqlite3, csv
from optparse import OptionParser

__author__ = "Tannerism"
__date__ = "$Jun 27, 2015 7:45:55 PM$"



parser = OptionParser()
parser.add_option("-s", "--setup", dest="setupPath", help="Setup the folder structure for the Money_Talks application", metavar="SETUP")

options, args = parser.parse_args()

# if the setup flag was passed it will create the necessary folder structure
if options.setupPath != None:
    print "Setting up 'Money Talks' folder structure . . ."
    setupMoney.createFolderStructure(options.setupPath)
    print "Complete: Folder structure created in " + os.path.join(options.setupPath, setupMoney.appFolder)
else:
    print "Now lets do some stuff"