# Standard Library
from datetime import datetime

# Third Party Library
from pydantic import Field
from schemas.base import BaseSchema


class UserUpdateRequestSchema(BaseSchema):
    agreed_at: datetime = Field(
        ...,
        title="同意日時",
        description="規約に同意した日時",
        example=datetime.now().isoformat(),  # type: ignore
    )


class UserCreateRequestSchema(UserUpdateRequestSchema):
    id: str = Field(
        ..., title="ID", description="ユーザーを識別するID", example="000001"  # type: ignore
    )


class UserSchema(UserCreateRequestSchema):
    is_deleted: datetime = Field(
        ...,
        title="削除フラグ",
        description="削除されたかどうかのフラグ",
        example=datetime.now().isoformat(),  # type: ignore
    )
    created_at: datetime = Field(
        ..., title="作成日時", description="データが作成された日時", example=datetime.now().isoformat()  # type: ignore
    )
    updated_at: datetime = Field(
        ..., title="更新日時", description="データが最後に更新された日時", example=datetime.now().isoformat()  # type: ignore
    )
