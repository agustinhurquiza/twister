import re
import os
import requests
import warnings
from weatherstack_api_error import WeatherStackAPIError


class WeatherApi:
    '''
    This module provides a WeatherApi class for fetching weather data from the WeatherStack API.

    Attributes
    ----------
        http : bool
            True if it use HTTP protocol, False for HTTPS
        domain : str
            The domain uses for the API request.
        unit : char
            The unit uses for the API request, [m, s, f]
        request : dict
            The current request.

    Methods
    -------
        init(unit: str = 'm', http: bool = True) -> None:
            Constructor for the WeatherApi class.
        base_url(self) -> str:
            Returns the base url for the API call based on http and domain values.
        check_query(query: str) -> bool:
            Checks if a query is valid for the API call.
        get_weather(query: str) -> bool:
            Calls the API to fetch weather data for a given query.
        parser_request() -> dict:
            Parses the JSON response from the API call into a dictionary of relevant information.
        clean_request() -> None:
            Cleans up the request attribute after parsing the JSON response.
        raise_weather_stack_exception() -> None:
            Raises a WeatherStackAPIError exception if the API call was unsuccessful.
    '''

    http = False
    domain = 'api.weatherstack.com/current'
    unit = 'm'
    request = None

    def __init__(self, unit: str = 'm', http: bool = True) -> None:
        '''
        Constructor for the WeatherApi class.

        Parameters
        ----------
        unit str :
            Unit of measurement to use for temperature. Default is 'm' for metric.
            Other options are 's' for scientific and 'f' for Fahrenheit.
        http bool :
            Whether to use http or https for the API call. Default is True.

        Raises
        ------
        AssertionError: if the unit parameter is not one of 'm', 's', or 'f'.
        '''
        assert unit in ['m','s','f'], 'Unit not available.'

        self.http = http
        self.unit = unit

    def base_url(self) -> str:
        '''
        Returns the base URL for the Weather API call based on the http attribute.

        Returns
        -------
            str
                The base URL for the API call.
        '''
        if self.http:
            base_url = 'http://'
        else:
            base_url = 'https://'

        return f'{base_url}{self.domain}'

    def check_query(self, query: str) -> bool:
        '''
        Checks whether a query string is valid for the API call.

        Parameters
        ----------
            query : str
                The query string to check.

        Returns
        -------
            bool
                True if the query string is valid, False otherwise.
        '''
        MAX_LEN_QUERY = 58
        REGEX_QUERY = '^[A-Za-z0-9_-]*$'

        regex = re.compile(REGEX_QUERY)

        if len(query) > MAX_LEN_QUERY:
            return False

        return bool(regex.match(query))

    def get_weather(self, query: str) -> None:
        '''
        Calls the API to fetch weather data for a given query.
        Parameters
        ----------
            query : str
                The query string to retrieve weather data for.

        '''
        access_key = os.environ.get('WEATHERSTACK_TOKEN')
        params = {'query': query,
                  'access_key': access_key,
                  'units': self.unit}
        request = requests.get(self.base_url(), params=params)
        self.request = request.json()

        if 'success' in self.request.keys():
            self.raise_weather_stack_exception()

    def parser_request(self) -> dict:
        '''
        Parses the JSON response from the API request into a dictionary of weather data.

        Returns
        -------
            dict
                A dictionary of weather data.
        '''
        location = self.request.get('location', {})
        current = self.request.get('current', {})

        return {'country': location['country'],
                'localtime': location['localtime_epoch'],
                'region': location['name'],
                'lon': location['lon'],
                'lat': location['lat'],
                'temperature': current['temperature'],
                'weather_code': current['weather_code'],
                'weather_descriptions': current['weather_descriptions'],
                'wind_speed': current['wind_speed'],
                'wind_degree': current['wind_degree'],
                'wind_dir': current['wind_dir'],
                'pressure': current['pressure'],
                'precip': current['precip'],
                'humidity': current['humidity'],
                'cloudcover': current['cloudcover'],
                'feelslike': current['feelslike'],
                'uv_index': current['uv_index'],
                'visibility': current['visibility'],
                'is_day': current['is_day'] == 'yes'}

    def clean_request(self) -> None:
        '''
        Cleans up the request attribute after parsing the JSON response.
        '''
        request = None

    def raise_weather_stack_exception(self) -> None:
        '''
        Raises a WeatherStackAPIError exception if the API call was unsuccessful.
        '''
        success = self.request.get('success', True)
        error = self.request.get('error', {})

        if not success:
            raise WeatherStackAPIError(
                code=error['code'],
                error_type=error['type'],
                info=error['info']
            )
