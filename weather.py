#coding:utf-8
import os, sys, urllib2, urllib, json
from utils import *
from time import *
from log import *

class ForecastEntry:
  def __init__(self):
    self.dt = None
    self.weatherMain = ""
    self.description = ""
    self.temp = 0
    self.temp_min = 0
    self.temp_max = 0
    self.windSpeed = 0

def parseForecast(item):
    fc = ForecastEntry()
    fc.dt = item['dt']
    fc.weatherMain = item['weather'][0]['main']
    fc.description = item['weather'][0]['description']
    fc.temp = item['main']['temp']
    fc.temp_min = item['main']['temp_min']
    fc.temp_max = item['main']['temp_max']
    fc.windSpeed = item['wind']['speed']
    WPLog("time:%s weatherMain:%s description:%s temp:%s windSpeed:%s" % \
          (getDayAndHour(fc.dt), fc.weatherMain, fc.description, fc.temp, fc.windSpeed))

    return fc

def forecastRain(fcList, forecastCnt, city):
    if len(fcList) < forecastCnt:
        return "forecastRain len error"

    list = fcList[:forecastCnt]
    rainList = filter(lambda item: item.weatherMain == "Rain", list)

    if len(rainList) == 0:
        return "%s no rain from %s to %s" % (city, getDayAndHour(list[0].dt), getDayAndHour(list[-1].dt))
    else:
        rainTime = reduce(lambda x, y: "%s, %s" % (x, y), map(lambda x: "%s" % getDayAndHour(x.dt), rainList))
        return "%s will rain(%s) from %s to %s" % (city, rainTime, getDayAndHour(list[0].dt), getDayAndHour(list[-1].dt))

#Rain Clouds Clear and Snow etc.
def getPeriodWeather(fcList):
    if len(filter(lambda item: item.weatherMain == "Rain", fcList)):
        return "Rain"
    elif len(filter(lambda item: item.weatherMain == "Clouds", fcList)):
        return "Clouds"
    elif len(filter(lambda item: item.weatherMain == "Clear", fcList)):
        return "Clear"
    else:
        return fcList[0].weatherMain

#today time from 5:00~23:00
# 5 8 11 14 --> 17 20 23
def forecastToday(fcList, city):
    listLen = len(fcList)
    if listLen < 7:
        return "list len error:%d" % listLen

    minTemp = min(map(lambda x: x.temp, fcList))
    maxTemp = max(map(lambda x: x.temp, fcList))

    speedList = map(lambda x: x.windSpeed, fcList)
    maxWindSpeedIndex = speedList.index(max(speedList))

    index = listLen / 2 + 1
    fc = getPeriodWeather(fcList[:index])
    fcNext = getPeriodWeather(fcList[index:])
    if fc != fcNext:
        fc += " to %s" % fcNext

    return "%s %s, temp:%d/%d, %02d:00 wind:%.2f" % (city, fc, minTemp, maxTemp, localtime(fcList[maxWindSpeedIndex].dt).tm_hour, fcList[maxWindSpeedIndex].windSpeed)

class Weather:
    def __init__(self, appid, city, lang="en"):
        self.appid, self.city, self.lang = appid, city, lang
        WPLog("init Class Weather for %s" % (city))

    def getWeather(self, queryString):
        try:
            req = urllib2.Request(queryString)
            response = urllib2.urlopen(req, timeout=20)
            rt = json.loads(response.read())
            return rt
        except Exception, e:
            WPLog("getWeather queryString:%s except:%s" % (queryString, e))

    def getCurrWeather(self):
        queryString = "http://api.openweathermap.org/data/2.5/weather?" + \
                      urllib.urlencode({'lang': self.lang, 'mode': 'json', 'units': 'metric', 'q': self.city, 'appid': self.appid})
        rt = self.getWeather(queryString)
        if rt != None:
            rt = "%s %d:00 %s %.2f" % (self.city, localtime(rt['dt']).tm_hour, rt['weather'][0]['description'], rt['main']['temp'])
            WPLog("getCurrWeather success, %s" % (rt))
            return rt

        return rt

    def getForecastWeather(self, forecastCnt):
        queryString = "http://api.openweathermap.org/data/2.5/forecast?" + \
                      urllib.urlencode({'lang': self.lang, 'mode': 'json', 'units': 'metric', 'q': self.city, 'appid': self.appid, 'cnt':forecastCnt})
        rt = self.getWeather(queryString)
        if rt != None:
            rt = map(parseForecast, rt['list'])
            WPLog("getForecastWeather success, Forecast len:%d" % (len(rt)))

        return rt

if __name__ == '__main__':
    city = "shanghai"
    '''
    wt = Weather("you id", city)
    #print wt.getCurrWeather()
    fcList = wt.getForecastWeather(40)
    '''
    fcList = list()
    for i in range(40):
        fcList.append(ForecastEntry())
        fcList[i].dt = i
        fcList[i].weatherMain = "Clouds"
        fcList[i].temp = i

    fcList[3].weatherMain = "Rain"
    fcList[4].weatherMain = "Rain"


    print forecastRain(fcList, 40, city)
    print forecastToday(fcList[:7], city)


