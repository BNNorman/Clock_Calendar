import os

os.environ["DISPLAY"]=":0.0"

import tkinter as tk
import datetime
from WhoIsComing import Calendar

daynamefont=("Courier",100,"bold")
timefont=("Courier",100,"bold")
comingfont=("Courier",48,"bold")
namelistfont=("Courier",48)
spacefont=("Courier",100)

def centerWindow(win,win_width,win_height):
	win.update_idletasks()
	screen_width=win.winfo_screenwidth()
	screen_height=win.winfo_screenheight()

	x=int((screen_width/2)-(win_width/2))
	y=int((screen_height/2)-(win_height/2))
	win.geometry("{}x{}+{}+{}".format(win_width,win_height,x,y))

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.weekday=tk.StringVar()
        self.timenow=tk.StringVar()
        self.coming=tk.StringVar()

        self.dayframe=tk.Label(self, textvariable=self.weekday,text="day", fg='#f00', justify="center")
        self.dayframe.config(font=daynamefont)
        self.dayframe.grid(row=0,column=0)

        self.clockframe=tk.Label(self, textvariable=self.timenow,text="time", justify="center")
        self.clockframe.config(font=timefont)
        self.clockframe.grid(row=1,column=0)

        self.space=tk.Label(self,text="", justify="center")
        self.space.config(font=spacefont)
        self.space.grid(row=2,column=0)

        self.comingtoday=tk.Label(self,text="Coming Today?", fg='#00f', justify="center")
        self.comingtoday.config(font=comingfont)
        self.comingtoday.grid(row=3,column=0)

        self.comingframe=tk.Label(self, textvariable=self.coming,text="", justify="center")
        self.comingframe.config(font=namelistfont)
        self.comingframe.grid(row=4,column=0)


    def clock_update(self):
        now=datetime.datetime.now()
        dayname=now.strftime("%A")[:3]
        monthname=now.strftime("%b")[:3]
        day=int(now.strftime("%d"))
        self.weekday.set(dayname+" "+str(day)+" "+monthname+" "+str(now.year))
        self.timenow.set(now.strftime("%H:%M:%S"))
        self.coming.set(Calendar[dayname])
        ####################
        self.after(1000,self.clock_update)

try:
	root = tk.Tk()
	centerWindow(root,1280,1024)
	app = Application(master=root)
#	centerWindow(app,1280,1024)
	app.update_idletasks()
	app.clock_update()
	app.mainloop()
except Exception as e:
	print("Error ",e)
