import SDL_DS3231
import datetime
import os
import time

rtc=SDL_DS3231.SDL_DS3231(1,0x68)

rtctime=rtc.read_datetime()

print("DS3231 time:",rtctime)
