'''
Created on 14-Mar-2018

@author: sairam
'''

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from tabulate import  tabulate
from datetime import datetime
from maks_lib import output_path
import time

print('Program Execution Started...')
starttime = time.time()

today = datetime.now()

#CSV File Location.
path = output_path+"Consolidate_ CoOp_Data_Mortgage"+today.strftime('%Y_%m_%d')+".csv"

table = []

#Required Fields To Scrap the data.
table_headers = ["Bank_Product_Name", "Min_Loan_Amount", "Term (Y)", "Interest_Type", "Interest", "APRC", "Mortgage_Loan_Amt", "Fixed_Rate_Term","Mortgage_Down_Payment"]

#Arranging the columns in given format.
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product",
         "Bank_Product_Type", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type",
         "Interest", "APRC", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason", "Mortgage_Pymt_Mode", "Fixed_Rate_Term",
         "Bank_Product_Code"]

table.append(table_headers)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}

#Getting PageSource Using requests module
resp = requests.get("https://www.co-operativebank.co.uk/mortgages/existing-customers-moving-rates", headers=headers)

#Getting Required Data Using BeautifulSoup.
jsoup = BeautifulSoup(resp.content, "html.parser")
divs = jsoup.find_all("div", attrs={"class": re.compile("c-rate-card js-rate-card js-rate-card-ret"), "identifier":re.compile("\d?yrfixopt")})

for div in divs:
    try:
        Bank_Product_Name = div.find("mark", attrs={"method-type":"MortgagesText"}).text
        Interest = div.find("mark", attrs={"data-crc-property": "Initial Rate Ret"}).text
        Interest_Type = div.find("a", attrs={"href": "#popup-initial-rate"}).text
        APRC = div.find("mark", attrs={"data-crc-property": "Initial APR Ret"}).text
        Mortgage_Down_Payment = div.find("mark", attrs={"data-crc-property": "Max Loan to Value"}).text
        Min_Loan_Amount = div.find("mark", attrs={"data-crc-property": "Minimum Loan Amount Ret"}).text
        term = re.findall("\d.*Year", Bank_Product_Name)
        if len(term)>=1:
            term = re.sub('[^0-9]','',term[0])
        else:
            term = None
        a = [Bank_Product_Name, Min_Loan_Amount, None, Interest_Type, Interest, APRC, None,term, str(100-int(re.sub('[^0-9.]','',Mortgage_Down_Payment)))+'%']
        table.append(a)
    except Exception as e:
        print(e)

lifes = jsoup.find_all("div", attrs={"class": re.compile("c-rate-card js-rate-card js-rate-card-ret"), "identifier":re.compile("lifetrkopt")})
for life in lifes:
    try:
        Bank_Product_Name = life.find("mark", attrs={"method-type":"MortgagesText"}).text
        Interest = life.find("mark", attrs={"data-crc-property":"Initial Rate Ret"}).text
        if "variable" in Interest:
            Interest_Type = "Variable"
        else:
            Interest_Type = "Fixed"
            APRC = life.find("mark", attrs={"data-crc-property":"Initial APR Ret"}).text

        Mortgage_Down_Payment = life.find("mark", attrs={"data-crc-property":"Max Loan to Value"}).text
        Min_Loan_Amount = life.find("mark", attrs={"data-crc-property":"Minimum Loan Amount Ret"}).text
        term = re.findall("\d.*Year", Bank_Product_Name)
        if len(term) >= 1:
            term = re.sub('[^0-9]', '', term[0])
        else:
            term = None
        a = [Bank_Product_Name, Min_Loan_Amount, None, Interest_Type, Interest, APRC, None,
             term, str(100-int(re.sub('[^0-9.]','',Mortgage_Down_Payment)))+'%']
        table.append(a)
    except:
        pass

print(tabulate(table))

#-----------------------------Moving Data To CSV File Using Pandas-----------------------------------
df = pd.DataFrame(table[1:], columns=table_headers)
df['Date'] = today.strftime('%m-%d-%Y')
df["Interest"] = df["Interest"].astype(str)+'%'
df["APRC"] = df["APRC"].astype(str)+'%'
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
df['Bank_Name'] = 'The Co-operative Bank'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Mortgages'
df['Bank_Product_Type'] = 'Mortgages'
df['Bank_Offer_Feature'] = "Offline"
df['Mortgage_Category'] = 'Existing Customers '
df['Mortgage_Reason'] = 'Primary Residence'
df['Mortgage_Pymt_Mode'] = 'Principal + Interest'
df['Bank_Product_Code'] = None
df = df[order]
df.to_csv(path,index=False) #Moving data to csv file

print('time=', (time.time() - starttime))
print('Execution Completed.')
