import logging
import dotenv
import os
from services.api_client import parse_rss
from services.email_client import send_mail
from handler.email_buildier import email_buildier
dotenv.load_dotenv()
API_KEY=os.getenv("API_KEY")
#COUNTRY=os.getenv("COUNTRY")
MAIL=os.getenv("EMAIL")
PASSWD=os.getenv("PASS")
EMAILS=os.getenv("EMAILS")
LIMIT=os.getenv("LIMIT")
#FILTER=os.getenv("FILTER")
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    if not API_KEY or not MAIL or not PASSWD or not LIMIT or not EMAILS:
        logger.error("Missing mandatory environment variables.")
        exit(1) 
    source = "https://isthereanydeal.com/feeds/IN/giveaways.rss"
    resp=parse_rss(source=source,API_KEY=API_KEY,LIMIT=float(LIMIT))
    if resp:
        body=email_buildier(response=resp)
        emails=EMAILS.split("\n")
        send_mail(mail=MAIL,passwd=PASSWD,receiver=emails,body=body)
    else: logger.info("No free games found")

