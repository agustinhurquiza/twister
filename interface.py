import pixie
import warnings
import os
from background import Background
from wsymbol import WSymbol

INTERFACE_DEFAULT_FONT = 'src/Ubuntu-Regular_1.ttf'
if not os.path.isfile(INTERFACE_DEFAULT_FONT):
    warnings.warn('Default font doesn\'t found.')

INTERFACE_SNOW_CODES    = [371, 368, 338, 335, 332, 329, 326, 323, 230, 179, 227]
INTERFACE_THUNDER_CODES = [395, 392, 389, 200, 386]
INTERFACE_CLOUDY_CODES  = [119, 116, 263, 266, 317]
INTERFACE_RAIN_CODES    = [350, 374, 362, 284, 281, 182, 143, 122, 353, 296, 176, 311,
                           293, 377, 320, 365, 359, 356, 305, 299, 185, 314, 308, 302]
INTERFACE_CLEAR_CODES   = [113]
INTERFACE_FOG_CODES     = [260, 248]


class Interface():

    def __init__(self, response:dict, font=INTERFACE_DEFAULT_FONT) -> None:
        self.response = response
        self.font = pixie.read_typeface(font)
        self.background = None
        self.wsymbol = WSymbol()
        self.width = 0
        self.hight = 0
        self.image = None


    def set_background(self) -> None:
        if self.response['weather_code'] in INTERFACE_SNOW_CODES:
            self.background = Background.BACKGORUND_SNOW
        elif self.response['weather_code'] in INTERFACE_THUNDER_CODES:
            self.background = Background.BACKGORUND_THUNDER
        elif self.response['weather_code'] in INTERFACE_CLOUDY_CODES:
            if self.response['is_day']:
                self.background = Background.BACKGORUND_CLOUDY_DAY
            else:
                self.background = Background.BACKGORUND_CLOUDY_NIGHT
        elif self.response['weather_code'] in INTERFACE_RAIN_CODES:
            self.background = Background.BACKGORUND_RAINY
        elif self.response['weather_code'] in INTERFACE_CLEAR_CODES:
            if self.response['is_day']:
                self.background = Background.BACKGORUND_SUNNY_DAY
            else:
                self.background = Background.BACKGORUND_SKY_NIGHT
        elif self.response['weather_code'] in INTERFACE_FOG_CODES:
            self.background = Background.BACKGORUND_FOG
        else:
            warnings.warn('Background unknown, the code: ' +
                          str(self.response['weather_code']) +
                          ' doesn\'t found')
            self.background = Background.BACKGORUND_UNKNOWN

        (self.width, self.hight) = self.background.get_size()
        self.image = pixie.read_image(self.background.get_image_path())


    def set_font(self, font_path : str) -> None:
        if not os.path.isfile(font_path):
            warnings.warn('Default font doesn\'t found.')
        self.font = pixie.read_typeface(font_path)


    def make_font(self, size: int) -> pixie.Font:
        font = self.font.new_font()
        font.size = size
        return font


    def make_imagen(self) -> None:
        icon = self.wsymbol.get_symbol_path_from_code(self.response['weather_code'], self.response['is_day'])
        icon = pixie.read_image(icon)
        tmpr = self.wsymbol.get_symbol_temp_from_code(self.response['temperature'])
        tmpr = pixie.read_image(tmpr)

        path = pixie.Path()
        path.rounded_rect(0.05*self.width, 0.5*self.hight, self.width-(0.1*self.width),
                          self.hight-(0.45*self.hight), 25, 25, 25, 25)

        mask = pixie.Mask(self.width, self.hight)
        mask.fill_path(path)

        blur = self.image.copy()
        blur.blur(100)
        blur.mask_draw(mask)
        self.image.draw(blur)

        self.image.draw(icon, pixie.translate(0.1*self.width, 0.07*self.hight) *
                              pixie.scale(0.4, 0.4))
        self.image.draw(tmpr, pixie.translate(0.5*self.width, 0.07*self.hight) *
                              pixie.scale(0.4, 0.4))

        self.image.fill_text(font=self.make_font(70),
                             text= str(self.response['temperature']) + ' °C',
                             h_align=pixie.LEFT_ALIGN,
                             bounds=pixie.Vector2(0.2*self.width, 0.1*self.hight),
                             transform=pixie.translate(0.75*self.width, 0.15*self.hight))

        self.image.fill_text(font=self.make_font(30),
                             text=self.response['region'] + ', ' + self.response['country'],
                             h_align=pixie.CENTER_ALIGN,
                             bounds=pixie.Vector2(1*self.width, 0.05*self.hight),
                             transform=pixie.translate(0*self.width, 0.52*self.hight))

        self.image.fill_text(font=self.make_font(30),
                             text=' ,'.join(self.response['weather_descriptions']),
                             h_align=pixie.CENTER_ALIGN,
                             bounds=pixie.Vector2(1*self.width, 0.05*self.hight),
                             transform=pixie.translate(0*self.width, 0.58*self.hight))

        text = 'Wind speed : {} Km/H \nWind degree : {}°\nWind Dir : {} \nPressure : {} MB\nPrecip : {} MM'
        self.image.fill_text(font=self.make_font(20),
                             text=text.format(self.response['wind_speed'], self.response['wind_degree'],
                                              self.response['wind_dir'], self.response['pressure'],
                                              self.response['precip']),
                             h_align=pixie.LEFT_ALIGN,
                             bounds=pixie.Vector2(0.3*self.width, 0.2*self.hight),
                             transform=pixie.translate(0.10*self.width, 0.72*self.hight))

        text = 'Humidity : {} kPa\nCloud cover : {} okta\nFeelslike : {} °C\nUV index : {} \nVisibility : {} Km/H\n'
        self.image.fill_text(font=self.make_font(20),
                             text=text.format(self.response['humidity'], self.response['cloudcover'],
                                              self.response['feelslike'], self.response['uv_index'],
                                              self.response['visibility']),
                             h_align=pixie.RIGHT_ALIGN,
                             bounds=pixie.Vector2(0.35*self.width, 0.2*self.hight),
                             transform=pixie.translate(0.55*self.width, 0.72*self.hight))


    def save_imagen(self, path) -> None:
        self.image.write_file(path)
