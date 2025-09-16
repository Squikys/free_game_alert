import requests
import json
from handler.date_parser import date_validator, formatted_time
import logging

logging.basicConfig(format='%(asctime)s %(message)s')

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)

def api_call_by_time(api_key:str,country:str,filter:str,limit_hours:int)->list:
    resp=[]
    running=True
    offset=0
    limit=200
    while running:
        logging.info(f"Running: Current offset = {offset}")
        data={
            "key":api_key,
            "country":country,
            "sort": "-time",
            "mature": True,
            "limit": limit,
            "offset":offset,
            "filter":filter  
        }
        try:
            res=requests.get(url="https://api.isthereanydeal.com/deals/v2",params=data)
            offset+=limit
            s=json.loads(json.dumps(res.json()))
            for i in s["list"]:
                if date_validator(time_stamp=i["deal"]["timestamp"],limit_hours=limit_hours):
                    if i["deal"]["price"]["amount"]==0:
                        d={
                            "title":i["title"],
                            "cut":i["deal"]["cut"],
                            "type":i["type"],
                            "banner": i["assets"]["banner300"],
                            "link": i["deal"]["url"],
                            "store":i["deal"]["shop"]["name"],
                            "regular":i["deal"]["regular"]["amount"],
                            "price":i["deal"]["price"]["amount"],
                            "expiry":formatted_time(i["deal"]["expiry"])
                        }
                        resp.append(d)
                else:
                    running=False
                    break
            logging.info(f"{formatted_time(s['list'][199]['deal']['timestamp'])}")
        except Exception as e:
            logging.error(e)
    return resp
'''
def api_call(api_key:str,country:str)->list:
    resp=[]
    running=True
    offset=0
    limit=5
    while running:
        data={
            "key":api_key,
            "country":country,
            "sort": "price",
            "mature": True,
            "limit": limit,
            "offset":offset   
        }
        res=requests.get(url="https://api.isthereanydeal.com/deals/v2",params=data)
        offset+=limit
        s=json.loads(json.dumps(res.json()))
        for i in s["list"]:
            if i["deal"]["price"]["amount"]==0:
                d={
                    "title":i["title"],
                    "cut":i["deal"]["cut"],
                    "price":i["deal"]["price"]["amount"]
                }
                resp.append(d)
            else:
                running=False
                break
            print("call")
    return resp

'''