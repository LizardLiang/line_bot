from lxml import etree

import requests

def get_url():
    r = requests.get('http://www.atmovies.com.tw/movie/now/')
    r_1 = etree.HTML(r.text)
    r_2 = r_1.xpath('//ul[@class=\"filmListAll2\"]')
    print("r_2", etree.tostring(r_2))
    r_3 = r_2[0].xpath('li')
    print("r_3", etree.tostring(r_3))
    text = ''
    text_1 = list()
    reply_text = ''
    for cnt in range(len(r_3)):
        r_4 = r_3[cnt].xpath('a')
        print("r_4", etree.tostring(r_4))
        text = r_4[0].xpath('text()')
        text_1 += text
        text_1 += "\n"
    reply_text = reply_text.join(text_1)
    return reply_text
        
    