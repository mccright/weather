#!/usr/bin/env python3
#
# Return a terse weather report using data from an api.openweathermap.org service.
# Examples:
#  matt@hostname:/testing/$ python3 weather.py
#  2023-12-23 13:23, 42.51°F, feels like 34.74°F, wind S 16.11 m/h, broken clouds, humidity 40%
#
#  matt@hostname:/testing/$ python3 weather.py -c denver
#  2023-12-10 13:10, 62.85°F, feels like 59.83°F, wind SSW 2.71 m/h, clear sky, humidity 21%
#
#  matt@hostname:/testing/$ python3 weather.py -c chicago -n us -f weather.ini
#  2023-12-29 13:29, 31.6°F, feels like 22.51°F, wind SSW 11.5 m/h, scattered clouds, humidity 49%
#
#  matt@hostname:/testing/$ python3 weather.py -c rome -n it
#  2023-12-30 13:30, 49.57°F, feels like 48.79°F, wind SSE 3.44 m/h, clear sky, humidity 62%
#
#  matt@hostname:/testing/$ python3 weather.py -c pune -n in
#  2023-12-20 11:35, 68.27°F, feels like 66.63°F, wind E 5.48 m/h, overcast clouds, humidity 39%
#
#  matt@hostname:/testing/$ python3 weather.py -h
#  usage: weather [-h] [-d] [-l LANGUAGE] [-c CITY_NAME] [-n NATION_NAME] [-u UNITS_OF_MEASUREMENT] [-f CONFIG_FILE_NAME]
#
#  weather: a terminal script to fetch current weather from openweathermap.org
#
#  options:
#    -h, --help            show this help message and exit
#    -d, --debug           Use to send debug logging to console (unfinished)
#    -l LANGUAGE, --language LANGUAGE
#                          Either collect the language. Or just use the default language.
#    -c CITY_NAME, --city_name CITY_NAME
#                          Either collect the target city name. Or just use the default city name.
#    -n NATION_NAME, --nation_name NATION_NAME
#                         Either collect the target nation name. Or just use the default country name
#    -u UNITS_OF_MEASUREMENT, --units_of_measurement UNITS_OF_MEASUREMENT
#                        Changes temp and wind speed units. Default: "imperial" Options are: "standard" (Kelvin/km),
#                        "metric" (Celsius/km), and "imperial" (Fahrenheit/miles) units.
#    -f CONFIG_FILE_NAME, --config_file_name CONFIG_FILE_NAME
#                         Name of the configuration file.
#
# Yes, I understand that this code has some long lines.

import argparse
from argparse import RawTextHelpFormatter
import configparser
import datetime
import json
import os
import requests
import sys

# Set some defaults
DEFAULT_LANGUAGE="en"
DEFAULT_CITY_NAME="urbandale"
DEFAULT_COUNTRY_NAME="us"
DEFAULT_CONFIG_FILE="weather.ini"
# The variable below changes temp and wind speed units. 
#    "standard" (Kelvin/km), 
#    "metric" (Celsius/km), and 
#    "imperial" (Fahrenheit/miles) units are available 
DEFAULT_UNITS="imperial"
# Set the environment variable name that contains your API key
API_KEY_VAR="OWM_API"


# set up the parser
# Use https://docs.python.org/3/library/argparse.html#argparse.RawTextHelpFormatter
# to wrap lines better in help messages
parser = argparse.ArgumentParser(
    prog="weather",
    description="weather: a terminal script to fetch current weather from openweathermap.org",
    formatter_class=RawTextHelpFormatter)

# add all the arguments
parser.add_argument(
    "-d", "--debug",
    required=False,
    default="False",
    action='store_true',
    help="Use to send debug logging to console (unfinished)")

parser.add_argument(
    # Either collect the language. Or just use the default language.
    "-l", "--language",
    required=False,
    default=DEFAULT_LANGUAGE,
    action='store',
    help="Either collect the language.\n \
Or just use the default language.")

parser.add_argument(
    # Either collect the target city name. Or just use the default city name.
    "-c", "--city_name",
    required=False,
    default=DEFAULT_CITY_NAME,
    action='store',
    help="Either collect the target city name.\n \
Or just use the default city name.")

parser.add_argument(
    # Either collect the target nation/country name. Or just use the default country name.
    "-n", "--nation_name",
    required=False,
    default=DEFAULT_COUNTRY_NAME,
    action='store',
    help="Either collect the target nation name.\n \
Or just use the default country name")

parser.add_argument(
    # Either collect the unit or measurement or use the default unit.
    "-u", "--units_of_measurement",
    required=False,
    default=DEFAULT_UNITS,
    action='store',
    help="Changes temp and wind speed units. Default: \"imperial\"\n \
Options are: \"standard\" (Kelvin/km),\n \
\"metric\" (Celsius/km), and\n \
\"imperial\" (Fahrenheit/miles) units.")

parser.add_argument(
    "-f", "--config_file_name",
    required=False,
    default=DEFAULT_CONFIG_FILE,
    action='store',
    help="Name of the configuration file.")

