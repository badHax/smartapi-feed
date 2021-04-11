import requests
import schedule
import sys
import time
from googleSheetsUtil import GoogleSheetsUtil

api_endpoint = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
webpage = 'https://www.nseindia.com/get-quotes/derivatives?symbol=NIFTY'

def job():
	print("updating sheet")
	headers = {'User-Agent': 'python/script'}
	s = requests.session()
	r1 = s.get(webpage, headers=headers)
	response = s.get(api_endpoint, headers=headers)
	
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
	gs.add_row_range(all_data, 'NIFTY',2)
	print("next update in {0} minutes".format(sys.argv[1]))
	

if(len(sys.argv) < 3):
	print('useage: nse_test.py interval_in_minutes google_sheet_id')
else:
	job()
	schedule.every(int(sys.argv[1])).minutes.do(job)
	while True:
		schedule.run_pending()
		time.sleep(1)