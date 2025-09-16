import logging
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
EMAILS=os.getenv("EMAILS")
LIMIT=os.getenv("LIMIT")
FILTER=os.getenv("FILTER")
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    if not API_KEY or not COUNTRY or not MAIL or not PASSWD or not FILTER or not LIMIT or not EMAILS:
        logger.error("Missing mandatory environment variables.")
        exit(1)
    resp=api_call_by_time(api_key=API_KEY,country=COUNTRY,filter=FILTER,limit_hours=int(LIMIT))
    if resp:
        body=email_buildier(response=resp)
        emails=EMAILS.split("\n")
        send_mail(mail=MAIL,passwd=PASSWD,receiver=emails,body=body)
    else: logger.info("No free games found")

