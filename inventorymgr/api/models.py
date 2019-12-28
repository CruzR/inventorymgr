"""Schemas for validating JSON objects."""


from typing import Any, Callable, Optional

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
    create_items = fields.Bool(required=True)
    qualifications = fields.Nested(QualificationSchema, required=True, many=True)


class RegistrationTokenSchema(Schema):
    """Marshmallow schema to validate registration tokens."""
    id = fields.Integer(required=True)
    token = fields.Str(required=True, validate=bool)
    expires = fields.DateTime(required=True)


class Gtin13IdField(fields.Field):
    """Marshmallow field for serializing an integer to a GTIN-13 id."""
    def serialize(self, attr: str, obj: Any,
                  accessor: Optional[Callable[[Any, str, Any], Any]] = None,
                  **kwargs: Any) -> Any:
        """Serialize data to a GTIN-13 id."""
        value = self.get_value(obj, attr, accessor) # type: ignore
        return '{:013d}'.format(value)


class BorrowableItemSchema(Schema):
    """Marshmallow schema to validate borrowable items."""
    id = fields.Integer(required=True)
    name = fields.Str(required=True, validate=bool)
    barcode = Gtin13IdField(attribute='id', dump_only=True)
