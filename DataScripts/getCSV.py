import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import json as json
import csv

yearIndex = 4
finalData = []

def cleanData(file_data, index):
    cleanedData = []
    for i in range(0, len(file_data)):
        try:
            companyData = file_data[i]
            symbol = companyData["symbol"]
            updatedDict = {"symbol": symbol}
            data = companyData["annualReports"][index]
            updatedDict.update(data)
            # data["symbol"] = symbol
            cleanedData.append(updatedDict)
        except:
            print(f"error at line {i}")
    return cleanedData

def updateData(file_data):
    for i in range(0, len(file_data)):
        try:
            existingCompanyData = finalData[i]
            companyData = file_data[i]
            data = companyData["annualReports"][yearIndex]
            existingCompanyData.update(data)
        except:
            print(f"error at line {i}")

# read cashflow
file_name="cashflow.json"
with open(file_name, "r") as file:
    file_data = json.load(file)

finalData = cleanData(file_data, yearIndex)

# read balance sheet
file_name="balanceSheet.json"
with open(file_name, "r") as file:
    file_data = json.load(file)
updateData(file_data)


# read income statement
file_name="incomeStatement.json"
with open(file_name, "r") as file:
    file_data = json.load(file)

updateData(file_data)

# read income statement
file_name="overview.json"
with open(file_name, "r") as file:
    file_data = json.load(file)

updateData(file_data)

keys = finalData[0].keys()

a_file = open("2017.csv", "a")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(finalData)
a_file.close()
