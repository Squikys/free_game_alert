import requests
import dotenv
import os
import json
from handler.date_parser import date_validator


def api_call_by_time(api_key:str,country:str)->list:
    resp=[]
    running=True
    offset=0
    limit=5
    while running:
        data={
            "key":api_key,
            "country":country,
            "sort": "-time",
            "mature": True,
            "limit": limit,
            "offset":offset   
        }
        res=requests.get(url="https://api.isthereanydeal.com/deals/v2",params=data)
        offset+=limit
        s=json.loads(json.dumps(res.json()))
        for i in s["list"]:
            if date_validator(time_stamp=i["deal"]["timestamp"],limit_hours=24):
                if i["deal"]["price"]["amount"]==0:
                    d={
                        "title":i["title"],
                        "cut":i["deal"]["cut"],
                        "type":i["type"],
                        "price":i["deal"]["price"]["amount"]
                    }
                    resp.append(d)
            else:
                running=False
                break
            print("call")
    return resp

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

