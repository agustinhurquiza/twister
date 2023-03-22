# Twister
## _The best Telegram bot for get weather_

## Disclaimer

This project was created for demonstrate and improvement my abilities in the differents areas like:
- Python
- Security
- Object-oriented programming (OOP)
- Documentation
- Development the news projects
- Git:
    * Basic commands
    * Branches
    * Relases
- Application management
- Data Base
- Data Analytic
- Code Style

I'm not trying to create something revolutionary or useful.

## About me
My name is [Agustin Urquiza](agustin.h.urquiza@gmail.com), I have a Bachelor in computer science obtained in FaMAF UNC. I have four years of experience in software development.


## Use cases and front end
I implemented a simple [telegram bot](https://t.me/terminator_2000_bot) that can get the weather in different places around the world. It can respond to two possible commands: **Telegram location** and **/place [city]**. The bot responds to your message with a .png image (124 KB). If you share your real location, it only responds once. Here are some examples:

<p align="center">
<img src="https://github.com/agustinhurquiza/twister/blob/main/examples/1.png" width="400" height="380">  <img src="https://github.com/agustinhurquiza/twister/blob/main/examples/2.png" width="400" height="380">
</p>

Also the bot support two commands more:

- **help:**
    > ************************* The twister Bot *************************\
    > Usage:\
    > \* /help: Get help mensagge.\
    > \* /start: Get information about this Bot.\
    > \* /place city: Get current weather in that city.\
    > \* Location: Get current weather in your location.

- **start:**
    > ************************* The twister Bot *************************\
    > It uses to obtain the weather in the different cities of the world.\
    > This bot may be tracked your data, username, location, lenguaje, etc.\
    > Author: Agustin Urquiza\
    > agustin.h.urquiza@gmail.com

## How run
Below, I have listed the steps to run the program:

1) Create environment ``` $ virtualenv env```
2) Active environment ``` $ source env/bin/activate```
3) Install requirements ``` $ pip install -r requirements.txt```
4) Save tokens(*) ```$ source password.sh key_file.bin <Telegram token> <Api weatherstack Token>```
5) Run program ``` $ python main.py [flags]```
    * --nodatabase: Disable database tracking
    * --showstat: Show statistics at the end of the program.
6) Finish program $ ctrl-c

\(\*\) Create Telegram Token: https://core.telegram.org/bots/tutorial \
\(\*\) Create Api WeatherStack key: https://weatherstack.com/documentation \
\(\*\) Create key_file.bin: ``` $ openssl rand -base64 32 > key.bin```


## Statitics

First you need enable the tracking see (How run).

Once you have pressed Ctrl-C, the Python program will proceed to calculate and display two plots - one showing the numbers of requests and clients, and another displaying a map with the locations of the requests. The files will save in stat directory.


<p align="center">
<img src="https://github.com/agustinhurquiza/twister/blob/main/examples/map.png" width="500" height="400">  <img src="https://github.com/agustinhurquiza/twister/blob/main/stat/2023-03-13_statistics.png" width="500" height="400">
</p>


## Architecture

### MessageType
Enum use in TelegramBot class. Representing the different kind of message available.

### WSymbol
This class handles the icons used in the different weather conditions.

### WeatherStackAPIError
Custom Exception for WeatherStack API errors.

### WeatherApi
This module provides a WeatherApi class for fetching weather data from the WeatherStack API.

### TelegramBot
This class implements a Telegram bot that provides the weather in different cities of the world.

### Interface
A class used for making an image using Pixie.

### Database
Class that encapsulates the database operations.

### Background
This class is an enum for different backgrounds.

```mermaid

classDiagram
      Background <|-- Enum
      MessageType <|-- Enum
      WeatherStackAPIError <.. WeatherApi
      WSymbol <.. Interface
      Background <.. Interface
      MessageType <.. TelegramBot
      WeatherApi <.. main
      TelegramBot <.. main
      Interface <.. main
      Database <.. main

      class Enum{
      }
      class MessageType{
      }
      class WSymbol{
          +__path__ : str
          +codes_dict : dict
          +parser_condition_codes()
          +get_symbol_path_from_code()
          +get_symbol_temp_from_code()
          +set_path()
          +get_abs_path()
          +get_size()
      }
      class WeatherStackAPIError{
          +code : int
          +error_type : str
          +info : str
      }
      class WeatherApi{
          +http : bool
          +domain : str
          +unit : char
          +request : dict
          +__init__()
          +base_url()
          +check_query()
          +get_weather()
          +parser_request()
          +clean_request()
          +raise_weather_stack_exception()
      }
      class TelegramBot{
          +bot : telegram.Bot
          +update_id : int
          +updates : (Update)
          +logger : Logger
          +current_update : Update
          +__init__()
          +filter_update()
          +wait_message()
          +send_help()
          +send_start()
          +send_weather()
          +get_current_user()
          +ignore_current_message()
      }
      class Interface{
          +response : dict
          +font : pixie.Font
          +background : Background
          +wsymbol : WSymbol
          +width : int
          +height : int
          +image : pixie.Image
          +white_font : bool
          +__init__()
          +set_background()
          +set_font()
          +make_font()
          +make_image()
          +save_image()
      }
      class Database{
          +__DB_LOCATION : str
          +__db_connection : sqlite3.Connection
          +__init__()
          +__del__()
          +__create_tabales__()
          +user_exist()
          +add_user()
          +add_register()
          +get_registers_from_epoch()
          +count_users()
          +draw_locations_in_a_map_and_statistics()
      }
      class Background{
          +__path__ : str
          +set_path(
          +get_abs_path()
          +get_image_path()
          +get_size()
      }
```
