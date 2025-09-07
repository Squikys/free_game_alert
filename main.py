import requests
import dotenv
import os
import json
dotenv.load_dotenv()
API_KEY=os.getenv("API_KEY")
COUNTRY=os.getenv("COUNTRY")


def api_call_time(api_key:str,country:str)->list:
    resp=[]
    running=True
    offset=0
    limit=5
    while running:
        data={
            "key":api_key,
            "country":country,
            "sort": "time",
            "mature": True,
            "limit": limit,
            "offset":offset   
        }
        res=requests.get(url="https://api.isthereanydeal.com/deals/v2",params=data)
        offset+=limit
        s=json.loads(json.dumps(res.json()))
        for i in s["list"]:
            if offset<=20:
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
if __name__ == "__main__":
    resp=api_call_time(api_key=API_KEY,country=COUNTRY)
    print(resp)

'''
print(res.json())
with open("resp.json",mode="w") as s:
    s.write(str(json.dumps(res.json())))'''