# Finished setting up the parser

# Get value from the environment, which, ideally 
# was sourced from your cloud secret store.
def get_env_value(val_name: str) -> str:
    try:
        if val_name in os.environ:
            OWM_API_VAL = os.environ.get(val_name)
        else:
            raise EnvironmentError(f"Failed because \"{val_name}\" is not set.")
    except Exception as e:
        print(f"Problem with environment variable: \"{val_name}\".")
        raise SystemExit(e)
    return OWM_API_VAL


# Get value from a config file: 
# https://github.com/mccright/PythonStuff/blob/main/otherNotes.md#get-values-from-a-config-file
def get_config(filename: str, section: str, val: str) -> str:
    config = configparser.ConfigParser()
    try:
        config.read([filename])
    except Exception as e:
        print(f"Failure getting config file. Filename: {filename}. Error: {e}")
        sys.exit()
    # create an object for a specific config file section
    try:
        weather = config[section]
    except Exception as e:
        print(f"Unknown config section problem. You requested section: {section}. Error: {e}")
        sys.exit()
    if weather == None:
        print(f"Empty or missing config section \"weather.\" ")
        sys.exit()
    # now get the values from that object
    try:
        target_value = weather.get(val)
        if target_value == None:
            print(f"Empty or missing config value. target_value = \"{target_value}\" ")
            sys.exit()
    except Exception as e:
        print(f"Failure getting config value \"{val}\" from file \"{filename}\". Error: {e}")        
        sys.exit()
    return target_value


def build_citynation(city_name: str, nation_name: str) -> str:
    try: 
        cityname = str(city_name).lower()
        citynation = cityname + str(",") + str(nation_name).lower()
    except Exception as e:
        print(f"Failure getting input or Improper input. Error: {e}")
        sys.exit()
    return citynation


# Thank you Matt Arderne at https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f?permalink_comment_id=3769668#gistcomment-3769668 
# for the excellent calculate_bearing(d) function    
def calculate_bearing(d: int) -> str:
    dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    ix = int(round(d / (360. / len(dirs))))
    return dirs[ix % len(dirs)]


def main():
    # parse the arg object
    arglist = parser.parse_args()
    # Use get_env_value() or get_config() function, depending on your setup.
    # This approach assumes that you have an environment 
    # variable "OWM_API" set with your OpenWeatherMap API key.
    OWMTOKEN = get_env_value(API_KEY_VAR)
    # Commented out the config file approach below because I am using an env var.
    """
    # This approach assumes that you have a configuration file "weather.ini"
    # that contains your OpenWeatherMap API key.
    try:
        # ToDo: fix the hard-coded variables below
        OWMTOKEN = get_config(arglist.config_file_name, 'weather', 'owmtokenA')
    except Exception as e:
        print(f"Generic failure getting config file content.\n \
from file \"{arglist.config_file_name}\"\n \
config section=\"weather\",\n \
value=\"owmtokenA\"\n \
Error: {e} -- {(sys.exc_info())}")
        exit()
    """
    # End of the config file code
    citynation = build_citynation(str(arglist.city_name), str(arglist.nation_name))
    url = (f"https://api.openweathermap.org/data/2.5/weather?appid={OWMTOKEN}&lang={arglist.language}&units={arglist.units_of_measurement}&q={citynation}")
    # print(f"{url}")
    try:
        response = requests.get(url)
    except requests.exceptions.Timeout as e:
        # ToDo: add retry code/loop
        print(f"Failed with timeout this run.")
        raise SystemExit(e)
    except requests.exceptions.TooManyRedirects as e:
        # Wrong URL?
        print(f"Failed with TooManyRedirects this run. Is the URL correct?: {url}")
        raise SystemExit(e)
    except requests.exceptions.RequestException as e:
    # Some other error -- little chance to recover. bail.
        print(f"Failed with TooManyRedirects this run.")
        raise SystemExit(e)
    try:
        jsonstr = json.loads(response.text)
        #print(f"{jsonstr}")
        posixdt = datetime.datetime.fromtimestamp(int(jsonstr['dt']))
        reporttime = datetime.date.strftime(posixdt, "%Y-%m-%d %R")
    except Exception as e:
        print(f"Failed this run. Bad response json? Error: ")
        raise SystemExit(e)
    try:
        winddir = calculate_bearing(jsonstr['wind']['deg'])
    except Exception as e:
        print("Failed this run. Bad wind degree int? Error: ")
        raise SystemExit(e)
    # Now print the data to the command line.
    try:
        print(f"{reporttime}, {jsonstr['main']['temp']}°F, feels like \
{jsonstr['main']['feels_like']}°F, wind {winddir} \
{jsonstr['wind']['speed']} m/h, \
{jsonstr['weather'][0]['description']}, \
humidity {jsonstr['main']['humidity']}%")
    except Exception as e:
        print("Failed this run. Problem printing to the terminal. Error: ")
        raise SystemExit(e)


if __name__ == '__main__':
    main()
