import requests, json, jsonparser, re
from lxml import etree


def web_to_json():
    r = requests.get('https://feebee.com.tw/s/?q=AIR+PODS')
    r_1 = etree.HTML(r.text)
    key = re.compile()
    t = r_1.xpath("//li[matches(@li, 'pure-g items + .*?')]")
    r_2 = etree.tostring(r_1)
    js = jsonparser.HTMLtoJSONParser.to_json(str(r_2))
    print('t', t)