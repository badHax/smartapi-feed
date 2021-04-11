from __future__ import print_function
import os
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from enum import Enum

class SheetName(Enum):
    NIFTY = 'NIFTY'
    BANKNIFTY = 'BANKNIFTY'
    FINNIFTY = 'FINNIFTY'

class GoogleSheetsUtil:
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file']
    MAJOR_RANGE_START = 'A'
    MAJOR_RANGE_END = 'K'
    SPREADSHEET_RANGE = MAJOR_RANGE_START+'2:'+ MAJOR_RANGE_END +'1000'

    def __init__(self,id):
        self.SPREADSHEET_ID = id
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('secret.json'):
            creds = service_account.Credentials.from_service_account_file('secret.json', scopes = self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

        self.__service =  build('sheets', 'v4', credentials=creds)
        
    def add_row_range(self, row_values, spreadsheet_name, row_num):
        batch_update_values_request_body = {
                  "valueInputOption": "USER_ENTERED",
                  "includeValuesInResponse": False,
                  "data": [
                    {
                      "majorDimension": "ROWS",
                      "range": '{0}!{1}{2}:{3}{4}'.format(spreadsheet_name,self.MAJOR_RANGE_START,row_num,self.MAJOR_RANGE_END,str(len(row_values))),
                      "values": row_values
                    }
                  ]
                }

        request = self.__service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=batch_update_values_request_body)
        response = request.execute()

        # TODO: Change code below to process the `response` dict:
        print(response)

    
    def clear_range(self):
        request = self.__service.spreadsheets().values().clear(spreadsheetId=self.SPREADSHEET_ID, range=self.SPREADSHEET_RANGE)
        response = request.execute()

        # TODO: Change code below to process the `response` dict:
        print(response)
        
    def get_sheet_data(self):
        # The A1 notation of the values to retrieve.
        range_ = '1:1000'  # TODO: Update placeholder value.

        # How values should be represented in the output.
        # The default render option is ValueRenderOption.FORMATTED_VALUE.
        value_render_option = ''  # TODO: Update placeholder value.

        # How dates, times, and durations should be represented in the output.
        # This is ignored if value_render_option is
        # FORMATTED_VALUE.
        # The default dateTime render option is [DateTimeRenderOption.SERIAL_NUMBER].
        date_time_render_option = ''  # TODO: Update placeholder value.

        request = self.__service.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID, range=range_)
        response = request.execute()

        # TODO: Change code below to process the `response` dict:
        print(response)
