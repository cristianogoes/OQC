from tkinter import *
import tkinter.messagebox

########################################################################
class screenOQC(object):
    """"""
    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.title("Outgoing Quality C")
        self.root.maxsize(width=800, height=600)
        self.root.minsize(width=800, height=600)
        self.frame = Frame(parent)
        self.root.protocol('WM_DELETE_WINDOW', self.disableX)
        self.frame.pack()
        self.menuOQC()
        self.toolbarOQC()
        self.statusBarOQC()
        self.root.resizable(0,0)
        self.center()

    def disableX(self):
        pass
    # ----------------------------------------------------------------------
    def hide(self):
        """"""
        self.root.withdraw()

    # ----------------------------------------------------------------------
    def openFrame(self):
        """"""
        self.hide()
        otherFrame = Toplevel()
        otherFrame.geometry("400x300")
        otherFrame.title("otherFrame")
        otherFrame.resizable(0, 0)
        otherFrame.protocol('WM_DELETE_WINDOW', self.disableX)
        handler = lambda: self.onCloseOtherFrame(otherFrame)
        btn = Button(otherFrame, text="Close", command=handler)
        btn.pack()

    # ----------------------------------------------------------------------
    def onCloseOtherFrame(self, otherFrame):
        """"""
        otherFrame.destroy()
        self.show()

    # ----------------------------------------------------------------------
    def show(self):
        """"""
        self.root.update()
        self.root.deiconify()

    # ----------------------------------------------------------------------
    def menuOQC(self):
        """"""
        menu = Menu(self.root)
        self.root.config(menu=menu)

        subMenu = Menu(menu, tearoff=0)
        menu.add_cascade(label='File', menu=subMenu)
        subMenu.add_command(label='Configuration', command=self.openFrame)
        subMenu.add_command(label='Report', command=self.doNothing)
        subMenu.add_separator()
        subMenu.add_command(label='Quit', command=self.h0)

        helpMenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=helpMenu)
        helpMenu.add_command(label="About", command=self.aboutICCT)

    # ----------------------------------------------------------------------
    """"""
    def toolbarOQC(self):
        toolbar = Frame(self.root)

        btn = Button(toolbar, text="Reconnect", command=self.openFrame)
        btn.pack(side=LEFT, padx=2, pady=2)
        confButton = Button(toolbar, text='Configuration', command=self.doNothing)
        confButton.pack(side=LEFT, padx=2, pady=2)
        reportButton = Button(toolbar, text='Report', command=self.doNothing)
        reportButton.pack(side=LEFT, padx=2, pady=2)
        exitButton = Button(toolbar, text='Exit', command=self.h0)
        exitButton.pack(side=RIGHT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=X)

    def statusBarOQC(self):
        status = Label(self.root, text="Preparing to do nothing.....", bd=1, relief=SUNKEN, anchor=W)
        status.pack(side=BOTTOM,fill=X)

    # ----------------------------------------------------------------------
    """"""
    def aboutICCT(self):
        tkinter.messagebox.showinfo('About', """
        Instituto Cal-Comp de Pesquisa e Inovação Tecnologia
        CNPJ: 21.640.591/0001-31
        Address: 7503, Torquato Tapajós Avenue, Tarumã
        Postal Code: 69041-025

        Version 1.0
        Created by Cristiano Goes & Evandro Duarte""")

    # ----------------------------------------------------------------------
    """"""
    def doNothing(self):
        print("ok ok I won't....")

    # ----------------------------------------------------------------------
    """"""
    def h0(self):
        answer = tkinter.messagebox.askquestion('Question', 'Deseja realmente sair?')

        if answer == 'yes':
            exit()

    def center(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y-30))

# ----------------------------------------------------------------------
if __name__ == "__main__":
    root = Tk()
    app = screenOQC(root)
    root.mainloop()