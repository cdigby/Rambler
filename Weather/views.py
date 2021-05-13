from django.shortcuts import render
from urllib.request import urlopen
from django.http import HttpResponse
import json
import calendar
from datetime import datetime

# Find the days of the week for the repsective date
def findDay(date):
        day = datetime.strptime(date, '%d %m %Y').weekday()
        return calendar.day_name[day]

# Get all the api info
def grabAll():

    # Grabs the api info and converts it with UTF-8 and turns it into JSON
    WeatherData = urlopen('https://api.openweathermap.org/data/2.5/onecall?lat=51.2362&lon=0.5704&exclude=minutely&appid=43c857fcf65df3b0311f0242f20bf506')
    string = WeatherData.read().decode('utf-8')
    WeatherDataJson = json.loads(string)


    ## ----- Current Weather Data ----- ##

    now = datetime.now()
    d1 = datetime.strptime(str(now), '%Y-%m-%d %H:%M:%S.%f')
    currentDay = datetime.now().strftime('%A')
    currentIcon = WeatherDataJson['current']['weather'][0]['icon']
    currentTemp = str(round((float(WeatherDataJson['current']['temp'])) - 273.15)) + "°C"
    currentWeather = WeatherDataJson['current']['weather'][0]['main']


    ## ----- Hourly Weather Data ----- ##

    # Hourly variables

    weatherH = ""
    iconH = ""
    descH = ""
    timeH = ""
    popH = ""

    # Reads the needed JSON info for each part
    for i in range(1, 12):

        weatherH = weatherH + WeatherDataJson['hourly'][i]['weather'][0]['main'] + " " + str(round((float(WeatherDataJson['hourly'][i]['temp'])) - 273.15)) + "°C" + ", "
        iconH = iconH + WeatherDataJson['hourly'][i]['weather'][0]['icon'] + ", "
        descH = descH + WeatherDataJson['hourly'][i]['weather'][0]['description'] + ", "
        timeH = timeH + str(WeatherDataJson['hourly'][i]['dt']) + ", "

        if WeatherDataJson['hourly'][i]['pop'] < 0.05 :
            popH = popH + "<5%, "
        else:
            popH = popH + str(int(WeatherDataJson['hourly'][i]['pop']*100)) + "%, "

    # Creating lists to store the hourly variables in

    weatherHourly1 = weatherH.split(', ')
    weatherHourly = weatherHourly1[:-1]

    iconHourly1 = iconH.split(', ')
    iconHourly = iconHourly1[:-1]

    descHourly1 = descH.split(', ')
    descHourly = descHourly1[:-1]

    timeHourly1 = timeH.split(', ')
    timeHourly = timeHourly1[:-1]

    popHourly1 = popH.split(', ')
    popHourly = popHourly1[:-1]

    list_of_times_hourly = []
    list_of_days_hourly = []
    list_of_times_hourly_H = []
    ListOfAll = []

    for i in range(0,11):
        list_of_times_hourly.append(datetime.fromtimestamp(int(timeHourly[i])).strftime('%Y-%m-%d %H:%M:%S'))
        date_first1 = datetime.strptime(list_of_times_hourly[i], '%Y-%m-%d %H:%M:%S')
        list_of_days_hourly.append(findDay(date_first1.strftime("%d %m %Y")))
        list_of_times_hourly_H.append(date_first1.strftime("%H:%M"))
        ListOfAll.append((weatherHourly[i], iconHourly[i], descHourly[i], list_of_days_hourly[i], list_of_times_hourly_H[i], popHourly[i]))
        
        
    ## ----- Daily Weather Data ----- ##

    # Daily variables

    weatherD = ""
    iconD = ""
    descD = ""
    timeD = ""
    popD = ""

    # Reads the needed JSON info for each part
    for i in range(0, 7):

        weatherD = weatherD + WeatherDataJson['daily'][i]['weather'][0]['main'] + " " + str(round((float(WeatherDataJson['daily'][i]['temp']['day'])) - 273.15)) + "°C" + ", "
        iconD = iconD + WeatherDataJson['daily'][i]['weather'][0]['icon'] + ", "
        descD = descD + WeatherDataJson['daily'][i]['weather'][0]['description'] + ", "
        timeD = timeD + str(WeatherDataJson['daily'][i]['dt']) + ", "

        if WeatherDataJson['daily'][i]['pop'] < 0.05 :
            popD = popD + "<5%, "
        else:
            popD = popD + str(int(WeatherDataJson['daily'][i]['pop']*100)) + "%, "

    # Creating lists to store the daily variables in

    weatherDaily1 = weatherD.split(', ')
    weatherDaily = weatherDaily1[:-1]

    iconDaily1 = iconD.split(', ')
    iconDaily = iconDaily1[:-1]

    descDaily1 = descD.split(', ')
    descDaily = descDaily1[:-1]

    timeDaily1 = timeD.split(', ')
    timeDaily = timeDaily1[:-1]

    popDaily1 = popD.split(', ')
    popDaily = popDaily1[:-1]

    list_of_times_daily = []
    list_of_days_Daily = []
    list_of_times_Daily_D = []
    ListOfAll2 = []

    for i in range(len(timeDaily)):
        list_of_times_daily.append(datetime.fromtimestamp(int(timeDaily[i])).strftime('%Y-%m-%d %H:%M:%S'))
        date_first1 = datetime.strptime(list_of_times_daily[i], '%Y-%m-%d %H:%M:%S')
        list_of_days_Daily.append(findDay(date_first1.strftime("%d %m %Y")))
        list_of_times_Daily_D.append(date_first1.strftime("%H:%M"))
        ListOfAll2.append((weatherDaily[i], iconDaily[i], descDaily[i], list_of_days_Daily[i], list_of_times_Daily_D[i], popDaily[i]))    
        

    data = {
        "currentDay": currentDay,
        "currentIcon": currentIcon,
        "currentTemp": currentTemp,
        "currentWeather": currentWeather,

        "ListOfAll": ListOfAll,
        "ListOfAll2":ListOfAll2
    }

    return data




# Create your views here.
def weather(request):

    data = grabAll()

    return render(request, 'weather/weatherPage.html', data)