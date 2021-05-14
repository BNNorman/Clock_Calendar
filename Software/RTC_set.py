import SDL_DS3231
import datetime
from dateutil.parser import * 
import os
import time

epoch=datetime.datetime.utcfromtimestamp(0)

def total_seconds(dt):
    return int((dt-epoch).total_seconds())

def set_pi(dt):
    ts=dt.strftime("%Y-%m-%d %H:%M:%S")
    os.system("sudo date -s '{}'".format(ts))
    print("Pi has been synchronised to",dt)
    
def set_rtc(dt):
    rtc.write_all(dt.second,dt.minute,dt.hour,None,dt.day,dt.month,dt.year % 100)
    print("RTC has been synchronised to ",dt)

rtc=SDL_DS3231.SDL_DS3231(1,0x68)

rtc_dt=rtc.read_datetime()
pi_dt=datetime.datetime.now()


print("RTC datetime:",rtc_dt)
print("PI datetime:",pi_dt)

print("Which datetime is correct?\nP = Pi\nR = RTC\nN = neither")
r=input("Enter P, R or N)?:")

r=r.upper()

if r=="R":
	set_pi(rtc_dt)
elif r=="P":
	set_rtc(pi_dt)

elif r=="N":
	ts=input("Enter the correct date-time: ")
	dt=parse(ts)
	set_rtc(dt)
	set_pi(dt)
else:
	print("Not changed")
