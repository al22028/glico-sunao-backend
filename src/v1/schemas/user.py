# Standard Library
from datetime import datetime

# Third Party Library
from pydantic import Field
from schemas.base import BaseSchema

user_term_agreed_field = Field(
    ...,
    title="同意フラグ",
    description="規約に同意したかを表すフラグ",
    example=False,  # type: ignore
)

user_term_agreed_at_field = Field(
    ...,
    title="同意日時",
    description="規約に同意した日時",
    example="0001-01-01T00:00:00.000000",  # type: ignore
)

user_id_field = Field(
    ...,
    title="ユーザーID",
    description="ユーザーを識別するID",
    example="000001",  # type: ignore
)

user_created_at_field = Field(
    ..., title="作成日時", description="データが作成された日時", example=datetime.now().isoformat()  # type: ignore
)


user_updated_at_field = Field(
    ..., title="更新日時", description="データが最後に更新された日時", example=datetime.now().isoformat()  # type: ignore
)

user_is_deleted_field = Field(
    ...,
    title="削除フラグ",
    description="削除されたかどうかのフラグ",
    example=False,  # type: ignore
)


class UserCreateRequestSchema(BaseSchema):
    """ユーザー作成リクエストスキーマ"""

    id: str = user_id_field
    term_agreed: bool = user_term_agreed_field


class UserSchema(BaseSchema):
    id: str = user_id_field
    term_agreed: bool = user_term_agreed_field
    term_agreed_at: datetime | None = user_term_agreed_at_field
    is_deleted: bool = user_is_deleted_field
    created_at: datetime = user_created_at_field
    updated_at: datetime = user_updated_at_field
