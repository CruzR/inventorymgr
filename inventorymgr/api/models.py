"""Schemas for validating JSON objects."""


from typing import Any, Callable, List, TypeVar, cast

import pydantic
from marshmallow import Schema, fields, post_dump, pre_load


class QualificationSchema(Schema):
    """Marshmallow schema to validate qualification JSON objects."""

    id = fields.Integer(required=True)
    name = fields.Str(required=True, validate=bool)


_T = TypeVar("_T")
_post_dump = cast(Callable[[_T], _T], post_dump)  # pylint: disable=invalid-name
_pre_load = cast(Callable[[_T], _T], pre_load)  # pylint: disable=invalid-name


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
    manage_checkouts = fields.Bool(required=True)
    qualifications = fields.Nested(QualificationSchema, required=True, many=True)

    @_post_dump
    def add_gtin13_field(self, data: Any, **kwargs: Any) -> Any:
        """Generate GTIN13 string from user id."""
        # pylint: disable=no-self-use,unused-argument
        data["barcode"] = "{:013d}".format(9_000_000 + data["id"])
        return data

    @_pre_load
    def remove_gtin13_field(self, data: Any, **kwargs: Any) -> Any:
        """Remove GTIN13 string before deserializing."""
        # pylint: disable=no-self-use,unused-argument
        if "barcode" in data:
            del data["barcode"]
        return data


class RegistrationTokenSchema(Schema):
    """Marshmallow schema to validate registration tokens."""

    id = fields.Integer(required=True)
    token = fields.Str(required=True, validate=bool)
    expires = fields.DateTime(required=True)


class BorrowableItemSchema(Schema):
    """Marshmallow schema to validate borrowable items."""

    id = fields.Integer(required=True)
    name = fields.Str(required=True, validate=bool)
    required_qualifications = fields.Nested(
        QualificationSchema, required=True, many=True
    )

    @_post_dump
    def add_gtin13_field(self, data: Any, **kwargs: Any) -> Any:
        """Generate GTIN13 string from item id."""
        # pylint: disable=no-self-use,unused-argument
        data["barcode"] = "{:013d}".format(data["id"])
        return data

    @_pre_load
    def remove_gtin13_field(self, data: Any, **kwargs: Any) -> Any:
        """Remove GTIN13 string before deserializing."""
        # pylint: disable=no-self-use,unused-argument
        if "barcode" in data:
            del data["barcode"]
        return data


class BorrowStateSchema(Schema):
    """Marshmallow schema for borrow state objects."""

    id = fields.Integer(required=True)
    borrowing_user = fields.Nested(UserSchema, required=True, only=("id", "username"))
    borrowed_item = fields.Nested(
        BorrowableItemSchema, required=True, only=("id", "name")
    )
    received_at = fields.DateTime(required=True)
    returned_at = fields.DateTime(required=True, allow_none=True)


class CheckoutRequestSchema(Schema):
    """Marshmallow schema for checkout requests."""

    borrowing_user_id = fields.Integer(required=True)
    borrowed_item_ids = fields.List(fields.Integer, required=True)


class CheckinRequestSchema(Schema):
    """Marshmallow schema for checkin requests."""

    user_id = fields.Integer(required=True)
    item_ids = fields.List(fields.Integer, required=True)


class LogEntrySchema(Schema):
    """Marshmallow schema for checkout / checkin logs."""

    id = fields.Integer(required=True)
    timestamp = fields.DateTime(required=True)
    action = fields.Str(required=True)
    subject_id = fields.Integer(required=True)
    secondary_id = fields.Integer()
    items = fields.Nested(BorrowableItemSchema, required=True, many=True, only=("id",))


class NewTransferRequest(pydantic.BaseModel):
    """Schema for creating transfer requests."""

    target_user_id: int
    borrowstate_id: int


class TransferRequest(pydantic.BaseModel):
    """Schema for existing transfer requests."""

    id: int
    target_user_id: int
    borrowstate_id: int

    class Config:
        """Enable ORM mode to allow converting SQLAlchemy models."""

        orm_mode = True


class TransferRequestCollection(pydantic.BaseModel):
    """Schema for a collection of transfer requests."""

    transferrequests: List[TransferRequest]
