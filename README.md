# weather
Display one-line of weather information in your terminal for any city+country supported on [OpenWeather](https://openweathermap.org/).  

If this is something you are considering, look at the vastly superior [https://github.com/gourlaysama/girouette](https://github.com/gourlaysama/girouette)!  It is an exceptionally capable and flexible utility for displaying OpenWeather information in a terminal.  

#### Why not girouette?  
I have moved/added my Linux and Windows environments too many times in recent years.  Some of those moves involved more time than I will admit reconfiguring my new giroutte installation.  

After giroutte installation and configuration, on Linux I added a bash alias that mapped the command "weather" to giroutte.  On Windows I did an analogous "*alias*" using a command file (*and later Powershell*).  
Here is an example for Linux from my .bash_aliases file:  

```terminal
# Get the current weather
# Depends on a config file in ~/.config/girouette/config.yml
if [ -x ~/bin/girouette ]; then
        alias weather='/usr/bin/echo `~/bin/girouette`'
fi
```

I have been using giroutte long enough to know what I want to see in my terminal, so it seemed rational to just code up a short script to fetch openweathermap.org data myself.  

#### This utility:  
Returns a terse weather report using data from an api.openweathermap.org service on a single line in my standard terminal configuration.  

You can supply a city and nation on the command line.  City names having one or more spaces, must be surrounded by quotes (e.g. "los angeles").  The nation is specified using the 2-letter [ISO 3166 code](https://en.wikipedia.org/wiki/ISO_3166).  See the examples below.  

#### Examples:  
```terminal
matt@hostname:/testing$ python3 weather.py
2023-12-23 13:23, 42.51°F, feels like 34.74°F, wind S 16.11 m/h, broken clouds, humidity 40%

matt@hostname:/testing$ python3 weather.py -c denver
2023-12-10 13:10, 62.85°F, feels like 59.83°F, wind SSW 2.71 m/h, clear sky, humidity 21%

matt@hostname:/testing$ python3 weather.py -c chicago -n us -f weather.ini
2023-12-29 13:29, 31.6°F, feels like 22.51°F, wind SSW 11.5 m/h, scattered clouds, humidity 49%

matt@hostname:/testing$ python3 weather.py -c rome -n it
2023-12-30 13:30, 49.57°F, feels like 48.79°F, wind SSE 3.44 m/h, clear sky, humidity 62%

matt@hostname:/testing$ python3 weather.py -c edinburgh -n uk
2023-12-58 16:58, 43.02°F, feels like 34.54°F, wind WSW 19.57 m/h, clear sky, humidity 82%

matt@hostname:/testing$ python3 weather.py -c santiago -n cl
2023-12-01 17:01, 71.17°F, feels like 70.05°F, wind SW 14.97 m/h, smoke, humidity 44%

matt@hostname:/testing$ python3 weather.py -c nairobi -n ke
2023-12-07 17:07, 63.72°F, feels like 63.64°F, wind NNE 6.91 m/h, broken clouds, humidity 82%

matt@hostname:/testing$ python3 weather.py -c "los angeles" -n us
2023-12-13 17:13, 63.43°F, feels like 63.09°F, wind SE 9.22 m/h, overcast clouds, humidity 77%

matt@hostname:/testing$ python3 weather.py -h
usage: weather [-h] [-d] [-c CITY_NAME] [-n NATION_NAME] [-f CONFIG_FILE_NAME]
  
weather: a terminal script to fetch current weather from openweathermap.org
  
optional arguments:
    -h, --help            show this help message and exit
    -d, --debug           Use to send debug logging to console
    -c CITY_NAME, --city_name CITY_NAME
                          Either collect the target city name. Or just use the default city name.
    -n NATION_NAME, --nation_name NATION_NAME
                          Either collect the target nation name. Or just use the default country name
    -f CONFIG_FILE_NAME, --config_file_name CONFIG_FILE_NAME
                          Name of the configuration file.
```

