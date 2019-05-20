"""
XXXXX

"""
import serial, socket

class ComSerial(object):

    def __init__(self, port = 'Com3'):
        self.port = port

    def configSerial(self):
        self.ser = serial.Serial()
        self.ser.port = self.port
        self.ser.baudrate = 9600
        self.ser.bytesize = 8
        self.ser.parity = 'N'
        self.ser.stopbits = 1
        self.ser.timeout = None
        self.ser.rtscts = False
        self.ser.dsrdtr = False
        self.ser.open()
        return self.ser

    def serialWrite(self,msgWriteSerial):
        msgWriteSerial = str(msgWriteSerial)
        msgWriteSerial = msgWriteSerial.encode('utf-8')
        msgWriteSerial = msgWriteSerial + b'\n'
        self.ser.write(msgWriteSerial)

    def serialRead(self):
        msgReadSerial = ''
        while self.ser.inWaiting() > 0:
            bytesToRead = self.ser.inWaiting()
            msgReadSerial = self.ser.read(bytesToRead)
        return msgReadSerial

class ComEthernet(object):

    def __init__(self, host='169.254.247.90', portIP=5800):
        self.host = host
        self.portIP = portIP

    def configEthernet(self):
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        adress=(self.host, self.portIP)
        self.tcp.connect(adress)

    def ethernetWrite(self,msgWriteEthernet):
        msgWriteEthernet = msgWriteEthernet.encode('utf-8')
        msgWriteEthernet = msgWriteEthernet + b'\r\n'
        self.tcp.send(msgWriteEthernet)

    def ethernetRead(self):
        return self.tcp.recv(1024)