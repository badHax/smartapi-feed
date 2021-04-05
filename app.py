## WebSocket
import os
from smartapi import WebSocket 
FEED_TOKEN= os.environ[FEED_TOKEN]
CLIENT_CODE=os.environ[CLIENT_CODE]
token="nse_cm|2885&nse_cm|1594&nse_cm|11536"
task="mw" #"mw"|"sfi"|"dp"
ss = WebSocket(FEED_TOKEN, CLIENT_CODE)

def on_tick(ws, tick):
    print("Ticks: {}".format(tick))

def on_connect(ws, response):
    ws.websocket_connection() # Websocket connection  
    ws.send_request(token,task) 
    
def on_close(ws, code, reason):
    ws.stop()

# Assign the callbacks.
ss.on_ticks = on_tick
ss.on_connect = on_connect
ss.on_close = on_close

ss.connect( )
