"""Schemas for validating JSON objects."""


from marshmallow import Schema, fields


class QualificationSchema(Schema):
    """Marshmallow schema to validate qualification JSON objects."""
    id = fields.Integer(required=True)
    name = fields.Str(required=True)


class UserSchema(Schema):
    """Marshmallow schema to validate user JSON objects."""
    id = fields.Integer()
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    create_users = fields.Bool()
    view_users = fields.Bool()
    update_users = fields.Bool()
    edit_qualifications = fields.Bool()
    qualifications = fields.Nested(QualificationSchema, many=True)
