#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import time
from tabulate import tabulate
from maks_lib import output_path

print('Program Execution Started...')
starttime = time.time()
Excel_table = []
to_day = datetime.datetime.now()
Path = output_path+'Consolidate_Clydesdale_Data_Deposits_v2_'+str(to_day.strftime("%Y_%m_%d"))+'.csv'

#Required Fileds to scrap the data.
table_headers = ["Bank_Product_Type", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term in Months", "Interest", "AER"]

# ###########             SIGNATURE SAVINGS ACCOUNT               ##################
response = requests.get('https://secure.cbonline.co.uk/personal/savings/everyday-instant-access-accounts/signature-savings-account/').content
jsoup = BeautifulSoup(response,'html.parser')
product_name = jsoup.find('table', attrs={'class':'policy-covered'}).find('thead').find('tr').find_all('th')[1].text
data = jsoup.find('thead').find('tr').find_all('th')[1].text
tbody = jsoup.find_all('tbody')[1]
for k in tbody.find_all('tr'):
    data = k.find_all('td')
    balance = data[0].text
    interest = data[1].text
    aer = interest
    Excel_table.append(['Savings',product_name,str(re.sub(r'[^\x00-\x7F]','',balance)),'Offline',None,interest+'%',aer+'%'])



##########             ISA               ##################
try:
    response = requests.get('https://secure.cbonline.co.uk/personal/savings/everyday-instant-access-accounts/instant-savings-account/').content
    jsoup = BeautifulSoup(response,'html.parser')
    table = jsoup.find('table', attrs={'class':'policy-covered'})
    product_name = table.find('thead').find('tr').find_all('th')[1].text
    for k in table.find('tbody').find_all('tr'):   #[0].find_all('td')[1].find('table',attrs={'class':'mb-10'}).find('tbody').find_all('tr').find_all('td')[0].text
        tds = k.find_all('td')
        trs = tds[1].find_all('tr')
        for tr in trs[1:]:
            _tds = tr.find_all('td')
            balance = _tds[0].text
            interest = _tds[1].text
            aer = _tds[2].text
            Excel_table.append(['Savings', product_name, str(re.sub(r'[^\x00-\x7F]','',balance.replace(' – ','-'))), 'Offline', None,interest+'%',aer+'%'])
except Exception as e:
    print(e)


##############################    TERM DEPOSIT     ######################################
try:
    response = requests.get('https://secure.cbonline.co.uk/personal/savings/fixed-term-and-notice-accounts/term-deposit/').content
    jsoup = BeautifulSoup(response, 'html.parser')
    table = jsoup.find('table', attrs={'class':'policy-covered'})
    table =table.find('table', attrs={'class':'mb-10'})
    for tr in table.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        product_name = tds[0].text
        balance = tds[1].text
        interest = tds[2].text
        aer = tds[3].text
        term = re.findall(r'\d+', product_name)[0]
        Excel_table.append(['Term Deposits', product_name, str(re.sub(r'[^\x00-\x7F]','',balance)), 'Offline', term,interest+'%',aer+'%'])

except Exception as e:
    print(e)


#################        CURRENT       ###############################
try:
    response = requests.get('https://secure.cbonline.co.uk/personal/current-accounts/interest-rates-and-charges/').content
    jsoup = BeautifulSoup(response,'html.parser')
    table = jsoup.find('table', attrs={'class':'mg-b-20'})
    for tr in table.find('tbody').find_all('tr')[:-1]:
        tds = tr.find_all('td')
        balance = tds[0].text
        interest = tds[1].text
        aer = tds[2].text
        Excel_table.append(['Current', "Current Account", str(re.sub(r'[^\x00-\x7F]','',balance)), 'Offline', None,interest+'%',aer+'%'])

except Exception as e:
    print(e)

print(tabulate(Excel_table))

#---------------------------------------Moving Data To CSV File-------------------------------------------------
df = pd.DataFrame(Excel_table,columns=table_headers)
df['Date'] = to_day.strftime("%m-%d-%Y")
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
df['Bank_Name'] = 'Clydesdale Bank'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Deposits'
df['Bank_Offer_Feature'] = 'Offline'
df['Interest_Type'] = 'Variable'
df['Bank_Product_Code'] = None

#Arranging all columns in given format.
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term in Months", "Interest_Type", "Interest", "AER", "Bank_Product_Code"]
df = df[order]
df.to_csv(Path, index=False) #Moving Data To CSV File

print('Execution Completed.')
print('time=',(time.time()-starttime)/60)








