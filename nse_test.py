import requests
import schedule
import sys
import datetime
import time
from datetime import timedelta
from googleSheetsUtil import GoogleSheetsUtil
import logging

logging.basicConfig(level=logging.DEBUG)

api_endpoint = 'https://www.nseindia.com/api/option-chain-'
webpage = 'https://www.nseindia.com/get-quotes/derivatives'


def get_symbol(name,instrument='indices'):
	print('updating {0} sheet...'.format(name))
	headers = {'User-Agent': 'python/script'}
	params = {('symbol',name)}
	s = requests.session()
	r1 = s.get(webpage, headers=headers,params=params)
	response = s.get(api_endpoint+instrument, headers=headers, params=params)
	
	if response.status_code == 400:
		response = s.get(api_endpoint)
	j = response.json()
	all_data = []
	for data in j['filtered']['data']:
		row_data = [
			data['CE']['strikePrice'],
			data['CE']['lastPrice'],
			data['CE']['openInterest'],
			data['CE']['changeinOpenInterest'],
			data['CE']['pchangeinOpenInterest'],
			data['PE']['strikePrice'],
			data['PE']['lastPrice'],
			data['PE']['openInterest'],
			data['PE']['changeinOpenInterest'],
			data['PE']['pchangeinOpenInterest']
			]
		all_data.append(row_data)
			
	gs = GoogleSheetsUtil(sys.argv[2])
	gs.add_row_range(all_data, name,2)
	print("next update in {0} minutes".format(sys.argv[1]))
	
	
def job(force=False):
	while True:
		now = datetime.datetime.now()
		end = now.replace(hour=13,minute=30,second=0,microsecond=0)
		if now < end or force:
			get_symbol('NIFTY')
			get_symbol('BANKNIFTY')
			get_symbol('RELIANCE','equities')
			time.sleep(int(sys.argv[1])*60)
		else:
			break
		
if(len(sys.argv) < 3):
	print('useage: nse_test.py interval_in_minutes google_sheet_id')
else:
	job(force=True)
	schedule.every().monday.at('09:00').do(job)
	schedule.every().tuesday.at('09:00').do(job)
	schedule.every().wednesday.at('09:00').do(job)
	schedule.every().thursday.at('09:00').do(job)
	schedule.every().friday.at('09:00').do(job)
		
	while True:
		schedule.run_pending()
		time.sleep(1)
