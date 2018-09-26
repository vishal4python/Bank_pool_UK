 # Library to be imported
import os, sys
import win32com.client
import time
from maks_lib import scripts
# Path and file name to be used for opening
path = scripts

# Change to our current directory where macro exists
os.chdir(path)

uk_banks = ["Bank of Ireland_Mortgage.xlsm"]

# Run us_banks
for uk_banks in uk_banks:
    time.sleep(5)
    if os.path.exists(uk_banks):
        xl=win32com.client.Dispatch("Excel.Application")
        xl.Workbooks.Open(path+str(uk_banks), ReadOnly=1)
    del xl
