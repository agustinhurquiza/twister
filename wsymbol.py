from enum import Enum
from typing import Union
import xmltodict
import warnings
import os

'''
    Consts
    ------
    The default wsymbol path.
'''
WSYMBOL_DEFAULT_PATH = 'src/img/icons/'
if not os.path.isdir(WSYMBOL_DEFAULT_PATH):
    warnings.warn('Wsymbol path doesn\'t found.')
WSYMBOL_DEFAULT_CONDITION_CODES_PATH = 'src/conditions_codes.xml'
if not os.path.isfile(WSYMBOL_DEFAULT_CONDITION_CODES_PATH):
    warnings.warn('Condition codes doesn\'t found.')

'''
    Consts
    ------
    The const use in the WSymbol Class.
'''
WSYMBOL_WIDTH = 512
WSYMBOL_HIGHT = 512
WSYMBOL_EXTENSION = '.png'


class WSymbol():
    '''
    This class handles the icons used in the diferents weather conditions.

    Attributes
    ----------
        __path__ : str
            Icons directory path.
        codes_dict : dict
            A dict with the diferents icons paths.

    Methods
    -------
    parser_condition_codes(codes_file) -> None:
        Load a xml file with the wheater codes.

    get_symbol_path_from_code(code: int, is_day: bool) -> str:
        Get the icon path from a especific code.

    get_symbol_temp_from_code(tmp: int) -> str:
        Get the icon path from temperature.

    set_path(path: str) -> None:
        Sete diferent path for the icons drectory.

    get_abs_path() -> str:
        Get absolut path for the icons directory.

    get_size() -> Union[int, int]:
        Get size for specific icon imagen.
    '''

    def __init__(self, path=WSYMBOL_DEFAULT_PATH, codes=WSYMBOL_DEFAULT_CONDITION_CODES_PATH) -> None:
        '''
        Constructs all the necessary attributes for the WSymbol object.

        Parameters
        ----------
            path : str
                Icons directory path.
            codes : str
                A xml file with the diferents icons paths. You can dowload from
                https://weatherstack.com/site_resources/weatherstack-weather-condition-codes.zip
        Returns
        -------
            None
        '''
        if not os.path.isdir(path):
            warnings.warn('Wsymbol path doesn\'t found.')
        self.__path__ = path
        self.codes_dict = {}

        self.parser_condition_codes(codes)

    def parser_condition_codes(self, codes_file=WSYMBOL_DEFAULT_CONDITION_CODES_PATH) -> None:
        '''
        Load a xml file with the wheater codes.

        Parameters
        ----------
            codes_file : str
                A xml file with the diferents icons paths. You can dowload from
                https://weatherstack.com/site_resources/weatherstack-weather-condition-codes.zip
        Returns
        -------
            None
        '''
        if not os.path.isfile(codes_file):
            warnings.warn('Condition codes doesn\'t found.')

        with open(codes_file) as fd:
            doc = xmltodict.parse(fd.read())
        codes = doc['codes']['condition']

        for code in codes:
            self.codes_dict[int(code['code'])] = {'description': code['description'],
                                                  'day_icon': code['day_icon'],
                                                  'night_icon': code['night_icon']}

    def get_symbol_path_from_code(self, code: int, is_day: bool) -> str:
        '''
        Get the icon path from a especific code.

        Parameters
        ----------
            codes : int
                Number of the wheater codes
            is_day : bool
                True if it's dya, false it's night.
        Returns
        -------
            path : str
                The imagen path for the input code.
        '''
        for cc, value in self.codes_dict.items():
            if cc == code:
                if is_day:
                    return self.get_abs_path() + '/' + value['day_icon'] + WSYMBOL_EXTENSION
                else:
                    return self.get_abs_path() + '/' + value['night_icon'] + WSYMBOL_EXTENSION

        warnings.warn('Code unknown: ' + str(code))
        return self.get_abs_path() + '/' + 'unknown' + WSYMBOL_EXTENSION

    def get_symbol_temp_from_code(self, tmp: int) -> str:
        '''
        Get the icon path from temperature.

        Parameters
        ----------
            tmp : int
                The temperature.
        Returns
        -------
            path : str
                The imagen path for the input tmperature.
        '''
        if tmp > 30:
            return self.get_abs_path() + '/' + 'hot' + WSYMBOL_EXTENSION
        elif tmp < 10:
            return self.get_abs_path() + '/' + 'cold' + WSYMBOL_EXTENSION
        else:
            return self.get_abs_path() + '/' + 'cool' + WSYMBOL_EXTENSION

    def set_path(self, path: str) -> None:
        '''
        Set a diferent path for the wsymbol imagenes.

        Parameters
        ----------
            path : str
                The new path for the new directory of the wsymbol imagenes.
        Returns
        -------
            None
        '''
        if not os.path.isdir(path):
            warnings.warn('Wsymbol path doesn\'t found.')
        self.__path__ = path

    def get_abs_path(self) -> str:
        '''
        Get the absolut path of the one WSymbol.

        Parameters
        ----------
            None
        Returns
        -------
            path : str
                The absolut path for the especific wsymbol imagen.
        '''
        return os.path.abspath(self.__path__)

    def get_size(self) -> Union[int, int]:
        '''
        Get size of the one WSymbol imagen.

        Parameters
        ----------
            None
        Returns
        -------
            size : [int, int]
                The size for the especific wsymbol imagen.
        '''
        return (WSYMBOL_WIDTH, WSYMBOL_HIGHT)
