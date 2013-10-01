# Test to have a moving calendar date for time preferences

import Tkinter as tk
import sys, string, calendar
import time

year = time.localtime()[0]
month = time.localtime()[1]
day = time.localtime()[2]

fnta = ("Times", 12)
fnt = ("Times", 14)
fntc = ("Times", 18, 'bold')


#English Options 
strtitle = "Calendar"
strdays = "Su  Mo  Tu  We  Th  Fr  Sa"
dictmonths = {'1':'Jan','2':'Feb','3':'Mar','4':'Apr','5':'May',
              '6':'Jun','7':'Jul','8':'Aug','9':'Sep','10':'Oct','11':'Nov',
              '12':'Dec'}

class myCal:
    
    def __init__(self, master, arg_year, arg_month, arg_day):

        
       # top = self.top = tk.Toplevel(master)
        
        try : 
            self.intmonth = int(arg_month)
        except: 
            self.intmonth = int(1)

        self.canvas = tk.Canvas(master, width =200, height =220,
                                relief =tk.RIDGE, background ="white", borderwidth =1)
        self.canvas.create_rectangle(0,0,303,30, fill="#a4cae8",width=0 )
        self.canvas.create_text(100,17, text=strtitle,  font=fntc, fill="#2024d6")

        stryear = str(arg_year)
        self.year_var=tk.StringVar()
        self.year_var.set(stryear)
                
        self.month_var=tk.StringVar()
        strnummonth = str(self.intmonth)
        strmonth = dictmonths[strnummonth]
        self.month_var.set(strmonth)

        self.my_var = tk.StringVar()
        strym = strmonth + ' ' +stryear
        self.my_var.set(strym)

        self.lblYear = tk.Label(master, textvariable = self.my_var,
                                font = fnta, background="white")
        self.lblYear.place(x=85, y = 50)
        
        self.canvas.create_text(100,90, text=strdays, font=fnta)
        self.canvas.pack (expand =1, fill =tk.BOTH)
        self.fnFillCalendar()

    def fnFillCalendar(self):
        init_x_pos = 20
        arr_y_pos = [110,130,150,170,190,210]
        intposarr = 0
        self.canvas.delete("DayButton")
        self.canvas.update()
        intyear = int(self.year_var.get())
        monthcal = calendar.monthcalendar(intyear, self.intmonth)    

            xpos = init_x_pos 
            print arr_y_pos
            ypos = arr_y_pos[intposarr]
            for item in row:	
                stritem = str(item)
                if stritem == "0":
                    xpos += 27
                else :
                    tagNumber = tuple(("Daybutton",stritem))
                    self.canvas.create_text(xpos, ypos , text=stritem, 
                                            font=fnta,tags=tagNumber)	
                    xpos += 27
            intposarr += 1
                    

def frac(n): return 360. * n / 500

class Pie:

    def __init__(self, master):
        self.c = tk.Canvas(width=100, height=100)
        self.c.create_arc((4,4,98,98), fill="green", start=frac(0), extent = frac(100))
        self.c.create_arc((4,4,98,98), fill="blue", start=frac(100), extent = frac(400))
        self.c.pack()


class Together:

    def __init__(self, master):
        self.myframe = tk.Frame(master)
        self.myframe.pack()
        self.cal = myCal(self.myframe, year, month, day)
        self.pie = Pie(self.myframe)
        

root = tk.Tk()
root.title("Interface")
Together(root)
root.mainloop()
