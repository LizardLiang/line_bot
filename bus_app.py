import requests
from lxml import etree

def find_bus(bus_name):
    r = requests.get('http://www.e-bus.gov.taipei/index_6_1.html#')
    r_1 = etree.HTML(r.text)
    r_2 = r_1.xpath('//script')
    for r_3 in r_2:
        t = r_3.xpath('text()')
        try:
            for t_6 in t:
                try:
                    t_4 = str(t_6).split(';')
                    for t_5 in t_4:
                        try:
                           t_1 = t_5.split('(')
                        except:
                            t_1 = t_5.split('(')
                        print('t_1', t_1)
                        t_2 = t_1[1].split(')')
                        t_3 = t_2[0].split(',')
                        print('t_3', t_3)
                except:
                    continue
                if bus_name in t_3[2]:
                    print('bus', t_3[2])
        except:
            continue
