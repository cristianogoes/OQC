from tkinter import *
import tkinter.messagebox
import pandas as pd
import Comunicacao, ScannerFile, sys
import threading
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches


########################################################################
class screenOQC(threading.Thread):
    def __init__(self, parent):
        """Constructor"""
        self.root = parent

        self.x1 = 0
        self.x2 = 0
        self.loop_active_w = True
        self.loop_active_r = False
        self.loop_new = True
        self.statusRun = True
        self.seconds = 0
        self.num_apr = 0
        self.num_rep = 0

        self.label2 = Label(self.root, text="Hello", font="Arial 30", width=10)
        # self.label2.pack()
        self.label = Label(self.root, text="0 s", font="Arial 30", width=10)
        # self.label.pack()
        self.label1 = Label(self.root, text=">>> 0 s", font="Arial 30", width=10)
        # self.label1.pack()

        self.label.after(1000, self.refresh_label)

        self.root.title("Outgoing Quality C")
        self.root.maxsize(width=800, height=600)
        self.root.minsize(width=800, height=600)
        self.frame = Frame(parent)
        self.frame.pack()

        self.center()
        self.root.resizable(0,0)
        self.root.protocol('WM_DELETE_WINDOW', self.disableX)

        self.menuOQC()
        self.toolbarOQC()
        self.statusBarOQC()
        self.dashboard()
        self.graphPie()
        self.graph2()
        self.frame3()
        self.oqcIni()

        threading.Thread.__init__(self)
        threading.Thread(target=self.run)
        self.daemon = True

        self.start()

    def screenGUI(self):
        screenConfiguration(self.root)

    def screenReport(self):
        screenConfiguration(self.root)

    def menuOQC(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)

        subMenu = Menu(menu, tearoff=0)
        menu.add_cascade(label='File', menu=subMenu)
        subMenu.add_command(label='Configuration', command=self.screenGUI)
        subMenu.add_command(label='Report', command=self.screenReport)
        subMenu.add_separator()
        subMenu.add_command(label='Quit', command=self.h0)

        helpMenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=helpMenu)
        helpMenu.add_command(label="About", command=self.aboutICCT)

    def toolbarOQC(self):
        toolbar = Frame(self.root)

        btn = Button(toolbar, text="Reconnect", command=self.doNothing)
        btn.pack(side=LEFT, padx=2, pady=2)
        confButton = Button(toolbar, text='Configuration', command=self.screenGUI)
        confButton.pack(side=LEFT, padx=2, pady=2)
        reportButton = Button(toolbar, text='Report', command=self.screenReport)
        reportButton.pack(side=LEFT, padx=2, pady=2)
        exitButton = Button(toolbar, text='Exit', command=self.h0)
        exitButton.pack(side=RIGHT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=X)

    def statusBarOQC(self):
        self.status = Label(self.root, bd=1, relief=SUNKEN, anchor=W)
        #status = Label(self.root, text="Preparing to do nothing.....", bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM,fill=X)

    def scale_image(self,input_image_path, output_image_path, width=None, height=None):
        original_image = Image.open(input_image_path)
        w, h = original_image.size
        print('The original image size is {wide} wide x {height} '
              'high'.format(wide=w, height=h))

        if width and height:
            max_size = (width, height)
        elif width:
            max_size = (width, h)
        elif height:
            max_size = (w, height)
        else:
            # No width or height specified
            raise RuntimeError('Width or height required!')

        original_image.thumbnail(max_size, Image.ANTIALIAS)
        original_image.save(output_image_path)

        scaled_image = Image.open(output_image_path)
        width, height = scaled_image.size
        print('The scaled image size is {wide} wide x {height} '
              'high'.format(wide=width, height=height))

    def dashboard(self):
        dashboard = Frame(self.root)

        canvas1 = Canvas(dashboard, width=173, height=100, bg='red')
        canvas1.pack(side=LEFT,padx=2, pady=2)

        self.scale_image(input_image_path='ICCT.png', output_image_path='ICCT_scaled.png', width=200, height=100)

        imagem = tkinter.PhotoImage(file="ICCT_scaled.png")
        img = Label(canvas1, image=imagem)
        img.imagem = imagem
        img.pack(side=LEFT, fill="both", expand="yes")

        a = "OP: PRODUTO A"
        b = "Tempo Padrão: 20,0 s"
        c = "Operadores 3"
        d = "OQC"

        aa = a + "\n" + b + "\n" + c

        status1 = Label(dashboard, width=45, height=6, bg="#759FCB", bd=1, relief=FLAT,font=('Arial', 12), anchor=CENTER)
        status1.pack(side=LEFT, pady=2, padx=2)
        maqnome = Label(dashboard, width=25, height=6, bg="#CE7634", bd=1, relief=FLAT,font=('Arial', 12), anchor=CENTER)
        maqnome.pack(side=LEFT, pady=2, padx=2)

        status1.configure(text="%s" % aa)
        maqnome.configure(text="%s" % d)

        dashboard.pack(side=TOP,fill=X)

    def aboutICCT(self):
        tkinter.messagebox.showinfo('About', """
        Instituto Cal-Comp de Pesquisa e Inovação Tecnologia
        CNPJ: 21.640.591/0001-31
        Address: 7503, Torquato Tapajós Avenue, Tarumã
        Postal Code: 69041-025

        Version 1.0
        Created by Cristiano Goes & Evandro Duarte""")

    def doNothing(self):
        print("ok ok I won't....")

    def h0(self):
        answer = tkinter.messagebox.askquestion('Question', 'Deseja realmente sair?')

        if answer == 'yes':
            self.root.destroy()
            sys.exit()

    def center(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y-30))

    def disableX(self):
        pass

    def graphPie(self):
        self.frame2 = Frame(self.root)

        self.figure2 = plt.Figure(figsize=(4, 3), dpi=100)
        self.subplot2 = self.figure2.add_subplot(111)
        self.labels2 = ['APR', 'REP']
        self.colors = ['#11C724', '#EC2D0B']
        self.pieSizes = [self.x1, self.x2]
        self.explode2 = (0.01, 0.01)
        self.subplot2.pie(self.pieSizes, colors=self.colors, explode=self.explode2, labels=self.labels2, autopct='%1.1f%%', shadow=True,
                     startangle=90)
        self.subplot2.axis('equal')
        self.pie2 = FigureCanvasTkAgg(self.figure2, self.frame2)
        self.pie2.get_tk_widget().pack(side=LEFT)

        self.frame2.pack(side=TOP, fill=X)

    def graph2(self):

        self.labels = ['Produzido', 'Falta Produzir']
        self.sizes = [0, 100]
        self.colors2 = ['#17C627', '#D2E5D4']
        self.explode = (0.05, 0.05)
        #self.labels = ['Frogs', 'Hogs', 'Dogs', 'Logs']
        #self.sizes = [15, 30, 45, 10]
        #self.colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
        #self.explode = (0.05, 0.05, 0.05, 0.05)

        self.figure3 = plt.Figure(figsize=(4, 3), dpi=100)
        self.subplot3 = self.figure3.add_subplot(111)
        self.subplot3.pie(self.sizes, colors=self.colors2, labels=self.labels, autopct='%1.1f%%', startangle=90, pctdistance=0.85, explode=self.explode)

        self.circle = matplotlib.patches.Circle((0, 0), 0.7, color='white')
        self.subplot3.add_artist(self.circle)

        self.subplot3.axis('equal')
        self.pie3 = FigureCanvasTkAgg(self.figure3, self.frame2)
        self.pie3.get_tk_widget().pack(side=LEFT)

    def frame3(self):
        fram3 = Frame(self.root, bg='white')
        status1 = Label(fram3, width=50, height=8,fg='white', text="Em Produção", bg="green", bd=1, relief=FLAT,
                        font=('Arial', 40), anchor=CENTER)
        status1.pack(pady=10, padx=10)
        fram3.pack(side=TOP, fill=X)

    def oqcIni(self):
        self.y =0

        df0 = []
        self.DFX0 = pd.DataFrame(df0)
        df6 = []
        self.DFX6 = pd.DataFrame(df6)
        df7 = []
        self.DFX7 = pd.DataFrame(df7)

        arrayJig = []
        self.dfArrayjig = pd.DataFrame(arrayJig, columns=['station', 'port', 'result'])

        self.seri = Comunicacao.ComSerial()
        self.t = self.seri.configSerial()
        print(self.t.name)

        #self.scanner = ScannerFile.Scandir(pathToWatch="C:\\Users\\bb8ga121\\Desktop\\TESTE_CHIP_IC")
        self.scanner = ScannerFile.Scandir(pathToWatch="C:\OQC")
        self.scanner.configPath()

    def oqcNewFile(self):
        newFile = self.scanner.scannerFile()

        if newFile:
            ii = 0
            for ii in range(len(newFile)):
                status_indice = self.scanner.readFile(newFile[ii], 3)[0:1]
                error_codigo = self.scanner.readFile(newFile[ii], 4)
                status_test = self.scanner.readFile(newFile[ii], 5)
                station = self.scanner.readFile(newFile[ii], 7)[1:2]
                porta = newFile[ii][(len(newFile[ii]) - 5):(len(newFile[ii]) - 4)]

                self.dfArrayjig = self.dfArrayjig.append(pd.Series([station, porta, status_indice], index=self.dfArrayjig.columns),
                                               ignore_index=True)
                ii += 1

        self.X6 = self.dfArrayjig[self.dfArrayjig['station'] == '6'].copy()
        self.X7 = self.dfArrayjig[self.dfArrayjig['station'] == '7'].copy()

        if self.X6.station.count() == 4:
            self.X6 = self.X6.sort_values(by=['port'])
            self.DFX6 = self.X6['station'].map(str) + self.X6['port'].map(str) + self.X6['result'].map(str)
            self.DFX6 = self.DFX6.reset_index(drop=True)
            self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '6'].index, inplace=True)
        if self.X7.station.count() == 4:
            self.X7 = self.X7.sort_values(by=['port'])
            self.DFX7 = self.X7['station'].map(str) + self.X7['port'].map(str) + self.X7['result'].map(str)
            self.DFX7 = self.DFX7.reset_index(drop=True)
            self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '7'].index, inplace=True)

        frames = [self.DFX0, self.DFX6, self.DFX7]
        self.X1 = pd.concat(frames)
        self.X1 = self.X1.reset_index(drop=True)
        print('Database para envio')
        print(self.X1)

        if self.DFX6.size:
            self.DFX6 = self.DFX6.drop([0, 1, 2, 3], axis=0)
        if self.DFX7.size:
            self.DFX7 = self.DFX7.drop([0, 1, 2, 3], axis=0)
        if self.X1.size:
            self.y = self.X1.size
            self.yy = 0
            self.loop_new = False
            self.refresh_label1()

    def run(self):
        while self.statusRun:
            while self.loop_active_r:
                self.out=''
                self.out = self.t.readline()
                if self.out != '':
                    self.label2.configure(text="%s" %self.seconds)
                    self.loop_active_w = True
                    self.loop_active_r = False
                    self.yy += 1
                    #self.root.update()
                    self.label1.after(2000, self.refresh_label1)

    def refresh_label(self):
        """ refresh the content of the label every second """
        self.seconds += 1
        total = 8

        ee = 'APROVADO: ' + str(self.num_apr) + ' - REPROVADO: ' + str(self.num_rep)
        ee = ee + ' --- PRODUZIDO: ' + str(self.num_apr) + ' - FALTA PRODUZIR: ' + str(total - self.num_apr)
        self.label.configure(text="%i s" % self.seconds)
        self.status.configure(text="%s" % ee)

        self.subplot2.clear()
        self.subplot2.pie([self.x1, self.x2],colors=self.colors, explode=self.explode2, labels=self.labels2, autopct='%1.1f%%', shadow=True,
                          startangle=90)
        self.figure2.canvas.draw_idle()

        val = self.num_apr
        val1 = (val*100)/total
        if val > total:
            val1 = 100

        self.subplot3.clear()
        self.subplot3.pie([val1, 100 - val1], colors=self.colors2, labels=self.labels, autopct='%1.1f%%', startangle=90,
                          pctdistance=0.85, explode=self.explode)
        self.circle = matplotlib.patches.Circle((0, 0), 0.7, color='white')
        self.subplot3.add_artist(self.circle)
        self.subplot3.axis('equal')
        self.figure3.canvas.draw_idle()

        if self.loop_new:
            self.oqcNewFile()

        self.label.after(1000, self.refresh_label)

    def refresh_label1(self):
        """ refresh the content of the label every second """
        if self.loop_active_w:
            if self.X1.size:
                    self.wwww = self.X1[0][self.yy]
                    print("Valor a ser enviado: ", self.wwww)
                    self.X1 = self.X1.drop([self.yy], axis=0)
                    self.seri.serialWrite(self.wwww)
                    self.label1.configure(text="%s" % self.wwww)
                    self.loop_active_w = False
                    self.loop_active_r = True
                    if self.wwww[2:3] =="P":
                        self.num_apr += 1
                        self.x1 = self.num_apr
                        print("x1: ",self.x1)
                    else:
                        self.num_rep += 1
                        self.x2 = self.num_rep
                        print("x2: ",self.x2)
            else:
                self.loop_new=True


