# Twister
## _The best Telegram bot for get weather_

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


![London](https://github.com/agustinhurquiza/twister/blob/main/examples/1.png)
![Sao Pablo](https://github.com/agustinhurquiza/twister/blob/main/examples/2.png)

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

1) Create environment $ virtualenv env
2) Active environment $ source env/bin/activate
3) Install requirements $ pip install -r requirements.txt
4) Save tokens(*) $ source password.sh key_file.bin <Telegram token> <Api weatherstack Token>
5) Run program $ python main.py [flags]
    * --nodatabase: Disable database tracking
    * --showstat: Show statistics at the end of the program.
6) Finish program $ ctrl-c

\(*) Create Telegram Token: https://core.telegram.org/bots/tutorial\
\(*) Create Api WeatherStack key: https://weatherstack.com/documentation\
\(*) Create key_file.bin: $ openssl rand -base64 32 > key.bin


## Statitics

First you need enable the tracking see (How run).

Once you have pressed Ctrl-C, the Python program will proceed to calculate and display two plots - one showing the numbers of requests and clients, and another displaying a map with the locations of the requests

![map](https://github.com/agustinhurquiza/twister/blob/main/examples/map.png)


## Architecture

```mermaid
classDiagram
      Animal <|-- Duck
      Animal <|-- Fish
      Animal <|-- Zebra
      Animal : +int age
      Animal : +String gender
      Animal: +isMammal()
      Animal: +mate()
      class Duck{
          +String beakColor
          +swim()
          +quack()
      }
      class Fish{
          -int sizeInFeet
          -canEat()
      }
      class Zebra{
          +bool is_wild
          +run()
      }
```
