## WebSocket
import os
from smartapi import WebSocket,SmartConnect

apiKey = os.environ["SMART_API_KEY"]
#create object of call
obj=SmartConnect(api_key=apiKey)

#login api call

data = obj.generateSession(os.environ["SMART_API_CLIENT_ID"]),os.environ["SMART_API_CLIENT_PASSWORD"]))
#refreshToken= data['data']['refreshToken']

#fetch the feedtoken
feedToken=obj.getfeedToken()

#fetch User Profile
#userProfile= obj.getProfile(refreshToken)

token="nse_cm|2885&nse_cm|1594&nse_cm|11536"
task="mw" #"mw"|"sfi"|"dp"
ss = WebSocket(feedToken, "R12345")

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
