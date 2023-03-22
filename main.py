#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import asyncio
import time
import os
import sys
from typing import NoReturn
from interface import Interface
from weather_api import WeatherApi
from data_base import Database
from telegram_bot import TelegramBot, MessageType
import argparse
import signal

'''
This module includes the main function and auxiliary functions to run the Telegram bot.

Usage:
-----
    To run this module, use the following command:
        $ python bot.py [options]

Options:
-------
    --nodatabase: Disable database tracking
    --showstat: Show statistics at the end of the program.

Functions:
---------
    signal_handler(signal, frame) -> NoReturn:
        Handle keyboard interrupts by raising a KeyboardInterrupt.
    parser() -> NoReturn:
        Parses command-line arguments.
    main(db: Database, track: bool) -> NoReturn:
        The main function that runs the Telegram bot.
        It receives the Database instance and a boolean flag to indicate whether to track messages in the database.
        It starts an infinite loop to listen for incoming messages and handle them accordingly.
'''


EXTENSION = '.png'
TEMP_FILE = '.tmp/'
ERROR_CODE_CITY_NOT_FOUND = 615


def signal_handler(signal: signal.Signals, frame) -> NoReturn:
    raise KeyboardInterrupt
    quit()


def parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('--nodatabase', action='store_true',
                        help='Disable database tracking')

    parser.add_argument('--showstat', action='store_true',
                        help='Show statistics at the end of the program.')

    args = parser.parse_args()
    return args


async def main(db: Database, track: bool) -> NoReturn:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger('Telegram Bot')

    wapi = WeatherApi()
    bot = TelegramBot(logger)
    count = 0

    while True:
        message = await bot.wait_menssage()
        is_real_location = False

        if message is MessageType.MENSAGGE_TYPE_HELP:
            await bot.send_help()
        elif message is MessageType.MENSAGGE_TYPE_START:
            await bot.send_start()
        elif message is MessageType.MENSAGGE_TYPE_NO_SUPPORT:
            bot.ignore_current_message()
        else:
            if message is MessageType.MENSAGGE_TYPE_LOCATION:
                lat = str(bot.current_update.message.location.latitude)
                lon = str(bot.current_update.message.location.longitude)
                query = lat + ',' + lon
            if message is MessageType.MENSAGGE_TYPE_PLACE:
                is_real_location = True
                try:
                    query = bot.current_update.message.text.split('/place ')[1]
                except IndexError as e:
                    await bot.send_message('City dont found, please try again.')
                    continue

                true_location = wapi.check_query(query)
                if not true_location:
                    await bot.send_message('Error city dont found.')
                    continue
            try:
                pass
            except WeatherStackAPIError as error:
                if error.code == ERROR_CODE_CITY_NOT_FOUND:
                    await bot.send_message('City dont found, please try again.')
                    continue
                else:
                    await bot.send_message('Sorry, we are currently unable to process your request.\
                                            We apologize for any inconvenience this may have caused.')
                raise error

            if track:
                user = bot.get_current_usser()
                if not db.user_exist(user['id']):
                    db.add_user(user)

            weather = wapi.get_weather(query)
            weather = wapi.parser_request()
            if track:
                db.add_register(weather, user['id'], is_real_location, time.time())

            interface = Interface(weather)
            interface.set_background()
            interface.make_imagen()
            interface.save_imagen(TEMP_FILE + str(count) + EXTENSION)
            await bot.send_weather(TEMP_FILE + str(count) + EXTENSION)
            wapi.clean_request()
            interface = None
            count += 1


if __name__ == '__main__':
    args = parser()
    db = Database()
    signal.signal(signal.SIGINT, signal_handler)

    start_time = int(time.time())

    if not os.path.exists(TEMP_FILE):
        os.makedirs(TEMP_FILE)
    try:
        asyncio.run(main(db, not args.nodatabase))
    except KeyboardInterrupt:
        if os.path.exists(TEMP_FILE):
            os.system('rm -r ' + TEMP_FILE)
        if args.showstat and not args.nodatabase:
            print('\n*********************************************************')
            db.draw_locations_in_a_map_and_statistics(start_time)
            print('*********************************************************\n')
            quit()
