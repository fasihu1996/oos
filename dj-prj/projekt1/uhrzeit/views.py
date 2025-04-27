from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.http import HttpResponse
from datetime import timezone, datetime
from django.shortcuts import render

def get_time(request, continent="Europe", city="Berlin"):
    try:
        tz = f"{continent}/{city}"
        timez = ZoneInfo(tz)
        utc_dt = datetime.now(timezone.utc)
        local_dt = utc_dt.astimezone(timez).strftime("%H:%M:%S %Y-%m-%d")
    except ZoneInfoNotFoundError:
        return HttpResponse(f"""
                <!DOCTYPE>
                <html>
                <body>
                Invalid timezone: {tz}
                </body>
                </html>
                """)

    return HttpResponse(f"""
    <!DOCTYPE>
    <html>
    <body>
    {local_dt} ({city} in the {continent} region)
    </body>
    </html>
    """)