import requests
import dotenv
import os
import json
dotenv.load_dotenv()
print(os.getenv("API_KEY"))
data={
    "key":os.getenv("API_KEY"),
    "sort": "-cut"
}
res=requests.get(url="https://api.isthereanydeal.com/deals/v2",params=data)

print(res.json())
with open("resp.json",mode="w") as s:
    s.write(str(json.dumps(res.json())))
