# Playing around with the time interface

import Tkinter as tk
from Tkinter import Tk
import Image, ImageTk
import tkSimpleDialog as dialogp
from collections import namedtuple
import timeMethods as tm
reload(tm)
import mainGraphic as mg
import tkMessageBox


class Elicitation(tk.Frame):

    def __init__(self, master, config):
        tk.Frame.__init__(self, master)

        self.config = config

        self.problist = [float(i)/10 for i in range(0,11)]
        self.d = dict([ (p, {'aglobal': {'var': tk.StringVar(),
                                         'left': 'b1', 'right':'b2'},
                        'choice': dict(),
                        'progress': dict() })
                   for p in self.problist])

        self.iprobs = iter(self.problist)
        self.probvar = tk.IntVar()

        # Setting up the main frames
        self.real_main = tk.Frame(master)
       # self.real_main.grid(sticky = 'nswe')
        self.real_main.columnconfigure(0, weight = 1)
        self.real_main.rowconfigure(0, weight = 1)

        self.choice_list = mg.ChoiceList(self.real_main, self.d)
        self.progress = mg.ProgressBar(self.real_main, self.d)

        # The next button
        self.next_bt = tk.Button(self.real_main,
                                 text = 'Next',
                                 command = self.go_next_prob )
        self.next_bt.grid(row = 3, column = 2, padx = 3)

    def check_choice(self):
        print "This is the choice", self.probvar.get()


        p1 = float(self.probvar.get()) / 10
        print "p1", p1

        if p1 == 0:
            control_var = True

        else:
            prev_var = self.d[p1]['choice']['var'].get()
            print "relevant var", prev_var

            if prev_var == 0:
                control_var = False
                tkMessageBox.showwarning(
                    "Incomplete choice",
                    "Please make a choice")

            else:
                control_var = True

        return control_var



    def go_next_prob(self):

        c0 = self.check_choice()
        print "control var:", c0
        if c0 == False:
            print "do not pass"
        else:
            print "ready to go"

            try:
                p = self.iprobs.next()
                self.probvar.set(int(10*p))

                graphic = mg.MainGraphic(self.real_main, self.config, self.d, p)

                self.d[p]['progress'].configure( state = 'active')


            except StopIteration:
                self.end_change_choices()

        return None



class TopElicitation():

    def __init__(self, master, ind):

        self.problist = [float(i)/10 for i in range(0,11)]

        self.top_frame = tk.Frame(master)
        self.top_frame.grid()

        self.configs = { 1: { 'x0': 300, 'x1': 500, 'R': 10, 'r':4 },
                         2: { 'x0': 5000, 'x1': 20000, 'R': 100, 'r':14 },
                         3: { 'x0': 7, 'x1': 7, 'R': 7, 'r':7 }}

        self.config_frames = dict([(cnum, Elicitation(self.top_frame, config))
                                   for cnum, config in self.configs.items()])
        self.configvar = tk.IntVar()
        self.iconfigs = iter(self.configs.keys())

        self.ind = ind


        lab_frame = tk.Frame(self.top_frame)
        lab_frame.grid(row = 0)

        ind_lab = tk.Label(lab_frame,
                           text = 'Individual ID: {}'.format(self.ind))
        ind_lab.grid(row = 0, column = 0, sticky = 'w')

        self.config_lab = tk.Label(lab_frame,
                              text = 'Question 1 of 7')
        self.config_lab.grid( row = 0, column = 1, sticky = 'e')


        # The next button
        self.next_bt = tk.Button(self.top_frame,
                                 text = 'New configuration',
                                 command = lambda: self.next_config(master) )
        self.next_bt.grid(row = 3, column = 2, padx = 3)


    def next_config(self, master):
        cnum = self.iconfigs.next()
        self.configvar.set(cnum)
        pnum = cnum - 1
        try:
            prev_config_screen = self.config_frames[pnum]
            prev_config_screen.real_main.grid_forget()
        except:
            pass
        config_screen = self.config_frames[cnum]
        config_screen.real_main.grid()

        self.config_lab.configure(text =
                                  'Question {} of 7'.format(self.configvar.get()))

        return None

    def get_data(self):
        cnum = self.configvar.get()
        ind = self.ind

        choice = [self.config_frames[self.configvar.get()].
                  d[p]['choice']['var'].get() for p in self.problist]

        data = {'cnum': cnum,
                'ind': ind,
                'choices': tuple(choice)}

        return(data)


def choice(var):
    left_dic = {1:1, 2:0}
    left = left_dic[var]
    right = abs(left - 1)
    return left, right

def main_run():
    reload(tm)
    reload(mg)
    root = tk.Tk()
    root.rowconfigure(0, weight = 1)
    root.columnconfigure(0, weight = 1)
    root.minsize(1020, 500)
    root.geometry('+900+500')
    a = TopElicitation(root, 2)
    #root.mainloop()
    print 'bob'

    return a


"""

pc =[ (getd3['ind'], getd3['cnum']) + choice(p) for p in getd3['choices']]

mydat = [ (j, pc[j]) for j in range(len(pc))]

pd.DataFrame.from_items(mydat, orient = 'index', columns = ['ind', 'config', 'left', 'right'])

pd.concat([f,g])

"""
