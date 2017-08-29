import sys, os
from time import *

#time mode
class TM:
    (showAll, notYear) = range(1, 3)

def getTimeStr(mode=TM.showAll):
    lt = localtime()

    if mode == TM.notYear:
        timeStr = "%02d%02d %02d:%02d:%02d" % (lt.tm_mon, lt.tm_mday, lt.tm_hour, lt.tm_min, lt.tm_sec)
    else:
        timeStr = "%04d%02d%02d %02d:%02d:%02d" % (lt.tm_year, lt.tm_mon, lt.tm_mday, lt.tm_hour, lt.tm_min, lt.tm_sec)

    return timeStr

def getDayAndHour(timestamp):
    lt = localtime(timestamp)
    return "%02d-%02d" % (lt.tm_mday, lt.tm_hour)