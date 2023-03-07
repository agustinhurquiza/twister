from enum import Enum
from typing import Union
import warnings
import os

'''
    Consts
    ------
    The default backgound path.
'''
DEFAULT_BACKGROUND_PATH = 'src/img/backgrounds/'
if not os.path.isdir(DEFAULT_BACKGROUND_PATH):
    warnings.warn('Background doesn\'t found.')

'''
    Consts
    ------
    The const use in the Background Class.
'''
BACKGROUND_WIDTH = 800
BACKGROUND_HIGHT = 656
BACKGROUND_EXTENSION = '.png'


class Background(Enum):
    '''
    This clases is an enum for the diferents backgrounds.

    Attributes
    ----------
        __path__ : str
            Background directory path.

    Methods
    -------
    set_path(path: str) -> None:
        Set a diferent path for the backgrounds imagenes.

    get_abs_path() -> str:
        Get the absolut path of he backgound directory.

    get_image_path() -> str:
        Get the absolut path of the one Background enum.

    get_size() -> Union[int, int]:
        Get size of the one Background imagen.
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

    def set_path(self, path: str) -> None:
        '''
        Set a diferent path for the backgrounds imagenes.

        Parameters
        ----------
            path : str
                The new path for the new directory of the backgrounds imagenes.
        Returns
        -------
            None
        '''
        if not os.path.isdir(path):
            warnings.warn('Background path doesn\'t found.')
        self.__path__ = path

    def get_abs_path(self) -> str:
        '''
        Get the absolut path of he Background directory.

        Parameters
        ----------
            None
        Returns
        -------
            path : str
                The absolut path directory of the backgrounds imagenes.
        '''
        return os.path.abspath(self.__path__)

    def get_image_path(self) -> str:
        '''
        Get the absolut path of the one Background enum.

        Parameters
        ----------
            None
        Returns
        -------
            path : str
                The absolut path for the especific background imagen.
        '''
        if self.value == Background.BACKGROUND_SUNNY_DAY.value:
            return self.get_abs_path() + '/' + '01' + BACKGROUND_EXTENSION
        if self.value == Background.BACKGROUND_SKY_NIGHT.value:
            return self.get_abs_path() + '/' + '02' + BACKGROUND_EXTENSION
        if self.value == Background.BACKGROUND_CLOUDY_DAY.value:
            return self.get_abs_path() + '/' + '03' + BACKGROUND_EXTENSION
        if self.value == Background.BACKGROUND_CLOUDY_NIGHT.value:
            return self.get_abs_path() + '/' + '04' + BACKGROUND_EXTENSION
        if self.value == Background.BACKGROUND_RAINY.value:
            return self.get_abs_path() + '/' + '05' + BACKGROUND_EXTENSION
        if self.value == Background.BACKGROUND_THUNDER.value:
            return self.get_abs_path() + '/' + '06' + BACKGROUND_EXTENSION
        if self.value == Background.BACKGROUND_SNOW.value:
            return self.get_abs_path() + '/' + '07' + BACKGROUND_EXTENSION
        if self.value == Background.BACKGROUND_FOG.value:
            return self.get_abs_path() + '/' + '08' + BACKGROUND_EXTENSION
        else:
            # BACKGROUND_UNKNOWN
            warnings.warn('Background missed.')
            return self.get_abs_path() + '/' + 'unknown' + BACKGROUND_EXTENSION

    def get_size(self) -> Union[int, int]:
        '''
        Get size of the one Background imagen.

        Parameters
        ----------
            None
        Returns
        -------
            size : [int, int]
                The size for the especific background imagen.
        '''
        return (BACKGROUND_WIDTH, BACKGROUND_HIGHT)
