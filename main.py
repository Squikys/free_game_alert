import dotenv
import os
from services.api_client import api_call_by_time
dotenv.load_dotenv()
API_KEY=os.getenv("API_KEY")
COUNTRY=os.getenv("COUNTRY")

if __name__ == "__main__":
    resp=api_call_by_time(api_key=API_KEY,country=COUNTRY)
    print(resp)
    print(f"{len(resp)=}")

'''
print(res.json())
with open("resp.json",mode="w") as s:
    s.write(str(json.dumps(res.json())))'''
