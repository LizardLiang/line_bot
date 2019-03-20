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

def find_bus(bus_name, stop_name):
    url_time = 'https://ptx.transportdata.tw/MOTC/v2/Bus/EstimatedTimeOfArrival/City/Taipei/' + bus_name + '?$format=JSON'
    url_route = 'https://ptx.transportdata.tw/MOTC/v2/Bus/StopOfRoute/City/Taipei/' + bus_name + '?$format=JSON'
    url_info = 'https://ptx.transportdata.tw/MOTC/v2/Bus/Route/City/Taipei/' + bus_name + '?$format=xml'
    a = Auth(app_id, app_key)
    # 抓預估到站時間
    response = requests.get(url_time, headers= a.get_auth_header())
    # 抓路線圖
    response_1 = requests.get(url_route, headers= a.get_auth_header())
    #抓公車資訊
    response_info = requests.get(url_info, headers= a.get_auth_header())
    data = json.loads(response.content)
    #data_1 = json.loads(response_1.content)
    data_info = json.loads(response_info.content)
    stop_1st = data_info[0]["DepartureStopNameZh"]
    stop_last = data_info[0]["DestinationStopNameZh"]
    print(stop_1st, stop_last)
    reply = ""
    #stops_0 = data_1[0]['Stops'] #路線圖的stops
    reply = set_time(data, stop_name)
    return reply
    
   

def set_time(data, stop_name):
    reply = ""
    for d_1 in data:
            try:
                if d_1['Direction'] == 0 and d_1['StopName']['Zh_tw'] == stop_name:
                    reply += 'StopName = ' + d_1['StopName']['Zh_tw'] + '(' + str(d_1['EstimateTime']) + ")min\n"
                    return reply
            except ValueError:
                print(ValueError)
            except :
                if d_1['Direction'] == 0 and d_1['StopName']['Zh_tw'] == stops['StopName']['Zh_tw']:
                    reply += 'StopName = ' + d_1['StopName']['Zh_tw'] + '(公車未發車)' + "\n"
                    return reply
    

