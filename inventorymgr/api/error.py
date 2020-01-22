"""
Helper types and functions for the JSON API.

APIError
    Common exception class thrown by API views.

handle_api_error()
    Converts APIError instances to Flask responses.

handle_validation_error()
    Converts ValidationError instances during schema validation to responses.
"""

from typing import cast, Dict

from flask import jsonify, Response
from marshmallow import ValidationError


class APIError(Exception):

    """Base class for exceptions raised by JSON API views."""

    status_code = 400

    def __init__(self, reason: str, status_code: int):
        super().__init__(self)
        self.reason = reason
        self.status_code = status_code

    def as_dict(self) -> Dict[str, str]:
        """Convert exception to a dict to be returned from an API call."""
        return {"reason": self.reason}


def handle_api_error(error: APIError) -> Response:
    """Convert an APIError to a Flask result to be return from an API call."""
    response = jsonify(error.as_dict())
    response.status_code = error.status_code
    return cast(Response, response)


def handle_validation_error(error: ValidationError) -> Response:
    """Convert a ValidationError from parsing JSON input to a error response."""
    response = jsonify({"reason": "validation_failed", "errors": error.messages})
    response.status_code = 400
    return cast(Response, response)
