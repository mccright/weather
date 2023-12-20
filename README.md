# weather
Display one-line of weather information in your terminal for any city+country supported on [OpenWeather](https://openweathermap.org/).  

If this is something you are considering, look at the vastly superior [https://github.com/gourlaysama/girouette](https://github.com/gourlaysama/girouette)!  It is an exceptionally capable and flexible utility for displaying OpenWeather information in a terminal and may be a perfect for many.  

### Why not girouette?  
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

### This utility:  
Returns a terse weather report using data from an api.openweathermap.org service on a single line in my standard terminal configuration.  The report includes: 
* date and time of weather measurements (in your local time zone if it can be determined by OpenWeatherMap)  
* measured temperature, defaults to Fahrenheit (change via command line/alias or default in code for Celsius)  
* "feels like" temperature, defaults to Fahrenheit (change via command line/alias or default in code for Celsius or Kelvin)  
* wind direction  
* wind speed, defaults to miles/hour (change via command line/alias or default in code for km/hour)  
* humidity in percent  

This script requires an [OpenWeather API key](https://openweathermap.org/appid) (free for 1 call per second -- put it in the configuration file).  

You can supply a city and nation on the command line.  City names having one or more spaces, must be surrounded by quotes (e.g. "los angeles").  The nation is specified using the 2-letter [ISO 3166 code](https://en.wikipedia.org/wiki/ISO_3166).  See the examples below.  

### Installation:
I assume that you already have Python installed and use it regularly.  Clone this repository (```git clone https://github.com/mccright/weather-in-terminal.git```) and make any customizations to meet your needs.  Then locate ```weather.py``` and ```weather.ini``` in your local bin path.  Then add a shell alias (*with command line options to meet your needs*) analogous to the example below:  

```terminal
# Get the current weather
# Depends on a config file in ~/bin/weather.ini (or some 
# other location, which you will specify on the command line)
if [ -x ~/bin/weather.py ]; then
        alias weather='/usr/bin/python3 ~/bin/weather.py'
fi
```

In a Windows-only environment you can also set up a Windows shortcut pointing to (*with paths that match your endpoint and with command line options that meet your needs*):  
```terminal
C:\Windows\System32\cmd.exe /K "C:\PROGRA~1\Python311\python.exe  C:\testing\weather.py"
```

### Examples:  
*Without using the ```alias``` approach outlined above, to demonstrate command line options...*  
```terminal
matt@hostname:/testing$ python3 weather.py
2023-12-19 13:23, 42.51°F, feels like 34.74°F, wind S 16.11 m/h, broken clouds, humidity 40%

matt@hostname:/testing$ python3 weather.py -c denver
2023-12-19 13:10, 62.85°F, feels like 59.83°F, wind SSW 2.71 m/h, clear sky, humidity 21%

matt@hostname:/testing$ python3 weather.py -c chicago -n us -f weather.ini
2023-12-19 13:29, 31.6°F, feels like 22.51°F, wind SSW 11.5 m/h, scattered clouds, humidity 49%

matt@hostname:/testing$ python3 weather.py -c rome -n it
2023-12-19 13:30, 49.57°F, feels like 48.79°F, wind SSE 3.44 m/h, clear sky, humidity 62%

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

options:
  -h, --help            show this help message and exit
  -d, --debug           Use to send debug logging to console
  -l LANGUAGE, --language LANGUAGE
                        Either collect the language. Or just use the default language.
  -c CITY_NAME, --city_name CITY_NAME
                        Either collect the target city name. Or just use the default city name.
  -n NATION_NAME, --nation_name NATION_NAME
                        Either collect the target nation name. Or just use the default country name
  -u UNITS_OF_MEASUREMENT, --units_of_measurement UNITS_OF_MEASUREMENT
                        Changes temp and wind speed units. Default: "imperial" Options are: "standard" (Kelvin/km),
                        "metric" (Celsius/km), and "imperial" (Fahrenheit/miles) units.
  -f CONFIG_FILE_NAME, --config_file_name CONFIG_FILE_NAME
                        Name of the configuration file.
```

