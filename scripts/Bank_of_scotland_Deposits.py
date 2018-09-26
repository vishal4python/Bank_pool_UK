import requests as req
from bs4 import BeautifulSoup as bs
import datetime
import pandas as pd
import warnings
from tabulate import tabulate
import time
from maks_lib import output_path
import re

print('Program Exection Started...')
starttime = time.time()

warnings.simplefilter(action='ignore')
now = datetime.datetime.now()
data_table = []

#Required Fields to scrap the data.
column = ["Bank_Product_Name","Interest","AER","Term in Months","Interest_Type","Bank_Product_Type", "Balance"]

headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}

#------------------------------------Savings Account----------------------------------------------
res = req.get("https://www.bankofscotland.co.uk/savings/", headers=headers)
jsoup = bs(res.content)
table = jsoup.find("table", attrs={"title":"Savings Table"})
trs = table.find_all("tr")

pro_type = jsoup.find("div", attrs={"id":"savings-accounts"})
product_type = pro_type.find_all("div", attrs={"class":"inner-tile"})
products = []
for i in product_type:
    if "Term Savings" in i.text:
        term="Term Deposits"
    elif "savings" in i.text.lower():
        term = "Savings"
    else:
        term = i.text
    products.append(term)
products.append("Savings")
products = sorted(products)

count = 0
for tr in trs:
    try:
        tds = tr.find_all("td")
        tax = tds[1].text.replace("\n",' ')
        t = tax.count("AER")
        if t>1:
            tax = tax.split("AER")[0]+"AER"

        tax_ = re.findall('(\d.*gross/AER|\d.*free/AER)',tax)
        gross = None
        aer = None
        if len(tax_)>=1:
            gross = re.sub('[^0-9.% ]', '', tax_[0])
            aer = gross
        else:
            gross = re.findall("\d.*gross",tax)

            if len(gross)>=1:
                gross = re.sub('[^0-9.%]','',gross[0])
            aer = re.findall(" \d.*AER",tax)
            if len(aer)>=1:
                aer = re.sub('[^0-9.%]','',aer[0])
        a = ["Young", "Help", "Junior"]
        found = False
        for i in a:
            if i in tds[0].text:
                found= True
                break
        year = tds[1].text.replace("\n", ' ')
        year = re.findall('(\d\d? .*year|\d\d? .*months)',year)

        if len(year)>=1:
            if "month" in year[0].lower():
                year = int(re.sub('[^0-9]','',year[0]))
            else:
                year = int(re.sub('[^0-9]', '', year[0]))*12
        else:
            year = None
        if not found:
            print('tds[3]==', tds[0])

            if ('Monthly Saver') and ('Children') not in tds[0].text :
                data_table.append([tds[0].text,gross, aer, year, tds[3].text,products[count],None])
                count = count+1

    except Exception as e:
        print(e)




#----------------------------------------CURRENT-------------------------------------------------------
try:

    res = req.get("https://www.bankofscotland.co.uk/bankaccounts/classic/", headers=headers)

    jsoup = bs(res.content)

    product_type = jsoup.find("div",attrs={"class": "sp-pat-103-column-copy-responsive s01-uv-default independent"}).find('h1').text

    product_name = product_type

    data = jsoup.find("ul", attrs={"class": "tick-list-green"}).find_all('li')[0].text

    AER = re.findall("\d\.?.?.?%", data)

    Balance = re.findall("£\d.*\. V", data)[0]
    Balance = re.sub("[^0-9-,.]", '', Balance).strip('.')
    t = [product_name, AER[1], AER[0], None, "Variable", "Current", Balance]
    data_table.append(t)
except Exception as e:
    print(e)

print(tabulate(data_table))
#------------------------------------Moving Data to CSV File using Pandas----------------------------------------------

# Arrange the Order of all fields.
columns= ["Date","Bank_Native_Country","State","Bank_Name","Bank_Local_Currency","Bank_Type","Bank_Product","Bank_Product_Type","Bank_Product_Name","Balance","Bank_Offer_Feature","Term in Months","Interest_Type","Interest","AER","Bank_Product_Code"]
df = pd.DataFrame(data_table,columns=column)
df["Date"] = now.strftime("%m-%d-%Y")
df["Bank_Native_Country"] = "UK"
df["State"] = "London"
df["Bank_Name"] = "Bank of Scotland"
df["Bank_Local_Currency"] = "GBP"
df["Bank_Type"] = "Bank"
df["Bank_Product"] = "Deposits"
df["Bank_Offer_Feature"] = "Offline"
df["Bank_Product_Code"] = None
df = df[columns]
df.to_csv(output_path + "Consolidate_Bank_of_Scotland_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)  #Location of a file to store the data

print('time=',(time.time()-starttime)) #Displaying total execution time.