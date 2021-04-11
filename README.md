# smartapi-feed

A simple tool to read options(calls/puts) from the National Stock Exchange of India index feed using smartapi

## Requirements
 1. Google cloud account [here](https://console.cloud.google.com/home/dashboard)
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

Then run

```bash
python nse_test.py <number_of minutes_iterval> <google_sheet_id>
```



