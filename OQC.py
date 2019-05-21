
import time
import pandas as pd
import Comunicacao, ScannerFile

df0=[]
DFX0 = pd.DataFrame(df0)
df6=[]
DFX6 = pd.DataFrame(df6)
df7=[]
DFX7 = pd.DataFrame(df7)

arrayJig = []
dfArrayjig = pd.DataFrame(arrayJig, columns=['station', 'port', 'result'])

if __name__=='__main__':

    out = ''
    seri = Comunicacao.ComSerial()
    t = seri.configSerial()

    scanner = ScannerFile.Scandir(pathToWatch="C:\\Users\\bb8ga121\\Desktop\\TESTE_CHIP_IC")
    scanner.configPath()
    time.sleep(1)

    while 1:
        time.sleep(1)
        newFile = scanner.scannerFile()

        if newFile:
            ii = 0
            for ii in range(len(newFile)):

                status_indice = scanner.readFile(newFile[ii],3)
                error_codigo = scanner.readFile(newFile[ii],4)
                status_test = scanner.readFile(newFile[ii],5)
                station = scanner.readFile(newFile[ii],7)[1:2]
                porta = newFile[ii][(len(newFile[ii])-5):(len(newFile[ii])-4)]

                dfArrayjig = dfArrayjig.append(pd.Series([station, porta, status_indice], index=dfArrayjig.columns), ignore_index=True)

                ii += 1

        X6 = dfArrayjig[dfArrayjig['station'] == '6'].copy()
        X7 = dfArrayjig[dfArrayjig['station'] == '7'].copy()

        if X6.station.count() == 4:
            X6 = X6.sort_values(by=['port'])
            DFX6 = X6['station'].map(str) + X6['port'].map(str) + X6['result'].map(str)
            DFX6 = DFX6.reset_index(drop=True)
            dfArrayjig.drop(dfArrayjig[dfArrayjig.station == '6'].index, inplace=True)
        if X7.station.count() == 4:
            X7 = X7.sort_values(by=['port'])
            DFX7 = X7['station'].map(str) + X7['port'].map(str) + X7['result'].map(str)
            DFX7 = DFX7.reset_index(drop=True)
            dfArrayjig.drop(dfArrayjig[dfArrayjig.station == '7'].index, inplace=True)

        frames = [DFX0, DFX6, DFX7]
        X1 = pd.concat(frames)
        X1 = X1.reset_index(drop=True)
        print('Database para envio')
        print(X1)

        if X1.size:
            for y in range(X1.size):
                wwww = X1[0][y]
                print("Valor a ser enviado: ",wwww)
                X1 = X1.drop([y],axis=0)
                seri.serialWrite(wwww)
                out = t.readline()
                """
                if out != '':
                    if out == b'finalizado\n':
                        print(">> NEXT: ")
                    out = ''
                """
                y += 1
            if DFX6.size:
                DFX6 = DFX6.drop([0, 1, 2, 3], axis=0)
            if DFX7.size:
                DFX7= DFX7.drop([0, 1, 2, 3], axis=0)