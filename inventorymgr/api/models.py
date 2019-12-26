"""Schemas for validating JSON objects."""


from marshmallow import Schema, fields


class QualificationSchema(Schema):
    """Marshmallow schema to validate qualification JSON objects."""
    id = fields.Integer(required=True)
    name = fields.Str(required=True, validate=bool)


class UserSchema(Schema):
    """Marshmallow schema to validate user JSON objects."""
    id = fields.Integer(required=True)
    username = fields.Str(required=True, validate=bool)
    password = fields.Str(required=True, load_only=True, validate=bool)
    create_users = fields.Bool(required=True)
    view_users = fields.Bool(required=True)
    update_users = fields.Bool(required=True)
    edit_qualifications = fields.Bool(required=True)
    qualifications = fields.Nested(QualificationSchema, required=True, many=True)


class RegistrationTokenSchema(Schema):
    """Marshmallow schema to validate registration tokens."""
    id = fields.Integer(required=True)
    token = fields.Str(required=True, validate=bool)
    expires = fields.DateTime(required=True)
