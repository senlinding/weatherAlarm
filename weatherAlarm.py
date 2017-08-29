#coding:utf-8
import os, sys, urllib2, urllib, json, getopt
from utils import *
from time import *
from weather import *
from smtpEmail import *
from log import *

sysConfig = ""
configPath = "config.json"

def initConfig():
    global sysConfig, configPath
    with open(configPath) as configFile:
        sysConfig = json.load(configFile)
        print sysConfig.keys()

    print "initConfig ok, path:%s" % configPath

def usage():
    print "weatherAlarm.py usage:"
    print "weatherAlarm.py [--configPath=PATH] [--show]"
    print ('''
        usage: weatherAlarm [OPTION]...
        General options:
            -h, --help             show this help message and exit
            -s, --show             show city forecast
            -c, --city             city name for show
            --configPath           config file path, default config.json
        ''')

def showForecast(city):
    global sysConfig
    initConfig()
    maxForecastCnt = 40

    wt = Weather(sysConfig["appid"], city, "zh_cn")
    fcList = wt.getForecastWeather(maxForecastCnt)
    if fcList != None:
        print forecastRain(fcList, len(fcList), city)

def compareTime(tm, timeStr):
    separator = timeStr.find(":")
    return tm.tm_hour == int(timeStr[:separator]) and tm.tm_min == int(timeStr[separator + 1:])

class ForecastTime:
    def __init__(self, getForecastTime, sendMsgTime):
        self.getTm = getForecastTime
        self.sendTm = sendMsgTime

def runForecast():
    global sysConfig
    initConfig()
    initLogFile("weather")
    maxForecastCnt = sysConfig["maxForecastCnt"]
    fcTodayTm = ForecastTime(sysConfig["forecasToday"]["getForecastTime"], sysConfig["forecasToday"]["sendMsgTime"])
    fcRainTm = ForecastTime(sysConfig["forecasRain"]["getForecastTime"], sysConfig["forecasRain"]["sendMsgTime"])
    appid = sysConfig["appid"]
    fcTodayCity = sysConfig["forecasToday"]["city"]
    fcRainCity = sysConfig["forecasRain"]["city"]

    if maxForecastCnt < 7:
        WPLog("maxForecastCnt error:%d" % maxForecastCnt)
        return

    resultToday, resultRain = None, None
    while 1:
        tm = localtime()
        if compareTime(tm, fcTodayTm.getTm):
            wt = Weather(appid, fcTodayCity)
            fcList = wt.getForecastWeather(maxForecastCnt)
            if fcList != None:
                resultToday = forecastToday(fcList[:7], fcTodayCity)
                if resultToday.find("Rain") > 0:
                    resultToday = "%s, %s" % (resultToday, forecastRain(fcList, 7, fcTodayCity))
                WPLog(resultToday)

        if compareTime(tm, fcTodayTm.sendTm) and resultToday != None:
            loginResult, newEmail = getLoginEmail()
            if loginResult == True:
                map(lambda to: newEmail.send(to, "Auto:" + resultToday, resultToday), sysConfig["forecasToday"]["email"])
            resultToday = None

        if compareTime(tm, fcRainTm.getTm):
            wt = Weather(appid, fcTodayCity)
            fcList = wt.getForecastWeather(maxForecastCnt)
            if fcList != None:
                resultRain = forecastRain(fcList, 7, fcRainCity)
                WPLog(resultRain)

        if compareTime(tm, fcRainTm.sendTm) and resultRain != None:
            loginResult, newEmail = getLoginEmail()
            if loginResult == True:
                map(lambda to: newEmail.send(to, "Auto:" + resultRain, resultRain), sysConfig["forecasRain"]["email"])
            resultRain = None

        sleep(60)

class opMode:
    (showMode, runMode) = range(1, 3)
if __name__ == '__main__':
    mode = opMode.runMode
    city = "shanghai"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:s", ["help", "city", "configPath=", "show"])
    except Exception, e:
        usage()
        sys.exit(1)

    for key, val in opts:
        if key == "--configPath":
            configPath = val
        elif key == "-s" or key == "--show":
            mode = opMode.showMode
        elif key == "-c" or key == "--city":
            city = val
        elif key == "-h" or key == "--help":
            usage()
            sys.exit(1)

    if mode == opMode.showMode:
        showForecast(city)
    else:
        runForecast()


