import requests
from lxml import etree

def find_bus(bus_name):
    r = requests.get('http://www.e-bus.gov.taipei/index_6_1.html#')
    r_1 = etree.HTML(r.text)
    r_2 = r_1.xpath('//script')
    for r_3 in r_2:
        t = r_3.xpath('text()')
        try:
            if bus_name in str(t[0]):
                print('bus', str(t[0]))
        except:
            continue
