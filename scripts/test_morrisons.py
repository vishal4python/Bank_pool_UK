from bs4 import BeautifulSoup
import requests
import re



##########################          category_1        #############################################

# response = requests.get('https://groceries.morrisons.com/webshop/getCategories.do?tags=').content
# print(response)
# jsoup = BeautifulSoup(response,'html.parser')
#
# href = jsoup.find('div', attrs={'class':'js-nav-entries'}).find('ul').find_all('li',attrs = {'class':re.compile('CATEGORY ')})
# for a in href:
#     href_1 = a.find('a')
#     # cat_1_name = href_1.find('span')
#     print(href_1['href'],       href_1.text )

####################################################################################################

import morrisons_href
morrisons_href.category_1_frozen
for href_2 in morrisons_href.category_1_frozen:

    response = requests.get('https://groceries.morrisons.com'+str(href_2[0])).content
    # print(response)
    print('----------------------------------------------------------------------------------------------------------'+str(href_2[1]))
    jsoup = BeautifulSoup(response, 'html.parser')
    try:

        href = jsoup.find('div', attrs={'class':'js-nav-entries'}).find('ul').find_all('li',attrs = {'class':re.compile('CATEGORY ')})
        for a in href:
            href_1 = a.find('a')
            # cat_1_name = href_1.find('span')
            print(href_1['href'],       href_1.text )
    except:
        pass


