import requests, json, jsonparser, re
from lxml import etree


def web_to_json():
    r = requests.get('https://feebee.com.tw/s/?q=AIR+PODS')
    r_1 = etree.HTML(r.text)
    name = r_1.xpath('//li[starts-with(@class, "pure-g")]')
    t = r_1.xpath("//span[starts-with(@class,'price ellipsis xlarge')]|//li[starts-with(@class,'price ellipsis xlarge')]")
    price = ''
    name_l = list()
    price_l = list()
    print(len(t), len(name))
    for cnt in range(len(name)-1):
        """
        name_2 = name[cnt].xpath('span')
        name_3 = name_2[0].xpath('a')
        name_4 = name_3[0].attrib['title']
        """
        name_1 = name[cnt].xpath('string(.)')
        name_1 = name_1.replace('\n', '')
        name_1 = name_1.replace(' ', '')
        name_1 = name_1.replace('價格', '')
        if name_1 != None:
            name_l.append(name_1)
        try:
            price = t[cnt].xpath('string(.)')
            price = price.replace('\n', '')
            price = price.replace(' ', '')
            price = price.replace('價格', '')
            price_l.append(price)
        except:
            reply = name_1 + ' ' + price
    print(name_l, price_l)
  