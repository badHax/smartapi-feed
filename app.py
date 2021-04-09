## WebSocket
import os
import sys
import json
import _thread
from smartapi import WebSocket,SmartConnect
from optionsDownloader import IndexOptionsDownloader
from googleSheetsUtil import GoogleSheetsUtil, SheetName
from datetime import datetime


#credentials
api_key = os.environ["SMART_API_KEY"]
client_id = os.environ["SMART_API_CLIENT_ID"]
client_password = os.environ["SMART_API_CLIENT_PASSWORD"]

#create object of call
obj=SmartConnect(api_key=api_key)

#login api call
data = obj.generateSession(client_id,client_password)

#fetch the feedtoken
feedToken=obj.getfeedToken()

def main():
    if data['message'] != 'SUCCESS':
        print(data['message'])
        sys.exit()
    print("logged in to angelbroking successfully")
    
    #if today is a trading day (weekday)
    if(datetime.today().weekday() < 5):
        downloader = IndexOptionsDownloader(data)
        
        if(not downloader.is_valid_index_files()):
            downloader.download_nse_options()
        
        nifty_files = []
        bank_files = []
        for root, dirs, files in os.walk('.'):
            for filename in files:
                if filename.startswith(SheetName.NIFTY.name):
                    nifty_files.append(filename)
                if filename.startswith(SheetName.BANKNIFTY.name):
                    bank_files.append(filename)
        
        c1 = 0
        for filename in nifty_files:     
            _thread.start_new_thread(os.system,('python optionsSocket.py {0} {1} {2} {3}'.format(feedToken,client_id, filename, c1),))
            c1 += 1
        c2 = 0
        for filename in bank_files:
            _thread.start_new_thread(os.system,('python optionsSocket.py {0} {1} {2} {3}'.format(feedToken,client_id, filename, c2),))
            c2 += 1
            
        while 1:
            pass
        
if __name__ == "__main__":
    main()