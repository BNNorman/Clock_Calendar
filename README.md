# Clock_Calendar
Clock calendar display with music 

# Intro
My mum's eyesight is failing and she's got such bad arthritis that she is house and chair bound all day. So I decided to make a big clock calendar which she can see and to feed it to her TV via an HDMI port so that she has some idea of time and date. In addition it also plays her favourite CDs in a continuous loop and displays the names of pending visitors (family - we have a schedule so that she sees someone during the day).

She doesn't have WiFi.

# Solution
I decided to use a Raspberry Pi zero (non-wifi) 

![image](https://user-images.githubusercontent.com/15849181/118278394-e0509f80-b4c1-11eb-8bbe-3191be9ea329.png)

coupled with a DS3132 RTC board.

![image](https://user-images.githubusercontent.com/15849181/118277995-5dc7e000-b4c1-11eb-949a-d93006bc11b6.png)

The project uses systemd files to start the important programs should mum, or anyone else, power off the Pi.

# Wiring

Very simple:-

```
PI  RTC
1   VCC
3   SDA
5   SCL
6   GND

```

# Pi Setup

Follow these instructions to enable SPI

https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/set-up-and-test-i2c

Follow these instructions to add support for the RTC:-

https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/set-rtc-time

Disable the pi screen blanking - otherwise the clock display disappears and doesn't come back without a keyboard/mouse attached.

# python libraries

Nothing very special here. Just use pip3 to install

## SPI

```
pip3 install spidev SPI-py
```
## RTC
I used this library to provide python access to the RTC module.

https://github.com/switchdoclabs/RTC_SDL_DS3231

NOTE: use i2cdetect to check the two addresses of the RTC module (0x68 and 0x57). These are used on line 87 in the library and may need changing to match your device.

## smbus

Required by the SDL_DS3231 library

```
pip3 install smbus-python
```

## dateutil

The parser is used when you enter to date/time to correct the RTC in the RTC_set.py program.


# systemd

## Clock.service

This launches the tkinter Clock display (Clock.py) which is in /home/pi/ClockCal.

```
[Unit]
Description=Clock Service
StartLimitIntervalSec=10
After=graphical.target
Wants=graphical.target

[Service]
Type=simple
Restart=always
RestartSec=10
User=pi
Group=pi
StandardError=syslog
StandardOutput=syslog
SyslogIdentifier=Clock
WorkingDirectory=/home/pi/ClockCal
ExecStart=python3 /home/pi/ClockCal/Clock.py

[Install]
WantedBy=graphical.target
```

## RTC_Update.service

This service keeps the Pi in sync with the RTC - there are other ways to do this

```
[Unit]
Description=RTC Updater Service
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=5
User=pi
Group=pi
StandardError=syslog
StandardOutput=syslog
SyslogIdentifier=RTC_Update
WorkiingDirectory=/home/pi/ClockCal
ExecStart=python3 /home/pi/ClockCal/RTC_Update.py

[Install]
WantedBy=multi-user.target
```

## VLC.service

This starts VLC which loads the playlist pi.xspf from the /home/pi working directory. VLC is configured to play the playlist in a continuous loop.

```
[Unit]
Description=VLC music player Service
StartLimitIntervalSec=10
After=graphical.target
Wants=graphical.target

[Service]
Type=simple
Restart=always
RestartSec=10
User=pi
Group=pi
StandardError=syslog
StandardOutput=syslog
SyslogIdentifier=VLC
WorkingDirectory=/home/pi
Environment="DISPLAY=:0.0"
ExecStart=/usr/bin/vlc pi.xspf

[Install]
WantedBy=graphical.target
```

# Software

## Clock.py

This creates a tkinter app of a set size and centers it on the screen. With my TV the Pi display was too big. Turning off underscan had no effect so this program's window has been tweaked for mum's 42inch TV. You may need to modify font sizes and window sizes to suit.

It reads the current Pi date/time and displays it on screen.

Mum likes to know who of us is coming to see her so it also displays a list of visitors which is held in the dictionary in WhoIsComing.py. I list names in order morning/lunch/evening. However, mum understands that things change and we can't always be there or guarantee a time.

## RTC_Update.py

This program, runs in a continuous loop and compares the Pi date/time to the RTC. If the RTC and Pi date/times are different the Pi is adjusted to the RTC.

## RTS_set.py
This program displays the date/time from both the RTC and Pi. You can then choose which is correct and sync the RTC and PI. If neither are correct you can enter the time/date of your choosing and the Pi/RTC will be synced.

## RTC_datetime.py
Just a utility to display the RTC datetime.

## SDL_DS3231.py
The library required to access the RTC.
