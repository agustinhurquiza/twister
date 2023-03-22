import pixie
import warnings
import os
from typing import NoReturn
from background import Background
from wsymbol import WSymbol

'''
Constants
---------
    The path of the default font.
'''
INTERFACE_DEFAULT_FONT = 'src/Ubuntu-Regular_1.ttf'
if not os.path.isfile(INTERFACE_DEFAULT_FONT):
    warnings.warn('Default font not found.')

'''
Constants
---------
    Used to match the weather with the background image.
'''
INTERFACE_SNOW_CODES = [371, 368, 338, 335, 332, 329, 326, 323, 230, 179, 227]
INTERFACE_THUNDER_CODES = [395, 392, 389, 200, 386]
INTERFACE_CLOUDY_CODES = [119, 116, 263, 266, 317]
INTERFACE_RAIN_CODES = [350, 374, 362, 284, 281, 182, 143, 122, 353, 296, 176, 311,
                        293, 377, 320, 365, 359, 356, 305, 299, 185, 314, 308, 302]
INTERFACE_CLEAR_CODES = [113]
INTERFACE_FOG_CODES = [260, 248]


class Interface():
    '''
    A class used for making an image using Pixie.

    Attributes
    ----------
        response : dict
            The response obtained from the API. The format is:
                response = {'country': str,
                            'region': str,
                            'temperature': int,
                            'weather_code': int,
                            'weather_descriptions': [str],
                            'wind_speed': int,
                            'wind_degree': int,
                            'wind_dir': str,
                            'pressure': int,
                            'precip': int,
                            'humidity': int,
                            'cloudcover': int,
                            'feelslike': int,
                            'uv_index': int,
                            'visibility': int,
                            'is_day': bool}.
        font : pixie.Font
            The font used in the image, default is 'Ubuntu-Regular_1.ttf'.
        background : Background
            Contains information about the background image.
        wsymbol : WSymbol
            Contains information about the icons used in the image.
        width : int
            The width of the image.
        height : int
            The height of the image.
        image : pixie.Image
            The edited image.
        white_font : bool
            True if the background is black, False otherwise.

    Methods
    -------
        __init__(response: dict, font=INTERFACE_DEFAULT_FONT) -> NoReturn:
            Constructs all the necessary attributes for the Interface object.

        set_background() -> NoReturn:
            Sets the background image.

        set_font(font_path: str) -> NoReturn:
            Sets a different font to use in the image.

        make_font(size: int) -> pixie.Font:
            Edits the font for the different text in the image.

        make_image() -> NoReturn:
            Draws the different parts of the final picture.

        save_image(path) -> NoReturn:
            Saves the image in the specified path.
    '''


    def __init__(self, response: dict, font: str = INTERFACE_DEFAULT_FONT) -> NoReturn:
        '''
        Constructs all the necessary attributes for the Interface object.

        Parameters
        ----------
            response : dict
                Response obtained from the API, format:
                    {
                        'temperature': float,
                        'region': str,
                        'country': str,
                        'is_day': bool,
                        'weather_code': int,
                        'weather_descriptions': list[str],
                        'wind_speed': float,
                        'wind_degree': int,
                        'wind_dir': str,
                        'pressure': float,
                        'precipitation': float,
                    }
            font : str
                The font used in the image, default 'Ubuntu-Regular_1.ttf'.
        '''
        self.response = response
        self.font = pixie.read_typeface(font)
        self.background = None
        self.wsymbol = WSymbol()
        self.width = 0
        self.height = 0
        self.image = None
        self.white_font = False


    def set_background(self) -> NoReturn:
        '''
        Set the background image.
        '''
        if self.response['weather_code'] in INTERFACE_SNOW_CODES:
            self.background = Background.BACKGROUND_SNOW
        elif self.response['weather_code'] in INTERFACE_THUNDER_CODES:
            self.background = Background.BACKGROUND_THUNDER
        elif self.response['weather_code'] in INTERFACE_CLOUDY_CODES:
            if self.response['is_day']:
                self.background = Background.BACKGROUND_CLOUDY_DAY
            else:
                self.background = Background.BACKGROUND_CLOUDY_NIGHT
        elif self.response['weather_code'] in INTERFACE_RAIN_CODES:
            self.background = Background.BACKGROUND_RAINY
        elif self.response['weather_code'] in INTERFACE_CLEAR_CODES:
            if self.response['is_day']:
                self.background = Background.BACKGROUND_SUNNY_DAY
            else:
                self.background = Background.BACKGROUND_SKY_NIGHT
        elif self.response['weather_code'] in INTERFACE_FOG_CODES:
            self.background = Background.BACKGROUND_FOG
        else:
            message = 'Unknown background, the code: ' + str(self.response['weather_code']) + ' was not found'
            warnings.warn(message)
            self.background = Background.BACKGROUND_UNKNOWN

        self.width, self.height = self.background.get_size()
        (path, self.white_font) = self.background.get_image_path()
        self.image = pixie.read_image(path)


    def set_font(self, font_path: str) -> NoReturn:
        '''
        Set a different font used in the image.

        Parameters
        ----------
            font_path : str
                Path for the font.
        '''
        if not os.path.isfile(font_path):
            warnings.warn('Default font not found.')
        self.font = pixie.read_typeface(font_path)


    def make_font(self, size: int) -> pixie.Font:
        '''
        Constructs a font object with the given size.

        Parameters
        ----------
            int
                The size of the font.
        Returns
        -------
            Pixie.Font
                The resulting font object.
        '''
        if not self.white_font:
            color = pixie.Color(0, 0, 0, 0.78125)
        else:
            color = pixie.Color(0.78125, 0.78125, 0.78125, 1)

        font = self.font.new_font()
        font.paint.color = color
        font.size = size
        return font


    def make_imagen(self) -> NoReturn:
        '''
        Draw the different parts of the final picture.
        '''
        icon = self.wsymbol.get_symbol_path_from_code(self.response['weather_code'],
                                                      self.response['is_day'])
        icon = pixie.read_image(icon)
        tmpr = self.wsymbol.get_symbol_temp_from_code(self.response['temperature'])
        tmpr = pixie.read_image(tmpr)

        path = pixie.Path()
        path.rounded_rect(0.05 * self.width, 0.5 * self.height, self.width - (0.1 * self.width),
                          self.height - (0.45 * self.height), 25, 25, 25, 25)

        mask = pixie.Mask(self.width, self.height)
        mask.fill_path(path)

        blur = self.image.copy()
        blur.blur(100)
        blur.mask_draw(mask)
        self.image.draw(blur)

        self.image.draw(icon, pixie.translate(0.1 * self.width, 0.07 * self.height) * pixie.scale(0.4, 0.4))
        self.image.draw(tmpr, pixie.translate(0.5 * self.width, 0.07 * self.height) * pixie.scale(0.4, 0.4))

        self.image.fill_text(font=self.make_font(70),
                             text=str(self.response['temperature']) + ' °C',
                             h_align=pixie.LEFT_ALIGN,
                             bounds=pixie.Vector2(0.2 * self.width, 0.1 * self.height),
                             transform=pixie.translate(0.75 * self.width, 0.15 * self.height))

        self.image.fill_text(font=self.make_font(30),
                             text=self.response['region'] + ', ' + self.response['country'],
                             h_align=pixie.CENTER_ALIGN,
                             bounds=pixie.Vector2(1 * self.width, 0.05 * self.height),
                             transform=pixie.translate(0 * self.width, 0.52 * self.height))

        self.image.fill_text(font=self.make_font(30),
                             text=' ,'.join(self.response['weather_descriptions']),
                             h_align=pixie.CENTER_ALIGN,
                             bounds=pixie.Vector2(1 * self.width, 0.05 * self.height),
                             transform=pixie.translate(0 * self.width, 0.58 * self.height))

        text = 'Wind speed: {} Km/H \nWind degree: {}°\nWind Dir: {} \nPressure: {} MB\nPrecip: {} MM'
        self.image.fill_text(font=self.make_font(20),
                             text=text.format(self.response['wind_speed'], self.response['wind_degree'],
                                              self.response['wind_dir'], self.response['pressure'],
                                              self.response['precip']),
                             h_align=pixie.LEFT_ALIGN,
                             bounds=pixie.Vector2(0.3 * self.width, 0.2 * self.height),
                             transform=pixie.translate(0.10 * self.width, 0.72 * self.height))

        text = 'Humidity: {} kPa\nCloud cover: {} okta\nFeelslike: {} °C\nUV index: {} \nVisibility: {} Km/H\n'
        self.image.fill_text(font=self.make_font(20),
                             text=text.format(self.response['humidity'], self.response['cloudcover'],
                                              self.response['feelslike'], self.response['uv_index'],
                                              self.response['visibility']),
                             h_align=pixie.RIGHT_ALIGN,
                             bounds=pixie.Vector2(0.35 * self.width, 0.2 * self.height),
                             transform=pixie.translate(0.55 * self.width, 0.72 * self.height))


    def save_imagen(self, path: str) -> NoReturn:
        '''
        Save the imagen in the especific path.

        Parameters
        ----------
            path : str
                The path where the image is saved.
        '''
        self.image.write_file(path)
