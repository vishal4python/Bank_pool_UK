import time
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd
import re

import warnings
warnings.simplefilter(action='ignore')

from selenium.webdriver.common.keys import Keys


startTime = time.time()

# url = browser.get('https://www.enterprise.co.uk/en/reserve.html#book')
time.sleep(5)

airport = [["Hartsfield–Jackson Atlanta International Airport","Atlanta, Georgia","ATL"],["Chicago O'Hare International Airport","Chicago, Illinois","ORD"],["Los Angeles International Airport","Los Angeles, California","LAX"],["Dallas/Fort Worth International Airport","Dallas–Fort Worth Metroplex, Texas","DFW"],["John F. Kennedy International Airport","New York, New York","JFK"],["Denver International Airport","Denver, Colorado","DEN"],["San Francisco International Airport","San Francisco, California","SFO"],["McCarran International Airport","Las Vegas, Nevada","LAS"],["Charlotte Douglas International Airport","Charlotte, North Carolina","CLT"],["Miami International Airport","Miami, Florida","MIA"],["Phoenix Sky Harbor International Airport","Phoenix, Arizona","PHX"],["George Bush Intercontinental Airport","Houston, Texas","IAH"],["Seattle–Tacoma International Airport","SeaTac, Washington","SEA"],["Orlando International Airport","Orlando, Florida","MCO"],["Newark Liberty International Airport","Newark, New Jersey","EWR"],["Minneapolis–Saint Paul International Airport","Minneapolis–Saint Paul, Minnesota","MSP"],["Logan International Airport","Boston, Massachusetts","BOS"],["Detroit Metropolitan Airport","Romulus, Michigan","DTW"],["Philadelphia International Airport","Philadelphia, Pennsylvania","PHL"],["LaGuardia Airport","New York, New York","LGA"],["Fort Lauderdale–Hollywood International Airport","Fort Lauderdale, Florida","FLL"],["Baltimore–Washington International Airport","Linthicum, Maryland","BWI"],["Ronald Reagan Washington National Airport","Arlington, Virginia","DCA"],["Chicago Midway International Airport","Chicago, Illinois","MDW"],["Salt Lake City International Airport","Salt Lake City, Utah","SLC"],["Washington Dulles International Airport","Dulles, Virginia","IAD"],["San Diego International Airport","San Diego, California","SAN"],["Daniel K. Inouye International Airport","Honolulu, Hawaii","HNL"],["Tampa International Airport","Tampa, Florida","TPA"],["Portland International Airport","Portland, Oregon","PDX"]]
for i in airport[:1]:
    for k in [[15, 17], [15, 22]]:
        print(i[2])


        start_date = (datetime.now() + timedelta(days=k[0])).strftime('%m/%d/%Y')
        end_date = (datetime.now() + timedelta(days=k[1])).strftime('%m/%d/%Y')
        print(start_date, end_date)
        pickup_year = (datetime.now() + timedelta(days=k[0])).strftime('%B %Y')
        return_year = (datetime.now() + timedelta(days=k[1])).strftime('%B %Y')
        pickup_month = (datetime.now() + timedelta(days=k[0])).strftime('%m')
        return_month = (datetime.now() + timedelta(days=k[1])).strftime('%m')
        pickup_date = (datetime.now() + timedelta(days=k[0])).strftime('%d')
        return_date = (datetime.now() + timedelta(days=k[1])).strftime('%d')
        print('https://www.hertz.com/rentacar/reservation/')
        browser = webdriver.Firefox()
        browser.maximize_window()
        browser.get('https://www.hertz.com/rentacar/rental-car-deals/asia-aunz-onefreeday?icid_source=enUS&icid_medium=hero_banner_4&icid_campaign=aunz_onefreeday')
        time.sleep(5)
        try:
            browser.find_element_by_class_name('acsCloseButton acsAbandonButton ').click()
        except:
            pass
        # time.sleep(5)
        browser.find_element_by_xpath('//*[@id="pickup-location"]').send_keys(i[2])
        time.sleep(5)
        browser.find_element_by_xpath('//*[@id="pickup-location"]').send_keys(Keys.RETURN)
        time.sleep(5)
        browser.find_element_by_xpath('/html/body').click()


        #PICKUP DATE




        browser.find_element_by_xpath('//*[@id="pickup-date-box"]/div[2]/div').click()
        time.sleep(2)
        print(browser.find_element_by_xpath("//div[@class='calendar']/div[1]//h1[@data-automation-id='"+str(int(pickup_month))+"']").text)
        print(pickup_year)
        try:

            print("print try")
            time.sleep(2)

            browser.find_element_by_xpath("//div[@class='calendar']/div[1]//tbody//td[contains(text(), '1')]").click()
        except Exception as e:
            # pickup_year in browser.find_element_by_xpath("//div[@class='calendar']/div[2]//h1[@data-automation-id='"+str(int(pickup_month))+"']").text:
            print("print else")
            time.sleep(2)
            browser.find_element_by_xpath("//div[@class='calendar']/div[2]//tbody//td[contains(text(), '1')]").click()

        # elif pickup_year in browser.find_element_by_xpath("//div[@class='calendar']/div[1]//h1[@data-automation-id='"+str(int(pickup_month))+"']").text:
        #     time.sleep(2)
        #     browser.find_element_by_xpath("//div[@class='calendar']/div[1]//tbody//td[contains(text(), '"+str(int(pickup_date))+"')]").click()
        #
        # else:
        #     browser.find_element_by_xpath("//div[@class='calendar']/div[2]//tbody//td[contains(text(), '"+str(int(pickup_date))+"')]").click()

        time.sleep(3)



        # browser.find_element_by_xpath("//div[@class='calendar']/div[1]//tbody//td[contains(text(), '"+pickup_date+"')]").click()
        # time.sleep(3)
        # print('-------------------------------------------------------------------------------------------------------------------------------------------------')




        #RETURN DATE


        browser.find_element_by_xpath('//*[@id="dropoff-date-box"]/div[2]/div').click()
        time.sleep(2)
        print(return_year)
        try:

            browser.find_element_by_xpath("//div[@class='calendar']/div[1]//tbody//td[contains(text(), '"+str(int(return_date))+"')]").click()

        except Exception as e: # return_year in browser.find_element_by_xpath("//div[@class='calendar']/div[2]//h1[@data-automation-id='"+str(int(return_month))+"']").text:
            browser.find_element_by_xpath("//div[@class='calendar']/div[2]//tbody//td[contains(text(), '"+str(int(return_date))+"')]").click()

        # browser.find_element_by_xpath("//div[@class='calendar']/div[1]//tbody//td[contains(text(), '"+return_date+"')]").click()
        # element = browser.find_element_by_class_name('pagination-r')
        # browser.execute_script("arguments[0].click();", element)

        time.sleep(5)


        #TIME
        browser.find_element_by_css_selector('#pickup-time > select > option:nth-child(25)').click()
        browser.find_element_by_css_selector('#dropoff-time > select > option:nth-child(25)').click()
        #AGE
        browser.find_element_by_css_selector('#ageSelector > option:nth-child(8)').click()
        #PROMOCODE
        browser.find_element_by_css_selector('#discounts').click()
        try:
            browser.find_element_by_css_selector('#pc > label:nth-child(1) > input:nth-child(2)').clear()   ##ok-btn
        except:
            pass

        # browser.find_element_by_css_selector('.special-offers').click()
        time.sleep(5)
        browser.find_element_by_css_selector('#res-submit-btns > div > div > div:nth-child(2) > button').click()
        time.sleep(10)
        try:
            browser.find_element_by_css_selector('#ok-btn').click()
        except:
            pass
        time.sleep(3)

        # print(browser.page_source)
        print(browser.current_url)


        # jsoup = BeautifulSoup(browser.page_source)
        # div = jsoup.find('div', attrs={'id':'vehicles-list'})
        # for divs in div.find_all('div', attrs={'class':'vehicle'}):
        #     car_class = divs.find('div',attrs={'class':'vehicle-header clearfix'}).find('span')
        #     print(car_class.text)
        #     car_name = divs.find('h1').text
        #     print(car_name)
        #     xpath = divs.find('div',attrs={'class':'price-wrapper'}) if divs is not None else None
        #     rates = xpath.find('button',attrs={'class':'secondary priced'}) if xpath is not None else None
             #//*[@id="vehicles-list"]/div[19]/article/div[1]/div[2]/div/div[1]/div/div/div/button
        time.sleep(5)
        # for car in browser.find_elements_by_class_name('vehicle'):
        #     print(car)
        #     xpath = car.find_element_by_xpath('//*[@id="vehicles-list"]/div[3]/article/div[1]/div[2]/div/div[1]/div/div/div/button').click()
        #     time.sleep(3)
        #     print(browser.page_source)
        #     browser.back()
        #     time.sleep(3)
        # cars = browser.find_elements_by_class_name('vehicle')
        # car_len = len(cars)
        #
        # for i in range(car_len):
        #     try:
        #         cars[i].find_element_by_xpath("//*[@id='vehicles-list']/div["+str(i+3)+"]/article/div[1]/div[2]/div/div[1]/div/div/div/button").click()
        #         time.sleep(4)
        #         print(browser.page_source)
        #         browser.back()
        #         time.sleep(4)
        #         cars = browser.find_elements_by_class_name('vehicle')
        #
        #     except Exception as e:
        #         print(e)

        browser.close()
        # except Exception as e:
        #     print(e)
