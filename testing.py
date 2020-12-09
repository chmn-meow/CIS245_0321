from datetime import datetime
import time

dt = datetime.now()
today = dt.strftime("%A, %B %d")
day = dt.strftime("%A")
tyme = dt.strftime("%I:%M %p")

timestamp = 1607556781
last_called = datetime.fromtimestamp(timestamp).strftime("%I:%M %p on %A, %B %d")

print(last_called)