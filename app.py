## WebSocket
import os
import sys
from smartapi import WebSocket,SmartConnect
from optionsDownloader import IndexOptionsDownloader
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
token="nse_cm|3045" #&nse_cm|1594&nse_cm|11536"
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

def on_connect(ws, response):
    ws.websocket_connection() # Websocket connection  
    ws.send_request(token,task) 
    
def on_close(ws, code, reason):
    ws.stop()

if __name__ == "__main__":
    main()