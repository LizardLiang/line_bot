from lxml import etree

import requests, re

def get_url():
    r = requests.get('http://www.atmovies.com.tw/movie/now/')
    r.encoding = 'big-5'
    r_1 = etree.HTML(r.text)
    r_2 = r_1.xpath('//ul[@class=\"filmListAll2\"]')
    print("r_2", etree.tostring(r_2[0]))
    r_3 = r_2[0].xpath('li')
    text = ''
    text_url = ''
    text_1 = list()
    reply_text = ''
    for cnt in range(len(r_3)):
        print("r_3", etree.tostring(r_3[cnt]))
        r_4 = r_3[cnt].xpath('a')
        print("r_4", etree.tostring(r_4[0]))
        text_url = etree.tostring(r_4[0])
        text = r_4[0].xpath('text()')
        text_1 += text
        text_1 += "\n"
    reply_text = reply_text.join(text_1)
    return reply_text
        
def get_teaser(movie_name):
    url = 'https://www.youtube.com/user/truemovie1/search?query=' + movie_name
    res = requests.get(url, verify=False)
    r = etree.HTML(res.text)
    r_1 = r.xpath('//a')
    print("len(r_1)", len(r_1))
    last = None
    for entry in r_1:
        m = re.search("v=(.*)", entry.attrib['href'])
        print("m", m)
        if m:
            target = m.group(1)
            if target == last:
                continue
            if re.search("list", target):
                continue
            last = target
            print("target", target)
            return target
    