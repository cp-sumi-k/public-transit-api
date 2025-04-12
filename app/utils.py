from datetime import datetime
import pytz

TIME_FORMAT = "%H:%M:%S"

def convert_times(time: str, tz_str="Asia/Kolkata"):
    """Convert time string to ISO format with timezone.
    
    Args:
        time (str): Time string in HH:MM:SS format
        tz_str (str): Timezone string (default: Asia/Kolkata)
    
    Returns:
        str: ISO formatted datetime string with timezone or None if invalid
    """
    if not time:
        return None

    try:
        local_tz = pytz.timezone(tz_str)
        t = datetime.strptime(time, TIME_FORMAT).time()
        today = datetime.now(local_tz).date()
        dt_local = local_tz.localize(datetime.combine(today, t))
        return dt_local.isoformat()
    except Exception:
        return None
