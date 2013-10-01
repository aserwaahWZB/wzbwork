import timeMethods

class ChoiceList(TimeMethods):

    def __init__(self, master, pdic):
        tk.Frame.__init__(self, master)
        self.grid()

        self.pdic = pdic
        self.problist = self.pdic.keys()

        self.cl_frame = tk.LabelFrame(master,
                                      text = 'Choice History and Mangos')
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

#root = Tk()
#ChoiceList(root)
