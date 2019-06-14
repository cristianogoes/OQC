"""
XXXXX

"""
import os
import win32com.client
import collections

class Scandir(object):

    def __init__(self,pathToWatch):
        self.pathToWatch=pathToWatch

    def configPath(self):
        os.chdir(self.pathToWatch)
        self.before = dict([(f, None) for f in os.listdir(self.pathToWatch)])

    def scannerFile(self):
        self.after = dict([(f, None) for f in os.listdir(self.pathToWatch)])

        self.added = [f for f in self.after if not f in self.before]
        self.removed = [f for f in self.before if not f in self.after]
        self.before = self.after
        return self.added

    def readFile(self,file,targetLine):
        numLine = 0
        with open(file, 'r') as fileTemp:
            for resultLine in iter(lambda: fileTemp.readline(), b'\n'):
                numLine += 1
                if numLine == targetLine:
                    break
        return resultLine

class ScandirSSD(object):

    def __int__(self):
        self.ssd = dict()

    def sccannerSSD(self, Computer,User,Password):
        objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        objSWbemServices = objWMIService.ConnectServer(Computer, "root\cimv2", User, Password)
        colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_IDEController")

        self.ssd = dict([(f.Name, None) for f in colItems])

        return len(self.ssd)-1
