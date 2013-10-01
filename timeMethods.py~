import Tkinter as tk
import tkSimpleDialog as dialog

class TimeMethods(tk.Frame):

    def __init__(self, master, pdic):
        self.problist = pdic.keys()
        self.pdic = pdic


    def adjust_choices(self, event):
        prob = float(self.scale.get())/10
        adj = self.pdic[prob]['choice']['b1'].select()

        [self.fill_forward_list(k, prob) for k in self.problist]
        [self.fill_back_list(k, prob) for k in self.problist]

        return None

    def go_back(self, probvar):
        print probvar.get()
        self.draw_bucket_frame(self.real_main, probvar)
        return None

    def fill_forward_list(self, p, j):
        if p > j:
            self.pdic[p]['choice']['b2'].select()

        return None

    def fill_back_list(self, p, j):
        if p < j:
            self.pdic[p]['choice']['b1'].select()

        return None


    def end_change_choices(self):
        end_dialog = dialog.askstring(
            "You will now be given the chance to review your answers.", 
            "Please click OK to continue.")
        self.choice_list.scale.config(state = 'active')
        return None


    def fill_radio(self, probvar):
        print 'mongoose'      
        d = probvar
        cdic = self.pdic[d]['choice']
        choice_bt =  self.pdic[d]['aglobal']['var'].get()
        
        d1 = round(d - 0.1, 1)
        
        print cdic
        print choice_bt
        

        selected_button = cdic[choice_bt]
        selected_button.select()

        c_var = cdic['var'].get()
        print "this is the var:", c_var

        try:
            prev_button = self.pdic[d1]['choice']
            prev_var = self.pdic[d1]['choice']['var'].get()

            if c_var == 2:
                if prev_var == 1:
                    switch_dialog = dialog.askstring(
                        "Message.", 
                        """You just selected the right option. 
                        Would you like to enforce this choice 
                        for your remaining decisions?""")
                    [self.fill_forward_list(k, d) for k in self.problist]
                       
        except KeyError:
            if cdic['var'].get() == 2:
                rational_dialog = dialog.askstring(
                    "Message.", 
                    " Are you sure of this decision?")
       
    
                
        return None

