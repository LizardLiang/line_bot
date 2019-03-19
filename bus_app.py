import requests
from lxml import etree

def find_bus(bus_name):
    r = requests.get('http://www.e-bus.gov.taipei/index_6_1.html#')
    r_1 = etree.HTML(r.text)
    r_2 = r_1.xpath('//script')
    for r_3 in r_2:
        t = r_3.xpath('text()')
        try:
            print('t', t[0])
            if bus_name in t[0]:
                print('bus', t[0])
        except:
            continue
