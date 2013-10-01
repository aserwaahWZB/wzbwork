import timeMethods as tm
import Tkinter as tk
import Image, ImageTk
from collections import namedtuple
print "finished import"


class MainGraphic(tm.TimeMethods):

    def __init__(self, master, config, pdic, p):
        tk.Frame.__init__(self, master)
        self.grid()
        
        self.problist = pdic.keys()
        self.pdic = pdic
        self.p = p
         
       # Setting up the images
        self.env_img = self.get_envelope_pic()

        # Dealing with the buckets
        
        self.tpv = tk.IntVar()
        self.tpv.set(self.p)

        print self.tpv.get() +5

        self.config = config
        

        self.buttons = self.draw_bucket_frame(master, self.p, config)


        # Defne message texts
        self.rational = "Are you sure you want to make this decision?"
        self.switch = ("You just selected the lottery on the right." 
                       "Would you like to enforce this choice for" 
                       "all your future decisions?")
        self.endmsg = ("Thank you for completing your choices." 
                       "If you wish, you will now have the opportunity" 
                       "to adjust any choices using the sliding bar" 
                       "on the left.")




    def draw_bucket_frame(self, master, probvar, config):
   
        graph_frame = self.make_main_frame(master, probvar)

        side = { "left" : ("left", "blue", "purple", 0),
                 "right" : ( "right", "green", "orange", 1)}
       
        side_spec = namedtuple('Side', 'side colh coll coln x r')
        
        left_attr = side_spec._make(side['left'] 
                                    + (self.config['x0'], self.config['r']))
       
        right_attr = side_spec._make(side['right'] 
                                     + (self.config['x1'], self.config['R']))
        
        attributes = (left_attr, right_attr)

        left, right = [self.make_side(graph_frame, attrs, probvar) 
                       for attrs in attributes]
  
        return left, right
    
  
       
    def make_side(self, master, attrs, probvar):
        
        side = attrs.side
        coln = attrs.coln
        x = attrs.x
        r = attrs.r
        bgs = dict( zip( ("high", "low"), (attrs.colh, attrs.coll) ) )
        
        side_frame = self.make_risk_frame(master, side, coln)
        # self.set_bg(self.lf)
        
        ev_frame = tk.Frame(side_frame)
        ev_frame.grid(row = 3, sticky = 'S', pady = 10)
        
        high, low = [self.make_high_low_frame(ev_frame, c)
                     for c in [1,2]]
        
        self.draw_envelopes(ev_frame, probvar, x, r, high, low, bgs)
        self.make_global_text_label(side_frame, x, probvar)
        bt = self.make_global_choice_button(side_frame, side, probvar)

        return bt




    def make_global_choice_button(self, master, side, probvar):
     #   gcdic = {'Left': 'b1', 'Right':'b2'}

        gcvar = self.pdic[probvar]['aglobal']['var']
        gcval = self.pdic[probvar]['aglobal'][side]
        
        cb = tk.Radiobutton(master,
                            text = "Choose {}".format(side),
                            variable = gcvar,
                            command = lambda: self.fill_radio(probvar),
                            value = gcval)
        cb.grid(row = 0)
        return cb


    def make_global_text_label(self, master, high, probvar):
        
        p = int(probvar * 100)
        x = high
        t = 'today'
        lab = "{}% chance of receiving {} {}."
        
        l1 = tk.Label(master, 
                      text = lab.format(p, x, t),font = ("Arial", 17))
        l1.grid(row = 1, sticky = 'S')
        return l1
            
    
        
        
    def make_main_frame(self, master, probvar):
        # main frame to hold everything
        pval = probvar
        self.main = tk.LabelFrame(master,
                                  text = 'probability = {}'.format(pval))
        self.main.grid(row = 1, column = 0, sticky = 'nswe')
        self.main.columnconfigure(0, weight = 1)
        self.main.columnconfigure(1, weight = 1)
        self.main.rowconfigure(0, weight = 1)
        self.main.rowconfigure(1, weight = 1)
        
        return self.main
        
        
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
            
    def calc_probs(self, p):
        n = int(p * 20)
        
        high_left = min(10, n)
        high_right = max(0, n - 10)
        low_left = max(0, 10 - n)
        low_right = min(10, 20 - n)
        return  high_left, low_right, low_left, high_right
    

    def calc_envelopes(self, p, x, r, safe, risky):
        probs = self.calc_probs(p)
        frames = [safe, risky]
        amounts = [x, r]
        hl = ['high', 'low', 'low', 'high']
            
        env_configs = zip(frames*2, probs, hl,
                          amounts + list(reversed(amounts)))
        
        return env_configs

    def make_ball(self, master, i):
        c1 = tk.Canvas(master, height = 36, width = 36)
        c1.create_text(20,20, 
                            text = '{}'.format(i), 
                       font = ("Helvetica", 10),
                       anchor = 'center')
        
        c1.grid(sticky = 'N')
        return c1


    def draw_envelopes(self, master, probvar, x, r, safe, risky, bgs):
        p = probvar
        env_configs = self.calc_envelopes(p, x, r, safe, risky)
        balls = dict([(i, self.make_ball(i)) for
                      i in range(0,20)])
        [self.show_ball(master, p, lcol, amt, bgs) 
         for master, p, lcol, amt in env_configs]
        
        return None

    def show_ball(self, master, p, lcol, amt, bgs):

        r = iter(range(p))
        for i in range(p):
            f = r.next()
            self.c1 = tk.Canvas(master, height = 36, width = 36)
            self.c1.create_oval(7, 7, 36, 36, fill = bgs[lcol])
            self.c1.create_text(20,20, 
                                text = '{}'.format(f), 
                                font = ("Helvetica", 10),
                                anchor = 'center')
           
            self.c1.grid(sticky = 'N')
           
        return None


    def show_env(self, master, p, lcol, amt, bgs):

        for i in range(p):
            print "this is i", i
            self.imgframe = tk.Frame(master, bg = bgs[lcol])
            self.imgframe.grid(pady = 1)

            self.l1 = tk.Label(self.imgframe, image = self.env_img,
                               text = 'Rs {}'.format(amt),
                               compound = tk.CENTER, bd = 0)
            self.l1.image = self.env_img
            self.l1.grid(padx = 3, pady = 3, sticky = 'N')
            
        return None


