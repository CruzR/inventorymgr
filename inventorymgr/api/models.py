"""Schemas for validating JSON objects."""


from marshmallow import Schema, fields


class QualificationSchema(Schema):
    """Marshmallow schema to validate qualification JSON objects."""
    id = fields.Integer(required=True)
    name = fields.Str(required=True)
