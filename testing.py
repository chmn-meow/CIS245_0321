import datetime

today = datetime.datetime.now()
# timezone = datetime.timedelta(hours=-6)
# corrected_time = utc_dt_aware + timezone
updt = today.strftime("%A, %B, %d")
day = today.day
month = today.month
tm = today.time()
tme = tm.strftime("%I:%m %p")

timestamp = 1607470253
last_called = datetime.datetime.fromtimestamp(timestamp)


print(today)
print(updt)
print(day)
print(month)
print(tm)
print(tme)