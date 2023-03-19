import os
import asyncio
import logging
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)

if __version_info__ < (20, 0, 0, 'alpha', 1):
    raise RuntimeError(
        f'It is not compatible with your current PTB version {TG_VER}.'
        f'visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html'
    )

from telegram.error import Forbidden, NetworkError
from telegram.constants import MessageEntityType
from telegram import Bot, Update
from typing import NoReturn
from enum import Enum

'''
Constants
---------
    Different husefully constants.
'''
TELEGRAM_BOT_TIMEOUT = 2
TELEGRAM_BOT_HELP_COMMAND = '/HELP'
TELEGRAM_BOT_START_COMMAND = '/START'
TELEGRAM_BOT_PLACE_COMMAND = '/PLACE'

TELEGRAM_BOT_HELP_TEXT = '''\
*********** The twister Bot ***********
Usage:
* /help: Get help mensagge.\n
* /start: Get information about this Bot.\n
* /place city: Get current weather in that city.\n
* Location: Get current weather in your location.
***************************************'''

TELEGRAM_BOT_START_TEXT = '''\
*********** The twister Bot ***********
It uses to obtain the weather in the different\
cities of the world.
This bot may be tracked your data, username,\
location, lenguaje, etc.\n\n
Author: Agustin Urquiza
agustin.h.urquiza@gmail.com
***************************************'''


class MensaggeType(Enum):
    '''
    Enum use in TelegramBot class. Representing the different kind of mensagge
    available.
    '''
    MENSAGGE_TYPE_NO_SUPPORT = 0
    MENSAGGE_TYPE_HELP = 1
    MENSAGGE_TYPE_START = 2
    MENSAGGE_TYPE_PLACE = 3
    MENSAGGE_TYPE_LOCATION = 4


class TelegramBot:
    '''
    This class implements a Telegram bot that provides the weather in different
    cities of the world.

    Attributes
    ----------
        bot : telegram.Bot
            Representing the Telegram bot associated with this instance of the
            TelegramBot class.
        update_id : int
            An integer representing the ID of the latest update processed.
        updates : (Update)
            A tuple of Update objects representing the updates received by the
            Telegram bot associated.
        logger : Logger
            The logger used to log messages and events related to this instance.
        current_update : Update
            This attribute is updated whenever a new update is received and
            processed by the wait_message method.

    Methods
    -------
        __init__(logger) -> NoReturn:
            Initializes the class and sets up the telegram bot.
        filter_update(update) -> MensaggeType:
            Filters the updates received by the bot and determines the type of
            message received.
        wait_message() -> MensaggeType:
            Waits for a new message from the user and returns the type of message received.
        send_help() -> NoReturn:
            Sends a help message to the user.
        send_start() -> NoReturn:
            Sends a start message to the user.
        send_weather(img_path) -> NoReturn:
            Sends a photo to the user.
        get_current_user() -> dict:
            Returns a dictionary with the current user's information.
        ignore_current_message() -> NoReturn:
            Ignores the current message received.
    '''

    def __init__(self, logger: logging.Logger) -> NoReturn:
        '''
        Constructor of the TelegramBot class.

        Parameters
        ----------
            logger : logging.Logger
                Logger object to log events in the bot.
        '''
        self.bot = Bot(os.environ['TELEGRAM_TOKEN'])
        self.update_id = None
        self.updates = ()
        self.logger = logger
        self.current_update = None

        self.logger.info('Listening for new messages...')


    async def filter_update(self, update: Update) -> MensaggeType:
        '''
        Classify a message according to the command sent by the user.

        Parameters
        ----------
            update : Update
                That contains information about the message sent by the user.

        Returns
        -------
            MensaggeType
                Type of command sent by the user.
        '''
        if update.message and update.message.location:
            return MensaggeType.MENSAGGE_TYPE_LOCATION
        elif (update.message and update.message.entities and
              update.message.entities[0].type == MessageEntityType.BOT_COMMAND.value):
            if TELEGRAM_BOT_HELP_COMMAND in update.message.text.upper():
                return MensaggeType.MENSAGGE_TYPE_HELP
            elif TELEGRAM_BOT_START_COMMAND in update.message.text.upper():
                return MensaggeType.MENSAGGE_TYPE_START
            elif TELEGRAM_BOT_PLACE_COMMAND in update.message.text.upper():
                return MensaggeType.MENSAGGE_TYPE_PLACE
            else:
                return MensaggeType.MENSAGGE_TYPE_NO_SUPPORT
        else:
            return MensaggeType.MENSAGGE_TYPE_NO_SUPPORT


    async def wait_menssage(self) -> MensaggeType:
        '''
        This method waits for new messages to arrive and returns the type of message
        received.

        Returns:
        --------
            MensaggeType:
                An Enum representing the type of message received.
        '''
        try:
            if self.update_id is None:
                # Clear old updates.
                self.update_id = (await self.bot.get_updates())[0].update_id + 1
                await self.bot.get_updates(offset=self.update_id)
        except IndexError:
            self.update_id = 0

        while True:
            try:
                self.updates = await self.bot.get_updates(offset=self.update_id,
                                                          timeout=TELEGRAM_BOT_TIMEOUT)
            except NetworkError:
                await asyncio.sleep(1)
            except Forbidden:
                # The user has removed or blocked the bot.
                self.update_id += 1

            if self.updates != ():
                self.current_update = self.updates[0]
                self.update_id = self.current_update.update_id
                break

        type = await self.filter_update(self.current_update)
        user = self.current_update.message.from_user.username
        self.logger.info(f'New message from: {user} type: {type}')
        return type


    async def send_help(self) -> NoReturn:
        '''
        This method sends the help message to the user.
        '''
        self.update_id += 1
        await self.current_update.message.reply_text(TELEGRAM_BOT_HELP_TEXT)
        user = self.current_update.message.from_user.username
        self.logger.info(f'It has replied to: {user}.')


    async def send_start(self) -> NoReturn:
        '''
        This method sends the start message to the user.
        '''
        self.update_id += 1
        await self.current_update.message.reply_text(TELEGRAM_BOT_START_TEXT)
        user = self.current_update.message.from_user.username
        self.logger.info(f'It has replied to: {user}.')


    async def send_weather(self, img_path: str) -> NoReturn:
        '''
        This method sends the current weather to the user.

        Parameters:
        -----------
        img_path: str
            The path of the image containing the weather information.
        '''
        self.update_id += 1
        await self.current_update.message.reply_photo(photo=img_path)
        user = self.current_update.message.from_user.username
        self.logger.info(f'It has replied to: {user}.')


    def get_current_usser(self) -> dict:
        '''
        Returns a dictionary representing the current user who sent the message.

        Returns:
        --------
        dict :
            The dictionary includes the following keys:
                user = {
                    id : int,
                    first_name: str,
                    last_name: str or None,
                    username: str or None,
                    language_code: str or None
                }
        '''
        return self.current_update.message.from_user.to_dict()


    def ignore_current_message(self) -> NoReturn:
        '''
        Ignore current message beacuse the menssage isnt support.
        '''
        self.update_id += 1
