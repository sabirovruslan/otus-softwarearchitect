from flask import Response, json

from app.rest_utils import status


def json_response(data=None, status_code=status.HTTP_200_OK, headers=None):
    return Response(
        json.dumps({'data': data}),
        status=status_code,
        headers=headers,
        mimetype='application/json',
    )
