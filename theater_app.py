import gspread
import sys
import datetime
import json
from oauth2client.service_account import ServiceAccountCredentials

user_id = list()
user_status = list()

def connect_to_sheet():
    GDriveJSON = 'FAMAX-ef61fdf82b20.json'
    GSpreadSheet = 'line-bot'
    global worksheet
    while True:
        try:
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
            key = ServiceAccountCredentials.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open(GSpreadSheet).worksheet('theater')
            print('connect to spread successful')
            return worksheet
        except Exception as ex:
            print('無法連線Google試算表', ex)
            sys.exit(1)
            
def find_theater(keyword):
    wks = connect_to_sheet()
    theaters = wks.col_values(1)
    print(theaters)
    code = wks.col_values(2)
    for theater_t in theaters:
        if keyword == theater_t:
            return code[theaters.index(theater_t)]
    return '-1'