from selenium import webdriver
from tabulate import tabulate
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import datetime
from maks_lib import output_path

print('Program Execution Started.')
starttime = time.time()
today  = datetime.datetime.now()
Excel_Table = []

#Csv FIle Location
path = output_path+"Consolidate_clydesdale_Data_Mortgage_"+str(today.strftime('%Y_%m_%d'))+'.csv'

#Required Fields To Scrap the Data
table_headers = ["Bank_Product_Name", "Interest", "APRC","Mortgage_Down_Payment",'Mortgage_Loan_Amt']

#Selenium Browser
browser = webdriver.Firefox()
browser.maximize_window()
cases = [[90000, 18000], [270000, 54000], [450000, 90000]]

for case in cases:
    browser.get('https://secure.cbonline.co.uk/personal/mortgages/all-our-mortgages/')
    browser.find_element_by_xpath('//*[@id="ftb"]').click()
    browser.find_element_by_xpath('//*[@id="mgValue"]').send_keys(case[0])
    browser.find_element_by_xpath('//*[@id="mgAmount"]').send_keys(case[1])
    table = BeautifulSoup(browser.page_source).find('table',attrs={'id':'mortgage-calc-new'}).find('tbody')
    trs = table.find_all('tr')
    for td in trs:
        tds = td.find_all('td')
        product_name = tds[0].text
        mortgage_down_payment = re.search('[0-9]*',tds[1].text)
        interest = tds[2].text
        aprc = re.sub('[^0-9.%]', '', tds[5].text)
        if 'Let' not in product_name:
            if any([k for k in ['75'] if k in str(mortgage_down_payment.group(0))]):
                a = [product_name,interest,aprc,str(100-int(mortgage_down_payment.group(0)))+'%',case[0]-case[1]]
                Excel_Table.append(a)


browser.close()
print(tabulate(Excel_Table))

#-----------------------------Moving Data to Csv file using Pandas module-----------------------------------
#Arranging the columns in given format.
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product",
         "Bank_Product_Type", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)",
         "Interest_Type", "Interest", "APRC", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category",
         "Mortgage_Reason", "Mortgage_Pymt_Mode", "Fixed_Rate_Term", "Bank_Product_Code"]

df = pd.DataFrame(Excel_Table, columns=table_headers)
df["Date"] = today.strftime('%Y-%m-%d')
df['Term (Y)'] = '30'
df['Interest_Type'] = 'Variable'
df["Bank_Native_Country"] = "UK"
df["State"] = "London"
df["Bank_Name"] = "Clydesdale Bank"
df["Bank_Local_Currency"] = "GBP"
df["Bank_Type"] = "Bank"
df["Bank_Product"] = "Mortgages"
df["Bank_Product_Type"] = "Mortgages"
df["Bank_Offer_Feature"] = "Offline"
df['Min_Loan_Amount'] = None
df["Mortgage_Category"] = "New Purchase"
df["Mortgage_Reason"] = "Primary Residence"
df["Mortgage_Pymt_Mode"] = "Principal + Interest"
df["Bank_Product_Code"] = None
df["Fixed_Rate_Term"] = df["Bank_Product_Name"].apply(lambda x: re.search('[0-9]*',x).group(0) if x is not None else None )
df = df[order]
df2 = df.copy()
df2['Term (Y)'] = '25'
df3 = df.append(df2, ignore_index=True)
df4 = df3.copy()
df4['Term (Y)'] = '15'
df5 = df3.append(df4, ignore_index=True)
df6 = df5.copy()
df6['Term (Y)'] = '10'
df7 = df5.append(df6, ignore_index=True)
df7.to_csv(output_path + "Consolidate_clydesdale_Mortgage_v2_{}.csv".format(today.strftime("%m_%d_%Y")), index=False) #Moving Data to csv file.

print('time=', (time.time() - starttime))
print('Execution Completed.')






