import requests
from lxml import etree

def find_bus(bus_name):
    r = requests.get('http://www.e-bus.gov.taipei/index_6_1.html#')
    r_1 = etree.HTML(r.text)
    print('r', r.text)
    r_2 = r_1.xpath('//script')
    for r_3 in r_2:
        t = r_3.xpath('text()')
        print('t:', t[0])
        try:
            t2 = t.index('e')
        except:
            continue
        try:
            if bus_name in t2:
                print('t_2:', t_2)
                return t_2[1]
        except:
            print('none')