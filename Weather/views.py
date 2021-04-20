from django.shortcuts import render
from urllib.request import urlopen
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
    WeatherData = urlopen('https://api.openweathermap.org/data/2.5/onecall?lat=51.2362&lon=0.5704&exclude=minutely,daily&appid=43c857fcf65df3b0311f0242f20bf506')
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

    for i in range(0,11):
        list_of_times_hourly.append(datetime.fromtimestamp(int(timeHourly[i])).strftime('%Y-%m-%d %H:%M:%S'))


    list_of_days_hourly = []
    list_of_times_hourly_H = []

    for i in range(0,11):
        date_first1 = datetime.strptime(list_of_times_hourly[i], '%Y-%m-%d %H:%M:%S')
        list_of_days_hourly.append(findDay(date_first1.strftime("%d %m %Y")))
        list_of_times_hourly_H.append(date_first1.strftime("%H:%M"))

    ListOfAll = []

    for i in range(len(popHourly)):
        ListOfAll.append((weatherHourly[i], iconHourly[i], descHourly[i], list_of_days_hourly[i], list_of_times_hourly_H[i], popHourly[i]))

    data = {
        "currentDay": currentDay,
        "currentIcon": currentIcon,
        "currentTemp": currentTemp,
        "currentWeather": currentWeather,

        "ListOfAll": ListOfAll
    }
    return data

# Create your views here.
def weather(request):

    data = grabAll()

    return render(request, 'weather/weatherPage.html', data)