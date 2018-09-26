# -*- coding:utf-8 -*-
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import warnings
import datetime
from tabulate import tabulate
warnings.simplefilter(action='ignore')
today = datetime.datetime.now()
startTime = time.time()
state = None
city = None
Address = [[' 3491 E Indigo St', 'Gilbert'], [' 42721 w anne ln', 'Maricopa'], [' 433 W SANTA GERTRUDIS CIR', 'San Tan Valley'],
           [' 7503 SW 97th Terrace Rd', 'Ocala'], [' 2326 Timbergrove Dr', 'Valrico'], [' 3955 SE 17th St', 'Ocala'],
           [' 9218 SE 120th Loop', 'Summerfield'], [' 4087 Southwest 46th Terrace', 'Ocala'], [' 10141 SE 69th Ave', 'Belleview'],
           [' 5105 39th Ave N', 'St. Petersburg'], [' 206 Longview Avenue', 'Celebration'], [' 2810 Stratford Pointe Dr', 'West Melbourne'],
           [' 4825 PASCO AVE', 'Titusville'], [' 3119 Lake Point Circle', 'Acworth'], [' 9200 Four Acre Ct.', 'Charlotte'],
           [' 2536 Covington Loop', 'Graham'], [' 3060 Grassy Meadows Ct', 'Lincolnton'], [' 25268 W Cranston Pl', 'Buckeye'],
           [' 10350 S 182nd Ave', 'Goodyear'], [' 25033 N 67th Dr', 'peoria'], [' 89 E Macaw Ct', 'Queen Creek'], [' 27132 N 83rd Gln', 'Peoria'],
           [' 3219 W Lynne Ln', 'Phoenix'], [' 1105 Bainbridge Ln', 'Forney'], [' 2608 Castle Creek Dr', 'Little Elm'],
           [' 305 Goldfield Ln', 'Fort Worth'], [' 1010 Bainbridge Ln', 'Forney'], [' 220 Citrus Dr', 'Fate'], [' 3252 Silent Creek Trl', 'Fort Worth'],
           [' 8361 Bowspirit Ln', 'Hurst'], [' 2232 Riverbirch Ln', 'Rockwall'], [' 3224 Shoreside Pkwy', 'Hurst']]

Address_not_found = []

browser = webdriver.Firefox()

browser.maximize_window()

property_data_headers = ['Property_address','Date','Event & Source','Price','Appreciation','State','City','Website']
property_data = []


count = 0

for i in Address:
    try:
        browser.get('https://www.redfin.com/')
        time.sleep(3)
        print(i[0])
        #Address
        browser.find_element_by_xpath('//*[@id="search-box-input"]').clear()
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="search-box-input"]').send_keys(i[0])
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="search-box-input"]').send_keys(Keys.RETURN)
        time.sleep(5)

        if 'Sign up below to be notified when we expand to your area'.lower() in browser.page_source.lower():

            try:
                browser.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div/div/div[1]/button').click()
                print('===========================')
            except:pass
            Address_not_found.append(i)

            data = [i[0], 'Not Available', 'Not Available', 'Not Available', 'Not Available', state, city, 'Redfin']

            property_data.append(data)
            continue


        try:

            class_name = browser.find_elements_by_xpath('//div[@data-rf-test-name="item-row-active"]')

            found = False
            for k in class_name:
                time.sleep(3)
                if i[1].lower() in k.text.lower():
                    k.click()

                    found = True
                    break

            if not found:
                browser.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div/div/div[1]/button').click()
                print('|||||||||||||||||||||||||')
                Address_not_found.append(i)
                data = [i[0], 'Not Available', 'Not Available', 'Not Available', 'Not Available', state, city, 'Redfin']

        except Exception as e:
            print(e)
        time.sleep(3)
        try:
            browser.find_element_by_css_selector('#property-history-transition-node > div > div > div > p > span > a').click()
            time.sleep(5)

        except:
            pass

        try:
            browser.find_element_by_css_selector('#propertyHistory-expandable-segment > div.sectionBottomLinkContainer > div > span').click()
            time.sleep(5)

        except:
            pass

        try:
            browser.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div/div/div[1]/button').click()
        except:
            pass


        #Getting address details via BeautifulSoup
        if 'map-container' in browser.page_source.lower():
            Address_not_found.append(i)
            data = [i[0],'Not Available','Not Available','Not Available','Not Available',state,city,'Redfin']
            print('Map container')
            property_data.append(data)
            # continue
        elif 'No Records Yet'.lower() in browser.page_source.lower():
            Address_not_found.append(i)
            print('--------------------------')
            try:
                browser.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div/div/div[1]/button').click()
            except:pass

            data = [i[0],'Not Available', 'Not Available', 'Not Available', 'Not Available', state,city,'Redfin']

            property_data.append(data)

        elif 'oops' in browser.page_source.lower() and 'basic-table-2'.lower() not in browser.page_source.lower():

            Address.append(i)
            count = count+1
            if count ==5:
                break
            Address_not_found.append(i)

            print('@@@@@@@@@@@@@@@@@@@@@@')
            try:
                browser.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div/div/div[1]/button').click()
                time.sleep(2)
                continue
            except:
                pass

        else:

            jsoup = BeautifulSoup(browser.page_source)

            city_details = jsoup.find('div',attrs={'class':'HomeInfo inline-block'})
            address = city_details.find('span',attrs={'class':'street-address'}) if city_details is not  None else None
            address = address.text if address is not None else None
            city_details = city_details.find('span',attrs={'class':'citystatezip'}) if city_details is not None else None
            city = city_details.find_all('span')[0] if city_details is not None else None
            city = re.search('[ A-Za-z]+',city.text) if city is not None else None
            city = city.group(0) if city is not None else None
            # print(city)
            state = city_details.find_all('span')[1] if city_details is not None else None
            # print(state.text)

            table = jsoup.find('table', attrs={'class':'basic-table-2'}).find('tbody')
            if 'basic-table-2' not in browser.page_source.lower():
                print('+++++++++++++')
                Address.append(i)
                count = count+1
                if count ==3:
                    data = [address, 'Not Available', 'Not Available', 'Not Available', 'Not Available', state,city,'Redfin']
                    break



            trs = table.find_all('tr')
            for tr in trs:
                date = tr.find_all('td')[0].text
                # print(date)
                event = tr.find_all('td')[1].text
                # print(event)
                price = tr.find_all('td')[2].text
                # print(price)
                appreciation = tr.find_all('td')[3].text
                # print(appreciation)
                data = [address,date,event,price,appreciation,state.text,city,'Redfin']
                property_data.append(data)


    except Exception as e:
        print(e)

browser.close()


print(tabulate(property_data))
df = pd.DataFrame(property_data,columns=property_data_headers)
print(df)
print(Address_not_found)
df.to_excel("test_Redfin_1"+str(today.strftime('%Y_%m_%d'))+'.xlsx',index=False)
print('Time = ', (time.time()-startTime)/60)