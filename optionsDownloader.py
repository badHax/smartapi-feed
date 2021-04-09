import http.client
import json
import os
import socket
import sys
import re, uuid
from requests import get
from datetime import datetime
import pytz

''' 
    We update the options intrumnet list daily in case options
     were added or removed from the exchange
'''
class IndexOptionsDownloader:
    nifty_index_file = "NIFTY"
    bank_index_file = "BANKNIFTY"
    finance_index_file = "FINNIFTY"
    private_key = os.environ['SMART_API_KEY']
    exchange_name = 'nse_fo'
    max_token_per_file = 450
    
    try:
        clientPublicIp= " " + get('https://api.ipify.org').text
        if " " in clientPublicIp:
            clientPublicIp=clientPublicIp.replace(" ","")
        hostname = socket.gethostname()
        clientLocalIp=socket.gethostbyname(hostname)
    except Exception as e:
        print("Exception while retriving IP Address,using local host IP address",e)
    finally:
        clientPublicIp="106.193.147.98"
        clientLocalIp="127.0.0.1"
    clientMacAddress=':'.join(re.findall('..', '%012x' % uuid.getnode()))
    accept = "application/json"
    userType = "USER"
    sourceID = "WEB"
    
    def __init__(self, data):
        self.__data = data;
    
    def download_nse_options(self,):
        conn = http.client.HTTPSConnection("margincalculator.angelbroking.com")
        payload = json.dumps({
          "clientcode": self.__data['data']['clientcode']     })
        headers = {
          'X-PrivateKey': self.private_key,
          'X-UserType': self.userType,
          'X-SourceID': self.sourceID,
          'X-ClientPublicIP': self.clientPublicIp,
          'X-ClientLocalIP': self.clientLocalIp,
          'X-MACAddress': self.clientMacAddress,
          'Authorization': self.__data['data']['jwtToken'],
          'Content-Type': self.accept
        }
        conn.request("GET", "/OpenAPI_File/files/OpenAPIScripMaster.json", payload, headers)
        res = conn.getresponse()
        if(res.status == 200):
            print("successfully fetched options list")
            print("saving to file")
            data = res.read()
            jsonData = json.loads(data)
            self.__save_json_files(jsonData)
        else:
            print("failed to download daily index options list")
            sys.exit()
     
    def __save_json_files(self,jsonObj):
        nifty_data = []
        nifty_data_count = 0
        bank_nifty_data = []
        bank_nifty_data_count = 0
        fin_nifty_data = []
        fin_nifty_data_count = 0
        for instrumnet in jsonObj:
            if instrumnet['instrumenttype'] == 'OPTIDX': # index option
                if instrumnet['name'] == 'NIFTY':
                    if len(nifty_data) <= self.max_token_per_file:
                        nifty_data.append(instrumnet['token'])
                    else:
                        with open('{0}_{1}.txt'.format(self.nifty_index_file,nifty_data_count),'w') as niftyOutFile:
                            print('saving {0}'.format(niftyOutFile.name))
                            json.dump(nifty_data,niftyOutFile)
                            nifty_data = []
                            nifty_data_count += 1
                if instrumnet['name'] == 'BANKNIFTY':
                    if len(bank_nifty_data) <= self.max_token_per_file:
                        bank_nifty_data.append(instrumnet['token'])
                    else:
                        with open('{0}_{1}.txt'.format(self.bank_index_file,bank_nifty_data_count),'w') as niftyOutFile:
                            print('saving {0}'.format(niftyOutFile.name))
                            json.dump(bank_nifty_data,niftyOutFile)
                            bank_nifty_data = []
                            bank_nifty_data_count += 1
                            
                if instrumnet['name'] == 'FINNIFTY':
                    if len(fin_nifty_data) <= self.max_token_per_file:
                        fin_nifty_data.append(instrumnet['token'])
                    else:
                        with open('{0}_{1}.txt'.format(self.finance_index_file,fin_nifty_data_count),'w') as niftyOutFile:
                            print('saving {0}'.format(niftyOutFile.name))
                            json.dump(fin_nifty_data,niftyOutFile)
                            fin_nifty_data = []
                            fin_nifty_data_count += 1
        
        # finally save remaining files       
        if  len(nifty_data) > 0:
            with open('{0}_{1}.txt'.format(self.nifty_index_file,nifty_data_count),'w') as niftyOutFile:
                print('saving {0}'.format(niftyOutFile.name))
                json.dump(nifty_data,niftyOutFile)
        if  len(nifty_data) > 0:
            with open('{0}_{1}.txt'.format(self.bank_index_file,bank_nifty_data_count),'w') as niftyOutFile:
                print('saving {0}'.format(niftyOutFile.name))
                json.dump(bank_nifty_data,niftyOutFile)
        if  len(nifty_data) > 0:
            with open('{0}_{1}.txt'.format(self.finance_index_file,fin_nifty_data_count),'w') as niftyOutFile:
                print('saving {0}'.format(niftyOutFile.name))
                json.dump(fin_nifty_data,niftyOutFile)

                
    ''' 
        check if the option symbols were updated already for the day
        or if the files are empty
    '''            
    def is_valid_index_files(self):
        try:
            tz = pytz.timezone('Asia/Kolkata')
            today = datetime.now().astimezone(tz).strftime('%x');
            
            # last date modifeid time
            d1 = datetime.utcfromtimestamp(os.path.getmtime(self.nifty_index_file+'_0.txt')).astimezone(tz).strftime('%x')
            
            # size of file
            s1 = os.path.getsize(self.nifty_index_file+'_0.txt')
              
            if (today == d1) and (s1 > 0):
                print("options list already downloaded for today...")
                return True
            print ("options file is outdated")
            return False
        except OSError as err:
            print(err)
            return False