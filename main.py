import logging
import asyncio
import os
from typing import NoReturn
from interface import Interface
from weather_api import WeatherApi
from telegram_bot import TelegramBot, MensaggeType


async def main() -> NoReturn:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    logger = logging.getLogger('Telegram Bot')

    wapi = WeatherApi()
    bot = TelegramBot(logger)
    count = 0

    while True:
        message = await bot.wait_menssage()
        if message is MensaggeType.MENSAGGE_TYPE_HELP:
            await bot.send_help()
        elif message is MensaggeType.MENSAGGE_TYPE_START:
            await bot.send_start()
        elif message is MensaggeType.MENSAGGE_TYPE_NO_SUPPORT:
            bot.ignore_current_message()
        else:
            if message is MensaggeType.MENSAGGE_TYPE_LOCATION:
                lat = str(bot.current_update.message.location.latitude)
                lon = str(bot.current_update.message.location.longitude)
                query = lat + ',' + lon
            if message is MensaggeType.MENSAGGE_TYPE_PLACE:
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
                if error.code == 615:
                    await bot.send_message('City dont found, please try again.')
                    continue
                else:
                    await bot.send_message('Sorry, we are currently unable to process your request.\
                                            We apologize for any inconvenience this may have caused.')
                raise error

            weather = wapi.get_weather(query)
            weather = wapi.parser_request()
            interface = Interface(weather)

            interface.set_background()
            interface.make_imagen()
            interface.save_imagen('.tmp/' + str(count) + '.png')
            await bot.send_weather('.tmp/' + str(count) + '.png')
            wapi.clean_request()
            count += 1


if __name__ == "__main__":
    if not os.path.exists('.tmp'):
        os.makedirs('.tmp')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
        if os.path.exists('.tmp'):
            os.remove('.tmp')
