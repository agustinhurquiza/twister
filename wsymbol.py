from enum import Enum
from typing import Union
import xmltodict
import warnings
import os

WSYMBOL_DEFAULT_PATH = 'src/img/icons/'
if not os.path.isdir(WSYMBOL_DEFAULT_PATH):
    warnings.warn('Wsymbol path doesn\'t found.')
WSYMBOL_DEFAULT_CONDITION_CODES_PATH = 'src/conditions_codes.xml'
if not os.path.isfile(WSYMBOL_DEFAULT_CONDITION_CODES_PATH):
    warnings.warn('Condition codes doesn\'t found.')

WSYMBOL_WIDTH = 512
WSYMBOL_HIGHT = 512
WSYMBOL_EXTENSION = '.png'


class WSymbol():

    def __init__(self, path=WSYMBOL_DEFAULT_PATH) -> None:
        if not os.path.isdir(path):
            warnings.warn('Wsymbol path doesn\'t found.')
        self.__path__ = path
        self.codes_dict = {}

        self.parser_condition_codes(codes)

    def parser_condition_codes(self, codes_file=WSYMBOL_DEFAULT_CONDITION_CODES_PATH) -> None:
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
        for cc, value in self.codes_dict.items():
            if cc == code:
                if is_day:
                    return self.get_abs_path() + '/' + value['day_icon'] + WSYMBOL_EXTENSION
                else:
                    return self.get_abs_path() + '/' + value['night_icon'] + WSYMBOL_EXTENSION

        warnings.warn('Code unknown: ' + str(code))
        return self.get_abs_path() + '/' + 'unknown' + WSYMBOL_EXTENSION

    def get_symbol_temp_from_code(self, tmp: int) -> str:
        if tmp > 30:
            return self.get_abs_path() + '/' + 'hot' + WSYMBOL_EXTENSION
        elif tmp < 10:
            return self.get_abs_path() + '/' + 'cold' + WSYMBOL_EXTENSION
        else:
            return self.get_abs_path() + '/' + 'cool' + WSYMBOL_EXTENSION

    def set_path(self, path: str) -> None:
        if not os.path.isdir(path):
            warnings.warn('Backgorund doesn\'t found.')
        self.__path__ = path

    def get_abs_path(self) -> str:
        return os.path.abspath(self.__path__)

    def get_size(self) -> Union[int, int]:
        return (WSYMBOL_WIDTH, WSYMBOL_HIGHT)
