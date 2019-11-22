"""Schemas for validating JSON objects."""


from marshmallow import Schema, fields


class QualificationSchema(Schema):
    """Marshmallow schema to validate qualification JSON objects."""
    id = fields.Integer(required=True)
    name = fields.Str(required=True)


class UserSchema(Schema):
    """Marshmallow schema to validate user JSON objects."""
    id = fields.Integer(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    create_users = fields.Bool(required=True)
    view_users = fields.Bool(required=True)
    update_users = fields.Bool(required=True)
    edit_qualifications = fields.Bool(required=True)
    qualifications = fields.Nested(QualificationSchema, many=True)
