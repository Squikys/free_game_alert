from datetime import datetime, timedelta, timezone

def date_validator(time_stamp:str,limit_hours:str)->bool:

    timestamp = datetime.fromisoformat(time_stamp)
    now = datetime.now(timezone.utc).astimezone(timestamp.tzinfo)
    within_24h = now - timestamp <= timedelta(hours=limit_hours)

    return within_24h
