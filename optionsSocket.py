## WebSocket
import os
import sys
import json
from smartapi import WebSocket,SmartConnect
from optionsDownloader import IndexOptionsDownloader
from googleSheetsUtil import GoogleSheetsUtil, SheetName
from datetime import datetime
from timeit import default_timer as timer
import ast

task = ''
token = ''
sheetName = ''
interval = 20
start = -10
end = interval
row_num = 0

def main():
    global task
    global token
    global sheetName
    global start
    global row_num
    
    feedToken = sys.argv[1]
    client_id = sys.argv[2]
    sheetName = sys.argv[3]
    row_num = sys.argv[4]
    
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
    global start
    global end
    global interval
    
    print("Ticks: {}".format(tick))
    for i in tick:
        if 'ak' in i.keys() or 'tvalue' in i.keys():
            continue
        if i['name'] == 'sf' and 'ltp' in i.keys():
            if end - start >= interval:
                row = get_row_data(tick)
                sheetUtil = GoogleSheetsUtil()
                sheetUtil.add_row_range(row, sheetName.split('_')[0],row_num)
                start = timer()
            end = timer()
    
def on_connect(ws, response):
    ws.websocket_connection() # Websocket connection 
    ws.send_request(token,task) 
    
def on_close(ws, code, reason):
    ws.stop()

def get_row_data(tick):
    output = []
    for option in tick:
        row_data = []
        row_data.append(options['name'] if 'name' in options.keys() else '-')  
        row_data.append(options['tk'] if 'tk' in options.keys() else '-')  
        row_data.append(options['e'] if 'e' in options.keys() else '-')  
        row_data.append(options['ltp'] if 'ltp' in options.keys() else '-')  
        row_data.append(options['c'] if 'c' in options.keys() else '-')  
        row_data.append(options['nc'] if 'nc' in options.keys() else '-')  
        row_data.append(options['cng'] if 'cng' in options.keys() else '-')  
        row_data.append(options['v'] if 'v' in options.keys() else '-') 
        row_data.append(options['bq'] if 'bq' in options.keys() else '-')  
        row_data.append(options['bp'] if 'bp' in options.keys() else '-')  
        row_data.append(options['bs'] if 'bs' in options.keys() else '-')  
        row_data.append(options['sp'] if 'sp' in options.keys() else '-')  
        row_data.append(options['ltq'] if 'ltq' in options.keys() else '-') 
        row_data.append(options['ltt'] if 'ltt' in options.keys() else '-')
        row_data.append(options['ucl'] if 'ucl' in options.keys() else '-') 
        row_data.append(options['tbq'] if 'tbq' in options.keys() else '-') 
        row_data.append(options['mc'] if 'mc' in options.keys() else '-') 
        row_data.append(options['lo'] if 'lo' in options.keys() else '-')
        row_data.append(options['yh'] if 'yh' in options.keys() else '-')
        row_data.append(options['op'] if 'op' in options.keys() else '-')
        row_data.append(options['ts'] if 'ts' in options.keys() else '-')
        row_data.append(options['h'] if 'h' in options.keys() else '-')
        row_data.append(options['lcl'] if 'lcl' in options.keys() else '-')
        row_data.append(options['tsq'] if 'tsq' in options.keys() else '-')
        row_data.append(options['ap'] if 'ap' in options.keys() else '-')
        row_data.append(options['yl'] if 'yl' in options.keys() else '-')
        row_data.append(options['h'] if 'h' in options.keys() else '-')
        row_data.append(options['oi'] if 'oi' in options.keys() else '-')
        row_data.append(options['idsc'] if 'idsc' in options.keys() else '-')
        row_data.append(options['to'] if 'to' in options.keys() else '-')
        row_data.append(options['toi'] if 'toi' in options.keys() else '-')
        row_data.append(options['lter'] if 'lter' in options.keys() else '-')
        row_data.append(options['hter'] if 'hter' in options.keys() else '-')
        row_data.append(options['setltyp'] if 'setltyp' in options.keys() else '-')
        output.append(row_data)
    return output

def get_token_string(filename):
        output = ''
        with open(filename, 'r') as filereader:
            strData = filereader.read()
            token_list = ast.literal_eval(strData)
            for tk in token_list:
                if len(output) > 1:
                    output += '&'
                output += "nse_fo|" + tk
        return output
        
if __name__ == "__main__":
    main()