class ChoiceList(tm.TimeMethods):

    def __init__(self, master, pdic):
        tk.Frame.__init__(self, master)
        self.grid()

        self.pdic = pdic
        self.problist = self.pdic.keys()

        self.cl_frame = tk.LabelFrame(master,
                                      text = 'Choice History')
        self.cl_frame.grid(row = 1, column = 2)


        for p in self.problist:
            self.single_choice(self.cl_frame, p)


        self.scale = tk.Scale(self.cl_frame,
                              from_ = 0, to = 10,
                              length = 300, state = 'disabled')

        self.scale.grid(row = 0, rowspan = 11, column = 1)
        self.scale.bind('<ButtonRelease-1>', self.adjust_choices)


    def single_choice(self, master, p):
        cdic = dict()

        cdic['bt_frame'] = tk.Frame(master)
        cdic['var'] = tk.IntVar(cdic['bt_frame'])
        cdic['v1'] = 1
        cdic['v2'] = 2


        cdic['b1'], cdic['b2'] = self.make_buttons(cdic['var'],
                                                   cdic['v1'],
                                                   cdic['v2'],
                                                   cdic['bt_frame'], p)
        self.pdic[p]['choice'] = cdic
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


class ProgressBar(tm.TimeMethods):

    def __init__(self, master, pdic):
        tk.Frame.__init__(self, master)
        self.grid()

        self.pdic = pdic
        self.problist = pdic.keys()

        self.prog_frame = tk.Frame(master)
        self.prog_frame.grid(sticky = 'sw')

        self.prog_label = tk.Label(self.prog_frame,
                                   text = "Progress")
        self.prog_label.grid(row = 0, column = 0, sticky = 'w', pady = 4)

        self.prog_buttons = tk.Frame(self.prog_frame)
        self.prog_buttons.grid( row = 0, column = 1)

     
        [self.make_progress_buttons(self.prog_buttons, p) for p in self.problist]


    def make_progress_buttons(self, master, prob):
        bt = tk.Button(master, text = prob, state = 'disabled')
        bt.grid(row = 0, column = int(prob*10))
        self.pdic[prob]['progress'] = bt
        return None


def test_run(p):
    root = Tk()
    fred = MainGraphic(root,  
                       { 'x0': 300, 'x1': 500, 'R': 10, 'r':4 }, d, p)

    return fred
