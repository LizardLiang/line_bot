import requests, json, hmac, base64
from lxml import etree
from hashlib import sha1
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
from pprint import pprint

app_id = '5b0874b66c94481289e4d20efec3ab24'
app_key = '4Fw377NVqLHNRt6b_ypYoDB0iqI'

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }

def find_bus(bus_name):
    a = Auth(app_id, app_key)
    response = requests.get('http://ptx.transportdata.tw/MOTC/v2/Bus/Stop/City/Taipei?$top=30&$format=JSON', headers= a.get_auth_header())
    response_1 = requests.get('https://ptx.transportdata.tw/MOTC/v2/Bus/StopOfRoute/City/Taipei/235?$format=JSON', headers= a.get_auth_header())
    data = json.loads(response.content)
    data_1 = json.loads(response_1.content)
    for d_1 in data:
        print('d_1', d_1)
    for stops in data_1:
        print('stops:', stops["stops"])
   
