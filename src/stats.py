# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Tannerism"
__date__ = "$Aug 9, 2015 9:03:45 AM$"

if __name__ == "__main__":
    print "Hello World"

aggregate = {}

def calculateTotals(pur, curTotals):
#     GENERATE OVERALL STATISTICS
    try:
        curTotals['total']['debit'] += abs(pur['debit'])
    except:
        curTotals['total']['debit'] += 0
    try:
        curTotals['total']['credit'] += abs(pur['credit'])
    except:
        curTotals['total']['credit'] += 0
    
#    GENERATE ANNUAL STATISTICS
    try:
        curTotals['byYear'][pur['year']]
    except:
        curTotals['byYear'][pur['year']] = {'total':{'debit':0, 'credit':0}, 'byMonth':{}}
    try:
        curTotals['byYear'][pur['year']]['total']['credit'] +=  abs(pur['credit'])
    except:
        curTotals['byYear'][pur['year']]['total']['credit'] = 0
    try:
        curTotals['byYear'][pur['year']]['total']['debit'] += abs(pur['debit'])
    except:
        curTotals['byYear'][pur['year']]['total']['debit'] =0
        
#   GENERATE MONTHLY STATISTICS
    try:
        curTotals['byYear'][pur['year']]['byMonth'][pur['month']]
    except:
        curTotals['byYear'][pur['year']]['byMonth'][pur['month']] = {'debit':0, 'credit':0}
    try:
        curTotals['byYear'][pur['year']]['byMonth'][pur['month']]['credit'] += abs(pur['credit'])
    except:
        curTotals['byYear'][pur['year']]['byMonth'][pur['month']]['credit'] =0
    try:
        curTotals['byYear'][pur['year']]['byMonth'][pur['month']]['debit'] += abs(pur['debit'])
    except:
        curTotals['byYear'][pur['year']]['byMonth'][pur['month']]['debit'] =0
    return curTotals

def aggregateByAttr(pur, attr):
    global aggregate
#    base = {'debit':0, 'credit':0}
#    baseYear = {'total':{'debit':0, 'credit':0}, 'byMonth':{}}
    curTotals = {'total':{'debit':0, 'credit':0}, 
    'byYear':{}}#{'total': base, 'byMonth':{}}}
    try:
        aggregate[attr]
    except:
        aggregate[attr] = {}
    try:
        curTotals = aggregate[attr][pur[attr]]
    except:
        aggregate[attr][pur[attr]] = {'total':{'debit':0, 'credit':0}, 
    'byYear':{}}
    curTotals = calculateTotals(pur, curTotals)
    aggregate[attr][pur[attr]] = curTotals

def aggregateByTime(pur):
    global aggregate
    curTotals = {'total':{'debit':0, 'credit':0}, 
    'byYear':{}}
    try:
        curTotals = aggregate['totalTransactions']
    except:
        aggregate['totalTransactions'] = {'total':{'debit':0, 'credit':0}, 'byYear':()}
    curTotals = calculateTotals(pur, curTotals)
    aggregate['totalTransactions'] = curTotals
    

def aggregateData(purchases):
    # aggregate by by:
    #   category - debit and credit overall, monthly and yearly
    #   match/store
    #   subcategory
    #   month/year
    global aggregate
    for pur in purchases:
        aggregateByAttr(pur,'category')
        aggregateByAttr(pur,'subcategory')
        aggregateByAttr(pur,'match')
        aggregateByTime(pur)
#    print aggregate
    return aggregate