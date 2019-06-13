from tkinter import *
import tkinter.messagebox
import pandas as pd
import Comunicacao, ScannerFile, sys
import threading
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches
from collections import deque


########################################################################
class screenOQC(threading.Thread):
    def __init__(self, parent):
        """Constructor"""
        self.root = parent

        self.x1 = 0
        self.x2 = 0

        self.input = True
        self.input_w = True
        self.input_r = False

        self.loop_new = False
        self.loop_active_w = False
        self.loop_active_r = False

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

        #self.label.after(1000, self.refresh_label)

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
        #self.oqcIni()

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

        btn = Button(toolbar, text="Connect", command=self.oqcIni)
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

        #self.scale_image(input_image_path='ICCT.png', output_image_path='ICCT_scaled.png', width=200, height=100)

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
        self.y = 0
        self.yy = 0

        df0 = []
        self.DFX0 = pd.DataFrame(df0)
        df1 = []
        self.DFX1 = pd.DataFrame(df1)
        df2 = []
        self.DFX2 = pd.DataFrame(df2)
        df3 = []
        self.DFX3 = pd.DataFrame(df3)
        df4 = []
        self.DFX4 = pd.DataFrame(df4)
        df5 = []
        self.DFX5 = pd.DataFrame(df5)
        df6 = []
        self.DFX6 = pd.DataFrame(df6)
        df7 = []
        self.DFX7 = pd.DataFrame(df7)
        df8 = []
        self.DFX8 = pd.DataFrame(df8)

        arrayJig = []
        self.dfArrayjig = pd.DataFrame(arrayJig, columns=['station', 'port', 'result'])

        inputJig =  [1,2,3,4,5,6,7,8]
        confJig = [0,0,1,0,0,0,0,1,1]
        self.dfInputJig = deque(inputJig)
        self.deqconfJig = deque(confJig)
        print(self.dfInputJig)

        self.seri = Comunicacao.ComSerial()
        self.t = self.seri.configSerial()
        #print(self.t.name)

        #self.ether = Comunicacao.ComEthernet()
        #self.ether.configEthernet()


        self.scanner = ScannerFile.Scandir(pathToWatch="C:\\Users\\bb8ga121\\Desktop\\TESTE_CHIP_IC")
        #self.scanner = ScannerFile.Scandir(pathToWatch="C:\\OQC")
        self.scanner.configPath()
        self.label.after(1000, self.refresh_label)

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

        self.X1 = self.dfArrayjig[self.dfArrayjig['station'] == '1'].copy()
        self.X2 = self.dfArrayjig[self.dfArrayjig['station'] == '2'].copy()
        self.X3 = self.dfArrayjig[self.dfArrayjig['station'] == '3'].copy()
        self.X4 = self.dfArrayjig[self.dfArrayjig['station'] == '4'].copy()
        self.X5 = self.dfArrayjig[self.dfArrayjig['station'] == '5'].copy()
        self.X6 = self.dfArrayjig[self.dfArrayjig['station'] == '6'].copy()
        self.X7 = self.dfArrayjig[self.dfArrayjig['station'] == '7'].copy()
        self.X8 = self.dfArrayjig[self.dfArrayjig['station'] == '8'].copy()

        print('Database')
        print(self.dfArrayjig)

        if self.deqconfJig[1]:
            if self.X1.station.count() == 4:
                self.X1 = self.X1.sort_values(by=['port'])
                self.DFX1 = self.X1['station'].map(str) + self.X1['port'].map(str) + self.X1['result'].map(str)
                self.DFX1 = self.DFX1.reset_index(drop=True)
                self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '1'].index, inplace=True)
        else:
            self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '1'].index, inplace=True)

        if self.deqconfJig[2]:
            if self.X2.station.count() == 4:
                self.X2 = self.X2.sort_values(by=['port'])
                self.DFX2 = self.X2['station'].map(str) + self.X2['port'].map(str) + self.X2['result'].map(str)
                self.DFX2 = self.DFX2.reset_index(drop=True)
                self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '2'].index, inplace=True)
        else:
            self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '2'].index, inplace=True)

        if self.deqconfJig[3]:
            if self.X3.station.count() == 4:
                self.X3 = self.X3.sort_values(by=['port'])
                self.DFX3 = self.X3['station'].map(str) + self.X3['port'].map(str) + self.X3['result'].map(str)
                self.DFX3 = self.DFX3.reset_index(drop=True)
                self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '3'].index, inplace=True)
        else:
            self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '3'].index, inplace=True)

        if self.deqconfJig[4]:
            if self.X4.station.count() == 4:
                self.X4 = self.X4.sort_values(by=['port'])
                self.DFX4 = self.X4['station'].map(str) + self.X4['port'].map(str) + self.X4['result'].map(str)
                self.DFX4 = self.DFX4.reset_index(drop=True)
                self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '4'].index, inplace=True)
        else:
            self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '4'].index, inplace=True)

        if self.deqconfJig[5]:
            if self.X5.station.count() == 4:
                self.X5 = self.X5.sort_values(by=['port'])
                self.DFX5 = self.X5['station'].map(str) + self.X5['port'].map(str) + self.X5['result'].map(str)
                self.DFX5 = self.DFX5.reset_index(drop=True)
                self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '5'].index, inplace=True)
        else:
            self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '5'].index, inplace=True)

        if self.deqconfJig[6]:
            if self.X6.station.count() == 4:
                self.X6 = self.X6.sort_values(by=['port'])
                self.DFX6 = self.X6['station'].map(str) + self.X6['port'].map(str) + self.X6['result'].map(str)
                self.DFX6 = self.DFX6.reset_index(drop=True)
                self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '6'].index, inplace=True)
        else:
            self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '6'].index, inplace=True)

        if self.deqconfJig[7]:
            if self.X7.station.count() == 4:
                self.X7 = self.X7.sort_values(by=['port'])
                self.DFX7 = self.X7['station'].map(str) + self.X7['port'].map(str) + self.X7['result'].map(str)
                self.DFX7 = self.DFX7.reset_index(drop=True)
                self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '7'].index, inplace=True)
        else:
            self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '7'].index, inplace=True)

        if self.deqconfJig[8]:
            if self.X8.station.count() == 4:
                self.X8 = self.X8.sort_values(by=['port'])
                self.DFX8 = self.X8['station'].map(str) + self.X8['port'].map(str) + self.X8['result'].map(str)
                self.DFX8 = self.DFX8.reset_index(drop=True)
                self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '8'].index, inplace=True)
        else:
            self.dfArrayjig.drop(self.dfArrayjig[self.dfArrayjig.station == '8'].index, inplace=True)

        frames = [self.DFX0, self.DFX1, self.DFX2, self.DFX3, self.DFX4, self.DFX5, self.DFX6, self.DFX7, self.DFX8]
        self.dfSend = pd.concat(frames)
        self.dfSend = self.dfSend.reset_index(drop=True)
        print('Database para envio')
        print(self.dfSend)

        if self.DFX1.size:
            self.DFX1 = self.DFX1.drop([0, 1, 2, 3], axis=0)
        if self.DFX2.size:
            self.DFX2 = self.DFX2.drop([0, 1, 2, 3], axis=0)
        if self.DFX3.size:
            self.DFX3 = self.DFX3.drop([0, 1, 2, 3], axis=0)
        if self.DFX4.size:
            self.DFX4 = self.DFX4.drop([0, 1, 2, 3], axis=0)
        if self.DFX5.size:
            self.DFX5 = self.DFX5.drop([0, 1, 2, 3], axis=0)
        if self.DFX6.size:
            self.DFX6 = self.DFX6.drop([0, 1, 2, 3], axis=0)
        if self.DFX7.size:
            self.DFX7 = self.DFX7.drop([0, 1, 2, 3], axis=0)
        if self.DFX8.size:
            self.DFX8 = self.DFX8.drop([0, 1, 2, 3], axis=0)

        if self.dfSend.size:
            #self.y = self.dfSend.size
            self.yy = 0
            self.loop_new = False
            self.loop_active_w = True
            self.refresh_label1()

    def run(self):
        while self.statusRun:
            while self.input_r:
                self.out = ''

                self.out = self.t.readline()
                # self.out = self.ether.ethernetRead()

                if self.out != '':
                    self.input_w = True
                    self.input_r = False
                    self.label1.after(2000, self.refresh_label1)

            while self.loop_active_r:
                self.out=''

                self.out = self.t.readline()
                #self.out = self.ether.ethernetRead()

                if self.out != '':
                    self.label2.configure(text="%s" %self.seconds)
                    self.loop_active_w = True
                    self.loop_active_r = False
                    self.yy += 4
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

        if self.input:
            self.refresh_label1()

        if self.loop_new:
            self.oqcNewFile()

        self.label.after(1000, self.refresh_label)

    def refresh_label1(self):
        """ refresh the content of the label every second """
        if self.input_w:
            if self.dfInputJig:
                    self.temp = self.dfInputJig.popleft()
                    self.wwww = "I"+str(self.temp)
                    print("Valor a ser enviado: ", self.wwww)

                    self.seri.serialWrite(self.wwww)
                    #self.ether.ethernetWrite(self.wwww)

                    self.input_w = False
                    self.input_r = True

            else:
                self.loop_new = True
                self.input_w = False
                self.input_r = False


        if self.loop_active_w:
            if self.dfSend.size:
                    self.wwww = "O"+(self.dfSend[0][self.yy])[0:1]+(self.dfSend[0][self.yy])[2:3]+(self.dfSend[0][self.yy+1])[2:3]
                    self.wwww = self.wwww + (self.dfSend[0][self.yy+2])[2:3]+(self.dfSend[0][self.yy+3])[2:3]
                    print("Valor a ser enviado: ", self.wwww)
                    self.dfSend = self.dfSend.drop([self.yy], axis=0)
                    self.dfSend = self.dfSend.drop([self.yy+1], axis=0)
                    self.dfSend = self.dfSend.drop([self.yy+2], axis=0)
                    self.dfSend = self.dfSend.drop([self.yy+3], axis=0)

                    self.seri.serialWrite(self.wwww)
                    #self.ether.ethernetWrite(self.wwww)

                    self.label1.configure(text="%s" % self.wwww)
                    self.loop_active_w = False
                    self.loop_active_r = True

                    if self.wwww[2:3] == "P":
                        self.num_apr += 1
                        self.x1 = self.num_apr
                        print("x1: ", self.x1)
                    else:
                        self.num_rep += 1
                        self.x2 = self.num_rep
                        print("x2: ", self.x2)
            else:
                self.loop_new = True

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