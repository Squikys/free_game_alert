import requests
import json
from handler.date_parser import date_validator, formatted_time,convert_to_ist, is_within_last_24_hours
import logging

import xml.etree.ElementTree as ET
import json
import re
from xml.sax.saxutils import unescape
import requests
import sys
from pathlib import Path
logging.basicConfig(format='%(asctime)s %(message)s')

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)


def get_game_assets(game_title:str,API_KEY:str):

    lookup_url = "https://api.isthereanydeal.com/games/lookup/v1"
    params = {
        "key": API_KEY,
        "title": game_title
    }
    resp = requests.get(lookup_url, params=params)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("found"):
        print(f"Game not found: {game_title}")
        return None

    game_info = data["game"]
    assets = game_info.get("assets", {})
    banner_url = assets.get("banner300")
    return banner_url


def parse_rss(source:str,API_KEY:str,LIMIT:float)->list:
    if source.startswith("http://") or source.startswith("https://"):
        resp = requests.get(source)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
    else:
        root = ET.parse(source).getroot()

    channel = root.find('channel')
    if channel is None:
        for elem in root:
            if 'channel' in elem.tag:
                channel = elem
                break

    extracted_items = []
    for item in channel.findall('item'):
        publish_date = item.findtext('pubDate')
        title = item.findtext('title')
        desc = item.findtext('description') or ''

        a_tag_match = re.search(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
                                desc, re.IGNORECASE | re.DOTALL)
        game_real_title = None
        link_to_store = None
        if a_tag_match:
            link_to_store = a_tag_match.group(1).strip()
            game_real_title = unescape(a_tag_match.group(2)).strip()

        expiry_date = None
        match_full_date = re.search(
            r'\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s+\d{1,2}\s+\w+\s+\d{4}\s+\d{2}:\d{2}:\d{2}\s+\+\d{4}\b', 
            desc
        )
        if match_full_date:
            expiry_date = match_full_date.group(0)
        else:
            match_simple = re.search(r'(?i)(?:expire|end|until)[^\d]*(\d{1,2}\s\w+\s\d{4})', desc)
            if match_simple:
                expiry_date = match_simple.group(1)


        if is_within_last_24_hours(publish_date,limit=LIMIT):
            extracted_items.append({
                "publish_date": formatted_time(str(convert_to_ist(publish_date))) if publish_date else None,
                "title": title,
                "game_real_title": game_real_title,
                "expiry": formatted_time(str(convert_to_ist(expiry_date))) if expiry_date else None,
                "link": link_to_store,
                "banner": get_game_assets(game_title=game_real_title,API_KEY=API_KEY) if game_real_title else None
            })

    return extracted_items




'''
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