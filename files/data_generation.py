import csv
from random import randint, sample, randrange
import random

''' This is  Part 1 of the exercise to create test data for Stock position aggregation
This py module reads a csv file containing Symbol, Fund, Sector, Price...etc
and creates different  Fund position files containing acct,symbol, qty
Account and Quantities are randomly generated inside the code. But Symbol and Fund are also randomly
picked from the loaded csv file
Input: Symbol,Fund,Price...
Output Fund1.csv (acct,symbol,qty)  Fund2.csv....
This module uses all key data structures and some key concepts like List and Dictionary Comprehension
'''

# # 1.0 Generate '0' padded client accounts in a given range excluding any given list of accounts:

# # We just  decided that our Account codes are  4 char fixed length and we want to generate 1000 Acct. codes
# # We also just designate some accounts as special  and don't want to be one of client accounts
exclude_accts = [0, 99, 999]
# # Auto Generate 1000 accounts 0..999 with 0 prepended i.e 0000...9999  and exclude some Accounts
# # Below code is a List Comprehension to generate list items
# # List Comprehension has [code_block_for_the_generated-item, generator/loop, predicate_to_control_gen_values]
acctList = [('0' * (4 - len(str(x)))) + str(x) for x in range(1000) if (x not in exclude_accts)]
#print(acctList)
# # You can do any predicate expression e.g create acct range in 10s: if (x%10 == 0)

# # 2.0 Read the Security file. Read only Symbol and FunType column for this project
# # Setup input data dir
dataDir = "C:/dev/python/data/"  # Unix path style (with forward slash) will work in windows too
secFile = dataDir + "Security.csv"
# print(secFile)

# # 2.1 Read the Symbol:Fund column  data using csv Module, we need only these columns

# secFundReader = csv.DictReader(open(secFile, 'r'), delimiter=',', fieldnames=["Fund", "Sector"])
secFundReader = csv.DictReader(open(secFile, 'r'), delimiter=',')
next(secFundReader)  # Skip the header row

# # 2.3 Create a Symbol:FundType dict / map from reader rows using Dictionary Comprehension (like List Comprehension)
# # Also, reader itself is a List of Dictionaries
secFundMap = {row["Symbol"]: row["Sector"] for row in secFundReader}  # For dictionary we need two col. key/val
# print(secFundMap)

# # 2.4 Create Symbol and Fund as separate lists  for iteration use
secList = list(secFundMap.keys())
# print(secList)
fundList = list(secFundMap.values())
# print(fundList)


# # 3.0 Create a Dictionary of Funds containing List of positions. Each position as tuples
# # Data Structure:  All Position = {Fund1:[(acct1,symol1,qty1), (acct2,symol2,qty2),...], Fund2:[(acct1,symol1,qty1)..}
# # Data Logic is:  Fund =  File, Positions = rows which are List of items, each row is a tuple = columns
# # Randomly generate 10K positions picking random acct/symbol/qty and add this item to corresponding fund of the symbol
# # Note: This might add dupe rows like same acct/sec. We can treat this as another Security Buy on another date,
# #   Or  we can also add the qty to existing position (via lookup / not done here) and create a net position

allFundPositions = {fund: [] for fund in fundList}  # Generate the empty fund list to add random positions (Dict Comp.)
for _ in range(20):  # Just loop 10K times we don't need look count,  '_' defines ignore!
    act = random.choice(acctList)
    symbol = random.choice(secList)
    qty = randrange(1000, 10000, 100)  # Select random qty between 1K-10K but select only 100 qty lot as in real trading
    fund = secFundMap[symbol]
    newPosition = (act, symbol, qty) # Could be dupe acct/sec but OK
    currPosition = allFundPositions[fund]
    currPosition.append(newPosition)

print(allFundPositions)
# # TBD: We'll implement the logic to convert/write  allFundPositions to  different files

# #
# #
# # -------- Below are Alternate way of coding some logic mentioned above-------------
# # Alt Form: acctList = [('0' * (4 - len(str(x)))) + str(x) for x in range(100) if (x != 0 and x != 9)]

# #
# # ALt Form:  Another explicit way (w/o dict comprehension) to create dictionary from csv file
# secFundReader = csv.DictReader(open(secFile, 'r'), delimiter=',', fieldnames=["Symbol", "Fund"])
# next(secFundReader)
# secFundMap = {} # Empty dict
# for row in secFundReader:
#     secFundMap[row["Symbol"]] = row["Fund"]
# print(secFundMap)
#
# # Alt Form: We can also just read a single column of any field from csv file as a list using list comprehension
#     --But for our use we needed a map matching each Symbol and corresponding Fund as above
#     --Below is  yet another way of creating dict from csv file
# secList = [x[0] for x in csv.reader(open(secFile, 'r'), delimiter=',')] # x[0] is first col/symbol
# fundList = [x[3] for x in csv.reader(open(secFile, 'r'), delimiter=',')]
# Since we know secList and FunList matches in each row, we can use  zip command to fuse a dictionary
# secFundMap = dict(zip(secList, fundList))
# del secFundMap['Symbol']  # get rid of the header
# print(secFundMap)