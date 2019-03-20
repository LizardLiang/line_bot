import requests, json, jsonparser
from lxml import etree


def web_to_json():
    r = requests.get('https://feebee.com.tw/s/?q=AIR+PODS')
    r_1 = etree.HTML(r.text)
    r_2 = etree.tostring(r_1)
    js = jsonparser.HTMLtoJSONParser.to_json(r_2)
    print(js)