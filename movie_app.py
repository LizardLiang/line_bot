from lxml import etree

import requests

def get_url():
    r = requests.get('http://www.atmovies.com.tw/movie/now/')
    r_1 = etree.HTML(r.text)
    r_2 = r_1.xpath('//ul[@class=\"filmListAll2\"]')
    r_3 = r_2[0].xpath('li')
    text = ''
    for cnt range len(r_3):
        r_4 = r_3[cnt].xpath('a')
        text = r_4[0].xpath('text()') + '\n'
    return text
        
    