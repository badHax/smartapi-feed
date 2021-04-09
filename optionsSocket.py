## WebSocket
import os
import sys
import json
from smartapi import WebSocket,SmartConnect
from optionsDownloader import IndexOptionsDownloader
from googleSheetsUtil import GoogleSheetsUtil, SheetName
from datetime import datetime

task = ''
token = ''
sheetName = ''

def main():
    global task
    global token
    global sheetName
    
    feedToken = sys.argv[1]
    client_id = sys.argv[2]
    sheetName = sys.argv[3]
    
    task = "mw"
    token = get_token_string(sheetName)
        
    # Assign the callbacks.
    ss = WebSocket(feedToken, client_id)
    ss.on_ticks = on_tick
    ss.on_connect = on_connect
    ss.on_close = on_close
        
    print("*** starting live feed {0} ***".format(sheetName))
    ss.connect()
        
def on_tick(ws, tick):
    print("Ticks: {}".format(tick))
    if "ltt" in tick[0]:
        row = get_row_data(tick)
        print("appending row to {0} \n {1}".format(sheetName, row))
        sheetUtil = GoogleSheetsUtil()
        sheetUtil.add_row_range(row, sheetName)
        
def on_connect(ws, response):
    ws.websocket_connection() # Websocket connection 
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

def get_token_string(filename):
        output = ''
        with open(filename + ".txt", 'r') as filereader:
            strData = filereader.read()
            jsonObj = json.loads(strData)
            for instrument in jsonObj:
                if len(output) > 1:
                    output += '&'
                output += "nse_fo|" + instrument['token']
        return output
        
if __name__ == "__main__":
    main()