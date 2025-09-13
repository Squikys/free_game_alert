from datetime import datetime, timedelta, timezone

def date_validator(time_stamp:str,limit_hours:float)->bool:

    timestamp = datetime.fromisoformat(time_stamp)
    now = datetime.now(timezone.utc).astimezone(timestamp.tzinfo)
    within_24h = now - timestamp <= timedelta(hours=limit_hours)

    return within_24h

def formatted_time(iso_date:str)->str:

    import pytz
    dt = datetime.fromisoformat(iso_date)
    ist = pytz.timezone("Asia/Kolkata")
    dt_ist = dt.astimezone(ist)
    formatted_date = dt_ist.strftime("%B %d, %Y %I:%M %p")
    return formatted_date
