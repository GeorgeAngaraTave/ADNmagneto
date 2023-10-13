class HttpStatus(object):
    """docstring for HttpStatus"""
    OK = 'success!'
    AUTH_ERROR_MSG = 'The server could not verify that you are authorized to access the URL requested.'
    UNAUTHORIZED = 'You are not authorized to access the requested resource.'
    FORBIDDEN = 'you don\'t have permission to access the requested resource.'
    RESOURCE_NOT_EXIST = 'The requested resource doesn\'t exists.'
    DEFAULT_ERROR_MESSAGE = 'An error occurred. Please try again.!'
    UNEXPECTED_ERROR = 'Unexpected Error.'
