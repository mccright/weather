# weather
Display one-line of weather information in you terminal for any city+country supported on [OpenWeather](https://openweathermap.org/).  

If this is something you are considering, look at the vastly superior [https://github.com/gourlaysama/girouette](https://github.com/gourlaysama/girouette)!  It is an exceptionally flexible utility for displaying OpenWeather information in a terminal.  

#### Why not girouette?  
I have moved/added my Linux and Windows environments too many times in recent years.  Some of those moves involved more time than I will admit reconfiguring my new giroutte installation.  
I have been using giroutte long enough to know what I want to see in my terminal, so it seemed rational to just code up a short script to fetch openweathermap.org data myself.  

#### This utility:  
Returns a terse weather report using data from an api.openweathermap.org service on a single line in my standard terminal configuration.  

#### Examples:  
```terminal
matt@hostname:/testing/$ python3 weather.py
2023-12-23 13:23, 42.51°F, feels like 34.74°F, wind S 16.11 m/h, broken clouds, humidity 40%

matt@hostname:/testing/$ python3 weather.py -c denver
2023-12-10 13:10, 62.85°F, feels like 59.83°F, wind SSW 2.71 m/h, clear sky, humidity 21%

matt@hostname:/testing/$ python3 weather.py -c chicago -n us -f weather.ini
2023-12-29 13:29, 31.6°F, feels like 22.51°F, wind SSW 11.5 m/h, scattered clouds, humidity 49%

matt@hostname:/testing/$ python3 weather.py -c rome -n it
2023-12-30 13:30, 49.57°F, feels like 48.79°F, wind SSE 3.44 m/h, clear sky, humidity 62%

matt@hostname:/testing/$ python3 weather.py -h
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

