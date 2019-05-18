
import time
from collections import deque
import Comunicacao, ScannerFile

list_name = []
list_status = []
deq_name = deque(list_name)
deq_status = deque(list_status)

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

                deq_name.append(newFile[ii])
                deq_status.append(status_indice)
                ii += 1

        if deq_status:
            print("TAMANHO: ",len(deq_status))
            print("Pass: ",deq_status.count("P\n"))
            print("Fail: ",deq_status.count("F\n"))

            #Fila - FIFO
            deq_name.popleft()
            value = deq_status.popleft()

            """
            #Pilha - LIFO
            deq_name.pop()
            value = deq_status.pop()
            """

            seri.serialWrite(value)

            out = t.readline()

            if out != '':
                if out == b'finalizado\n':
                    print(">> NEXT: ")
                out = ''
        else:
            print("Fila vazia: ")