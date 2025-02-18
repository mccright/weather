# weather
Display one-line of weather information in your terminal for any city+country supported on [OpenWeather](https://openweathermap.org/).  

If this is something you are considering, look at the vastly superior [https://github.com/gourlaysama/girouette](https://github.com/gourlaysama/girouette)!  It is an exceptionally capable and flexible utility for displaying OpenWeather information in a terminal and may be a perfect for many.  

## Why not girouette?  
I have moved/added my Linux and Windows endpoints too many times in recent years.  Some of those moves involved investing more time than I will admit reconfiguring my new giroutte installation.  

After giroutte installation and configuration, on Linux I add a bash alias that maps the command "weather" to giroutte.  On Windows I did an analogous "*alias*" using a command file (*and later Powershell*).  
Here is an example for Linux from my .bash_aliases file:  

```terminal
# Get the current weather
# Depends on a config file in ~/.config/girouette/config.yml
if [ -x ~/bin/girouette ]; then
        alias weather='/usr/bin/echo `~/bin/girouette`'
fi
```

I have been using giroutte long enough to know what I want to see in my terminal, so it seemed rational to just code up a short script to fetch openweathermap.org data myself.  

## This utility:  
Returns a terse weather report using [data](https://openweathermap.org/current#data) from an [api.openweathermap.org service](https://openweathermap.org/current) on a single line in my standard terminal configuration.  I use it multiple times every day.  The report includes:  
* date and time of weather measurements (in your local time zone if it can be determined by OpenWeatherMap)  
* measured temperature, defaults to Fahrenheit (change via command line/alias or default in code for Celsius)  
* "feels like" temperature, defaults to Fahrenheit (change via command line/alias or default in code for Celsius or Kelvin)  
* wind direction  
* wind speed, defaults to miles/hour (change via command line/alias or default in code for km/hour)  
* humidity in percent  

This script requires an [OpenWeather API key](https://openweathermap.org/appid) (*free for 1 call per second*) -- put it in the configuration file *or* get it into your environment (ideally from your secret store, rather than a clear text file.  It is easy to [sign-up for an account](https://openweathermap.org/home/sign_up) and then [get the required key](https://home.openweathermap.org/api_keys).  

You can supply a city and nation on the command line.  City names having one or more spaces, must be surrounded by quotes (e.g. "los angeles").  The nation is specified using the 2-letter [ISO 3166 code](https://en.wikipedia.org/wiki/ISO_3166).  See the examples below.  

## Lookup the abbreviation, country code, and/or Lat.Lon. for a city you want to monitor.  
You can use the [OpenWeatherMap geo-coding API](https://openweathermap.org/api/geocoding-api) to lookup the country code or lat/lon for a given city.

In the example below, we request the locations named "pune" and the API returned three: Pune, India; Pune, Indonesia; and Pune, Timor Leste.  In my case, I wanted Pune, India, so my city/nation would be ```python3 weather.py -c r pune -n in```.

```terminal
curl https://api.openweathermap.org/geo/1.0/direct?q=pune&limit=5&appid=[put your API key here]
[
  {
    "name": "Pune",
    "local_names": {
      "mr": "पुणे शहर",
      "ar": "مدينة بونه",
      "ml": "പൂണെ",
      "te": "పూణే",
      "en": "Pune",
      "zh": "浦那",
      "hi": "पुणे",
      "kn": "ಪುಣೆ",
      "pa": "ਪੁਣੇ",
      "he": "פונה",
      "ur": "شہر پونے",
      "ps": "پونی",
      "ru": "Пуне",
      "fa": "پونه"
    },
    "lat": 18.521428,
    "lon": 73.8544541,
    "country": "IN",
    "state": "Maharashtra"
  },
  {
    "name": "Pune",
    "lat": 1.7837578,
    "lon": 127.8542945,
    "country": "ID",
    "state": "North Maluku"
  },
  {
    "name": "Pune",
    "lat": -9.36924,
    "lon": 124.31618,
    "country": "TL",
    "state": "Oecussi-Ambeno"
  }
]
```


## Installation:
I assume that you already have Python installed and use it regularly.  Clone this repository (```git clone https://github.com/mccright/weather-in-terminal.git```) and make any customizations to meet your needs.  Then locate ```weather.py``` and ```weather.ini``` in your local bin path (*or not, for more resistance to abuse*).  Then add a shell alias (*with command line options to meet your needs*) analogous to the example below:  

```terminal
# Get the current weather
# This example depends on
# A) your OpenWeatherMap API key is in the local environment (the default) *or*
# B) your OpenWeatherMap API key is in a config file in ~/bin/weather.ini (without the '-f')
#  (or someother location, which you will specify on the command line or as shown below 
#  in a bash alias, for example `-f path_to_config_file/weather.ini`)
function weather() {
  if [ -r ${HOME}/bin/weather.py ] && [ -r "${HOME}/.config/weather-in-terminal/weather.ini" ]; then
        /usr/bin/python3 ${HOME}/bin/weather.py -f ${HOME}/.config/weather-in-terminal/weather.ini
  fi
}
```

In a Windows-only environment you can also set up a Windows shortcut pointing to (*with paths that match your endpoint and with command line options that meet your needs*):  

```terminal
C:\Windows\System32\cmd.exe /K "C:\PROGRA~1\Python311\python.exe  C:\testing\weather.py"
```

## Examples:  

*Without using the ```alias``` approach outlined above, to demonstrate command line options...*  

```terminal
matt@hostname:/testing$ python3 weather.py
2023-12-19 13:23, 42.51°F, feels like 34.74°F, wind S 16.11 m/h, broken clouds, humidity 40%

matt@hostname:/testing$ python3 weather.py -c denver
2023-12-19 13:10, 62.85°F, feels like 59.83°F, wind SSW 2.71 m/h, clear sky, humidity 21%

matt@hostname:/testing$ python3 weather.py -c chicago -n us -f ~/secured/weather.ini
2023-12-19 13:29, 31.6°F, feels like 22.51°F, wind SSW 11.5 m/h, scattered clouds, humidity 49%

matt@hostname:/testing$ python3 weather.py -c rome -n it
2023-12-19 13:30, 49.57°F, feels like 48.79°F, wind SSE 3.44 m/h, clear sky, humidity 62%

matt@hostname:/testing/$ python3 weather.py -c pune -n in
2023-12-20 11:35, 68.27°F, feels like 66.63°F, wind E 5.48 m/h, overcast clouds, humidity 39%

matt@hostname:/testing$ python3 weather.py -c edinburgh -n uk
2023-12-19 16:58, 43.02°F, feels like 34.54°F, wind WSW 19.57 m/h, clear sky, humidity 82%

matt@hostname:/testing$ python3 weather.py -c santiago -n cl
2023-12-19 17:01, 71.17°F, feels like 70.05°F, wind SW 14.97 m/h, smoke, humidity 44%

matt@hostname:/testing$ python3 weather.py -c nairobi -n ke
2023-12-19 17:07, 63.72°F, feels like 63.64°F, wind NNE 6.91 m/h, broken clouds, humidity 82%

matt@hostname:/testing$ python3 weather.py -c "los angeles" -n us
2023-12-19 17:13, 63.43°F, feels like 63.09°F, wind SE 9.22 m/h, overcast clouds, humidity 77%

matt@hostname:/testing$ python3 weather.py -h
usage: weather [-h] [-d] [-l LANGUAGE] [-c CITY_NAME] [-n NATION_NAME] [-u UNITS_OF_MEASUREMENT] [-f CONFIG_FILE_NAME]

weather: a terminal script to fetch current weather from openweathermap.org

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Use to send debug logging to console (unfinished)
  -l LANGUAGE, --language LANGUAGE
                        Either collect the language.
                         Or just use the default language.
  -c CITY_NAME, --city_name CITY_NAME
                        Either collect the target city name.
                         Or just use the default city name.
  -n NATION_NAME, --nation_name NATION_NAME
                        Either collect the target nation name.
                         Or just use the default country name
  -u UNITS_OF_MEASUREMENT, --units_of_measurement UNITS_OF_MEASUREMENT
                        Changes temp and wind speed units. Default: "imperial"
                         Options are: "standard" (Kelvin/km),
                         "metric" (Celsius/km), and
                         "imperial" (Fahrenheit/miles) units.
  -f CONFIG_FILE_NAME, --config_file_name CONFIG_FILE_NAME
                        Name of the configuration file.
matt@hostname:/testing$
```

## Other Python-Based CLI Weather Lookup Scripts  
current-conditions-openweather  
https://github.com/jfcarr/current-conditions-openweather/  
Simple text output of current weather conditions, retrieved from OpenWeather API.  

PyWeather  
https://gitlab.com/o355/PyWeather  
The fun way to check the weather in a terminal.  

MesoPy (MesoWest API Wrapper): Current Weather Conditions  
https://github.com/nick3499/mesowest_latest_ob  


## Other Weather APIs to try  
* Weather API https://github.com/weatherapicom/python  
