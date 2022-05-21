#!/bin/python3
# Weather Display for RPi 4, four 64x64 RGB Matrix display
# running on a Raspberry Pi with Adafruit 'Matrix HAT and RTC', four 64x64 panels part# 4321
# configured as a 256 wide x 64 high display
# This program assumes the system clock is maintained elsewhere.
# Time will not be retrieved from the Internet.
#
# files:
# wd.py  - main routine
# owd.py - object that holds the display object
# owd_icons.bmp - Contains Openwaether.org icons to display
# samplebase.py - object which contains parameter parsing for the display

"""
This example queries the Open Weather Maps site API to find out the current
weather for your location... and display it on a screen!
if you can find something that spits out JSON data, we can display it
"""
import time
import requests
import owd
import sys

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

is_metric = False

if is_metric:
    UNITS = "metric"  # can pick 'imperial' or 'metric' as part of URL query
    print("metric units")
else:
    UNITS = "imperial"
    print("imperial units")

# Use cityname, country code where countrycode is ISO3166 format.
# E.g. "New York, US" or "London, GB"
LOCATION = "Durham, NC, US"
LOCATION = secrets["openweather_location"]
print("Getting weather for {}".format(LOCATION))
# Set up from where we'll be fetching data
DATA_SOURCE = ( "http://api.openweathermap.org/data/2.5/weather?q=" + LOCATION + "&units=" + UNITS )
DATA_SOURCE += "&appid=" + secrets["openweather_token"]
# You'll need to get a token from openweather.org, looks like 'b6907d239510d614a2e88330741fa221'
# it goes in your secrets.py file on a line such as:
# 'openweather_token' : 'your_big_humongous_gigantor_token',
#
'''
See: https://openweathermap.org/api for the API.
Example: https://api.openweathermap.org/data/2.5/weather?lat=35&lon=139&appid={API key}

{
 'coord': {
  'lon': -78.8664, 
  'lat': 36.0335  }, 
 'weather': 
  [{
    'id': 803, 
    'main': 'Clouds', 
    'description': 'broken clouds', 
    'icon': '04d'
  }], 
 'base': 'stations', 
 'main': {
  'temp': 72.61, 
  'feels_like': 73.27, 
  'temp_min': 69.85, 
  'temp_max': 75.43, 
  'pressure': 1013, 
  'humidity': 79}, 
 'visibility': 10000, 
 'wind': {
  'speed': 12.66, 
  'deg': 230, 
  'gust': 23.1}, 
 'clouds': {'all': 75}, 
 'rain': {'1h': 75,'3h': 75}, 
 'snow': {'1h': 75,'3h': 75}, 
 'dt': 1652962615, 
 'sys': {
  'type': 2, 
  'id': 2010473, 
  'country': 'US', 
  'sunrise': 1652954808, 
  'sunset': 1653005841}, 
 'timezone': -14400, 
 'id': 4464374, 
 'name': 'Durham', 
 'cod': 200}
'''
DATA_LOCATION = []
SCROLL_HOLD_TIME = 0  # set this to hold each line before finishing scroll

# --- Display setup ---
#if UNITS == "imperial" or UNITS == "metric":
    #openweather_graphics.OpenWeather_Graphics( matrix.display, am_pm=True, units=UNITS)

localtime_refresh = None
localtime_display = None
weather_refresh = None
#
# get the graphic display object ready
#
OW=owd.OpenWeather(LOCATION, am_pm=True, units=UNITS)
if (not OW.process()):
    OpenWeather.print_help()
    sys.exit(1)
#
#
#

value = ""
while True:
    # only query the online time once per hour (and on first run)
    #print("**********")
    # Erase then display the local time "hh:mm:ss AM" every second
    if (not localtime_display) or (time.monotonic() - localtime_display) > 1:
        OW.update_time()
        localtime_display = time.monotonic()

    # Update time locally every hour
    if (not localtime_refresh) or (time.monotonic() - localtime_refresh) > 3600:
        try:
            print("Getting time from internet!")
            #network.get_local_time()
            localtime_refresh = time.monotonic()
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
            continue

    # only query the weather every 10 minutes (and on first run)
    if (not weather_refresh) or (time.monotonic() - weather_refresh) > 600*2:
        a_time=time.strftime('%m-%d-%y %H:%M:%S', time.localtime(time.time()))
        print("TIME:",a_time)
        if not weather_refresh:
            OW.paint(LOCATION)
        try:
            #if value =="":
            value = requests.get(url=DATA_SOURCE).json() #, json_path=(DATA_LOCATION,))
            f=open("/tmp/openweather.log","a")
            f.write( "( " + a_time + ", " + str(value) + " )\n" )
            f.close()
            print("Response is", value)
            lon=value['coord']['lon']
            print("lon",lon)
            lat=value['coord']['lat']
            print("lat",lat)
            id=value['weather'][0]['id']
            main=value['weather'][0]['main']
            print("main", main)
            description=value['weather'][0]['description']
            print("description", description)
            icon=value['weather'][0]['icon']
            print("icon", icon)
            temp=value['main']['temp']
            print("temp", temp)
            feels_like=value['main']['feels_like']
            print("feels_like", feels_like)
            temp_min=value['main']['temp_min']
            print("temp_min", temp_min)
            temp_max=value['main']['temp_max']
            print("temp_max", temp_max)
            pressure=value['main']['pressure']
            print("pressure", pressure)
            humidity=value['main']['humidity']
            print("humidity", humidity)
            visibility=value['visibility']
            print("visibility", visibility)
            windspeed=value['wind']['speed']
            print("windspeed", windspeed)
            winddeg=value['wind']['deg']
            print("winddeg", winddeg)
            try:
                windgust=value['wind']['gust']
                print("windgust", windgust)
            except KeyError:
                windgust=None
            try:
                rain1h=value['rain']['1h']
                print("rain 1h", rain1h)
            except KeyError:
                rain1h=None
            try:
                rain3h=value['rain']['3h']
                print("rain 3h", rain3h)
            except KeyError:
                rain3h=None
            try:
                snow1h=value['snow']['1h']
                print("snow 1h", snow1h)
            except KeyError:
                snow1h=None
            try:
                snow3h=value['snow']['3h']
                print("snow 1h", snow3h)
            except KeyError:
                snow3h=None
            sunrise=value['sys']['sunrise']
            print("sunrise",time.strftime('%m %d %H:%M:%S', time.localtime(sunrise)))
            sunset=value['sys']['sunset']
            print("sunset",time.strftime('%m %d %H:%M:%S', time.localtime(sunset)))
            #gfx.display_weather(value)
            weather_refresh = time.monotonic()
            OW.update( LOCATION, lon, lat, id, main, description, icon, temp, feels_like, temp_min, temp_max, pressure, humidity, visibility, windspeed, winddeg, windgust, sunrise, sunset )
            OW.update_time()
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
            continue

    #time.sleep(SCROLL_HOLD_TIME)
    time.sleep(0.1)
