import sys, os, functools
from time import *
from utils import *

logFileName = ""

def initLogFile(appName=""):
    global logFileName
    if logFileName == "":
        logFileName = (appName + getTimeStr() + ".log").replace(' ', '_').replace(":", "")

    with open(logFileName, "w+") as fr:
        fr.write('log start time: ' + getTimeStr() + "\n")

    print "init log file[%s] ok!" % (logFileName)

def writeLog(buf, fileName="", mode=TM.notYear, printFlag=False):
    global logFileName
    if fileName != "":
        logFileName = fileName

    log = getTimeStr(mode) + ": " + buf

    if printFlag == True:
        print log

    if logFileName == "":
        return

    with open(logFileName, "a") as fr:
        fr.write(log + "\n")

#write and print log
WPLog = functools.partial(writeLog, printFlag=True)
WLog = functools.partial(writeLog, printFlag=False)

if __name__ == '__main__':
    initLogFile("test")
    writeLog("test123", printFlag=True)
    WPLog("hehe")

