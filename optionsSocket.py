## WebSocket
import os
import sys
import json
from smartapi import WebSocket
from optionsDownloader import IndexOptionsDownloader
from googleSheetsUtil import GoogleSheetsUtil, SheetName
from datetime import datetime
import time
import ast
import logging 

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

task = ''
token = ''
sheetName = ''
interval = 300 # every 5 minutes
last_checked = time.perf_counter() - interval

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
    
    logger.error("*** starting live feed {0} ***".format(sheetName))
    ss.connect()
        
def on_tick(ws, tick):
    global last_checked
    for i in tick:
        if 'ak' in i.keys() or 'tvalue' in i.keys():
            logger.error("Ticks: {}".format(tick))
            continue
        if 'ltp' in i.keys():
            if(time.perf_counter() - last_checked >= interval):
                logger.error("Tick: {}".format(i))
                row = get_row_data(i)
                sheetUtil = GoogleSheetsUtil()
                sheetUtil.add_row_range(row, sheetName.split('_')[0],row_num)
    
def on_connect(ws, response):
    ws.websocket_connection() # Websocket connection 
    ws.send_request(token,task) 
    
def on_close(ws, code, reason):
    ws.stop()

def get_row_data(options):
    row_data = []
    row_data.append('-' if 'name' not in options.keys() else options['name'])  
    row_data.append('-' if 'tk' not in options.keys() else options['tk'] )   
    row_data.append('-' if 'e' not in options.keys() else options['e'] )   
    row_data.append('-' if 'ltp' not in options.keys() else options['ltp'] )   
    row_data.append('-' if 'c' not in options.keys() else options['c'] )   
    row_data.append('-' if 'nc' not in options.keys() else options['nc'] )   
    row_data.append('-' if 'cng' not in options.keys() else options['cng'] )   
    row_data.append('-' if 'v' not in options.keys() else options['v'] )  
    row_data.append('-' if 'bq' not in options.keys() else options['bq'] )   
    row_data.append('-' if 'bp' not in options.keys() else options['bp'] )   
    row_data.append('-' if 'bs' not in options.keys() else options['bs'] )   
    row_data.append('-' if 'sp' not in options.keys() else options['sp'] )   
    row_data.append('-' if 'ltq' not in options.keys() else options['ltq'] )  
    row_data.append('-' if 'ltt' not in options.keys() else options['ltt'] ) 
    row_data.append('-' if 'ucl' not in options.keys() else options['ucl'] )  
    row_data.append('-' if 'tbq' not in options.keys() else options['tbq'] )  
    row_data.append('-' if 'mc' not in options.keys() else options['mc'] )  
    row_data.append('-' if 'lo' not in options.keys() else options['lo'] ) 
    row_data.append('-' if 'yh' not in options.keys() else options['yh'] ) 
    row_data.append('-' if 'op' not in options.keys() else options['op'] ) 
    row_data.append('-' if 'ts' not in options.keys() else options['ts'] ) 
    row_data.append('-' if 'h' not in options.keys() else options['h'] ) 
    row_data.append('-' if 'lcl' not in options.keys() else options['lcl'] ) 
    row_data.append('-' if 'tsq' not in options.keys() else options['tsq'] ) 
    row_data.append('-' if 'ap' not in options.keys() else options['ap'] ) 
    row_data.append('-' if 'yl' not in options.keys() else options['yl'] ) 
    row_data.append('-' if 'h' not in options.keys() else options['h'] ) 
    row_data.append('-' if 'oi' not in options.keys() else options['oi'] ) 
    row_data.append('-' if 'idsc' not in options.keys() else options['idsc'] ) 
    row_data.append('-' if 'to' not in options.keys() else options['to'] ) 
    row_data.append('-' if 'toi' not in options.keys() else options['toi'] ) 
    row_data.append('-' if 'lter' not in options.keys() else options['lter'] ) 
    row_data.append('-' if 'hter' not in options.keys() else options['hter'] ) 
    row_data.append('-' if 'setltyp' not in options.keys() else options['setltyp'] ) 
    return row_data

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
        
if __name__ == '__main__':
    main()