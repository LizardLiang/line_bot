import gspread
import sys
import datetime
import json
from oauth2client.service_account import ServiceAccountCredentials

user_id = list()
user_status = list()

def connect_to_spread():
    GDriveJSON = 'FAMAX-3647d846120a.json'
    GSpreadSheet = 'line-bot'
    global worksheet
    while True:
        try:
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
            key = ServiceAccountCredentials.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open(GSpreadSheet).worksheet('users')
            print('connect to spread successful')
            return worksheet
        except Exception as ex:
            print('無法連線Google試算表', ex)
            sys.exit(1)
            
def user_index(_id):
    global worksheet
    worksheet = connect_to_spread()
    global user_id
    user_id = worksheet.col_values(1)
    global user_status
    user_status = worksheet.col_values(2)
    if _id not in user_id:
        row_to_add = [_id, 0]
        worksheet.append_row(row_to_add)
        user_id.append(_id)
        user_status.append(0)
    return user_id.index(_id)

def check_status(_id):
    global user_id
    _index = user_index(_id)
    _status = user_status[_index]
    return _status

def set_status(_id, status):
    worksheet = connect_to_spread()
    _index = user_index(_id)
    user_status[_index] = 1
    worksheet.update_cell(2, _index+1, str(status))
    return 'set ' + _id + 'to search'

def clear_status(_id):
    worksheet = connect_to_spread()
    _index = user_index(_id)
    user_status[_index] = 0
    worksheet.update_cell(_index+1, 2, '0')
    return 'set ' + _id + 'to normal'