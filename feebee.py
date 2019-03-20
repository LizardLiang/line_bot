import requests, json, jsonparser
from lxml import etree


def web_to_json():
    r = requests.get('https://feebee.com.tw/s/?q=AIR+PODS')
    r_1 = etree.HTML(r.text)
    r_2 = etree.tostring(r_1)
    js = jsonparser.HTMLtoJSONParser.to_json(str(r_2))
    for li in js['html']['body']['div'][4]['div'][2]['ol']['li']:
        print(li['span'][1]['div'][0]['a']['span'][1][''])