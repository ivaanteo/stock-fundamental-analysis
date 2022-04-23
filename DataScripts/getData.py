import requests
import json
import csv
import time

# CHANGE THESE
pricesFile ="prices.json" 
cashflowFile = "cashflow.json"
balanceSheetFile = "balanceSheet.json"
incomeStatementFile = "incomeStatement.json"
overviewFile = "overview.json"

file_name = pricesFile


timeSeries = "TIME_SERIES_MONTHLY"
incomeStatement = "INCOME_STATEMENT"
cashfow = "CASH_FLOW"
balanceSheet = "BALANCE_SHEET"
overView = "OVERVIEW"

function = timeSeries

def get_data(ticker, count):
    url = f'https://www.alphavantage.co/query?function={function}&symbol={ticker}&apikey={count}'
    try:
        r = requests.get(url)
        data = r.json()
        save_to_json(data)
    except Exception as err:
        print("Failed to get data for: ", ticker)
        print("Error: ", err)

def save_to_json(data):
    with open(file_name, "r") as file:
        file_data = json.load(file)
    file_data.append(data)
    with open(file_name, "w") as file:
        json.dump(file_data, file)
        file.close()

with open('sp500.csv') as csv_file:
    start =148
    stop = 504
    csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_reader:
        if start < line_count <= stop:
            print("Index: ", line_count)
            print("Getting data for: ", row)
            get_data(row[0], line_count)
            line_count += 1
            print("Sleep for 12.1 seconds")
            time.sleep(12.1)
        elif line_count <= start:
            # increment until you get the correct line
            line_count+=1
        else:
            # exceeded, stop
            break
    print(f'Processed {line_count} lines.')

