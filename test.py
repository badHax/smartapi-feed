import sys
from smartapi import WebSocket

task = 'mw'

def on_tick(ws, tick):
    print("Ticks: {}".format(tick))

def on_connect(ws, response):
    ws.websocket_connection() # Websocket connection  
    ws.send_request('nse_fo|26000',task) 
    
def on_close(ws, code, reason):
    ws.stop()

ss = WebSocket('6944', 'TTYP1013')
# Assign the callbacks.
ss.on_ticks = on_tick
ss.on_connect = on_connect
ss.on_close = on_close

ss.connect( )