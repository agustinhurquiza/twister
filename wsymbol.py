import xmltodict
import warnings
import os
from enum import Enum
from typing import Union
from typing import NoReturn


'''
Constants
---------
    The default path for the WSymbol images.
'''
WSYMBOL_DEFAULT_PATH = 'src/img/icons/'
if not os.path.isdir(WSYMBOL_DEFAULT_PATH):
    warnings.warn('WSymbol path not found.')
WSYMBOL_DEFAULT_CONDITION_CODES_PATH = 'src/conditions_codes.xml'
if not os.path.isfile(WSYMBOL_DEFAULT_CONDITION_CODES_PATH):
    warnings.warn('Condition codes not found.')

'''
Constants
---------
    The constants used in the WSymbol class.
'''
WSYMBOL_WIDTH = 512
WSYMBOL_HEIGHT = 512
WSYMBOL_EXTENSION = '.png'


class WSymbol:
    '''
    This class handles the icons used in the different weather conditions.

    Attributes
    ----------
        __path__ : str
            The path to the directory containing the icons.
        codes_dict : dict
            A dictionary containing the paths to the different icons.

    Methods
    -------
        parser_condition_codes(codes_file) -> NoReturn:
            Load an XML file with the weather codes.

        get_symbol_path_from_code(code: int, is_day: bool) -> str:
            Get the icon path from a specific code.

        get_symbol_temp_from_code(tmp: int) -> str:
            Get the icon path from the temperature.

        set_path(path: str) -> NoReturn:
            Set a different path for the icons directory.

        get_abs_path() -> str:
            Get the absolute path for the icons directory.

        get_size() -> Union[int, int]:
            Get the size of a specific icon image.
    '''


    def __init__(self, path: str =WSYMBOL_DEFAULT_PATH, codes: str = WSYMBOL_DEFAULT_CONDITION_CODES_PATH):
        '''
        Constructs all the necessary attributes for the WSymbol object.

        Parameters
        ----------
            path : str
                The path to the directory containing the icons.
            codes : str
                An XML file with the paths to the different icons. You can download it from
                https://weatherstack.com/site_resources/weatherstack-weather-condition-codes.zip
        '''
        if not os.path.isdir(path):
            warnings.warn('WSymbol path not found.')
        self.__path__ = path
        self.codes_dict = {}

        self.parser_condition_codes(codes)


    def parser_condition_codes(self, codes_file: str = WSYMBOL_DEFAULT_CONDITION_CODES_PATH) -> NoReturn:
        '''
        Load an XML file with the weather codes.

        Parameters
        ----------
            codes_file : str
                An XML file with the paths to the different icons. You can download it from
                https://weatherstack.com/site_resources/weatherstack-weather-condition-codes.zip
        '''
        if not os.path.isfile(codes_file):
            warnings.warn('Condition codes not found.')

        with open(codes_file) as fd:
            doc = xmltodict.parse(fd.read())
        codes = doc['codes']['condition']

        for code in codes:
            self.codes_dict[int(code['code'])] = {'description': code['description'],
                                                  'day_icon': code['day_icon'],
                                                  'night_icon': code['night_icon']}


    def get_symbol_path_from_code(self, code: int, is_day: bool) -> str:
        '''
        Get the icon path for a specific code.

        Parameters
        ----------
            code : int
                The number representing the weather code.
            is_day : bool
                True if it's daytime, false if it's nighttime.

        Returns
        -------
            str
                The image path for the given code.
        '''
        for cc, value in self.codes_dict.items():
            if cc == code:
                if is_day:
                    return self.get_abs_path() + '/' + value['day_icon'] + WSYMBOL_EXTENSION
                else:
                    return self.get_abs_path() + '/' + value['night_icon'] + WSYMBOL_EXTENSION

        warnings.warn('Unknown code: ' + str(code))
        return self.get_abs_path() + '/' + 'unknown' + WSYMBOL_EXTENSION


    def get_symbol_temp_from_code(self, tmp: int) -> str:
        '''
        Get the icon path for a given temperature.

        Parameters
        ----------
            tmp : int
                The temperature.

        Returns
        -------
            str
                The image path for the given temperature.
        '''
        if tmp > 30:
            return self.get_abs_path() + '/' + 'hot' + WSYMBOL_EXTENSION
        elif tmp < 10:
            return self.get_abs_path() + '/' + 'cold' + WSYMBOL_EXTENSION
        else:
            return self.get_abs_path() + '/' + 'cool' + WSYMBOL_EXTENSION


    def set_path(self, path: str) -> NoReturn:
        '''
        Set a different path for the wsymbol images.

        Parameters
        ----------
            path : str
                The new path for the directory of the wsymbol images.
        '''
        if not os.path.isdir(path):
            warnings.warn('Wsymbol path not found.')
        self.__path__ = path


    def get_abs_path(self) -> str:
        '''
        Get the absolute path of the wsymbol.

        Returns
        -------
            str
                The absolute path for the specified wsymbol image.
        '''
        return os.path.abspath(self.__path__)


    def get_size(self) -> Union[int, int]:
        '''
        Get size of the wsymbol image.

        Returns
        -------
            Tuple[int, int]
                The size of the specified wsymbol image.
        '''
        return (WSYMBOL_WIDTH, WSYMBOL_HEIGHT)
