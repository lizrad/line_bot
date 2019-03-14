import gspread
import sys
import datetime
import json
from oauth2client.service_account import ServiceAccountCredentials
drinks = list()

def add_drinks(drink_name):
    d_index = check_drinks(drink_name)
    if d_index == -1:
        return -1
    else:
        return 0
    
    
def check_drinks(drink_name):
    GDriveJSON = 'FAMAX-ef61fdf82b20.json'
    GSpreadSheet = 'line-bot'
    while True:
        try:
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
            key = ServiceAccountCredentials.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open(GSpreadSheet).get_worksheet(1833798373)
        except Exception as ex:
            print('無法連線Google試算表', ex)
            sys.exit(1)
        global drinks
        drinks.users = worksheet.col_values(2)
        if drink_name in drinks:
            return drinks.index(drink_name)
        else:
            worksheet.append_row((json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str), user_id))
            return -1