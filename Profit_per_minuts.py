import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml

# Create an URL object
url = 'https://oldschool.runescape.wiki/w/RuneScape:Grand_Exchange_Market_Watch/Alchemy'
# Create object page
page = requests.get(url)

# parser-lxml = Change html to Python friendly format
# Obtain page's information
soup = BeautifulSoup(page.text, 'lxml')

# Obtain information from tag <table>
table1 = soup.find("table", class_="wikitable sortable sticky-header align-center-1 align-right-3 align-right-4 align-right-5 align-right-6 align-right-7 align-right-8 align-right-9 align-center-10 align-center-11")
table1


# Create table headers
headers = []
for i in table1.find_all("th"):
    title = i.text
    headers.append(title)
    
# Create 2D array
row = []
for j in table1.find_all("td"):
    title = j.text
    title = title.replace(",","")
    if title == "":
        title = j.get("data-sort-value")
        if title == "true":
            title = True
        elif title == "false":
            title = False
    row.append(title)   

arr =[[]]
col =[]
n = 1
for i,y in enumerate(row):
    if i in range(((n-1)*11),(11*n)):
        col.append(y)
    else:
        n +=1
        col =[]
        arr.append(col)

                
#Create DataFrame from 2D array
mydata = pd.DataFrame(arr,columns = headers)

#Drop column
mydata = mydata.drop("GE Price", axis = 1)
mydata = mydata.drop("Details", axis = 1)
mydata = mydata.drop("High Alch", axis = 1)
#mydata = mydata.drop("Profit", axis = 1)
#mydata = mydata.drop("Limit", axis = 1)
mydata = mydata.drop("Volume", axis = 1)
mydata = mydata.drop("Max profit", axis = 1)
mydata = mydata.drop("ROI%", axis = 1)


#drop invalid data
mydata=mydata.dropna()

#Data to int
mydata['Profit'] = mydata['Profit'].astype('int')
mydata['Limit'] = mydata['Limit'].astype('int')

#check if f2p or p2p
print('Are you Member? (y/n): ')
isSure = input().lower().strip() == 'n'

#Boolean input for p2p f2p
if isSure:
    mydata = mydata.loc[mydata["Members"] == False]

#Create number of alchs
print('How many minuts do you have?')
minuts = int(input())
sec = minuts * 60
Alchs = sec // 3

#calc money
coins = 0
count = 0
while Alchs > 0:
    if ( mydata.iloc[count]["Limit"] ) < Alchs:
        coins += mydata.iloc[count]["Profit"] * mydata.iloc[count]["Limit"]
        Alchs -= mydata.iloc[count]["Limit"]
        count += 1
    else:
        coins += Alchs * mydata.iloc[count]["Profit"]
        Alchs = 0
        
#To leva
'''
1 USD is 1.74 BGN
43.82 USD per 180M
'''

leva = 76.20

gold = leva / 180000000

print("Coins:")
print(coins)

print("BGN")
print(gold*coins)

print("mydata")
print(mydata)