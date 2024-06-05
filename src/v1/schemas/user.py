# Standard Library
from datetime import datetime

# Third Party Library
from pydantic import Field
from schemas.base import BaseSchema


class UserUpdateRequestSchema(BaseSchema):
    term_agreed: bool = Field(
        ...,
        title="同意フラグ",
        description="規約に同意したかを表すフラグ",
        example=False,  # type: ignore
    )
    term_agreed_at: datetime = Field(
        ...,
        title="同意日時",
        description="規約に同意した日時",
        example="0001-01-01T00:00:00.000000",  # type: ignore
    )


class UserCreateRequestSchema(UserUpdateRequestSchema):
    user_id: str = Field(
        ..., title="ID", description="ユーザーを識別するID", example="000001"  # type: ignore
    )


class UserSchema(UserCreateRequestSchema):
    is_deleted: bool = Field(
        ...,
        title="削除フラグ",
        description="削除されたかどうかのフラグ",
        example=False,  # type: ignore
    )
    created_at: datetime = Field(
        ..., title="作成日時", description="データが作成された日時", example=datetime.now().isoformat()  # type: ignore
    )
    updated_at: datetime = Field(
        ..., title="更新日時", description="データが最後に更新された日時", example=datetime.now().isoformat()  # type: ignore
    )
