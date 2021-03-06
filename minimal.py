# Playing around with the time interface

import Tkinter as tk
from Tkinter import Tk
import Image, ImageTk
import tkSimpleDialog

prob = 9

class monotoneDialog(tkSimpleDialog.Dialog):
    
    def body(self, master):
       tk. Label(master, 
                 text = """You just switched. 
                 Are you happy with this decision?""").grid(row = 0)

class rationalDialog(tkSimpleDialog.Dialog):
    
    def body(self, master):
       tk. Label(master, 
                 text = """Are you sure of this decision?""").grid(row = 0)

class endDialog(tkSimpleDialog.Dialog):
    
    def body(self, master):
       tk. Label(master, 
                 text = """Thank you for making your decisions. After clicking 'OK' you will have the opportunity to modify your choices. """).grid(row = 0)
    


class Elicitation(object):

    def __init__(self, master=None):


        # Setting up the main frames
        self.real_main = tk.Frame()
        self.real_main.grid(sticky = 'nswe')
        self.real_main.columnconfigure(0, weight = 1)
        self.real_main.rowconfigure(0, weight = 1)
        


        # Button frame
        self.bt_frame = tk.LabelFrame(self.real_main,
                                      text = 'Choice History')
        self.bt_frame.grid(column = 2)



        self.scale = tk.Scale(self.bt_frame, 
                              from_ = 0, to = 10,
                              length = 300, state = 'disabled')

        self.scale.grid(rowspan = 11, column = 1, sticky = 'S')
        self.scale.bind('<ButtonRelease-1>', self.adjust_choices)

        # Dealing with probabilities
        self.prob = tk.IntVar(self.real_main)
        self.prob.set(9)
        self.myp = self.prob.get()

        self.probs = [float(i)/float(10) for i in range(0,11)]
        self.pdic = dict( [ (p, dict()) for p in self.probs ])
        self.iprobs = iter(range(0, 11))

        for p in self. probs:
            self.single_choice(self.bt_frame, p)

        self.check = tk.Button(self.real_main,
                               text = 'Next!',
                               command = lambda: self.go_next_prob(self.prob))
        self.check.grid(row = 1, column = 2, padx = 3)


        # Setting up the images
        self.env_img = self.get_envelope_pic()


        # Delaing with the buckets
        self.safe_var = tk.StringVar(self.real_main)
        self.risk_var = tk.StringVar(self.real_main)
        self.safe_var.set('b1')
        self.risk_var.set('b2')
        self.radvar = tk.StringVar()

        # Back buttons
        self.back_frame = tk.LabelFrame(self.real_main)
        self.back_frame.grid(row = 1, sticky = 'e')

        self.back_label = tk.Label(self.real_main,
                                   text = "Progress.")
        self.back_label.grid(row=1, sticky = 'w')
        self.buttdic = dict( [ (p, dict()) for p in self.probs ])
        [self.make_progress_buttons(self.back_frame, p) for p in self.probs]

        self.amtdic = {'left': {'x': 150, 'r': None},
                       'right': {'x': 400, 'r': None}}

    def adjust_choices(self, event):
        prob = float(self.scale.get())/10
        adj = self.pdic[prob]['b1'].select()

        [self.fill_forward_list(k, prob) for k in self.probs]
        [self.fill_back_list(k, prob) for k in self.probs]

        return None


    def make_text_label(self, master, risky, probvar, coln):

        p = probvar.get() * 10
        x = self.amtdic[risky]['x']
        t = 'today'
        lab = "{}% chance of receiving {} {}."

        l1 = tk.Label(master, text = lab.format(p, x, t),font = ("Arial", 17))
        l1.grid(row = 0, sticky = 'S', column = coln)
        return l1


    def make_progress_buttons(self, master, prob):
        bt = tk.Button(master, text = prob, state = 'disabled')
        bt.grid(row = 0,column = int(prob*10))
        self.buttdic[prob]['bt'] = bt
        return None


    def make_back_button(self, master, probvar):
        probfix =  probvar.get()

        self.buttdic[float(probfix)/10]['prob'] = tk.IntVar()
        self.buttdic[float(probfix)/10]['prob'].set(probfix)

        use_prob = self.buttdic[float(probfix)/10]['prob']
        bt = self.buttdic[float(probfix)/10]['bt']
        bt.config(state = 'active',
                  command = lambda: self.go_back(use_prob))
       
        bt.grid(row = 0,column = probvar.get())
        bt.config(highlightcolor = "red")
      #  self.buttdic[float(probfix)/10]['bt'] = bt

        return None


    def go_back(self, probvar):
        print probvar.get()
        self.draw_bucket_frame(self.real_main, probvar)
        return None


    def draw_bucket_frame(self, master, probvar):
        self.main = self.make_main_bucket_frame(master, probvar)
        self.x0, self.R, self.x1, self.r = 150, 60, 400, 0

        self.frame_configs = { "left" : ( "blue", "purple", 0,
                                          self.x0, self.R) ,
                               "right" : ( "green", "orange", 1,
                                           self.x1, self.r) }

        self.x, self.y = [self.make_side(self.main, prosp, prospc,
                                         probvar.get())
                          for prosp, prospc in self.frame_configs.items()]
        self.make_choice_button(self.main, 'Left', 0, 'b1', probvar)
        self.make_choice_button(self.main, 'Right', 1, 'b2', probvar)

        self.make_text_label(self.main, 'left', probvar, 0)
        self.make_text_label(self.main, 'right', probvar, 1)

        new_bt = self.buttdic[float(probvar.get())/10]
        return None


    def go_next_prob(self, probvar):

        try:
            p = self.iprobs.next()
            print p
            probvar.set(p)
            self.make_back_button(self.back_frame, probvar)
            self.draw_bucket_frame(self.real_main, probvar)
            
        except StopIteration:
            self.end_change_choices()
            print "something?"
           
            
        return None


    def make_choice_button(self, master, risky, coln, cvar, probvar):
        sdic = {'Left': 'b1', 'Right':'b2'}
        self.cb = tk.Radiobutton(master,
                                 text = "Choose {}".format(risky),
                                 variable = self.radvar,
                                 command = lambda: self.fill_radio(probvar),
                                 value = cvar)
        self.cb.grid(row = 0, column = coln)
        return self.cb


    def fill_forward_list(self, p, j):
        if p > j:
            a.pdic[p]['b2'].select()

        return None

    def fill_back_list(self, p, j):
        if p < j:
            a.pdic[p]['b1'].select()

        return None

    def end_change_choices(self):
        end = endDialog(self.real_main)
        self.scale.config(state = 'active')

    def fill_radio(self, probvar):
        choice_bt =  self.radvar.get()
        d = float(probvar.get())/10
        d1 = round(d - 0.1, 1)

        self.mytestbutton = self.pdic[d][choice_bt]
        self.mytestbutton.select()
        a1 = self.pdic[d]['var'].get()

        try:
            self.prevtestbutton = self.pdic[d1][choice_bt]
            a2 = self.pdic[d1]['var'].get()
        except KeyError:
            if self.pdic[d]['var'].get() == 2:
                rational = rationalDialog(self.real_main)
    
        if a1 == 2:
            j = d
            print j
            self.a = myDialog(self.real_main)
            [self.fill_forward_list(k, j) for k in self.probs]
            self.end_change_choices()
        else:
            pass

        return None


    def single_choice(self, master, p):
        cdic = self.pdic[p]

        cdic['bt'] = tk.Frame(master)
        frame = cdic['bt']
        cdic['var'] = tk.IntVar(frame)

        cdic['v1'] = 1
        cdic['v2'] = 2


        cdic['b1'], cdic['b2'] = self.make_buttons(cdic['var'],
                                                   cdic['v1'],
                                                   cdic['v2'],
                                                   cdic['bt'], p)
        return None



    def make_buttons(self, var, val1, val2, frame, p):
        frame.grid(row = int(p*10))
        choice = "( {} , {} ; {} )"
        [x0, x1, y0, y1] = [80, 400, 40, 10]
        # text_A = choice.format(x1,p,y1)
        # text_B =  choice.format(x0,p,y0)

        text_A = "left"
        text_B = "right, {}".format(p)

        a1 = tk.Radiobutton(frame,
                            text = text_A,
                            variable = var, value = val1,
                            state = 'disabled')
        a2 = tk.Radiobutton(frame,
                            text = text_B,
                            variable = var, value = val2,
                            state = 'disabled')

        a1.grid(row = 0, column=1)
        a2.grid(row = 0 , column=3)

        return a1, a2



    def make_main_bucket_frame(self, master, probvar):
        # main frame to hold everything
        pval = float(probvar.get())/10
        self.main = tk.LabelFrame( self.real_main,
                                   text = 'probability = {}'.format(pval))
        self.main.grid(row = 0, column = 0, sticky = 'nswe')
        self.main.columnconfigure(0, weight = 1)
        self.main.columnconfigure(1, weight = 1)
        self.main.rowconfigure(0, weight = 1)
        self.main.rowconfigure(1, weight = 1)

        return self.main



    def make_side(self, master, prosp, prospc, p):

        coln = prospc[2]
        x = prospc[3]
        r = prospc[4]
        bgs = dict( zip( ("high", "low"), prospc[0:2] ) )

        self.lf = self.make_risk_frame(master, prosp, coln)
       # self.set_bg(self.lf)
        self.evf = self.make_envelope_frame(self.lf)
        self.high, self.low = [self.make_high_low_frame(self.evf, c)
                               for c in range(2)]
        self.draw_envelopes(p, x, r, self.high, self.low, bgs)
        return None

    def make_risk_frame(self, master, risky, coln):
        self.f = tk.Frame(master)  #, text = risky)
        self.f.grid(row = 1, column = coln, padx = 2, pady = 2, sticky = 'nswe')
        self.f.columnconfigure(0, weight = 1)
        self.f.rowconfigure(1, weight = 1)
        return self.f

    def set_bg(self, master, image = "bucket.gif"):
        bg_img0 = Image.open(image)
        # bg_img1 = bg_img0.crop((0, 0, 10, 0))
        bg_img2 = bg_img0.resize((380, 480), Image.ANTIALIAS)
        bg_img = ImageTk.PhotoImage(bg_img2)

        bg = tk.Label(master, image = bg_img)
        bg.image = bg_img
        bg.place(relx = 0, rely = 1, anchor = 'sw')
        return bg

    def make_envelope_frame(self, master):
        self.f = tk.Frame(master)
        self.f.grid(row = 3, sticky = 'S', pady = 40)
        return self.f

    def make_high_low_frame(self, master, coln):
        self.f = tk.Frame(master)
        self.f.grid(row = 1, sticky = 'S',
                    column = coln, padx = 3, pady = 3)
        return self.f


    def get_envelope_pic(image = "envelope.gif"):
        env_img0 = Image.open("envelope.gif")
        env_img1 = env_img0.resize((70, 35), Image.ANTIALIAS)
        env_img = ImageTk.PhotoImage(env_img1)
        return env_img

    def calc_probs(self, n):
        high_left = min(5, n)
        high_right = max(0, n - 5)
        low_left = max(0, 5 - n)
        low_right = min(5, 10 - n)
        return  high_left, low_right, low_left, high_right

    def calc_envelopes(self, p, x, r, safe, risky):
        probs = self.calc_probs(p)
        frames = [safe, risky]
        amounts = [x, r]
        hl = ['high', 'low', 'low', 'high']

        env_configs = zip(frames*2, probs, hl,
                          amounts + list(reversed(amounts)))

        return env_configs

    def draw_envelopes(self, p, x, r, safe, risky, bgs):
        env_configs = self.calc_envelopes(p, x, r, safe, risky)
        [self.show_env(frame, p, lcol, amt, bgs)
         for frame, p, lcol, amt in env_configs]

        return None

    def show_text_prospects(self, master):
        self.tab1 = tk.Label(self.left, text = ' ')

    def show_env(self, master, p, lcol, amt, bgs):

        for i in range(p):
            self.imgframe = tk.Frame(master, bg = bgs[lcol])
            self.imgframe.grid(pady = 1)

            self.l1 = tk.Label(self.imgframe, image = self.env_img,
                               text = 'Rs {}'.format(amt),
                               compound = tk.CENTER, bd = 0)
            self.l1.image = self.env_img
            self.l1.grid(padx = 3, pady = 3, sticky = 'N')

        return None


    def get_pic(image = "arrow.png"):
        env_img0 = Image.open('arrow.png')
        env_img1 = env_img0.resize((70, 35), Image.ANTIALIAS)
        env_img = ImageTk.PhotoImage(env_img1)
        return env_img

    def go_next(self, master):
        self.left_arrow = self.get_pic()
        self.gonext = tk.Label(image = self.left_arrow)
        self.gonext.image = self.left_arrow
        self.gonext.grid(row = 1, sticky = 'S')

        return self.gonext


root = tk.Tk()
root.rowconfigure(0, weight = 1)
root.columnconfigure(0, weight = 1)
root.minsize(1020, 500)
root.geometry('+900+500')
a = Elicitation(root)
#root.mainloop()
print 'bob'
