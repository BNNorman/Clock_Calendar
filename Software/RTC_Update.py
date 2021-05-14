import SDL_DS3231
import datetime
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
rtc_sec=total_seconds(rtc_dt)

pi_dt=datetime.datetime.now()
pi_sec=total_seconds(pi_dt)


print("RTC datetime:",rtc_dt,"seconds=",rtc_sec)
print("PI datetime:",pi_dt,"seconds=",pi_sec)

if rtc_dt.year==2000 or rtc_dt.year<pi_dt.year: # RTC reset state
    set_rtc(pi_dt)
elif total_seconds(rtc_dt)!=total_seconds(pi_dt):
    set_pi(rtc_dt)

print("RTC and Pi are in sync")
    
while True:
    
    rtc_dt=rtc.read_datetime()
    pi_dt=datetime.datetime.now()

    print("rtc=",rtc_dt)
    print("pi=",pi_dt)
    if total_seconds(rtc_dt)!=total_seconds(pi_dt):
        # set the Pi clock
        set_pi(rtc_dt)

    time.sleep(60)
