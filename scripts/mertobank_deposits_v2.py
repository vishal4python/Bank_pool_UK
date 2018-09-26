#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import time
starttime = time.time()
from tabulate import tabulate
from maks_lib import output_path
Excel_table = []
to_day = datetime.datetime.now()
Path = output_path+'Consolidate_Metro_Data_Deposits_v2_'+str(to_day.strftime("%Y_%m_%d"))+'.csv'
table_headers = ["Bank_Product_Type", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term in Months", "Interest", "AER"]

#####################     ISA      ##########################################
url = ['https://www.metrobankonline.co.uk/savings/products/instant-access-savings/','https://www.metrobankonline.co.uk/savings/products/instant-access-cash-isa/']
for urls in url:
    response = requests.get(urls, verify=False).content
    jsoup = BeautifulSoup(response,'html.parser')
    product_name = jsoup.find('div').find('div', attrs={'class':'headerIntroBlock headerIntroBlock-text_black headerIntroBlock_heroStyle'}).find('h2')
    table = jsoup.find('table',attrs={'class':re.compile('stacktable singlerow')})
    tds = table.find('tbody').find_all('tr')[1].find_all('td')
    interest = str(re.sub('[^0-9\.%]',' ',tds[0].text))
    balance = str(re.sub('[^0-9]',' ',tds[1].text))
    aer = interest
    Excel_table.append(['Savings', product_name.text.strip(), balance, 'Offline', None,interest, aer])

#####################     FIXED RATE CASH ISA   ########################################
try:
    response = requests.get('https://www.metrobankonline.co.uk/savings/products/fixed-rate-cash-isa/', verify=False).content
    jsoup = BeautifulSoup(response,'html.parser')
    product_name = jsoup.find('div').find('div', attrs={'class':'headerIntroBlock headerIntroBlock-text_black headerIntroBlock_heroStyle'}).find('h2')
    table = jsoup.find_all('table',attrs={'class':' singlerow'})
    td = table[0].find('tbody').find_all('tr')[1].find_all('td')
    balance = str(re.sub('[^0-9]',' ',td[1].text))

    trs = table[1].find_all('tr')
    for k in zip(trs[0].find_all('th'),trs[1].find_all('td')):
        print(k)
        aer = str(re.sub('[^0-9\.%]', ' ', k[1].text))
        interest = aer
        Excel_table.append(['Savings', product_name.text.strip(), balance, 'Offline', int(re.sub('[^0-9\.%]','',k[0].text)) * 12, interest, aer])
except Exception as e:
    print(e)

##############################          FIXED TERM SAVINGS              ###############################
try:
    response = requests.get('https://www.metrobankonline.co.uk/savings/products/fixed-term-savings/', verify=False).content
    jsoup = BeautifulSoup(response, 'html.parser')
    product_name = jsoup.find('div').find('div', attrs={'class': 'headerIntroBlock headerIntroBlock-text_black headerIntroBlock_heroStyle'}).find('h2')
    # print(product_name.text)
    table = jsoup.find_all('table',attrs={'class':' singlerow'})
    td = table[0].find('tbody').find_all('tr')[1].find_all('td')
    balance = str(re.sub('[^0-9]',' ',td[1].find('span').text))
    trs = table[1].find_all('tr')
    months = []

    for k in zip(trs[0].find_all('th'),trs[1].find_all('td')):
        print(k)
        term_in_months = k[0].text
        if 'year' in term_in_months.lower():
            term_in_months = int(re.sub('[^0-9]','',term_in_months))*12
        else:
            term_in_months = int(re.sub('[^0-9]', '', term_in_months))

        aer = str(re.sub('[^0-9\.%]', ' ', k[1].text))
        interest = aer
        Excel_table.append(['Savings', product_name.text.strip(), balance, 'Offline', term_in_months, interest, aer])


except Exception as e:
    print(e)

try:
    response = requests.get('https://www.metrobankonline.co.uk/bank-accounts/products/current-account/', verify=False).content
    jsoup = BeautifulSoup(response, 'html.parser')
    product_name = jsoup.find('div').find('div', attrs={'class': 'headerIntroBlock headerIntroBlock-text_black headerIntroBlock_heroStyle'}).find('h2')
    table = jsoup.find('table', attrs={'class': ' singlerow'})
    td = table.find('tbody').find_all('tr')[1].find_all('td')

    if 'none' in td[0].text.lower():
        balance = '0'
    else:
        balance =  str(re.sub('[^0-9]',' ',td[0]))
    Excel_table.append(['Current', product_name.text.strip(), balance, 'Offline', None, None, None])


except Exception as e:
    print(e)

df = pd.DataFrame(Excel_table,columns=table_headers)
df['Date'] = to_day.strftime("%m-%d-%Y")
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
df['Bank_Name'] = 'Metro Bank'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Deposits'
df['Interest_Type'] = 'Variable'
df['Bank_Product_Code'] = None


order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term in Months", "Interest_Type", "Interest", "AER", "Bank_Product_Code"]
df = df[order]
df.to_csv(Path, index=False)
print(tabulate(Excel_table))
print('time=',(time.time()-starttime))