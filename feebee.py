import requests, json, jsonparser


def web_to_json():
    r = requests.get('https://feebee.com.tw/s/?q=AIR+PODS')
    js = jsonparser.HTMLtoJSONParser.to_json(r.text)
    print(js)