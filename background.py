from enum import Enum
from typing import Union
from typing import NoReturn
import warnings
import os

'''
    Constants
    ---------
        The default background path.
'''
DEFAULT_BACKGROUND_PATH = 'src/img/backgrounds/'

if not os.path.isdir(DEFAULT_BACKGROUND_PATH):
    warnings.warn('Background directory not found.')

'''
    Constants
    ---------
        The constants used in the Background Class.
'''
BACKGROUND_WIDTH = 800
BACKGROUND_HEIGHT = 656
BACKGROUND_EXTENSION = '.png'


class Background(Enum):
    '''
    This class is an enum for different backgrounds.

    Attributes
    ----------
        __path__ : str
            Background directory path.

    Methods
    -------
        set_path(path: str) -> NoReturn:
            Sets a different path for the background images.

        get_abs_path() -> str:
            Gets the absolute path of the background directory.

        get_image_path() -> str:
            Gets the absolute path of the specified Background enum.

        get_size() -> Union[int, int]:
            Gets the size of the specified Background image.
    '''
    BACKGROUND_UNKNOWN = 0
    BACKGROUND_SUNNY_DAY = 1
    BACKGROUND_SKY_NIGHT = 2
    BACKGROUND_CLOUDY_DAY = 3
    BACKGROUND_CLOUDY_NIGHT = 4
    BACKGROUND_RAINY = 5
    BACKGROUND_THUNDER = 6
    BACKGROUND_SNOW = 7
    BACKGROUND_FOG = 8
    __path__ = DEFAULT_BACKGROUND_PATH

    def set_path(self, path: str) -> NoReturn:
        '''
        Sets a different path for the background images.

        Parameters
        ----------
            path : str
                The new path for the directory of the background images.
        '''
        if not os.path.isdir(path):
            warnings.warn('Background directory not found.')
        self.__path__ = path


    def get_abs_path(self) -> str:
        '''
        Gets the absolute path of the background directory

        Returns
        -------
            str
                The absolute path of the background directory.
    '''
        return os.path.abspath(self.__path__)


    def get_image_path(self) -> (str, bool):
        '''
        Gets the absolute path of the specified Background enum.

        Returns
        -------
            (str, bool)
                The absolute path of the specified Background enum.
                True if the background is black, False otherwise.
        '''
        if self.value == Background.BACKGROUND_SUNNY_DAY.value:
            return (self.get_abs_path() + '/' + '01' + BACKGROUND_EXTENSION, False)
        if self.value == Background.BACKGROUND_SKY_NIGHT.value:
            return (self.get_abs_path() + '/' + '02' + BACKGROUND_EXTENSION, True)
        if self.value == Background.BACKGROUND_CLOUDY_DAY.value:
            return (self.get_abs_path() + '/' + '03' + BACKGROUND_EXTENSION, False)
        if self.value == Background.BACKGROUND_CLOUDY_NIGHT.value:
            return (self.get_abs_path() + '/' + '04' + BACKGROUND_EXTENSION, True)
        if self.value == Background.BACKGROUND_RAINY.value:
            return (self.get_abs_path() + '/' + '05' + BACKGROUND_EXTENSION, True)
        if self.value == Background.BACKGROUND_THUNDER.value:
            return (self.get_abs_path() + '/' + '06' + BACKGROUND_EXTENSION, True)
        if self.value == Background.BACKGROUND_SNOW.value:
            return (self.get_abs_path() + '/' + '07' + BACKGROUND_EXTENSION, True)
        if self.value == Background.BACKGROUND_FOG.value:
            return (self.get_abs_path() + '/' + '08' + BACKGROUND_EXTENSION, False)
        else:
            # BACKGROUND_UNKNOWN
            warnings.warn('Background missed.')
            return self.get_abs_path() + '/' + 'unknown' + BACKGROUND_EXTENSION


    def get_size(self) -> Union[int, int]:
        '''
        Gets the size of the specified Background image.

        Returns
        -------
            Union[int, int]
                The size of the specified Background image.
        '''
        return BACKGROUND_WIDTH, BACKGROUND_HEIGHT
