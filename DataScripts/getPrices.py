import requests
import json
import csv
import datetime
from dateutil.relativedelta import relativedelta

rows = []

def dateFromString(dateString):
    dateList = dateString.split('-')
    year = int(dateList[0])
    month = int(dateList[1])
    day = int(dateList[2])
    date = datetime.datetime(year=year, month=month, day=day)
    return  date

def compareYearAndMonth(date1, date2):
    return date1.month == date2.month and date1.year == date2.year

file_name="prices.json"

priceDict = {}
priceMapping = {}

with open(file_name, "r") as file:
    priceData = json.load(file)
    availableDates = priceData[1]["Monthly Time Series"].keys()
    # map month to dates
    for x in availableDates:
        # we want to remove days from dates
        date = dateFromString(x)
        dateKey = f"{date.year}-{date.month}"
        priceMapping[dateKey] = x
    for i in range(0, len(priceData)):
        try:
            key = priceData[i]["Meta Data"]["2. Symbol"]
            prices = priceData[i]["Monthly Time Series"]
            priceDict[key] = prices
        except:
            print(f"could not get data for {i}")
    

headers = []
finalRows = []
fileName = "2017.csv"
with open(fileName, 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    headers = header
    # headers.append("currentPrice") # current price
    headers.append("priceAfterThreeMonths") # three month price
    count = 0
    for row in csvreader:

        symbol = row[0]
        dateString = row[1]

        # convert date string into date time object
        fiscalDateEnding = dateFromString(dateString)

        # 3 month date
        predictedDate = fiscalDateEnding + relativedelta(months=3)

        dateKey = f"{predictedDate.year}-{predictedDate.month}"
        mappedDateKey = priceMapping[dateKey]
        try:
            threeMonthPrice = priceDict[symbol][mappedDateKey]["4. close"]
            updatedRow = row
            updatedRow.append(threeMonthPrice)
            finalRows.append(updatedRow)
        except:
            print(f"date does not exist for stock {symbol}")
        count+=1
    file.close()


with open(fileName, 'w') as csvoutput:
    writer = csv.writer(csvoutput)
    writer.writerow(headers)
    writer.writerows(finalRows)
