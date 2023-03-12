
class WeatherStackAPIError(Exception):
    """
    Custom Exception for WeatherStack API errors.

    Attributes
    ----------
        code : int
            The HTTP status code that was returned by the API call.
        error_type : str
            The type of error that was returned by the API call.
        info : str
            A detailed error message that was returned by the API call.
    """

    def __init__(self, code: int, error_type: str, info: str):
        """
        Initializes a new instance of the WeatherStackAPIError class.

        Parameters
        ----------
            code : int
                The HTTP status code that was returned by the API call.
            error_type :
                str The type of error that was returned by the API call.
            info : str
                A detailed error message that was returned by the API call.
        """
        self.code = code
        self.error_type = error_type
        self.info = info
        super().__init__(self.info)
