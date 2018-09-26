import requests
from  tabulate import tabulate
import pandas as pd
import time
starttime = time.time()
import datetime
from maks_lib import output_path
today = datetime.datetime.now()

path = output_path+'Consolidate_Metro_Data_Mortgage_v2_'+today.strftime('%m_%d_%Y')+'.csv'

Excel_Table = []
table_headers = ['Bank_Product_Name', 'Term (Y)', 'Interest', 'APRC', 'Mortgage_Loan_Amt','Fixed_Rate_Term']


cases = [[90000, 18000], [270000, 54000], [450000, 90000]]
terms = [10, 15, 25, 30]
for term in terms:
    for case in cases:
        response = requests.get('https://www.metrobankonline.co.uk/api/mortgage/MortgageAffordability?isNewProperty=true&interestRate=1&termInYears='+str(term)+'&deposit='+str(case[1])+'&totalCost='+str(case[0])+'&fundsReleaseFee=35&legalFee=165&dischargeFee=50', verify=False).json()
        print(response)

        for data in response['mortgageProducts']:
            if 80 == int(data['maxLtv']):
                fixed_rate_term = data['initialRateTerm']
                print(fixed_rate_term)
                product_name = str(data['initialRateTerm']) +str(' year ')+ data['type']
                print(product_name)
                interest = str(data['interestRate'])+'%'
                print(interest)
                aprc = str(data['overallCost'])+'%'
                print(aprc)
                term_in_years = term
                print(term_in_years)
                mortgage_loan_amount = case[0]-case[1]
                print(mortgage_loan_amount)
                print("---------------------------------------------------------")

                a= [product_name,term_in_years,interest,aprc,mortgage_loan_amount,fixed_rate_term]
                Excel_Table.append(a)

        print('#################################################################')
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

print(tabulate(Excel_Table))
df = pd.DataFrame(Excel_Table, columns=table_headers)
df['Date'] = ' '+today.strftime('%Y-%m-%d')
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
df['Bank_Name'] = 'Metro Bank'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Mortgages'
df['Bank_Product_Type'] = 'Mortgages'
df['Bank_Offer_Feature'] = 'Offline'
df['Mortgage_Down_Payment'] = '20%'
df['Mortgage_Category'] = 'New Purchase'
df['Mortgage_Reason'] = 'Primary Residence'
df['Mortgage_Pymt_Mode'] = 'Principal + Interest'
df['Bank_Product_Code'] = None
df['Min_Loan_Amount'] = None
df['Interest_Type'] = 'Variable'
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type", "Interest", "APRC", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason", "Mortgage_Pymt_Mode", "Fixed_Rate_Term", "Bank_Product_Code"]
df = df[order]
df.to_csv(path, index=False)
print('time=',(time.time()-starttime))
