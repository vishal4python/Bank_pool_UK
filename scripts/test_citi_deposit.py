#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from tabulate import tabulate
import numpy as np
import datetime
from maks_lib import output_path

today = datetime.datetime.now()
path = output_path+"Consolidate_Citi_Data_Deposits_"+str(today.strftime('%Y_%m_%d'))+'.csv'
# path = "Consolidate_Citi_Data_Deposits_"+str(today.strftime('%Y_%m_%d'))+'.csv'

resp = requests.get("https://personal.natwest.com/personal/savings/compare-savings-accounts-new.html#ISAdesktop", verify = False)
