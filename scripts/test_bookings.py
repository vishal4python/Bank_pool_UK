from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime
from maks_lib import output_path
import time

start_time = time.time()

today = datetime.datetime.now()
path = output_path+"Bookings.com_global_hotels_count_"+str(today.strftime('%Y_%m_%d'))+'.csv'

table = []
table_columns = ["Country_Name","Hotel_Count"]

country_list = [["ad","0"],["ae","-25"],["af","-50"],["ag","-75"],["ai","-100"],["al","-125"],["am","-150"],
                ["ao","-200"],["as","-275"],["at","-300"],["au","-325"],["aw","-350"],
                ["az","-400"],["ba","-425"],["bb","-450"],["bd","-475"],["be","-500"],["bf","-525"],["bg","-550"],["bh","-575"],
                ["bi","-600"],["bj","-625"],["bl","-650"],["bm","-675"],["bn","-700"],["bo","-725"],["bq","-750"],["br","-775"],
                ["bs","-800"],["bt","-825"],["bw","-875"],["by","-900"],["bz","-925"],["ca","-950"],["cc","-975"],
                ["cd","-1e3"],["cg","-1050"],["ch","-1075"],["ci","-1100"],["ck","-1125"],["cl","-1150"],
                ["cm","-1175"],["cn","-1200"],["co","-1225"],["cr","-1250"],["cu","-1275"],["cv","-1300"],["cw","-1325"],
                ["cy","-1375"],["cz","-1400"],["de","-1425"],["dj","-1450"],["dk","-1475"],["dm","-1500"],
                ["do","-1525"],["dz","-1550"],["ec","-1575"],["ee","-1600"],["eg","-1625"],["er","-1675"],
                ["es","-1700"],["et","-1725"],["fi","-1750"],["fj","-1775"],["fk","-1800"],["fm","-1825"],["fo","-1850"],
                ["fr","-1875"],["ga","-1900"],["gb","-1925"],["gd","-1950"],["ge","-1975"],["gf","-2e3"],                   #["gg","-2025"],
                ["gh","-2050"],["gi","-2075"],["gl","-2100"],["gm","-2125"],["gn","-2150"],["gp","-2175"],["gq","-2200"],
                ["gr","-2225"],["gt","-2275"],["gu","-2300"],["gw","-2325"],["gy","-2350"],["hk","-2375"],
                ["hn","-2425"],["hr","-2450"],["ht","-2475"],["hu","-2500"],["id","-2525"],["ie","-2550"],
                ["il","-2575"],["in","-2625"],["iq","-2675"],["is","-2725"],              #,["im","-2600"]
                ["it","-2750"],["jm","-2800"],["jo","-2825"],["jp","-2850"],["ke","-2875"],["kg","-2900"],
                ["kh","-2925"],["ki","-2950"],["km","-2975"],["kn","-3e3"],["kw","-3075"],
                ["ky","-3100"],["kz","-3125"],["la","-3150"],["lb","-3175"],["lc","-3200"],["li","-3225"],["lk","-3250"],
                ["lr","-3275"],["ls","-3300"],["lt","-3325"],["lu","-3350"],["lv","-3375"],["ly","-3400"],["ma","-3425"],
                ["mc","-3450"],["md","-3475"],["me","-3500"],["mf","-3525"],["mg","-3550"],["mh","-3575"],["mk","-3600"],
                ["ml","-3625"],["mm","-3650"],["mn","-3675"],["mo","-3700"],["mp","-3725"],["mq","-3750"],["mr","-3775"],
                ["ms","-3800"],["mt","-3825"],["mu","-3850"],["mv","-3875"],["mw","-3900"],["mx","-3925"],["my","-3950"],
                ["mz","-3975"],["na","-4e3"],["nc","-4025"],["ne","-4050"],["nf","-4075"],["ng","-4100"],["ni","-4125"],
                ["nl","-4150"],["no","-4175"],["np","-4200"],["nr","-4225"],["nu","-4250"],["nz","-4275"],["om","-4300"],
                ["pa","-4325"],["pe","-4350"],["pf","-4375"],["pg","-4400"],["ph","-4425"],["pk","-4450"],["pl","-4475"],
                ["pm","-4500"],["pr","-4550"],["ps","-4575"],["pt","-4600"],["pw","-4625"],["py","-4650"],
                ["qa","-4675"],["re","-4700"],["ro","-4725"],["rs","-4750"],["ru","-4775"],["rw","-4800"],["sa","-4825"],
                ["sb","-4850"],["sc","-4875"],["se","-4925"],["sg","-4950"],["si","-5e3"],
                ["sk","-5050"],["sl","-5075"],["sm","-5100"],["sn","-5125"],["so","-5150"],["sr","-5175"],
                ["st","-5200"],["sv","-5225"],["sx","-5250"],["sy","-5275"],["sz","-5300"],["tc","-5325"],["td","-5350"],
                ["tg","-5400"],["th","-5425"],["tj","-5450"],["tl","-5500"],["tm","-5525"],
                ["tn","-5550"],["to","-5575"],["tr","-5600"],["tt","-5625"],["tw","-5675"],["tz","-5700"],
                ["ua","-5725"],["ug","-5750"],["us","-5800"],["uy","-5825"],["uz","-5850"],
                ["vc","-5900"],["ve","-5925"],["vg","-5950"],["vi","-5975"],["vn","-6e3"],["vu","-6025"],
                ["ws","-6075"],["xk","-6100"],["yt","-6150"],["za","-6175"],["zm","-6200"],["zw","-6225"]]
