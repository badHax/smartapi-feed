## WebSocket
import os
import sys
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

#web socket options
task="mw" #"mw"|"sfi"|"dp"
ss = WebSocket(feedToken, client_id)

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
            
        # Assign the callbacks.
        ss.on_ticks = on_tick
        ss.on_connect = on_connect
        ss.on_close = on_close
        
        print("*** starting live feed ***")
        ss.connect()
        
def on_tick(ws, tick):
    print("Ticks: {}".format(tick))
    if "ltt" in tick[0]:
        row = get_row_data(tick)
        sheetUtil = GoogleSheetsUtil()
        sheetUtil.add_row_range(row, SheetName.NIFTY)
        
def on_connect(ws, response):
    ws.websocket_connection() # Websocket connection 
    token = get_token_string(SheetName.NIFTY)
    ws.send_request(token,task) 
    
def on_close(ws, code, reason):
    ws.stop()

def get_row_data(tick):
    output = []
    for option in tick:
        row_data = []
        row_data.append(0)  #   open interest 
        row_data.append(0)  #   change in open interest
        row_data.append(0)  #   volume
        row_data.append(0)  #   implied volititlity
        row_data.append(0)  #   last trade price
        row_data.append(0)  #   change
        row_data.append(0)  #   bid quantity
        row_data.append(0)  #   bid price
        row_data.append(0)  #   bid price
        row_data.append(0)  #   ask price
        row_data.append(0)  #   strike price
        row_data.append(0)  #   bid quantity
        row_data.append(0)  #   bid price
        row_data.append(0)  #   ask price
        row_data.append(0)  #   ask quantity
        row_data.append(0)  #   last trade price put
        row_data.append(0)  #   implied volititlity put
        row_data.append(0)  #   volume put
        row_data.append(0)  #   change in oi put
        row_data.append(0)  #   oi put
        output.append(row_data)
    return output

def get_token_string(self, filename):
        output = ''
        with open(filename.name + ".txt", 'r') as nifty:
            for instrument in nifty:
                if len(output > 1):
                    output += '&'
                output += self.exchange_name + "|" + instrument['token']
        return output
        
if __name__ == "__main__":
    main()