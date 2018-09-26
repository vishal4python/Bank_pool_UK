import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import datetime
import time
start_time = time.time()
today = datetime.datetime.now()
from maks_lib import output_path
path = output_path+'Consolidate_SantanderBank_Data_Deposit_'+today.strftime('%m_%d_%Y')+'.csv'
Excel_data = []
table_headers = ['Bank_Product_Type', 'Bank_Product_name', 'Balance', 'Bank_Offer_Feature', 'Term in Months', 'Interest_Type', 'Interest', 'AER']
response = requests.get('https://www.santander.co.uk/uk/savings/compare-our-range').content
table = BeautifulSoup(response,'html.parser').find('table', attrs={'class':'fck_table table1 hv'})
if table is not None:
    for tr in table.find('tbody').find_all('tr'):
        product_name = tr.find('th').text
        if any(i for i in ['customers', 'junior', 'help'] if i in product_name.lower() ):
            continue
        tds = tr.find_all('td')
        interest_text = tds[1].text
        interest = re.findall('[0-9.]*%',interest_text)
        Balance = re.findall('£[0-9\.,]*', interest_text)
        offer = tds[3].text
        Product_Term = re.search('[0-9]* Year', product_name, re.IGNORECASE)
        Product_Term = int(re.search('[0-9]*', Product_Term.group(0)).group(0))*12 if Product_Term is not None else None
        Interest_Type = 'Fixed' if 'fixed' in product_name.lower() else 'Variable'
        # print(interest_text)
        if len(interest)==2:
            if len(Balance)==2:
                if int(re.sub('[^0-9.]', '', Balance[0])) > int(re.sub('[^0-9.]', '', Balance[1])):
                # a = [product_name, interest[i], bal, 'Online' if 'online' in offer.lower() else 'Offline']
                    a = ['Savings', product_name, str(re.sub('[^0-9.]', '', Balance[0]))+'+','Online' if 'online' in offer.lower() else 'Offline', Product_Term, Interest_Type,interest[0], interest[0]]
                    Excel_data.append(a)
                    a = ['Savings', product_name, str(re.sub('[^0-9.]', '', Balance[1])) +'-'+ str(int(re.sub('[^0-9.]', '', Balance[0]))-1), 'Online' if 'online' in offer.lower() else 'Offline',Product_Term, Interest_Type, interest[1], interest[1]]
                    Excel_data.append(a)
        else:
            # b = [product_name, interest[0] if len(interest[0])!=0 else '0.0%', Balance[0] if len(Balance)!=0 else None,'Online' if 'online' in offer.lower() else 'Offline']
            b = ['Savings', product_name, re.sub('[^0-9.]', '', Balance[0]) if len(Balance)!=0 else None, 'Online' if 'online' in offer.lower() else 'Offline', Product_Term,Interest_Type, interest[0] if len(interest[0])!=0 else '0.0%', interest[0] if len(interest[0])!=0 else '0.0%']
            Excel_data.append(b)
            print('-'.center(100,'-'))
        # break


# print(tabulate(Excel_data))





##################           1|2|3 CURRENT ACCOUNT      ##################################
try:
    response = requests.get('https://www.santander.co.uk/uk/current-accounts/123-current-account').content
    jsoup = BeautifulSoup(response,'html.parser')
    product_name = jsoup.find('div',attrs={'class':'top02'}).text
    print(product_name)
    data = jsoup.find('div',attrs={'class':'itab00'}).find('div').find_all('ul')[0].find_all('li')[1]
    balance = re.findall('£[0-9\,]*',data.text)
    print(balance[0])
    interest = re.findall('[0-9\.]*%',data.text)[1]
    print(interest)
    aer = re.findall('[0-9\.]*%',data.text)[0]
    print(aer)
    Excel_data.append(['Current', product_name, re.sub('[^0-9.]', '', balance[0]) if len(balance)!=0 else None, 'Offline', None, 'Variable', interest, aer])
except Exception as e:
    print(e)




# #####################           CURRENT ACCOUNT    #####################################
try:
    response = requests.get('https://www.santander.co.uk/uk/select/products/select-current-account').content
    jsoup = BeautifulSoup(response,'html.parser')
    product_name = jsoup.find('div',attrs={'class':'top02'}).text
    print(product_name)
    data = jsoup.find('div',attrs={'class':'itab00'}).find('div').find_all('ul')[1].find_all('li')[0]
    # print(data)
    balance = re.findall('£[0-9\,]*',data.text)
    interest = re.findall('[0-9\.]*%',data.text)[1]
    aer = re.findall('[0-9\.]*%',data.text)[0]
    Excel_data.append(['Current', product_name, re.sub('[^0-9.]', '', balance[0]) if len(balance) != 0 else None, 'Offline', None, 'Variable', interest,aer])
except Exception as e:
    print(e)

df = pd.DataFrame(Excel_data, columns=table_headers)
df['Date'] =  ' '+today.strftime("%m-%d-%Y")
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
df['Bank_Name'] = 'Santander Bank'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Deposits'
df['Bank_Product_Code'] = None

order = ["Date","Bank_Native_Country","State","Bank_Name","Bank_Local_Currency","Bank_Type","Bank_Product","Bank_Product_Type","Bank_Product_name","Balance","Bank_Offer_Feature","Term in Months","Interest_Type","Interest","AER","Bank_Product_Code"]
df = df[order]
df.to_csv(path, index=False)
print(tabulate(Excel_data))
