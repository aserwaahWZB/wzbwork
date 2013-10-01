import Tkinter as tk
import tkSimpleDialog as dialog


class TimeMethods(tk.Frame):

    def __init__(self, master, pdic):
        self.master = master
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
    
    def do_fill(self, p):
        [self.fill_forward_list(k, p) for k in self.problist]
        print "What next?"
        self.end_change_choices()

    def enable_change(self):
       
        pname = self.winfo_parent()
        parent = self._nametowidget(pname)
        choice_list = parent.winfo_children()[0]
        choice_list.scale.config( state = "active")
       

        main_graphic = parent.winfo_children()[-5]
        [button.configure(state = 'disabled')
         for button in main_graphic.buttons]

        [self.pdic[p]['progress'].configure( state = 'active') 
         for p in self.problist ]


    def end_change_choices(self):
        end_dialog = TimeDialog(self.master,
                                text = self.endmsg,
                                function = self.enable_change)

        return None

    def do_rationality(self):
        rational_switch_dialog = TimeDialog(self.master,
                                            text = self.switch,
                                            function = self.do_fill, p = 0)



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
                    switch_dialog = TimeDialog(self.master,
                                               text = self.switch,
                                               function = self.do_fill, p = d)

                    
                       
        except KeyError:
            if cdic['var'].get() == 2:
                rational_dialog = TimeDialog(self.master, 
                                             text = self.rational,
                                             function = self.do_rationality)
                
        return None


class TimeDialog(dialog.Dialog):

    def __init__(self, parent, text, function, **kwargs):
        self.mytext = text
        self.fun = function
        self.amevaluate = kwargs

        dialog.Dialog.__init__(self, parent)
     
    def perform(self, fun, **kwargs):
        fun( **kwargs)

    def body(self, parent):
        tk.Label(parent, text = self.mytext).grid(row=1)

    def apply(self):
        self.perform(self.fun, **self.amevaluate)
