import requests
from lxml import etree

def find_bus(bus_name):
    r = requests.get('http://www.e-bus.gov.taipei/index_6_1.html#')
    r_1 = etree.HTML(r.text)
    r_2 = r_1.xpath('//a')
    for r_3 in r_2:
        t = r_3.xpath('text()')
        t1 = etree.tostring(r_3, pretty_print=True)
        print('t:', t1)
        if bus_name in t1:
            r_4 = r_3.attrib['href']
            t_1 = etree.tostring(r_4)
            print('t_1:', t_1)
            t_2 = t_1.split('\"')
            print('t_2:', t_2[1])
            return t_2[1]