import requests
from lxml import etree

def find_bus(bus_name):
    r = requests.get('https://ptx.transportdata.tw/MOTC/v2/Bus/EstimatedTimeOfArrival/City/Taipei/235?$format=JSON')
    print('r:', r)
    print('len(r):', len(r))
