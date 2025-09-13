import dotenv
import os
from services.api_client import api_call_by_time
from services.email_client import send_mail
from handler.email_buildier import email_buildier
dotenv.load_dotenv()
API_KEY=os.getenv("API_KEY")
COUNTRY=os.getenv("COUNTRY")
MAIL=os.getenv("EMAIL")
PASSWD=os.getenv("PASS")

if __name__ == "__main__":
    resp=api_call_by_time(api_key=API_KEY,country=COUNTRY,limit_hours=24)
    if resp:
        body=email_buildier(response=resp)
        with open("emails.txt","r") as r:
            s=r.read()
        emails=s.split("\n")
        send_mail(mail=MAIL,passwd=PASSWD,receiver=emails,body=body)




'''
print(res.json())
with open("resp.json",mode="w") as s:
    s.write(str(json.dumps(res.json())))
'''
