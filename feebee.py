import requests, json, jsonparser, re
from lxml import etree


def web_to_json():
    r = requests.get('https://feebee.com.tw/s/?q=AIR+PODS')
    r_1 = etree.HTML(r.text)
    t = r_1.xpath("//li[starts-with(@class,'pure-g')]")
    t_1 = t[0]
    t_2 = t_1.xpath('string(.)')
    t_3 = t_2.replace('\n', '')
    t_4 = t_3.replace(' ', '')
    r_2 = etree.tostring(r_1)
    js = jsonparser.HTMLtoJSONParser.to_json(str(r_2))
    print('t', t_4)