# ----------------------------------------------------------------------
class cTimer(threading.Thread):
    def __init__(self,parent):

        self.root = parent
        self.oqcIni()

        self.loop_active_w = True
        self.loop_active_r = False
        self.loop_new = True
        self.statusRun = True
        self.seconds = 0

        self.label2 = Label(self.root, text="Hello", font="Arial 30", width=10)
        #self.label2.pack()
        self.label = Label(self.root, text="0 s", font="Arial 30", width=10)
        #self.label.pack()
        self.label1 = Label(self.root, text=">>> 0 s", font="Arial 30", width=10)
        #self.label1.pack()

        self.canvas = Canvas(self.root, width=200, height=100)
        self.canvas.pack()

        self.label.after(1000, self.refresh_label)

        threading.Thread.__init__(self)
        threading.Thread(target=self.run)
        self.daemon = True

        self.start()

    def oqcIni(self):
        self.y =0

        df0 = []
        self.DFX0 = pd.DataFrame(df0)
        df6 = []
        self.DFX6 = pd.DataFrame(df6)
        df7 = []
        self.DFX7 = pd.DataFrame(df7)

        arrayJig = []
        self.dfArrayjig = pd.DataFrame(arrayJig, columns=['station', 'port', 'result'])

        self.seri = Comunicacao.ComSerial()
        self.t = self.seri.configSerial()
        print(self.t.name)

        self.scanner = ScannerFile.Scandir(pathToWatch="C:\\Users\\bb8ga121\\Desktop\\TESTE_CHIP_IC")
        self.scanner.configPath()

    def oqcNewFile(self):
        newFile = self.scanner.scannerFile()

        if newFile:
            ii = 0
            for ii in range(len(newFile)):
                status_indice = self.scanner.readFile(newFile[ii], 3)[0:1]
                error_codigo = self.scanner.readFile(newFile[ii], 4)
                status_test = self.scanner.readFile(newFile[ii], 5)
                station = self.scanner.readFile(newFile[ii], 7)[1:2]
                porta = newFile[ii][(len(newFile[ii]) - 5):(len(newFile[ii]) - 4)]

                self.dfArrayjig = self.dfArrayjig.append(pd.Series([station, porta, status_indice], index=self.dfArrayjig.columns),
                                               ignore_index=True)
                ii += 1

        self.X6 = self.dfArrayjig[self.dfArrayjig['station'] == '6'].copy()
        self.X7 = self.dfArrayjig[self.dfArrayjig['station'] == '7'].copy()

        if self.X6.station.count() == 4:
            self.X6 = self.X6.sort_values(by=['port'])
            self.DFX6 = self.X6['station'].map(str) + self.X6['port'].map(str) + self.X6['result'].map(str)
            self.DFX6 = self.DFX6.reset_index(drop=True)
            self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '6'].index, inplace=True)
        if self.X7.station.count() == 4:
            self.X7 = self.X7.sort_values(by=['port'])
            self.DFX7 = self.X7['station'].map(str) + self.X7['port'].map(str) + self.X7['result'].map(str)
            self.DFX7 = self.DFX7.reset_index(drop=True)
            self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '7'].index, inplace=True)

        frames = [self.DFX0, self.DFX6, self.DFX7]
        self.X1 = pd.concat(frames)
        self.X1 = self.X1.reset_index(drop=True)
        print('Database para envio')
        print(self.X1)

        if self.DFX6.size:
            self.DFX6 = self.DFX6.drop([0, 1, 2, 3], axis=0)
        if self.DFX7.size:
            self.DFX7 = self.DFX7.drop([0, 1, 2, 3], axis=0)
        if self.X1.size:
            self.y = self.X1.size
            self.yy = 0
            self.loop_new = False
            self.refresh_label1()

    def run(self):
        while self.statusRun:
            while self.loop_active_r:
                self.out=''
                self.out = self.t.readline()
                if self.out != '':
                    self.label2.configure(text="%s" %self.seconds)
                    self.loop_active_w = True
                    self.loop_active_r = False
                    self.yy += 1
                    #self.root.update()
                    self.label1.after(2000, self.refresh_label1)

    def refresh_label(self):
        """ refresh the content of the label every second """
        self.seconds += 1
        self.label.configure(text="%i s" % self.seconds)
        if self.loop_new:
            self.oqcNewFile()
        self.label.after(1000, self.refresh_label)

    def refresh_label1(self):
        """ refresh the content of the label every second """
        if self.loop_active_w:
            if self.X1.size:
                    self.wwww = self.X1[0][self.yy]
                    print("Valor a ser enviado: ", self.wwww)
                    self.X1 = self.X1.drop([self.yy], axis=0)
                    self.seri.serialWrite(self.wwww)
                    self.label1.configure(text="%s" % self.wwww)
                    self.loop_active_w = False
                    self.loop_active_r = True
                    if self.wwww[2:3] =="P":
                        self.canvas.create_rectangle(25, 25, 130, 60, fill='green')
                    else:
                        self.canvas.create_rectangle(25, 25, 130, 60, fill='red')
            else:
                self.loop_new=True


