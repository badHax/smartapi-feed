import requests
import schedule
import sys
import time
from googleSheetsUtil import GoogleSheetsUtil

api_endpoint = 'https://www.nseindia.com/api/option-chain-indices'
webpage = 'https://www.nseindia.com/get-quotes/derivatives?symbol=NIFTY'

def job():
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
	}

	params = (
		('symbol', 'NIFTY'),
	)
	r1 = requests.get(webpage, headers=headers, verify=False)
	headers['Cookie'] = r1.headers['Set-Cookie']
	
	response = requests.get(api_endpoint, headers=headers, params=params, verify=False)

	if response.status_code == 400:
		response = requests.get(api_endpoint, headers=headers, params=params, verify=False)
	
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
	gs.add_row_range(all_data, 'NIFTY',0)
	

if(len(sys.argv) < 3):
	print('useage: nse_test.py interval_in_minutes google_sheet_id')
else:
	job()