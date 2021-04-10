## WebSocket
import os
import sys
import json
import _thread
from smartapi import WebSocket,SmartConnect
from optionsDownloader import IndexOptionsDownloader
from googleSheetsUtil import GoogleSheetsUtil, SheetName
from datetime import datetime
from flask import Flask
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(10)
not_done = []

#credentials
api_key = os.environ["SMART_API_KEY"]
client_id = os.environ["SMART_API_CLIENT_ID"]
client_password = os.environ["SMART_API_CLIENT_PASSWORD"]

#create object of call
obj=SmartConnect(api_key=api_key,disable_ssl=True)

#login api call
data = obj.generateSession(client_id,client_password)

#fetch the feedtoken
feedToken=obj.getfeedToken()

app = Flask(__name__)

def download_files():
    downloader = IndexOptionsDownloader(data)
    if(not downloader.is_valid_index_files()):
        downloader.download_nse_options()    

@app.route('/status')
def status():
    return "Tasks: {0}".format(len(executor._threads))
    
@app.route('/refresh')
def refresh():
    global data
    download_files()
    data = obj.generateSession(client_id,client_password)
    if data['message'] != 'SUCCESS':
        print(data['message'])
        return data['message']
    print("logged in to angelbroking successfully")
    return "I'm refreshed!"
    
@app.route('/start')
def hello():
    try:
        #if today is a trading day (weekday)
        if(datetime.today().weekday() >= 5):
            download_files()
            
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
                print('python optionsSocket.py {0} {1} {2} {3}'.format(feedToken,client_id, filename, c1))
                not_done.append(executor.submit(os.system,'python optionsSocket.py {0} {1} {2} {3}'.format(feedToken,client_id, filename, c1)))
                c1 += 1
            c2 = 0
            for filename in bank_files:
                not_done.append(executor.submit(os.system,'python optionsSocket.py {0} {1} {2} {3}'.format(feedToken,client_id, filename, c2)))
                c2 += 1
                
            return "I'm alive!"
        else:
            return "Sorry I don't work on weekends"
    except Exception as ex:
        print(ex)
        return 'failed to start, try /refresh first'
        
@app.route('/stop')
def bye():
    for future in not_done:
        print(future.result)
        future.cancel()
    executor._threads.clear()
    return "I'm dead!"
    
if __name__ == "__main__":
    app.run(port = int(os.environ['PORT']))