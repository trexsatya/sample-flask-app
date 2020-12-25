from functools import wraps

from flask import request, make_response, abort, jsonify
from marshmallow import Schema


def validate_with(schema: Schema):
    req_json = request.get_json()
    errors = schema.validate(req_json)
    if errors:
        print("Validation failed", errors, "Input", req_json)
        resp = make_response(jsonify(errors), 400)
        abort(resp)


def ensure_resource_present(data):
    if not data:
        errors = {"message": "Resource Not Found"}
        resp = make_response(jsonify(errors), 404)
        abort(resp)
