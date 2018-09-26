import csv
import pandas as pd
import numpy as np
from tabulate import tabulate


def csvValidator(inputFilePath, outputFilePath, jsonValidation):
    f = open(inputFilePath, 'r')
    reader = csv.reader(f)
    headers = next(reader)
    column = {}
    for h in headers:
        column[h] = []
    for row in reader:
        for h, v in zip(headers, row):
            column[h].append(v)
    validation = jsonValidation
    row_name = validation.get('row_name', None)
    table_headers = ['Error Location', 'Error Type', 'Row Number', 'Value', 'Column Name',row_name if row_name is not None else '']
    errorData = []
    errorData.append(table_headers)

    if row_name is not None:
        row_name = column[row_name]
    for validationKey in validation.keys():
        keyFound = column.get(validationKey, None)
        if keyFound is not None:
            obj = validation[validationKey]
            for j, i in enumerate(column[validationKey]):
                _strip = obj.get('strip', None)
                if _strip is not None:
                    if i is not None:
                        for st in _strip:
                            i = i.strip(st)

                skip = obj.get('skip', None)
                if skip is not None:
                    skipFound = False
                    for sk in skip:
                        if i is not None:
                            if len(i) == len(sk):
                                skipFound = True
                                break
                        if i == sk:
                            skipFound = True
                            break
                    if skipFound:
                        continue

                _type = obj.get('type', None)
                if _type is not None:
                    if _type == 'float':
                        try:
                            if '.' in str(i):
                                float(i)
                            else:
                                errorData.append(['typeFieldError', 'Type Not Found', j + 2, i, validationKey, row_name[j+2] if row_name is not None else None])
                                continue

                        except:
                            errorData.append(['typeFieldError', 'Type Not Found', j+2,i, validationKey,row_name[j+2] if row_name is not None else None])
                            continue
                    elif _type == 'int':
                        try:
                            if '.' not in str(i):
                                int(i)
                            else:
                                errorData.append(['typeFieldError', 'Type Not Found', j + 2, i, validationKey,row_name[j+2] if row_name is not None else None])
                                continue
                        except:
                            errorData.append(['typeFieldError', 'Type Not Found', j + 2, i, validationKey,row_name[j+2] if row_name is not None else None])
                            continue
                    elif _type == 'string':
                        try:
                            str(i)
                        except:
                            errorData.append(['typeFieldError', 'Type Not Found', j + 2, i, validationKey,row_name[j+2] if row_name is not None else None])
                            continue
                    elif _type == 'date':
                        try:
                            if i is not None:
                                if str(i).count('-')!=2:
                                    errorData.append(['typeFieldError', 'Type Not Found', j + 2, i, validationKey,row_name[j+2] if row_name is not None else None])
                                    continue
                        except:
                            errorData.append(['typeFieldError', 'Type Not Found', j + 2, i, validationKey,row_name[j+2] if row_name is not None else None])
                            continue
                _allowed = obj.get('allowed',None)

                if _allowed is not None:
                    if len(_allowed)!=0:
                        _allowed = [str(allow) for allow in _allowed]
                        if str(i) not in _allowed:
                            errorData.append(['allowedFieldError', 'Value Not found', j+2,i, validationKey,row_name[j+2] if row_name is not None else None])
                            continue

                _required = obj.get('required', None)
                if _required is not None:
                    if i is None:
                        errorData.append(['requireFieldError', 'Filed Not Found', j+2, i, validationKey,row_name[j+2] if row_name is not None else None])
                        continue
                    elif len(str(i))==0:
                        errorData.append(['requireFieldError', 'Filed Not Found', j + 2, i, validationKey,row_name[j+2] if row_name is not None else None])
                        continue
                    elif np.nan == i:
                        errorData.append(['requireFieldError', 'Filed Not Found', j + 2, i, validationKey,row_name[j+2] if row_name is not None else None])
                        continue

        elif validationKey =='compare':

            compare = column[validation['compare']['compare']]
            compare_with = column[validation['compare']['compare_with']]
            for id ,comp in enumerate(zip(compare,compare_with)):
                c1, c2 = comp
                if c1 is not None and c2 is not None:
                    if len(c1) !=0 and len(c2)!=0:
                        try:
                            c = [k.strip('%') for k in [c1,c2]]
                            c = [float(k.strip('%')) for k in c]
                            cmpValue = abs(c[0] - c[1])
                            difference = validation['compare'].get('difference', None)
                            if difference is not None:
                                if float(difference) < cmpValue:
                                        print(cmpValue)
                                        errorData.append(['Comparison Error', 'More Than Expected Value', id + 2, c, validation['compare']['compare_with'], row_name[id+2] if row_name is not None else None])
                        except Exception as e:
                            errorData.append(['Comparison Error', 'Not Possible to compare the give Two values', id + 2, c,validation['compare']['compare_with'], row_name[id+2] if row_name is not None else None])
            print(compare)
            print(compare_with)
        elif validationKey == 'match':
            name = column[validation['match']['name']]
            Ticker = column[validation['match']['ticker']]
            match_list = validation['match'].get('match_list', None)
            if match_list is not None:
                for id, comp in enumerate(zip(name, Ticker)):
                    if list(comp) not in match_list:
                        print(list(comp))
                        errorData.append(['Expectation Error', 'Expected data not Found', id + 2, list(comp),[validation['match']['name'],validation['match']['ticker']],row_name[id + 2] if row_name is not None else None])
            else:
                print('Match list data not found.')
        else:
            print(validationKey,'Not Found. Please Check column Name.')
    print(tabulate(errorData))
    df = pd.DataFrame(errorData[1:], columns=table_headers)
    df.to_csv(outputFilePath, index=False)


