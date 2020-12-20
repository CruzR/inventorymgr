"""Schemas for validating JSON objects."""


from datetime import datetime
from typing import List, Optional

import pydantic

__all__ = [
    "Qualification",
    "QualificationCollection",
    "NewQualification",
    "LoginRequest",
    "User",
    "UserCollection",
    "UserInfo",
    "NewUser",
    "UpdatedUser",
    "RegistrationToken",
    "RegistrationTokenCollection",
    "BorrowableItem",
    "BorrowableItemCollection",
    "NewItem",
    "UpdatedItem",
    "BorrowState",
    "BorrowStateCollection",
    "CheckoutRequest",
    "CheckinRequest",
    "LogEntry",
    "LogEntryCollection",
    "NewTransferRequest",
    "TransferRequest",
    "TransferRequestCollection",
]


class ExportModel(pydantic.BaseModel):
    """Pydantic base model for models loaded from DB objects."""

    class Config:  #  pylint: disable=too-few-public-methods
        """Enable ORM mode."""

        orm_mode = True


class Qualification(ExportModel):
    """Schema to validate qualification JSON objects."""

    id: int
    name: str


class QualificationCollection(pydantic.BaseModel):
    """Schema to validate collections of qualification objects."""

    qualifications: List[Qualification]


class NewQualification(pydantic.BaseModel):
    """Schema to validate to-be-created qualification objects."""

    name: str


class LoginRequest(pydantic.BaseModel):
    """Schema to validate login requests."""

    username: str
    password: str


class User(ExportModel):
    """
    Schema to validate user JSON objects.

    Since this is also used to expose user objects in the JSON API,
    the password field is not included.
    """

    id: int
    username: str
    create_users: bool
    view_users: bool
    update_users: bool
    edit_qualifications: bool
    create_items: bool
    manage_checkouts: bool
    qualifications: List[Qualification]
    barcode: str


class UserCollection(pydantic.BaseModel):
    """Schema to validate collections of user objects."""

    users: List[User]


class UserInfo(ExportModel):
    """Schema to validate user objects where only basic info is required."""

    id: int
    username: str
    barcode: str


class NewUser(pydantic.BaseModel):
    """
    Schema to validate to-be-created user objects.

    Unlike :class:`User`, this does not contain an id, since a new one
    will be generated. It does however require a password.
    """

    username: str
    password: str
    create_users: bool
    view_users: bool
    update_users: bool
    edit_qualifications: bool
    create_items: bool
    manage_checkouts: bool
    qualifications: List[Qualification]


class UpdatedUser(pydantic.BaseModel):
    """
    Schema to validate user update requests.

    Unlike the schema for creating new users, this requires the user's id,
    but providing a new password is optional.
    """

    id: int
    username: str
    password: Optional[str]
    create_users: bool
    view_users: bool
    update_users: bool
    edit_qualifications: bool
    create_items: bool
    manage_checkouts: bool
    qualifications: List[Qualification]


class RegistrationToken(ExportModel):
    """Schema to validate registration tokens."""

    id: int
    token: str
    expires: datetime


class RegistrationTokenCollection(pydantic.BaseModel):
    """Schema for a collection of registration tokens."""

    tokens: List[RegistrationToken]


class BorrowableItem(ExportModel):
    """Schema to validate borrowable items."""

    id: int
    name: str
    barcode: str
    required_qualifications: List[Qualification]


class BorrowableItemCollection(pydantic.BaseModel):
    """Schema for a collection of borrowable items."""

    items: List[BorrowableItem]


class ItemInfo(ExportModel):
    """Item schema for when less information is required."""

    id: int
    name: str
    barcode: str


class ShortItemInfo(ExportModel):
    """Item schema for when just id and barcode are required."""

    id: int
    barcode: str


class NewItem(pydantic.BaseModel):
    """Schema for to-be-created items."""

    name: str
    required_qualifications: List[Qualification]


class UpdatedItem(pydantic.BaseModel):
    """Schema for updating items."""

    id: int
    name: str
    required_qualifications: List[Qualification]


class BorrowState(ExportModel):
    """Schema for borrow state objects."""

    id: int
    borrowing_user: UserInfo
    borrowed_item: ItemInfo
    received_at: datetime
    returned_at: Optional[datetime]


class BorrowStateCollection(pydantic.BaseModel):
    """Schema for a collection of borrow states."""

    borrowstates: List[BorrowState]


class CheckoutRequest(pydantic.BaseModel):
    """Schema for checkout requests."""

    borrowing_user_id: int
    borrowed_item_ids: List[int]


class CheckinRequest(pydantic.BaseModel):
    """Marshmallow schema for checkin requests."""

    user_id: int
    item_ids: List[int]


class LogEntry(ExportModel):
    """Schema for checkout / checkin logs."""

    id: int
    timestamp: datetime
    action: str
    subject_id: int
    secondary_id: Optional[int]
    items: List[ShortItemInfo]


class LogEntryCollection(pydantic.BaseModel):
    """Schema for a collection of log entries."""

    logs: List[LogEntry]


class NewTransferRequest(pydantic.BaseModel):
    """Schema for creating transfer requests."""

    target_user_id: int
    borrowstate_id: int


class TransferRequest(ExportModel):
    """Schema for existing transfer requests."""

    id: int
    target_user_id: int
    borrowstate_id: int


class TransferRequestCollection(pydantic.BaseModel):
    """Schema for a collection of transfer requests."""

    transferrequests: List[TransferRequest]