ExcelData = []
for list in country_list:
    dummyDict = dict()
    try:
        print(list)
        print('https://www.booking.com/country/'+str(list[0])+'.html?aid=304142;label=gen173nr;sid=800230ed2783544d6a079c7508f3a574;inac=0&')

        response = requests.get('https://www.booking.com/country/'+str(list[0])+'.html?aid=304142;label=gen173nr;sid=800230ed2783544d6a079c7508f3a574;inac=0&')
        print(response)
        jsoup = BeautifulSoup(response.content, "lxml")
        CountryName = jsoup.find('h1')
        CountryName = CountryName.text.strip() if CountryName is not  None else None
        hotels = jsoup.find('h2', text=re.compile('([0-9,\.]*)'))
        # print(hotels.text.strip())
        # print(re.search('[0-9]+', hotels.text.strip()))
        hotels = re.search('[0-9,\.]+', hotels.text.replace('\n','')).group(0).strip() if hotels is not None else None
        print(CountryName, hotels)
        dummyDict['CountryName'] = CountryName
        dummyDict['Properties'] = hotels

        tab = jsoup.find('ul', attrs={'class':'ia_tab'})
        if tab is not None:
            number = 0
            for id, li in enumerate(tab.find_all('li')):
                if 'accommodations' in  li.text.lower():
                    number = id
                    break
            Accomidation = jsoup.find_all('li', attrs={'class':'ia_section'})
            if len(Accomidation)>=2:
                ul = Accomidation[number].find('ul')

                for li in ul.find_all('li'):
                    data = re.search('([0-9,\.]+)( .*)',li.text)
                    print(data.group(1), data.group(2))
                    dummyDict[data.group(2)] = data.group(1)
            ExcelData.append(dummyDict)
        # break
    except Exception as e:
        print(e)




print(ExcelData)

df = pd.DataFrame(ExcelData)
df['Date'] = today.strftime('%m-%d-%Y')

print(type(df.columns.values.tolist()))
order = df.columns.values.tolist()
orderDict = {0:'Date',
             1:'CountryName',
             2:'Properties'}
for k in orderDict.values():
    if k in order:
        order.remove(k)
for k in orderDict.items():
    order.insert(k[0],k[1])
df = df[order]
df.to_csv(path,index=False)
print(df)
#
#
print('End Time:', (time.time()-start_time)/60, 'min')