from functools import wraps

from flask import request, make_response, abort, jsonify
from marshmallow import Schema


def validate_with(schema: Schema):
    req_json = request.get_json()
    print(req_json)
    errors = schema.validate(req_json)
    if errors:
        print("Validation failed", errors)
        resp = make_response(jsonify(errors), 400)
        abort(resp)

