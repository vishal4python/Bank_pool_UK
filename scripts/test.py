import requests
from bs4 import BeautifulSoup
pages = ['',1,2,3,4,5,6]
for page in pages:
    response = requests.get('http://www.tesoro.es/en/deuda-publica/subastas/resultados-subastas-anteriores?type=bonos_del_estado&page='+str(page)).content
    print(response)
    div = BeautifulSoup(response).find('div', attrs={'class':'item-list'})
    if div is not None:

        for li in div.find_all('li'):
            print(li.find('a')['href'])
            resp = requests.get('http://www.tesoro.es'+li.find('a')['href']).content
            h2 = BeautifulSoup(resp).find('h2', attrs={'class':'pane-title'})
            print(h2.text)
            table = BeautifulSoup(resp).find('table')
            print(table)