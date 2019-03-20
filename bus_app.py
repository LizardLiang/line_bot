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
    # 抓預估到站時間
    response = requests.get('https://ptx.transportdata.tw/MOTC/v2/Bus/EstimatedTimeOfArrival/City/Taipei/235?$format=JSON', headers= a.get_auth_header())
    # 抓路線圖
    response_1 = requests.get('https://ptx.transportdata.tw/MOTC/v2/Bus/StopOfRoute/City/Taipei/235?$format=JSON', headers= a.get_auth_header())
    data = json.loads(response.content)
    data_1 = json.loads(response_1.content)
    reply = ""
    stops_0 = data_1[0]['Stops']
    for stops in stops_0:
        for d_1 in data:
            try:
                print(d_1['Direction'] == 0, d_1['StopName']['Zh_tw'] == stops['StopName']['Zh_tw'], reply)
                if d_1['Direction'] == 0 and d_1['StopName']['Zh_tw'] == stops['StopName']['Zh_tw']:
                    reply += 'StopName = ' + d_1['StopName']['Zh_tw'] + 'EST = ' + str(d_1['EstimateTime']) + "\n"
                    print('StopName = ', d_1['StopName']['Zh_tw'], 'EST = ', d_1['EstimateTime'])
            except ValueError:
                print(ValueError)
            except :
                reply += 'StopName = ' + d_1['StopName']['Zh_tw'] + 'EST = ' + str(d_1) + "\n"
                print('other error')
    return reply
   
