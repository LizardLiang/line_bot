import gspread
import sys
from oauth2client.service_account import ServiceAccountCredentials
users = list()

def check_user(user_id):
    GDriveJSON = 'FAMAX-ef61fdf82b20.json'
    GSpreadSheet = 'line-bot'
    while True:
        try:
            scope = ['https://spreadsheets.google.com/feeds']
            key = ServiceAccountCredentials.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open(GSpreadSheet).sheet1
        except Exception as ex:
            print('無法連線Google試算表', ex)
            sys.exit(1)
        global users
        users = worksheet.col_values(2)
        print('複製已存在的users' ,GSpreadSheet)
        if user_id in users:
            return users.index(user_id)
        else:
            users.append(user_id)
            worksheet.append_row((datetime.datetime.now(), textt))
    