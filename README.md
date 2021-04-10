# smartapi-feed

A simple tool to read options(calls/puts) from the National Stock Exchange of India index feed using smartapi

## Requirements
 1. AngelBroking Account [here](https://www.angelbroking.com/)
 2. Smart API account:
	 - create smart api account [here](https://smartapi.angelbroking.com/apps)
	 - create an app for market feed
	 - note the API Key
 3. Google cloud account [here](https://console.cloud.google.com/home/dashboard)
	- create a project
	- enable google sheet api
	- create credentials for service account. Download the credentials and save them secret.json
	- save secret.json in this folder
	- create a google sheet and share it with the email for the service account you created. Note the spreadsheet id
	
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install smartapi-feed.

```bash
$ python -m venv env

# mac os/unix
$ source tutorial-env/bin/activate
# windows
$ env\Scripts\activate.bat

$ pip install -r requirements.txt
```

## Usage

Set environment variables:
```bash
# on windows
setx SMART_API_CLIENT_ID <angel broking client id>
setx SMART_API_CLIENT_PASSWORD <angel broking client password>
setx SMART_API_KEY <api key from smart api>
setx SPREADSHEET_ID <google spreadsheet id>
setx PORT <port number>

```

Then run

```bash
python app.py
```
