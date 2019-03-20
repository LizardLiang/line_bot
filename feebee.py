import requests, json, jsonparser, re
from lxml import etree


def web_to_json():
    r = requests.get('https://feebee.com.tw/s/?q=AIR+PODS')
    r_1 = etree.HTML(r.text)
    name = r_1.xpath('//li[starts-with(@class, "pure-g")]')
    t = r_1.xpath("//span[starts-with(@class,'price ellipsis xlarge')]|//li[starts-with(@class,'price ellipsis xlarge')]")
    for cnt in range(len(name)):
        name_1 = name[cnt].xpath('string(.)')
        name_1 = name[cnt].replace('\n', '')
        name_1 = name[cnt].replace(' ', '')
        name_1 = name[cnt].replace('價格', '')
        price = t[cnt].xpath('string(.)')
        price = t[cnt].replace('\n', '')
        price = t[cnt].replace(' ', '')
        price = t[cnt].replace('價格', '')
        reply = name_1 + ' ' + price
    print(reply)
  