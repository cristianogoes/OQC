"""
XXXXX

"""
import os

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