# ----------------------------------------------------------------------
class screenConfiguration(object):
    def __init__(self,parent):
        """Constructor"""
        self.screenRoot = parent
        self.hide(self.screenRoot)

        self.otherFrame = Toplevel()
        self.otherFrame.geometry("400x300")
        self.otherFrame.title("otherFrame")

        self.center(self.otherFrame)
        self.otherFrame.resizable(0, 0)
        self.otherFrame.protocol('WM_DELETE_WINDOW', self.disableX)

        handler = lambda: self.onCloseOtherFrame(self.screenRoot,self.otherFrame)
        btn = Button(self.otherFrame, text="Close", command=handler)
        btn.pack()

        # variable storing time
        self.seconds = 0
        # label displaying time
        self.label = Label(self.otherFrame, text="0 s", font="Arial 30", width=10)
        self.label.pack()
        # start the timer
        self.label.after(1000, self.refresh_label)

    def center(self,parent):
        screen = parent
        screen.update_idletasks()
        width = screen.winfo_width()
        height = screen.winfo_height()
        x = (screen.winfo_screenwidth() // 2) - (width // 2)
        y = (screen.winfo_screenheight() // 2) - (height // 2)
        screen.geometry('{}x{}+{}+{}'.format(width, height, x, y-30))

    def disableX(self):
        pass

    def hide(self,parent):
        parent.withdraw()

    def onCloseOtherFrame(self, parent,otherFrame):
        """"""
        otherFrame.destroy()
        self.show(parent)

    def show(self,parent):
        """"""
        parent.update()
        parent.deiconify()

    def refresh_label(self):
        """ refresh the content of the label every second """
        # increment the time
        self.seconds += 1
        # display the new time
        self.label.configure(text="%i s" % self.seconds)
        # request tkinter to call self.refresh after 1s (the delay is given in ms)
        self.label.after(1000, self.refresh_label)


if __name__ == "__main__":
    root = Tk()
    app = screenOQC(root)
    root.mainloop()