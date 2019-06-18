"""
XXXXX

"""
import serial, socket
from serial import SerialException

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
        try:
            return self.ser
        except SerialException as errorConfigSerial:
            return errorConfigSerial

    def serialWrite(self,msgWriteSerial):
        msgWriteSerial = str(msgWriteSerial)
        msgWriteSerial = msgWriteSerial.encode('utf-8')
        msgWriteSerial = msgWriteSerial = b'\r\n'
        self.ser.write(msgWriteSerial)

    def serialRead(self):
        msgReadSerial = ''
        while self.ser.inWaiting() > 0:
            bytesToRead = self.ser.inWaiting()
            msgReadSerial = self.ser.read(bytesToRead)
        return msgReadSerial

class ComEthernet(object):

    def __init__(self, host='192.168.0.101', portIP=5800):
    #def __init__(self, host='10.58.72.69', portIP=5800):
        self.host = host
        self.portIP = portIP
        self.errorMsg = ''

    def configEthernet(self):
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        adress=(self.host, self.portIP)
        try:
            return self.tcp.connect(adress)
        except socket.error as errorConfigEthernet:
            print("Caught exception socket.error : %s" % errorConfigEthernet)
            return errorConfigEthernet

    def ethernetWrite(self,msgWriteEthernet):
        msgWriteEthernet = msgWriteEthernet.encode('utf-8')
        msgWriteEthernet = msgWriteEthernet + b'\r\n'
        try:
            self.tcp.send(msgWriteEthernet)
        except socket.error as errorWriteEthernet:
            print("Caught exception socket.error : %s" % errorWriteEthernet)
            return errorWriteEthernet


    def ethernetRead(self):
        try:
            return self.tcp.recv(1024)
        except socket.error as errorReadEthernet:
            print("Caught exception socket.error in read: %s" % errorReadEthernet)
            return errorReadEthernet
