from app.rest_utils import status


class RestException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = 'Ошибка во время выполнения запроса'

    def __init__(self, errors=None, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        self.errors = errors
        self.message = message or self.default_message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        if self.message:
            rv['message'] = self.message
        if self.errors:
            rv['errors'] = self.errors
        return rv


class MethodNotAllowedRequest(RestException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_message = 'Метод не найден'


class NotFound(RestException):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = 'Ресурс не найден'


class Forbidden(RestException):
    status_code = status.HTTP_403_FORBIDDEN
    default_message = 'Операция запрещена для данного пользователя'


class NotAuthorized(RestException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_message = 'Требуется авторизация'


class BadRequest(RestException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = 'Некорректно заполнены данные'
