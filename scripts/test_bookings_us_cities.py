from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime
from maks_lib import output_path
import time

start_time = time.time()

today = datetime.datetime.now()
path = output_path+"Bookings.com_us_states_"+str(today.strftime('%Y_%m_%d'))+'.csv'

table = []
table_columns = ["Country_Name","Hotel_Count"]
ExcelData = []
mainUrl = 'https://www.booking.com/discover/country/us.html?aid=304142;label=gen173nr;sid=800230ed2783544d6a079c7508f3a574'
response = requests.get(mainUrl)
print(response)
jsoup = BeautifulSoup(response.content, "lxml")
uls = jsoup.find('ul', attrs={'class':'dcsp-section-items'})
# print(uls)
for url in uls.find_all('h4', attrs={'class': 'dcsp-section-item__header'}):
    dummyDict = dict()
    try:
        subUrl = mainUrl[mainUrl.index('?'):]
        print('https://www.booking.com'+url.find('a')['href']+subUrl)

        response = requests.get('https://www.booking.com'+url.find('a')['href']+subUrl)
        print(response)
        jsoup = BeautifulSoup(response.content, "lxml")
        CountryName = jsoup.find('h1',attrs={'data-ats':re.compile('.*')})

        CountryName = CountryName.text.strip() if CountryName is not None else None
        hotels = jsoup.find('h2', text=re.compile('([0-9,\.]*)'))
        # print(hotels.text.strip())
        # print(re.search('[0-9]+', hotels.text.strip()))
        hotels = re.search('[0-9,\.]+', hotels.text.replace('\n', '')).group(0).strip() if hotels is not None else None
        print(CountryName, hotels)
        dummyDict['CountryName'] = CountryName
        dummyDict['Properties'] = hotels

        tab = jsoup.find('ul', attrs={'class': 'ia_tab'})
        if tab is not None:
            number = 0
            for id, li in enumerate(tab.find_all('li')):
                if 'accommodations' in li.text.lower():
                    number = id
                    break
            Accomidation = jsoup.find_all('li', attrs={'class': 'ia_section'})
            if len(Accomidation) >= 2:
                ul = Accomidation[number].find('ul')

                for li in ul.find_all('li'):
                    data = re.search('([0-9,\.]+)( .*)', li.text)
                    print(data.group(1), data.group(2))
                    dummyDict[data.group(2)] = data.group(1)
            ExcelData.append(dummyDict)
    except Exception as e:
     print(e)
print(ExcelData)

df = pd.DataFrame(ExcelData)
df['Date'] = today.strftime('%m-%d-%Y')

df.to_csv(path,index=False)
print(df)

print('End Time:', (time.time()-start_time)/60, 'min')