if __name__ == '__main__':
    validation = {
        'row_name':'Bank_Name',
        'Date':{
            'type': 'date',
            'required': True
        },
        'Bank_Native_Country':{
            'type':'string',
            'allowed':['US'],
            'required':True
        },
        'State':{
            'type':'string',
            'allowed':['New York'],
            'required':True
        },
        'Bank_Name':{
            'type':'string',
            'allowed':['ALLY', 'BANK OF AMERICA CORP', 'CAPITAL ONE', 'CITIGROUP INC', 'JP MORGAN CHASE & Co.', 'PNC FINANCIAL SERVICES GROUP INC',
                       'SUNTRUST BANKS INC', 'SYNCHRONY', 'WELLS FARGO'],
            'required':True
        },
        'Ticker':{
            'type':'string',
            'allowed':['ALLY', 'BAC', 'C', 'COF', 'JPM', 'PNC', 'STI', 'SYF', 'WFC'],
            'required':True
        },
        'Bank_Local_Currency':{
            'type':'string',
            'allowed':['USD'],
            'required':True
        },
        'Bank_Type':{
            'type':'string',
            'allowed':['Bank'],
            'required':True
        },
        'Bank_Product': {
            'type': 'string',
            'allowed': ['Deposits'],
            'required': True
        },
        'Bank_Product_Type': {
            'type': 'string',
            'allowed': ['Checking', 'CD', 'Savings'],
            'required': True
        },
        'Bank_Product_Code': {
            'type': 'string',
            'required': True
        },
        'Bank_Product_Name': {
            'type': 'string',
            'required': True
        },
        'Minm_Balance':{
            'type':'int',
            'skip':['']
        },
        'Maxm_Balance': {
            'type': 'int',
            'skip': ['']
        },
        'Bank_Offer_Feature':{
            'type':'string',
            'allowed':['Offline', 'Online'],
            'required':True
        },
        'Term_in_Months':{
            'type':'int',
            'allowed':[6,12,36],
            'skip':['']
        },
        'Interest_Type':{
            'type':'string',
            'allowed':['Variable', 'Fixed'],
            'required':True
        },
        'Interest':{
            'type':'float',
            'skip':[''],
            'strip':['%'],
        },
        'APY': {
            'type': 'float',
            'skip': [''],
            'strip': ['%'],
        },
        'compare': {
            'compare': 'APY',
            'compare_with': 'Interest',
            'difference': '0.01'
        },
        'match': {
            'name': 'Bank_Name',
            'ticker': 'Ticker',
            'match_list': [['ALLY', 'ALLY'], ['BANK OF AMERICA CORP', 'BAC'],['CAPITAL ONE', 'COF'],
                           ['CITIGROUP INC', 'C'], ['JP MORGAN CHASE & Co.', 'JPM'], ['PNC FINANCIAL SERVICES GROUP INC', 'PNC'],
                           ['SUNTRUST BANKS INC', 'STI'], ['SYNCHRONY', 'SYF'], ['WELLS FARGO', 'WFC']]
        },
        'match': {
            'name': 'Bank_Product_Type',
            'ticker': 'Bank_Product_Code',
            'match_list': [['Savings', '_MSBF'], ['Checking', '_MCCF'], ['CD', '6MCDF'],
                           ['CD', '12MCDF'],['CD', '36MCDF']
                                  ]}
         }
    path = 'C:\\Users\\vishal\\PycharmProjects\\pool_UK-master\\data\\output\\UK\\UK_FINAL_Deposits_Data_2018_05_11.csv'
    output = 'C:\\Users\\vishal\\PycharmProjects\\pool_UK-master\\data\\output\\UK\\error.csv'
    csvValidator(path, output, validation)
# Interest: Ally, Synchory and SunTrust if available check it, else ignore the errors
#Interest: for aggregator websites if available check it, else ignore the errors (except us.deposits.org)

# Compare the bank name and Ticker
# compare and publish if Interest and APY difference is more than 1%