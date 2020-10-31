from flask import jsonify, Flask
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from app.rest_utils import status
from app.rest_utils.exceptions import RestException


def handle_rest_exception(error):
    """Обработчик ошибок для RestException"""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def handle_internal_error(error):
    """Обработчик непредвиденных ошибок"""
    response = jsonify({'message': 'Ошибка сервера'})
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return response


def handle_method_not_allowed(error):
    response = jsonify({'message': 'Метод не найден'})
    response.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    return response


def handle_not_found(error):
    response = jsonify({'message': 'Ресурс не найден'})
    response.status_code = status.HTTP_404_NOT_FOUND
    return response


def handle_forbidden(error):
    response = jsonify({'message': 'Доступ запрещен'})
    response.status_code = status.HTTP_403_FORBIDDEN
    return response


def handle_unauthorized(error):
    response = jsonify({'message': 'Требуется авторизация'})
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return response


def handle_bad_request(error):
    errors = {}
    if isinstance(error, HTTPException):
        errors = error.data.get('errors')
    response = jsonify({'message': 'Некорректно заполнены данные', 'errors': errors})
    response.status_code = status.HTTP_400_BAD_REQUEST
    return response


def handle_validation_exception(error):
    response = jsonify({'message': 'Invalid request.', 'errors': error.data.get('messages')})
    response.status_code = error.code
    return response


def register_base_error_handlers(app: Flask):
    app.register_error_handler(RestException, handle_rest_exception)
    app.register_error_handler(status.HTTP_500_INTERNAL_SERVER_ERROR, handle_internal_error)
    app.register_error_handler(status.HTTP_405_METHOD_NOT_ALLOWED, handle_method_not_allowed)
    app.register_error_handler(status.HTTP_404_NOT_FOUND, handle_not_found)
    app.register_error_handler(status.HTTP_403_FORBIDDEN, handle_forbidden)
    app.register_error_handler(status.HTTP_401_UNAUTHORIZED, handle_unauthorized)
    app.register_error_handler(status.HTTP_400_BAD_REQUEST, handle_bad_request)
    app.register_error_handler(ValidationError, handle_validation_exception)
    app.register_error_handler(status.HTTP_422_UNPROCESSABLE_ENTITY, handle_validation_exception)
