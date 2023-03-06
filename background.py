from enum import Enum
from typing import Union
import warnings
import os

DEFAULT_BACKGROUND_PATH = 'src/img/backgrounds/'

if not os.path.isdir(DEFAULT_BACKGROUND_PATH):
    warnings.warn('Background doesn\'t found.')

BACKGROUND_WIDTH = 800
BACKGROUND_HIGHT = 656
BACKGROUND_EXTENSION = '.png'

class Background(Enum):
    BACKGORUND_UNKNOWN      = 0
    BACKGORUND_SUNNY_DAY    = 1
    BACKGORUND_SKY_NIGHT    = 2
    BACKGORUND_CLOUDY_DAY   = 3
    BACKGORUND_CLOUDY_NIGHT = 4
    BACKGORUND_RAINY        = 5
    BACKGORUND_THUNDER      = 6
    BACKGORUND_SNOW         = 7
    BACKGORUND_FOG          = 8
    __path__ = DEFAULT_BACKGROUND_PATH


    def set_path(self, path:str) -> None:
        if not os.path.isdir(path):
            warnings.warn('Background doesn\'t found.')
        self.__path__ = path


    def get_abs_path(self) -> str:
        return os.path.abspath(self.__path__)


    def get_image_path(self) -> str:
            if self.value == Background.BACKGORUND_SUNNY_DAY.value:
                return self.get_abs_path() + '/' + '01' + BACKGROUND_EXTENSION
            if self.value == Background.BACKGORUND_SKY_NIGHT.value:
                return self.get_abs_path() + '/' + '02' + BACKGROUND_EXTENSION
            if self.value == Background.BACKGORUND_CLOUDY_DAY.value:
                return self.get_abs_path() + '/' + '03' + BACKGROUND_EXTENSION
            if self.value == Background.BACKGORUND_CLOUDY_NIGHT.value:
                return self.get_abs_path() + '/' + '04' + BACKGROUND_EXTENSION
            if self.value == Background.BACKGORUND_RAINY.value:
                return self.get_abs_path() + '/' + '05' + BACKGROUND_EXTENSION
            if self.value == Background.BACKGORUND_THUNDER.value:
                return self.get_abs_path() + '/' + '06' + BACKGROUND_EXTENSION
            if self.value == Background.BACKGORUND_SNOW.value:
                return self.get_abs_path() + '/' + '07' + BACKGROUND_EXTENSION
            if self.value == Background.BACKGORUND_FOG.value:
                return self.get_abs_path() + '/' + '08' + BACKGROUND_EXTENSION
            else: # BACKGORUND_UNKNOWN
                warnings.warn('Background missed.')
                return self.get_abs_path() + '/' + 'unknown' + BACKGROUND_EXTENSION


    def get_size(self) -> Union[int, int]:
        return (BACKGROUND_WIDTH, BACKGROUND_HIGHT)
